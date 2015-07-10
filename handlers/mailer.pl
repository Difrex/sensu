#!/usr/bin/perl 

use strict;
use warnings;
use JSON;

my $json = <>;

my $message = decode_json($json);

my $statuses = {
	'2' => 'Critical',
	'1' => 'Warning',
	'0' => 'Ok'
};


# Get client values
my $client_name = $message->{client}->{name};
my $client_addr = $message->{client}->{address};
my $timestamp 	= localtime( $message->{client}->{timestamp} );

# Get check information
my $check_name 		= $message->{check}->{name};
my $check_out 		= $message->{check}->{output};
my $check_command	= $message->{check}->{command};
my $check_interval	= $message->{check}->{interval};
my $check_status 	= $statuses->{ $message->{check}->{status} };
my @ch 			= $message->{check}->{history};
my @check_history;
foreach my $c (@ch) {
	@check_history = @$c;
}

# Count history
my $ok_count 	= 0;
my $warn_count 	= 0;
my $crit_count 	= 0;
my $total = @check_history;
foreach my $stat (@check_history) {
	if ( $stat eq '2' ) {
		$crit_count++;
	}
	elsif ( $stat eq '1' ) {
		$warn_count++;
	}
	else {
		$ok_count++;
	}
}

# Build mail body message
my $mail_body = "
$timestamp
----------------------------------------------------
$client_name with $client_addr status: $check_status

=== Summary ===
CHECK: $check_name
CHECK COMMAND: $check_command
CHECK MESSAGE: $check_out

=== Check history ===
Check interval in seconds: $check_interval
TOTAL: $total
OK: $ok_count
WARNING: $warn_count
CRITICAL: $crit_count
";

# Send email
my $mail_cmd 	= 'mail';
my $mail_subg 	= "$client_name with address $client_addr status: $check_status";
my $mail_to 	= 'admins@example.com';

# Make text file
my $mail_file 	= '/tmp/'.$message->{client}->{timestamp}.'mail.txt';
open my $mail_fh, '>', $mail_file or die "$!\n";
print $mail_fh $mail_body;
close $mail_fh;

# Send it now!
`cat $mail_file | $mail_cmd -s "'$mail_subg'" $mail_to`;

# Remove temp file
my @rm_cmd = ('rm', '-f', $mail_file);
system(@rm_cmd) == 0 or die "$!\n";


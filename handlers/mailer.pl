#!/usr/bin/perl 

use strict;
use warnings;
use JSON;

use Data::Dumper;

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
my $timestamp   = localtime( $message->{client}->{timestamp} );

# Get check information
my $check_name     = $message->{check}->{name};
my $check_out      = $message->{check}->{output};
my $check_command  = $message->{check}->{command};
my $check_interval = $message->{check}->{interval};
my $check_status   = $statuses->{ $message->{check}->{status} };
my @ch             = $message->{check}->{history};
my @check_history;

foreach my $c (@ch) {
    @check_history = @$c;
}

# Count history
my $ok_count   = 0;
my $warn_count = 0;
my $crit_count = 0;
my $total      = @check_history;
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
my $mail_cmd = 'mail';
my $mail_subg
    = "$client_name with address $client_addr status: $check_status";
my $mail_to = 'admins@example.com';

# Make text file
my $mail_file = '/tmp/' . $message->{client}->{timestamp} . 'mail.txt';
open my $mail_fh, '>', $mail_file or die "$!\n";
print $mail_fh $mail_body;
close $mail_fh;

# Write current status to file
sub write_status {
    my ( $check_name, $status ) = @_;
    my $check_run_file = '/etc/sensu/handlers/run/' . $check_name;

    open my $run, '>', $check_run_file or die "Cannot open file: $!\n";
    print $run $status;
    close($run);
}

# Get previous status
sub get_previous_status {
    my ( $check_name, $status ) = @_;
    my $check_run_file = '/etc/sensu/handlers/run/' . $check_name;

    my $previous_check_status;
    open my $run, '<', $check_run_file or warn "Cannot open file: $!\n";
    if ($run) {
        while (<$run>) {
            $previous_check_status = $_;
        }
        close($run);

        return $previous_check_status;
    }

    # New checks hack
    else {
        write_status( $check_name, $status );

        return -1;
    }
}

# Check status
sub status_change {
    my ($message) = @_;

    my $check_name = $message->{check}->{name};

    # Current check status
    my $current_check_status = $message->{check}->{status};

    # Get provious check status
    my $previous_check_status
        = get_previous_status( $check_name, $current_check_status );

    if (   ( $previous_check_status == -1 )
        or ( $previous_check_status eq $current_check_status ) )
    {
        return -1;
    }
    else {
        return 0;
    }

}

# Send it if status changed
if ( status_change == 0 ) {

    `cat $mail_file | $mail_cmd -v -s "'$mail_subg'" $mail_to`;
}

# Remove temp file
my @rm_cmd = ( 'rm', '-f', $mail_file );
system(@rm_cmd) == 0 or die "$!\n";

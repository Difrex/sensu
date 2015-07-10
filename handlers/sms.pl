#!/usr/bin/perl 

use warnings;

use JSON;
use LWP::UserAgent;
use HTTP::Request;

use Getopt::Std;

sub init() {
    my $opt_string = 'n:';
    getopts("$opt_string");
    our ( $opt_n );
}

init();

# Get sensu output
my $json = <>;
my $message = decode_json($json);
my $check_name  = $message->{check}->{name};
my $client_name = $message->{client}->{name};
my @ch 			= $message->{check}->{history};
my @check_history;
foreach my $c (@ch) {
	@check_history = @$c;
}

my $crit_count 	= 0;
my $total = @check_history;
foreach my $stat (@check_history) {
	if ( $stat eq '2' ) {
		$crit_count++;
	}
}

# sms.ru API
my $id  = '';
my $num = '';
$num = $opt_n if $opt_n;
my $sms = "$client_name\n$check_name\n$crit_count";

my $uri = "http://sms.ru/sms/send?api_id=".$id."&to=".$num."&text=".$sms;

# Make request 
my $ua = LWP::UserAgent->new();
$ua->agent('sensu-sms-handler/0.1');

my $req = HTTP::Request->new( POST => $uri );
my $res = $ua->request($req);

if ( $res->is_success )  {
    exit 0;
}
else {
    exit 7;
}


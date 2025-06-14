use strict;
use warnings;
use lib 'lib';
use Keywords;

my $testlist = 'testlist.txt';
open my $fh, '<', $testlist or die "Cannot open $testlist: $!";

while (my $file = <$fh>) {
    chomp $file;
    open my $tf, '<', $file or die "Cannot open $file: $!";
    print "\nRunning Perl test: $file\n";

    while (my $line = <$tf>) {
        chomp $line;
        if ($line =~ /Ignition ON/i) {
            Keywords::ignition_on();
        } elsif ($line =~ /Ignition OFF/i) {
            Keywords::ignition_off();
        } elsif ($line =~ /Wait (\d+)/i) {
            sleep($1);
        } else {
            print "Unknown step: $line\n";
        }
    }
    close $tf;
}
close $fh;
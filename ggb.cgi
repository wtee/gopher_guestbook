#!/sys/pkg/bin/perl -w 

#ggb - Gopher Guest Book

use strict;
use Text::Wrap;
$Text::Wrap::columns=80;
use Fcntl qw(:flock);

$ENV{PATH} = "";
$> = $<;
$) = $(;

# === Configurable Variables ===

# this script's name so it can get all self-referential
my $name = "ggb.cgi";

# the greeting visitors will receive
my $greeting = "Thanks for stopping in.";

# the directory ggb is in for gopherlinks, make sure not to end with a "/"
my $base_dir ="/users/wt/ggb";

# full path name to ggb's directory, make sure not to end with a "/"
my $dir = "/ftp/pub$base_dir";

# the server that is hosting the script
my $server = "sdf.lonestar.org";

# the port number the server uses; don't change this unless you know its serving from a different port
my $port = 70;

# === End Configurable Variables ===

my $serv_string = "\tnull\ttext\t70";
my $ver = "ggb 0.0.1d";
my $footer = "i$serv_string\r\nipowered by $ver$serv_string\r\n";
my $comfile = "$dir/guestbook.cmt";
my $go_string = "\t$base_dir/$name\t$server\t$port";

my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst);
my @months = qw(January February March April May June July August September October November December);
my @mins = qw(00 01 02 03 04 05 06 07 08 09);

if ($#ARGV > 0  && $#ARGV < 250) {
    my $tmp = "$comfile.tmp";

    open (NEW, "> $tmp") && flock (NEW, LOCK_EX);
    my $mtime = (stat ($tmp))[9];
    my @date = (($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($mtime));
    if ($min >= 0 && $min <= 9) {
        $min = $mins[$min];
    }
    $year = $year + 1900;
    print NEW "$year $months[$mon] $mday, $hour:$min\n";
    print NEW wrap ("", "", @ARGV[0 .. $#ARGV]), "\n";
    print NEW "\n--------------------------------------------------------------------------------\n\n";
    if (-e $comfile) {
        open (OLD, "< $comfile") && flock (OLD, LOCK_EX);
        while (my $line = <OLD>) {
            print NEW $line;
        }
        close OLD;
    }
    close NEW;
    rename ($tmp, $comfile) || die "Can't rename!";
    chmod 0644, $comfile;
    print "iYour message has been posted.$serv_string\r\n";
    print "1View Guestbook$go_string\r\n";
    print ".\r\n";
    exit;
} elsif ($#ARGV >= 250) {
    print "3Sorry, message should be less than 250 words$serv_string";
    exit;
}

$Text::Wrap::separator = "$serv_string\r\n";
print wrap("i", "i", $greeting), "$serv_string\r\n";
$Text::Wrap::separator = "\n";
print "i$serv_string\r\n";
print "7Leave Message$go_string\r\n";
print  "iFeel free to leave a message of 250 words or less.$serv_string\r\n";
print "i$serv_string\r\ni--------------------------------------------------------------------------------$serv_string\r\ni$serv_string\r\n";
if (-e "$comfile") {
    open (FH, "< $comfile");
    while (<FH>) {
        chomp;
        print "i$_$serv_string\r\n";
    }
}
print $footer;
print ".\r\n";
#!/usr/bin/perl
#
##############################################################################

use strict 'vars';

my $acc = ""		;
chomp($acc = `whoami`)	;

my $nTime = time - 60*30	;	#30分前
my $bTime = time - 60*30	;	#30分前

#$ENV{'TZ'} = "PST"		;	#PST
my ($bsec, $bmin, $bhour, $bmday, $bmon, $byear, $bwday, $byday, $bisdst) = localtime($bTime);
$byear += 1900	;
$bmon++		;
if($bmon  < 10)	{$bmon  = "0$bmon";}
if($bmday < 10)	{$bmday = "0$bmday";}
if($bhour < 10)	{$bhour = "0$bhour";}
if($bmin  < 10)	{$bmin  = "0$bmin";}
if($bsec  < 10)	{$bsec  = "0$bsec";}
my $tFile = "/home/$acc/logs/access_log_$byear$bmon$bmday$bhour"	;

$ENV{'TZ'} = "JST-9"		;	#日本
my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($nTime);
$year += 1900	;
$mon++		;
if($mon  < 10)	{$mon  = "0$mon";}
if($mday < 10)	{$mday = "0$mday";}
if($hour < 10)	{$hour = "0$hour";}
if($min  < 10)	{$min  = "0$min";}
if($sec  < 10)	{$sec  = "0$sec";}

#my $home  = "../public_html/_bg"		;
#my $home  = "/home/ch2comi6/public_html"	;
my $home  = "/home/$acc/public_html"		;
my $lFile = "$home/_bg/fox.txt"			;
my $rFile = "$home/_service/PV$year$mon$mday.txt"	;

my $gTotal   = 0	;#全アクセス数
my $gReadcgi = 0	;#read.cgi
my $gHtml    = 0	;# .html
my $gDat     = 0	;# .dat
my $gGif     = 0	;# .gif .jpg ...etc
my $gText    = 0	;# .txt
my $gCgi     = 0	;# other CGIs
my $g302     = 0	;# 404 not found
my $gSonota  = 0	;# その他

&log_analize($tFile);
$gSonota = $gTotal - $gReadcgi - $gHtml - $gDat - $gText - $gGif - $gCgi - $g302	;

logout("gTotal = $gTotal (全アクセス数)\n")	;
logout("gReadcgi = $gReadcgi (read.cgi)\n")	;
logout("gHtml = $gHtml (.html)\n")		;
logout("gDat = $gDat (.dat)\n")			;
logout("gText = $gText (.txt)\n")		;
logout("gGif = $gGif (.gif .jpg ... etc)\n")	;
logout("gCgi = $gCgi (その他のCGI)\n")		;
logout("g404 = $g302 (404 not found)\n")	;
logout("gSonota = $gSonota (その他)\n")		;


&reportout()	;
&saveSetting()	;	#SETTING.TXT 保存 (for ジンギスカン仕様)

logout("$year/$mon/$mday $hour:$min:$sec ($acc , $tFile) FOX END -----\n")	;

print "FOX end($year/$mon/$mday $hour:$min:$sec) $acc , $tFile\n";
exit;

sub saveSetting
{
	my @dirs = ()	;
	my $folder = "$home/"		;
	print "### saveSetting($folder)\n"	;
	if(opendir(DIR,"$folder"))
	{
		@dirs = grep {!(/^\./) && -d "$folder/$_" } readdir(DIR);
		close DIR		;
	}
	foreach(@dirs)
	{
		if($_ !~ /ZZZ\-/)	{next;}
		my $a1 = $_	;
		my $a2 = $_	;
		$a1 =~ s/ZZZ\-//;
#		my $cmd = "cp $home/$a1/SETTING.TXT $home/$a2/SETTING.TXT";
#		print "$cmd\n"	;
		system("cp $home/$a1/SETTING.TXT $home/$a2/SETTING.TXT");
		system("cp $home/$a1/1000.txt $home/$a2/1000.txt");
		system("cp $home/$a1/head.txt $home/$a2/head.txt");
	}
	print "### saveSetting\n"	;

	unlink("$home/_bg/fox.txt");
	return 1;
}
sub log_analize
{
	my $file = $_[0]	;

	if(open(LLL ,"$file"))
	{
		while(<LLL>)
		{
			my $xxx = $_	;
			my ($dd1,$dd2,$dd3,$dd4,$lll,$dd6,$dd7) = split(/ /,$xxx)	;
			$gTotal   ++	;#全アクセス数
			if($lll =~ /\/read.cgi/)	{$gReadcgi++;next;}
			if($lll =~ /\.dat$/)		{$gDat++;next;}
			if($lll =~ /\.txt$/i)		{$gText++;next;}
			if($lll =~ /\.gz$/i)		{$gText++;next;}
			if($lll =~ /\.html$/)		{$gHtml++;next;}
			if($lll =~ /\.php$/i)		{$gHtml++;next;}
			if($dd7 =~ /301/)		{$gHtml++;next;}
			if($lll =~ /_bg/)		{$gHtml++;next;}
			if($lll =~ /\/$/)		{$gHtml++;next;}
			if($lll =~ /\.gif$/i)		{$gGif++;next;}
			if($lll =~ /\.ico$/i)		{$gGif++;next;}
			if($lll =~ /\.jpg$/i)		{$gGif++;next;}
			if($lll =~ /\.jpeg$/i)		{$gGif++;next;}
			if($lll =~ /\.cgi/)		{$gCgi++;next;}
			if($dd7 =~ /302/)		{$g302++;next;}
			if($lll =~ /\/dat\//)		{$gHtml++;next;}
logout("--- $lll ($dd7)\n");
		}
		close(LLL)	;
	}
	else
	{
		logout("[[[[[  open error $file  ]]]]]\n\n");
	}

	return 1		;
}

sub reportout
{
	my $xTotal = $gTotal	;#全アクセス数
	my $xReadcgi = $gReadcgi;#read.cgi
	my $xHtml = $gHtml	;# .html
	my $xDat = $gDat	;# .dat
	my $xGif = $gGif	;# .gif .jpg ...etc
	my $xText = $gText	;# .txt
	my $xSonota = $gSonota	;# その他

	$xHtml += $gCgi		;# other CGIs
	$xHtml += $g302		;# 404 not found

	if(!open(LOG,">>$rFile"))	{return 0;}

	print LOG "$year$mon$mday$hour\t$xTotal\t$xReadcgi\t$xHtml\t$xDat\t$xGif\t$xText\t$xSonota\n"	;
	close(LOG)	;

	return 1	;
}
sub logout
{
return 1;

	if(!open(LOG,">>$lFile"))	{return 0;}

	print LOG $_[0]	;
	close(LOG)	;

	return 1	;
}
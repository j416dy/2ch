#!/usr/bin/perl -w
use strict;
use CGI;
use File::stat;
#use LWP::UserAgent;
#use HTTP::Request;
#use HTTP::Status;

local our ($cgi, $livespan, $target, @BBSlist, $mxx);

$| = 1		;
$cgi = new CGI	;
umask(0)	;

$livespan = 6	;

$target = '../'	;

@BBSlist = &getBBSlist()	;

#	タイムゾーンの設定
	$ENV{TZ} = 'Asia/Tokyo';
	my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime;
	$year += 1900	;
	$mon ++		;
	if($mon  < 10)	{$mon  = "0$mon" ;}
	if($mday < 10)	{$mday = "0$mday";}
	if($hour < 10)	{$hour = "0$hour";}
	if($min  < 10)	{$min  = "0$min" ;}
	if($sec  < 10)	{$sec  = "0$sec" ;}


print "Content-Type: text/html\n\n"	;
print <<EOF;
<HTML lang="ja">
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
</HEAD>
<BODY bgcolor=white>
<font color=green>24open</font><BR>
EOF

#if(open(LOG,'>>','mmmlog.cgi'))	{print LOG "minute $year/$mon/$mday $hour:$min:$sec\n";close(LOG)	;}

$mxx = int($min)	;

print "min = $mxx<br>\n";
&step1()	;
&step2()	;
&step3()	;

print <<EOF;
<b>END</b>
</BODY>
</HTML>
EOF
exit;

###################################################
#	一時ファイル残骸お掃除
###################################################
sub ZangaiClear
{
	my ($bbs) = @_		;
	my $zan = "../$bbs"	;

	system("rm -f $zan/*.tmp")	;
	system("rm -f $zan/*.tmps")	;

	return 1;
}
###################################################
#	キャッシュお掃除
###################################################
sub CasheClear2
{
	my ($bbs) = @_		;
	my $tt0 = "../$bbs/i/"	;
	my $tt1 = "../$bbs/ii/"	;

	system("mv $tt0 $tt1")	;
	mkdir($tt0, 0777)	;
	chmod(0777, $tt0)	;
	system("rm -rf $tt1")	;

	return 1;
}
###################################################
#	キャッシュお掃除
###################################################
sub CasheClear
{
	my ($bbs) = @_		;
	my $ttt = "../$bbs/i/"	;

	my @dirs		;
	my $folder = $ttt	;
	if(opendir(DIR, $folder))
	{
		@dirs = grep(!/^\./ && "$folder$_", readdir(DIR));
		closedir DIR		;
	}

	my $nxx = @dirs			;
print "N=$nxx($folder) -> ";
	my $ima = time			;
	foreach my $xxx (@dirs)
	{
		my $prmtime = (local $_=stat("$folder$xxx")) ? $_->mtime : 0;
		my $keika = $ima - $prmtime	;
		$keika /= 60		;
		$keika /= 60		;
		$keika = int($keika)	;
#print "$xxx($keika) -> ";
		if($keika > $livespan)	{unlink("$folder$xxx");}
	}

	return 1	;
}
###################################################
#	BBSlist 取得
###################################################
sub getBBSlist
{
	my $hhh = $target	;

	my @dirs		;
	my $folder = $hhh	;
	if(opendir(DIR, $folder))
	{
		@dirs = grep(!/^\./ && -d "$folder$_", readdir(DIR));
		closedir DIR	;
	}
	my @aaa			;
	foreach (@dirs)
	{
		if(!-e "../$_/i/")	{next;}
		if(/^ZZZ-/)		{next;}
		push(@aaa, $_)	;
	}
	return sort @aaa	;
}
sub getNextBBS
{
	my $lastBBS = ''	;
	if(open(BBS,'F35lastBBS.txt'))
	{
		$lastBBS = <BBS>;
		close(BBS)	;
	}
#	$lastBBS = 'news7'	;

#print "lastBBS = $lastBBS<br>\n";
	my @sdirs = @BBSlist	;
	my $nx = 0		;
	my $nextBBS = ''	;
	foreach (@sdirs)
	{
#print " -- $_<br>\n";
		if($nx)	{$nextBBS = $_;last;}
		if($_ eq $lastBBS)	{$nx = 1;}
	}
	if($nx eq 0)		{$nextBBS = $sdirs[0];}
	if($nextBBS eq '')	{$nextBBS = $sdirs[0];}
#print "nextBBS = $nextBBS<br>\n";
	if(open(BBS,'>','F35lastBBS.txt'))
	{
		print BBS $nextBBS;
		close(BBS)	;
	}

	return $nextBBS		;
}
###################################################
#	step 1 おすすめサマリー
###################################################
sub step1
{
	if($mxx eq 0)	{return 0;}
#	if($xx % 5)	{return 0;}
print "<b>STEP1</b><br>\n";

#	my $bbs = 'trafficinfo'		;
#	my $bbs = 'mnewsplus'		;
	my $bbs = getNextBBS()		;

print "$bbs -> ";

	&CasheClear($bbs)		;
	&ZangaiClear($bbs)		;

print "end<br>\n";
	return 1	;
}
###################################################
#	step 2
###################################################
sub step2
{
print "<b>STEP2</b><br>\n";

	umask(0)				;
	if(!-e '/md/tmp/')
	{
		mkdir('/md/tmp/',0777)		;
		chmod(0777,'/md/tmp/')		;
	}
	if(!-e '/md/tmp/speedy/')
	{
		mkdir('/md/tmp/speedy/',0777)	;
		chmod(0777,'/md/tmp/speedy/')	;
	}
	if(!-e '/md/tmp/book/')
	{
		mkdir('/md/tmp/book/',0777)	;
		chmod(0777,'/md/tmp/book/')	;
	}

	if($mxx ne 0)	{return 0;}

	my $book0 = '/md/tmp/book/'		;
	my $book1 = '/md/tmp/book1/'		;
	if(!-e $book0)	{return 0;}
	rename($book0,$book1)			;
	unless(-e $book0){mkdir($book0,0777);}
	system("rm -rf $book1")			;
	return	1;
}
###################################################
#	step 3
###################################################
sub step3
{
print "<b>STEP3</b><br>\n";
}
##############################################################################

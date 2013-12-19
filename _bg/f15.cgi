#!/usr/bin/perl -w

# f15.cgi
# last modified 2002年 8月 27日 by あぼーん男爵

	use strict;
	use File::stat;
	use POSIX qw(:errno_h strftime);

	use IPC::SysV qw(ftok IPC_CREAT IPC_EXCL IPC_NOWAIT SEM_R SEM_A SEM_UNDO);
	use IPC::Semaphore;

	use lib qw(../test);
	use BBSD;

#	スクリプトのエラーを出力する為の処理です。通常は必要ありません。
#	{$|=1; print "Content-Type: text/html\n\n"; open STDERR, '>&', \*STDOUT;}
	{$|=1; print "Content-Type: text/html\n\n"; open STDERR, '>&STDOUT';}

	local our $mes		= 'The end of work.';

##################################################
#	設定ここから
##################################################

#	local our ($FILE_LIST, $FILE_PROXY0, $FILE_PROXY1, $FILE_LOG);

#	タイムゾーンの設定
	$ENV{TZ} = 'Asia/Tokyo'	;

	local our @subjects	;

	local our ($resNumMax, $resNumMaxL, $daresNum, $daresDay, $Rule150,
			$starRule, $rotateLog, $noAutoClean, $noBgJobXXX, $MesMes);
	$resNumMax   = 1000	;
	$resNumMaxL  = 1500	;
	$daresNum    = 2500	;
	$daresDay    = 1000*24	;
	$Rule150     = 9999	;
	$starRule    = undef	;
	$rotateLog   = undef	;
	$noAutoClean = 0	;
	$noBgJobXXX  = 0	;

#	スターシステムを有効にする場合は f22info.cgi で↓のように設定
#	$starRule = { NonMax => 50, StarMax => 500, CAP => 1, BE => 0, MARU => 0, KABU => 0 };
#	VIP のようにログをローテーションする場合は↓のように設定
#	$rotateLog = [ 'news4vip', 'some_board' ]; # 板名の配列リファレンス
#	AutoClean を実行しない場合は $noAutoClean を非ゼロ値に設定
#	BgJobXXX を実行しない場合は $noBgJobXXX を非ゼロ値に設定

##################################################
sub BgJob
{
	my $ita = $_[0]		;

require 'f22info.cgi'		;
&setF22info($ita)		;

	$mes .= " [$ita]"	;
	&BgJobXXX($ita)		;

#	my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime;
#	$year += 1900	;
#	$mon ++		;

#	open(YAN0,'>>','../test/00yakin.cgi');print YAN0 "***** $MesMes ($min)\n";close(YAN0);
}
##################################################
sub BgJobXXX
{
	my $ita = $_[0]		;

	if($noBgJobXXX)		{return 0;}

	local $_ = umask(0)	;
	my $ff0 = "../../_datArea/$ita"		;
	if(!-e $ff0)		{mkdir($ff0,0777);}		
	my $ff1 = "../../_datArea/$ita/pool"	;
	if(!-e $ff1)		{mkdir($ff1,0777);}		
	umask($_)		;

	if($ita =~ /tr$/)	{$resNumMax = 30; $resNumMaxL = 0;}

	# dat 落ち処理で F22 との競合を避ける
	my ($semid, $sem) = ftok("../$ita", 1);
	if ($semid)
	{
		if (($sem = new IPC::Semaphore($semid, 1, IPC_CREAT | IPC_EXCL | SEM_R | SEM_A)))
			{$sem->setval(0, 1);}
		else	{$sem = new IPC::Semaphore($semid, 0, SEM_R | SEM_A);}
	}

	# 競合する時は先に入った方に任せて待たずにスキップ
	if (!$sem || $sem->op(0, -1, IPC_NOWAIT | SEM_UNDO))
	{
		@subjects = ()		;
		if(ref $starRule)	{&BgJob9($ita,$starRule); &BgJob2($ita);}
		elsif(!&BgJob1($ita))	{&BgJob2($ita);}
		if(@subjects)		{&UpdateSubject($ita);}

		if($ita =~ /tr$/)
		{
			&RemoveLogFile("../../_datArea/$ita/pool/",1)	;
		}
		if ($sem)
		{
			$sem->op(0, 1, SEM_UNDO)	;
			$sem->remove			;
		}
	}
}
##################################################
sub RemoveLogFile
{
	my $folder = $_[0]	;	#ターゲットのフォルダ
	my $keikad = $_[1]	;	#N日以降たったら削除
	my @sdirs		;
&F22nippo("RemoveLogFile($folder)");

	if(opendir(DIR, $folder))
	{
		@sdirs = sort grep(!/^\./ && -f "$folder$_", readdir(DIR));
		closedir DIR	;
	}
	if(@sdirs < 1)		{return 0;}
#&F22nippo('--- fileNum = ' . @sdirs);

	my $ctime = time	;
foreach my $ttt (@sdirs)
{
	my $prmtime = (local $_=stat("$folder$ttt")) ? $_->mtime : 0;
	my $keika = $ctime - $prmtime	;
	$keika /= 60		;	#pun
	$keika /= 60		;	#jikan
	$keika /= 24		;	#nichi
	$keika = int($keika)	;
	if($keika > $keikad)
	{
		if($ttt !~ /bbslist/){unlink("$folder$ttt");}
#&F22nippo("--- $folder$ttt removed. $keika > $keikad");
	}
}
	return 1;
}
##################################################
sub UpdateSubject4snow
{
	my	$bbs = $_[0]	;

#	&F22nippo('############### N=' . @subjects . " ($bbs,$bbsPath)");
#	&F22nippo('##### ' . join(',', @subjects));
	my $err = bbsd($bbs, 'purge', join(',', @subjects), 'nolog');
	if ($err) { &F22nippo("bbsd(purge): $bbs/" . join(',', @subjects) . ": $err"); }

	open(local *F, "../$bbs/subject.txt") or return 1;
	my $utime = $^V lt v5.7.2 ? time : undef;
	foreach (grep(/^924\d{7}$/, <F>)) {
		/^(\d+)\.dat<>/ or next;
		utime($utime, $utime, "../$bbs/dat/$1.dat");
		$err = bbsd($bbs, 'raise', $1, 'nolog');
		if ($err) { &F22nippo("bbsd(raise): $bbs/$1: $err"); }
	}
	close(F);

	return 1;
}
##################################################
sub UpdateSubject
{
	my	$bbs = $_[0]	;

	if(IsSnowmanServer)
	{
		return &UpdateSubject4snow($bbs)	;
	}

	my	$bbsPath = "../$bbs/subject.txt"	;
	my	$bbsTemp = "../$bbs/subject.txt.$$"	;
	my	$iii		;
	my	(@sub1, @sub924);
	my	%datDel		;

#	&F22nippo('############### N=' . @subjects . " ($bbs,$bbsPath)");
	foreach (@subjects)
	{
#		&F22nippo('##### ' . $iii++ . "=$_");
		$datDel{$_} = 'deldel';
	}

	if(open(SUBTXT, $bbsPath))
	{
		my $utime = $^V lt v5.7.2 ? time : undef;
		local $_; while (<SUBTXT>)
		{
			my ($datNN, $subn) = split(/\.dat<>/)	;
			if($datDel{$datNN})
			{
				chomp($subn);
#				&F22nippo("##### $datDel{$datNN} ($datNN)$datNN.dat | $subn");
			}
			elsif($datNN =~ /^924\d{7}$/)
			{
				utime($utime, $utime, "../$bbs/dat/$datNN.dat");
				push(@sub924, $_)	;
			}
			else
			{
				push(@sub1, $_)		;
			}
		}
		close(SUBTXT)	;
	}

#	&F22nippo("##### SUBJECT.TXT ##########");
	if(open(SUB2, '>', $bbsTemp))
	{
    		print SUB2 @sub924, @sub1;
		close(SUB2)	;
		rename($bbsTemp, $bbsPath);
	}
	return 1;
}
##################################################
##################################################
sub StarThread
{
	my $starRule = $_[1];
	my $firstlog = '';

	if(open(THREAD, $_[0]))
	{
		#１つ目の要素を読み込む
		$firstlog = <THREAD>;
		#改行カット
		chomp($firstlog);
		close(THREAD)	;
	}

	#１つ目の要素を加工する
	my ($from,$mail,$time,$message,$title) = split(/<>/,$firstlog);

$time =~ /ID:(.+)/;
print "Star## <b> $from $1 </b><br>\n";

	if($starRule->{CAP})
	{
		if($from =~ /★$/)	{return 1;}
	}
	if($starRule->{BE})
	{
		if($time =~ /2BP/ && $starRule->{BE} >= 5)	{return 1;}
		if($time =~ /BRZ/ && $starRule->{BE} >= 4)	{return 1;}
		if($time =~ /PLT/ && $starRule->{BE} >= 3)	{return 1;}
		if($time =~ /DIA/ && $starRule->{BE} >= 2)	{return 1;}
		if($time =~ /S(?:<[^>]+>)?★/)			{return 1;}
	}
	if($starRule->{MARU})
	{
		if($time =~ /●/)	{return 1;}
	}
	if($starRule->{KABU})
	{
		if($time =~ /株主優待/)	{return 1;}
	}

	return 0;
}
##################################################
sub BgJob9
{
	my $ita = $_[0]	;
	my $folder = "../$ita/dat/"	;
	my $NonMax  = $_[1]->{NonMax}	;
	my $StarMax = $_[1]->{StarMax}	;
	my @sdirs	;

	if($ita ne 'liveplus')	{return 0;}

print "Star## <br>\n";
	if(opendir(DIR, $folder))
	{
		@sdirs = sort grep(!/^\./ && -f "$folder$_" && /\.dat$/, readdir(DIR));
		closedir DIR	;
	}
	my $fileNum = @sdirs	;
	&F22nippo("J1#$ita = $fileNum <= $resNumMaxL");
#	if($fileNum <= $resNumMaxL)	{return 0;}

print "Star## fileNum = $fileNum<br>\n";
	my ($Star, $NonS, $ccc) = (0, 0);
	my (%xdateStar, %xdateNonS)	;
	foreach (@sdirs)
	{
		my $xxx = $_	;
		$xxx =~ s/\.dat$//i or next	;
		my $xdate = &getLastUpdate("$folder$_")		;
		my $xStar = &StarThread("$folder$_",$_[1])	;
		if($xStar)	{$Star ++; $xdateStar{$xxx} = $xdate;}
		else		{$NonS ++; $xdateNonS{$xxx} = $xdate;}
	}
print "Star## Star = $Star<br>\n";
print "Star## NonS = $NonS<br>\n";
	my @junbanStar = sort { $xdateStar{$a} <=> $xdateStar{$b}; } keys %xdateStar	;
	my @junbanNonS = sort { $xdateNonS{$a} <=> $xdateNonS{$b}; } keys %xdateNonS	;
# all = 64
# star = 52
# other = 12

	$ccc = $NonS		;
	foreach (@junbanNonS)
	{
		if($ccc <= $NonMax)	{last;}

		my $moveto = "../../_datArea/$ita/pool/"	;
		my $delhtm = "../$ita/html/$_.html"		;
		my $cmdx1 = "$folder$_.dat"	;
		my $cmdx2 = "$moveto$_.dat"	;

		if(-e $cmdx2)	{next;}

		_mv($cmdx1, $cmdx2)	;
		$ccc --			;
		push(@subjects, $_)	;
		unlink($delhtm)		;
	}
print "Star## STEP1 END<br>\n";
	$ccc = $Star		;
	foreach (@junbanStar)
	{
		if($ccc <= $StarMax)	{last;}

		my $moveto = "../../_datArea/$ita/pool/"	;
		my $delhtm = "../$ita/html/$_.html"		;
		my $cmdx1 = "$folder$_.dat"	;
		my $cmdx2 = "$moveto$_.dat"	;

		if(-e $cmdx2)	{next;}

		_mv($cmdx1, $cmdx2)	;
		$ccc --			;
		push(@subjects, $_)	;
		unlink($delhtm)		;
	}
print "Star## STEP2 END<br>\n";
	return 1;
}
##################################################
sub BgJob1
{
	my $ita = $_[0]	;
	my $folder = "../$ita/dat/";
	my @sdirs	;
	my %xdate	;

	if(opendir(DIR, $folder))
	{
		@sdirs = sort grep(!/^\./ && -f "$folder$_" && /\.dat$/, readdir(DIR));
		closedir DIR	;
	}
	my $fileNum = @sdirs	;
	&F22nippo("J1#$ita = $fileNum <= $resNumMaxL");
	if($fileNum <= $resNumMaxL)	{return 0;}

	foreach (@sdirs)
	{
		my $xxx = $_	;
		$xxx =~ s/\.dat$//i or next	;
		$xdate{$xxx} = &getLastUpdate("$folder$_")	;
	}

	my @junban = sort { $xdate{$a} <=> $xdate{$b}; } keys %xdate	;
	my $ccc = $fileNum	;
	foreach (@junban)
	{
if(/^924/)
{
	$ccc --	;
	next	;
}

if($ccc <= $resNumMax)
{
#&F22nippo("--- $_ $xdate{$_}");
	$ccc --	;
}
else
{
	my $moveto = "../../_datArea/$ita/pool/"	;
	my $delhtm = "../$ita/html/$_.html"		;

my $cmdx1 = "$folder$_.dat"	;
my $cmdx2 = "$moveto$_.dat"	;

	if(-e $cmdx2)
	{
#&F22nippo("EEE $_ $xdate{$_}");
	}
	else
	{
#&F22nippo("ooo $_ $xdate{$_}");
#&F22nippo("$cmdx1,$cmdx2,$delhtm");
&F22nippo($cmdx1);
#print "mv $cmdx1 $cmdx2<br>\n"	;
		_mv($cmdx1, $cmdx2)	;
		$ccc --	;
		push(@subjects, $_)	;

#####TOP700
my $xTime = time		;
my $DNSbby = "206.223.150.131"	;
my $AHOST = "d8.d7.d6.d5.d4.d3.d2.d1.d0.$_.$ita.$ENV{'SERVER_NAME'}.3.$xTime.33.u.la.";
&foxDNSquery($AHOST,$DNSbby)	;
#####TOP700
	}
	unlink($delhtm)		;
}
	}
	return 1;
}
#############################################################################
#	BBY/BBS
#############################################################################
sub foxDNSquery
{
	my ($host,$nameserver) = @_	;

print "$host<br>\n"	;

	use Net::DNS;
	my $res = Net::DNS::Resolver->new(recurse => 0, nameservers => [$nameserver]);
	$res->bgsend($host);

	return 1		;
}
##################################################
sub getLastUpdate
{
	local $_ = stat($_[0])			;
	my @lt = localtime($_ ? $_->mtime : 0)	;
	return strftime('%Y%m%d%H%M%S', @lt)	;
}
##################################################
sub BgJob2
{
	my $ita = $_[0]	;
	my $folder = "../$ita/dat/";
	my @sdirs	;

	if(opendir(DIR, $folder))
	{
		@sdirs = sort grep(!/^\./ && -f "$folder$_" && /\.dat$/, readdir(DIR));
		closedir DIR	;
	}
	if(@sdirs < 1)		{return 0;}
	&F22nippo("J2#$ita = " . @sdirs);

	foreach (@sdirs)
	{
		if(&IsOldDat($folder, $_))
		{
			&go2Pool($ita, $_)	;
		}
	}

	return 1;
}
sub go2Pool
{
	my $d0 = "../$_[0]/dat/$_[1]"	;	
	my $d1 = "../../_datArea/$_[0]/pool/$_[1]";
	my $d2 = $_[1]			;
	$d2 =~ s/\.dat$//i		;
	my $delHtml = "../$_[0]/html/$d2.html"	;

print "mv $d0 $d1<br>\n";
_mv($d0, $d1)		;
unlink($delHtml)	;
	push(@subjects, $d2)	;

#####TOP700
my $xTime = time		;
my $DNSbby = "206.223.150.131"	;
my $AHOST = "d8.d7.d6.d5.d4.d3.d2.d1.d0.$d2.$_[0].$ENV{'SERVER_NAME'}.3.$xTime.33.u.la.";
&foxDNSquery($AHOST,$DNSbby)	;
#####TOP700

#	&F22nippo("#go $d0 $d1 $delHtml");
}
sub IsOldDat
{
	my $fName = "$_[0]$_[1]";
	my $datno = $_[1]	;
	my $gPool = 0		;
	my ($prmode, $prsize, $prmtime) = (local $_=stat($fName)) ? ($_->mode, $_->size, $_->mtime) : (0, 0, 0);
	$prsize = int($prsize/1024)	;

	my $ctime = time	;
	my $keika = $ctime - $prmtime	;
	$keika /= 60		;	#pun
	$keika /= 60		;	#jikan
	my $keikaH = int($keika);
	$keika /= 24		;	#nichi
	$keika = int($keika)	;

	if($datno =~ /^924/)	{return 0;}

	$datno =~ s/\.dat$//i	;
	my $keika1 = $ctime - $datno	;
	$keika1 /= 60	;	#pun
	$keika1 /= 60	;	#jikan
	$keika1 /= 24	;	#nichi
	$keika1 = int($keika1)	;

#	&F22nippo("#R150 $datno $keika1 ($Rule150) $prmode");

	if($keika1 > $Rule150)	{return 1;}	#150日ルール。
	my $x24 = $daresDay	;		#hour
#print "keikaH = $keikaH , daresDay = $daresDay , <br>\n";
	if($x24 > 24)	{$x24 = 24;}
	if($keikaH < $x24)	{return 0;}	#$daresDay時間以上たっていないと対象外。
	if($prmode == 0100555)	{return 1;}	#スレッドストップ。
	if($prsize >= 512)	{return 1;}	#でかいのは落ち
	if($prsize >= 480 && $keika >= 7)	#480k over , 7days past after latest posting
				{return 1;}	#でかいのは落ち
	my $ts = 0;
	if($prsize < 64)			#小さいのは即死判定
	{
		if($keikaH < $daresDay)	{return 0;}
		$ts = threadSize($fName);
		if($ts < $daresNum)	{$gPool=1;}
	}
	elsif($prsize > 64)			#大きいのは 1,000超え判定
	{
		$ts = threadSize($fName);
		if($ts > 980)	{$gPool=1;} 
	}
	if($ts eq 0)		{return 0;}
	if($daresNum <= $ts && $ts <= 980)	{return 0;}

	&F22nippo("#$fName $gPool $keika($daresDay) $prsize ts=$ts($daresNum)");

	if($gPool eq 1)		{return 1;}
	return 0;
}
sub threadSize
{
	if(open(THREAD, $_[0]))
	{
		my @logdat=<THREAD>	;	#ログを配列に読み込む
		close(THREAD)		;
		return scalar @logdat	;
 	}
	return -1			;
}
##################################################
	my @flt = localtime;
	local our $fYmd = strftime('%Y%m%d', @flt);
	local our $fY_m_d_T = strftime('%Y/%m/%d %T', @flt);
if(&IsServerBusy){F22Exit('busy');}
else
{	#いろいろやろうかと、、
	my $iii = 0	;
    for($iii = 1; $iii <= 18; $iii++)
    {

#	&F22nippo('#いろいろやろうかと、、');
	my $LastBBS = &getLastBBS;
	my $NextBBS = &getNextBBS($LastBBS);
	if($NextBBS =~ /tr$/)	{$NextBBS = &getNextBBS($NextBBS);}
#	&F22nippo("#前回は$LastBBSだったので、今回は$NextBBS。");
print "$LastBBS -&gt; $NextBBS<br>\n";
#	&F22nippo("($iii)$LastBBS -&gt; $NextBBS<br>\n")	;
	local our @sigs;
	$SIG{$_} = sub { push(@sigs, $_[0]); } foreach (qw/HUP INT PIPE ALRM TERM USR1 USR2 IO VTALRM PROF/);
	&BgJob($NextBBS);
	&F22nippo('Got signal' . (@sigs > 1 ? 's: ' : ': ') . join(', ', @sigs)) if (@sigs);

	open(FLB,'>','lastbbs15.txt');
	print FLB $NextBBS;
	close(FLB)	;
    }
}
sub getLastBBS
{
	if(!open(LB,'lastbbs15.txt')){return 'open err LASTBBS';}
	my $lb = <LB>	;
	close(LB)	;
	return $lb	;
}
sub getNextBBS
{
	my $cb = $_[0]	; 
	if(!open(BBSLIST,'../_service/bbslist.txt')){return 'open err BBSLIST';}
	my @bbslist = <BBSLIST>;
	close(BBSLIST)	;

	my $find = 0	;
	foreach (@bbslist)
	{
		chomp	;
		if($find)	{return $_;}
		if($_ eq $cb)	{$find = 1;}
	}
	if($bbslist[0])
	{
		#$bbslist[0] =~ s/\r?\n?$//;
		return $bbslist[0];
	}
	return 'next'	;
}
##################################################
sub IsServerBusy
{
	return 0;

	my ($upt, $av);
	open(UPTIME, 'uptime |'); $upt = <UPTIME>; close(UPTIME);
	($av) = $upt =~ /([.\d]+), [.\d]+, [.\d]+$/;

	open (LOG, '>>', "../_service/$fYmd.txt");
	print LOG "$fY_m_d_T LA=$upt";
	close (LOG);

	if($av > 10)	{return 1;}
	return 0;
}
##################################################
sub F22Exit
{
	open (LOG, '>>', "../_service/err$fYmd.txt");
	print LOG "$fY_m_d_T $_[0]\n";
	close (LOG);

	print "Content-Type: text/html; charset=shift_jis\n\n";
	print "えらーで　おわた。\n";
#	exit;
}
##################################################
sub F22nippo
{
return;
	open (LOG, '>>', "logs/$fYmd.txt");
	print LOG "$fY_m_d_T F15 $_[0]\n";
	close (LOG);
}


# XXX
#print "Content-Type: text/plain\n\n$mes\n";
print "$mes\n";
exit;
#-------------------------------------------------


##################################################
sub _cp
{
	local $/;
	open(local *SRC, $_[0]) or return;
	open(local *DST, '>', $_[1]) or close(SRC), return;
	my $st = stat(*SRC);
	print DST <SRC>;
	close(DST);
	close(SRC);
	chmod($st->mode, $_[1]);
	utime($st->atime, $st->mtime, $_[1]);
	1;
}
sub _mv
{
	rename($_[0], $_[1]) and return 1;
	$! == EXDEV or return;
	_cp($_[0], $_[1]) and unlink($_[0]);
}
#################################################################################################
#
#################################################################################################

#!/usr/bin/perl -w

# f22.cgi
# last modified 2002年 8月 27日 by あぼーん男爵

	use strict;
	use File::stat;
	use Socket;
	use IO::Handle qw(autoflush);
	use POSIX qw(:errno_h strftime);
	use Time::Local qw(timegm);

	use IPC::SysV qw(ftok IPC_CREAT IPC_EXCL IPC_NOWAIT SEM_R SEM_A SEM_UNDO);
	use IPC::Semaphore;

	use lib qw(../test);
	use BBSD;

#	スクリプトのエラーを出力する為の処理です。通常は必要ありません。
#	{$|=1; print "Content-Type: text/html\n\n"; open STDERR, '>&', \*STDOUT;}
	{$|=1; print "Content-Type: text/html\n\n"; open STDERR, '>&STDOUT';}

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
sub AutoClean
{
	if($noAutoClean)	{return 0;}

require 'pool.cgi'	;
&Pool($_[0])		;

	return 1;
}
##################################################
sub BgJob
{
	my $ita = $_[0]		;

require 'f22info.cgi'		;
&setF22info($ita)		;

	&BgJobXXX($ita)		;

	my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime;
	$year += 1900	;
	$mon ++		;

	&AutoClean($ita)	;

	# news4vip, 12時00分のみ
	if(ref $rotateLog && $hour == 12 && $min < 10)
	{
		foreach (@$rotateLog)
		{
			&RenameLogFile("../../test/ggg/${_}dat/",14);
		}
	}
	#if($hour > 1 && $hour < 12 && $min > 40)
	if($hour == 2 && $min > 40)
	{
		$MesMes = 'log clear';
		&RemoveLogFile("./logs/",3)		;
		&RemoveLogFile("../_service/",3)	;
		#&RemoveLogFile("../../test/ggg/${ita}dat/",14)	;
		#&RemoveLogFile("../../test/ggg/${ita}name/",2)	;
		&RemoveLogFile("../test/sss/",14)	;
		# ggg の消去で単純に $ita を使った場合
		# 当該サーバ上の板数が 3 の倍数等だと
		# いつまでも順番が回ってこない板が出てしまう
		if(open(local *F, '../_service/bbslist.txt'))
		{
			local $_; while	(<F>)
			{
				chomp	;
				&RemoveLogFile("../../test/ggg/${_}dat/",14)	;
				&RemoveLogFile("../../test/ggg/${_}name/",2)	;
			}
			close(F)	;
		}
	}
	if($min < 10)
	{

		my $ninzuu = &getNinzu	;
		open (LOG,'>>',"../_service/IPnum-$year-$mon-$mday.txt");
		print LOG "$year/$mon/$mday $hour:$min:$sec $ninzuu\n";
		close (LOG);

		$MesMes = 'tool clear'	;

		local $_ = umask(0)	;
		foreach my $bck0 ('/md/tmp/book', '../test/book', '../test/cook')
		{
			my $bck1 = $bck0 . '1'	;
			rename($bck0, $bck1)	;
			unless(-e $bck0)	{mkdir($bck0, 0777);}
			_rm_rf($bck1)		;
		}
		umask($_)		;

		if(IsSnowmanServer && open(local *F, '../_service/bbslist.txt'))
		{
			# clearids の前に各フロントの countids 終了を期したいが
			# sleep するのは筋が悪いしとりあえずここでは対策しない
			while (<F>)
			{
				chomp	;
				my $err = bbsd_db($_, 'clearids', 'samba24', 'nolog');
				if ($err)	{ &F22nippo("bbsd_db(clearids): $_: $err"); }
			}
			close(F)	;
		}
	}

	if(IsSnowmanServer && $ENV{SERVER_NAME} !~ /bbspink\.com$/ && -e '../_service/bbslist.txt' && $^V ge v5.8.0)
	{
		my $src = '../test/bbs-yakin.cgi';
		my $dst = '../test/maido3ad'	;
		my ($stsrc, $stdst) = (stat($src), stat($dst));
		my (@bbss, @dstfiles)		;
		if(open(local *F, '../_service/bbslist.txt'))
		{
			@bbss = sort <F>;
			close(F)	;
			chomp(@bbss)	;
		}
		if($stdst && opendir(local *D, $dst))
		{
			@dstfiles = sort grep(-f "$dst/$_", readdir(D));
			closedir(D)	;
		}
		if($stsrc && (!$stdst || $stsrc->mtime > $stdst->mtime || join(',', @bbss) ne join(',', @dstfiles)))
		{
			require $src	;
			my %garbage = map(($_ => 1), @dstfiles);
			unless($stdst)
			{
				mkdir($dst, 0755);
				chmod(0755, $dst);
			}
			foreach my $bbs (@bbss)
			{
				local $_ = stat("$dst/$bbs")	;
				delete $garbage{$bbs}		;
				next if ($_ && $stsrc->mtime <= $_->mtime);
				if(open(local *HTM, '>', \$_))
				{
					# YakinCounterCode() ではファイルハンドル名が HTM になってる
					&YakinCounterCode($bbs)	;
					close(HTM)		;
					s/^<P>//i		;
					if(open(HTM, '>', "$dst/$bbs.$$"))
					{
						print HTM	;
						close(HTM)	;
						chmod(0644, "$dst/$bbs.$$")				;
						utime($stsrc->atime, $stsrc->mtime, "$dst/$bbs.$$")	;
						rename("$dst/$bbs.$$", "$dst/$bbs")			;
						&F22nippo("generated \"$dst/$bbs\" from \"$src\"")	;
					}
				}
			}
			unlink(map("$dst/$_", keys %garbage))	;
			utime($stsrc->atime, $stsrc->mtime, $dst);
		}
	}

#	open(YAN0,'>>','../test/00yakin.cgi');print YAN0 "***** $MesMes ($min)\n";close(YAN0);
}
sub getNinzu
{
	my $nfiles = 0	;

	if(IsSnowmanServer)
	{
		opendir(DIR, '..') or return 0;
		foreach (grep(!/^(?:[._]|ZZZ-)/ && !-f "../$_" && -e "../$_/SETTING.TXT", readdir(DIR)))
		{
			my $n = bbsd_db($_, 'countids', 'samba24', 'nolog');
			if ($n =~ /\D/)	{ &F22nippo("bbsd_db(countids): $_: $n"); }
			else		{ $nfiles += $n; }
		}
		closedir DIR	;
	}
	else
	{
		foreach my $d ('/md/tmp/book', '../test/book')
		{
			opendir(DIR, $d) or next;
			$nfiles = grep(!/^\./ && -f "$d/$_", readdir(DIR));
			closedir DIR	;
			last		;
		}
	}

	return $nfiles	;
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

	# dat 落ち処理で F15 との競合を避ける
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

	if(-e "../ZZZ-$ita")
	{
		foreach ('SETTING.TXT', 'head.txt', '1000.txt')
		{
#			_cp("../$ita/$_", "../ZZZ-$ita/$_")	;
			_cp("../$ita/$_", "../_zzz/$ita/$_")	;
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
sub RenameLogFile
{
	my ($dir, $num) = @_;

	$dir =~ s/\/$//;
	my $olddir = "$dir.old";

	rename("$dir.$num", $olddir);
	_rm_rf($olddir);

	for (my $i = $num; $i > 0; $i--) {
		rename("$dir." . ($i - 1), "$dir.$i");
	}
	rename($dir, "$dir.0");
	mkdir($dir, 0777);
	chmod(0777, $dir);

	return 0;
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
print "mv $cmdx1 $cmdx2<br>\n"	;
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

#print "$host<br>\n"	;

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

#	&F22nippo('#いろいろやろうかと、、');
	my $LastBBS = &getLastBBS;
	my $NextBBS = &getNextBBS($LastBBS);
#	&F22nippo("#前回は$LastBBSだったので、今回は$NextBBS。");
	&F22nippo("($iii)$LastBBS ---> $NextBBS")	;

	local our @sigs;
	$SIG{$_} = sub { push(@sigs, $_[0]); } foreach (qw/HUP INT PIPE ALRM TERM USR1 USR2 IO VTALRM PROF/);
	&BgJob($NextBBS);
	&F22nippo('Got signal' . (@sigs > 1 ? 's: ' : ': ') . join(', ', @sigs)) if (@sigs);

	open(FLB,'>','lastbbs.txt');
	print FLB $NextBBS;
	close(FLB)	;
}
sub getLastBBS
{
	if(!open(LB,'lastbbs.txt')){return 'open err LASTBBS';}
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
&F22nippo("##### $find $_ $cb");
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
	my ($upt, $av);
	open(UPTIME, 'uptime |'); $upt = <UPTIME>; close(UPTIME);
	($av) = $upt =~ /([.\d]+), [.\d]+, [.\d]+$/;

	open (LOG, '>>', "../_service/$fYmd.txt");
	print LOG "$fY_m_d_T LA=$upt";
	close (LOG);

	if($av > 100)	{return 1;}
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
	open (LOG, '>>', "logs/$fYmd.txt");
	print LOG "$fY_m_d_T F22 $_[0]\n";
	close (LOG);
}

##################################################
#	設定ここまで
##################################################


#=================================================
# ここから先、proxy.cgi 作成処理
#=================================================
# リスト取得の設定
#=================================================

#タイムアウト処理
sub timeout { die local $! = ETIMEDOUT; }
$SIG{ALRM} = \&timeout;

my ($FILE_LOG);
my (@log, $mes, $time);

#ファイルのパス
#$FILE_PROXY8  = '../test/proxy998.cgi';
#$FILE_PROXY9  = '../test/proxy999.cgi';
$FILE_LOG     = 'logs/proxy_log.txt';

#取得先情報
#$server8      = 'qb4.2ch.net';
#$path8        = '/.f22x/proxy998.txt';
#$server9      = 'bbq.2ch.net';
#$path9        = '/F22/proxy999.txt';

# Get List
&get_2ch_file('qb6.2ch.net','/.f22x/proxy998.txt','../test/proxy998.cgi');
&get_2ch_file('f22base.2ch.net','/proxy999.txt','../test/proxy999.cgi');

&get_2ch_file('f22base.2ch.net','/docomo_ad.txt','../test/docomo_ad.txt');

$mes          = 'The end of work.';

#=================================================
# リストを作成する
#=================================================
# ファイルが壊れないよう、作業用ファイルに書いてからリネームする。
# proxy0.cgi からは、そのままの状態で書きこむ。

#=================================================
# 終了処理
#=================================================
# ログは規定数のみ保存する。
# 保存する数は、200という数値を変えることで変えられる。

$time = localtime;

chmod(0666, $FILE_LOG);
if ( open(IN, $FILE_LOG) ) {
    @log = <IN>;
    close(IN);
    $#log = 200 if ($#log > 200);
}

if ( open(LOG, '>', $FILE_LOG) ) {
    print LOG "$time $mes\n";
    print LOG @log;
    close(LOG);
}

print "Content-Type: text/plain\n\n$mes\n";
exit;
#-------------------------------------------------

######	エラー処理
sub error
{
	my ($topic) = @_;
	print "Content-Type: text/html; charset=shift_jis\n\n$topic";
	exit;
}

######	get_2ch_file
sub get_2ch_file
{
	my ($server, $filename, $target) = @_;

	return if (!$server || !$filename || !$target);

	my ($mode, $mtime) = (local $_=stat($target)) ? ($_->mode, $_->mtime) : (undef, undef);

	alarm(5);
	eval {
		my $host = inet_aton($server) or die "inet_aton: $server: $!";
		my $sockaddr = pack_sockaddr_in(80, $host);

		socket(local *SO, PF_INET, SOCK_STREAM, 0) or die "socket: $!";
		connect(SO, $sockaddr) or do { close(SO); die "connect: $server: $!"; };
		autoflush SO;
		$_ = defined $mtime ? strftime("If-Modified-Since: %a, %d %b %Y %T GMT\r\n", gmtime($mtime)) : '';
		print SO "GET $filename HTTP/1.1\r\nHost: $server\r\nConnection: close\r\n$_\r\n";

		my $status = 0;
		$mtime = undef;
		while (<SO>) {
			last if (!/\S/);
			/^HTTP\/\d+\.\d+ (\d+) / and $status = $1;
			/^Last-Modified: (?:Sun|Mon|Tue|Wed|Thu|Fri|Sat)\w*, {1,2}(\d{1,2})[ -](Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[ -](\d{2,4}) {1,2}(\d{1,2}):(\d{2}):(\d{2}) GMT/i
				and $mtime = timegm($6, $5, $4, $1, index('JanFebMarAprMayJunJulAugSepOctNovDec', $2) / 3, $3);
		}
		if ($status == 200) {
			open(local *FOUT, '>', "$target.$$") or do { local @_ = <SO>; close(SO); die "open: $target.$$: $!"; };
			#flock(FOUT, 2);
			print FOUT <SO>;
			close(FOUT);
		}
		else {
			local @_ = <SO>;
		}
		close(SO);
		die "HTTP status = $status;" if ($status != 200);
	};
	alarm(0);

	if ($@ && $@ !~ /^HTTP status = 304;/) {
		chomp($@);
		&F22nippo("get_2ch_file($server,$filename,$target) Failed($@)");
		unlink("$target.$$");
		return 1;
	}
	elsif (!$@) {
		chmod($mode, "$target.$$") if (defined $mode);
		utime($mtime, $mtime, "$target.$$") if (defined $mtime);
		rename("$target.$$", $target);
	}

	return 0;
}
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
sub _rm_rf
{
	opendir(local *D, $_[0]) or return;
	while (defined (my $e = readdir(D))) {
		if ($e eq '.' || $e eq '..') {
		}
		elsif (-d "$_[0]/$e") {
			_rm_rf("$_[0]/$e");
		}
		else {
			unlink("$_[0]/$e");
		}
	}
	closedir(D);
	rmdir($_[0]);
}
#################################################################################################
#
#################################################################################################

use strict;
use File::stat;
use Sys::Hostname;
use POSIX qw(strftime);

local our (%kname, %server); # italist.pl
local our ($remake, $magic, $DATAREA, $chanHome, $chanName, $ssvv);

##############################################################################
sub Pool
{
	my $ike = $_[0]				;
	if($ike =~ /tr$/)			{return 0;}

	require '../test/asokin/italist.pl'	;
	&readItaList				;

	print "<br><br>START($ike)------------><br>\n"	;

	$remake = 0				;

	$magic = 1000			;
	$DATAREA = '../../_datArea'	;
	print "DATAREA = $DATAREA<br>\n\n"	;

	$chanHome = 'http://www.2ch.net/'	;
	$chanName = '２ちゃんねる'		;

	$ssvv = (split(/\./, $ENV{SERVER_NAME} || $server{$ike} || hostname))[0];

	if(&Pool3Kako($ike))	{&Kakolist3($ike)	;}
	print "<------- end\n"	;
}
##############################################################################
sub Pool3Kako
{
	my	$itaName = $_[0]			;
	my	$folder = "$DATAREA/$itaName/pool/"	;

	print "Pool3Kako($folder)<br>\n"		;

	if($itaName =~ /tr$/)	{return 0;}

	my	@dirs		;
	if(opendir(DIR, $folder))
	{
		@dirs = grep(!/^\./ && -f "$folder$_" && /\.dat$/, readdir(DIR));
		closedir DIR	;
	}

	my $fileNum = @dirs	;
	print "FILE数 = $fileNum ($remake)<br>\n"	;
	if(!$remake && !$fileNum)	{return 0;}

	my	$ccc = 0		;
	foreach(@dirs)
	{
		my $xxx = $_		;
		$xxx =~ s/\.dat$//i	;
		if($ccc >= $magic)		{last;}
		if(int($xxx) < 1000000000)	{next;}


		my $moveto = "$DATAREA/$itaName/oyster/"	;
		mkdir($moveto, 0777)	;
		chmod(0777, $moveto)	;

		my $bangof0 = substr($xxx,0,4)	;
		$moveto = "$DATAREA/$itaName/oyster/$bangof0/"	;
		mkdir($moveto, 0777)	;
		chmod(0777, $moveto)	;

		my $cmdx1 = "$folder$xxx.dat"	;
		my $cmdx2 = "$moveto$xxx.dat"	;

		if(-e $cmdx2)	{next;}

#		print "cmdx1=$cmdx1\n"	;
#		print "cmdx2=$cmdx2\n"	;

		rename($cmdx1,$cmdx2)	;
		$ccc ++			;
	}
	return 1;
}
##############################################################################
sub Kakolist3
{
	my	$itaname = $_[0]			;
	my	$folder = "$DATAREA/$itaname/oyster/"	;
	my	$indexfile = "../$itaname/kako/index.html"	;
	my	$subjectxt = "../$itaname/kako/subject.txt"	;

	print "Kakolist3($itaname)<br>\n"			;

	my	@sdirs		;
	if(opendir(DIR, $folder))
	{
		@sdirs = sort { $b cmp $a; } grep(!/^\./ && -d "$folder$_" && /.../ && /^1/, readdir(DIR));
		closedir DIR	;
	}

	foreach my $ttt (@sdirs)
	{
		my $subd = 0	;
		my $infofile = "../$itaname/kako/o$ttt/info.txt";
		if(open(PINFOFILE, $infofile))
		{
			my $infoA = <PINFOFILE>;
			close(PINFOFILE);
			chomp($infoA)	;
			(undef,undef,undef,$subd,undef) = split(/\t/,$infoA);
		}
		&html_ctrl($itaname,$ttt,$subd);
	}

	local *PINDEXFILE		;
	open(PSUBJECTT,'>',$subjectxt)	;
	open(PINDEXFILE,'>',$indexfile)	;

&html_head($itaname)		;
	foreach my $ttt (@sdirs)
	{
		my ($subd, $subs);
		my $infofile = "../$itaname/kako/o$ttt/info.txt";
		if(open(PINFOFILE, $infofile))
		{
			my $infoA = <PINFOFILE>;
			close(PINFOFILE);
			chomp($infoA)	;
			(undef,undef,undef,$subd,$subs) = split(/\t/,$infoA);
print PINDEXFILE<<EOF;
<TR><TD><A TARGET="_blank" HREF="o$ttt/">#$itaname$ttt</A></TD><TD align=right>$subd</TD><TD align=right>$subs</TD><TD align=right><A HREF="o$ttt/subject.txt">subject.txt</A></TD></TR>
EOF
print PSUBJECTT "o$ttt<>$ttt ($subd)\n";
		}
	}
&html_foot		;
	close(PINDEXFILE)	;
	close(PSUBJECTT)	;

}
##############################################################################
sub html_ctrl
{
	my $bbs	  = $_[0]		;
	my $numx0 = &getDatNum($bbs,$_[1])	;
	my $numx1 = $_[2]		;
	if(!$remake && $numx1 == $numx0)	{return;}

	print "sate $_[1] $numx1/$numx0\n";

	mkdir("../$bbs/kako/o$_[1]",0777);
	chmod(0777,"../$bbs/kako/o$_[1]");

	&Kakohtml3($bbs,$_[1])	;
}
##############################################################################
sub Kakohtml3
{
	my ($itaname, $sokonum) = @_	;

	my $sx = substr($sokonum,0,4)	;
	my $folder = "$DATAREA/$itaname/oyster/$sx/"		;
	my $pfolder = "../$itaname/kako/o$sx/"			;
	my $infofile  = "../$itaname/kako/o$sx/info.txt"	;

	my $indexfile  = $pfolder . 'index.html'		;
	my $subjecttxt = $pfolder . 'subject.txt'		;

	print "Kakohtml3 $itaname ($sokonum)<br>\n"		;

	mkdir($pfolder, 0777)	;
	chmod(0777, $pfolder)	;

	my	@junban		;
	if(opendir(DIR, $folder))
	{
		@junban = sort { $b cmp $a; } grep(!/^\./ && -f "$folder$_", readdir(DIR));
		closedir DIR	;
	}

	my %threTitle		;

if(open(YSUBJECTT, $subjecttxt))
{
	local $_; while(<YSUBJECTT>)
	{
		my ($tNo,$tTitle) = split(/<>/)	;
		$tNo =~ s/\.dat$//i		;
		chomp($tTitle)			;
#print "$tNo,$tTitle<BR>\n";
		$threTitle{$tNo} = $tTitle	;
	}
	close(YSUBJECTT)	;
}

	my $ttlt = 0;
	local (*MSUBJECTT, *MINDEXFILE)	;
	open(MSUBJECTT,'>',$subjecttxt)	;
	if(open(MINDEXFILE,'>',$indexfile))
	{
		&html_index_head($itaname)	;
		foreach(@junban)
		{
			my $xxx = $_		;
			$xxx =~ s/\.dat$//i	;
#print "$_ $threTitle{$xxx}\n";
			if(!defined $threTitle{$xxx})
			{
				&html_index_body($folder,$xxx,$itaname)	;
			}
			else
			{
print MINDEXFILE "$xxx <A HREF=\"/test/read.cgi/$itaname/$xxx/\">$threTitle{$xxx}</A><BR>\n";
print MSUBJECTT  "$xxx.dat<>$threTitle{$xxx}\n";
			}
			$ttlt ++		;
		}
		&html_index_foot($itaname,$sokonum,$infofile,$ttlt)	;
		close(MINDEXFILE)	;
	}
	close(MSUBJECTT)	;
}
##############################################################################
sub html_index_body
{
	my ($folder, $datno, $itaname) = @_	;

	my $threadfile = "$folder$datno.dat"	;
	my @logdat = ''	;
if(open(THREAD, $threadfile))
{
	@logdat=<THREAD>;	#ログを配列に読み込む
	close(THREAD)	;
}
	#１つ目の要素を読み込む
	my $firstlog = $logdat[0];
	#改行カット
	chomp($firstlog);
	
	#１つ目の要素を加工する
	my ($name,$mail,$time,$message,$subject) = split(/<>/,$firstlog);
		my $typeSign = '※';
		my $acho = '-'	;
	if(!$time)
	{
		$firstlog =~ /([^,]*),([^,]*),([^,]*),([^,]*),([^,]*)$/;
		($name,$mail,$time,$message,$subject) = ($1,$2,$3,$4,$5);
		$typeSign = '　';
		$acho = '*'	;
	}

	if($acho eq '-')
	{
	$mail =~ s/ //gi;
#	$message =~ s/&amp/&/gi;
	$message =~ s/&amp(?!;)/&/g;

	$message =~ s/(https?|ftp|gopher|telnet|whois|news)\:([\w|\:\!\#\$\%\=\&\-\^\`\\\|\@\~\[\{\]\}\;\+\*\,\.\?\/]+)/<a href=\"$1\:$2\" target=\"_blank\">$1\:$2<\/a>/ig;
	}
	else
	{
	$name =~ s/＠｀/,/gi;
	$mail =~ s/＠｀/,/gi;
	$subject =~ s/＠｀/,/gi;
	$message =~ s/＠｀/,/gi;
	$message =~ s/&amp/&/gi;
	$message =~ s/(https?|ftp|gopher|telnet|whois|news)\:([\w|\:\!\#\$\%\=\&\-\^\`\\\|\@\~\[\{\]\}\;\+\*\,\.\?\/]+)/<a href=\"$1\:$2\" target=\"_blank\">$1\:$2<\/a>/ig;
	}

	$message =~ s/blank"&gt;/blank">/gi;

	my $resnum=@logdat;

#print "$datno.dat<> ($resnum)\n";

print MINDEXFILE "$datno <A HREF=\"/test/read.cgi/$itaname/$datno/\">$subject ($resnum)</A><BR>";
print MSUBJECTT  "$datno.dat<>$subject ($resnum)\n";
$acho = '#';
}
##############################################################################
sub html_index_head
{
	my	$itaname  = $_[0]	;

print MINDEXFILE<<EOF;

<HTML>
<HEAD>
<TITLE>$chanName　過去ログ倉庫</TITLE>
</HEAD>
<BODY>
<a href="/$itaname/index.html">■掲示板に戻る■</a>
 <a href="/kakolog.html">■過去ログ倉庫めにゅーに戻る■</a><P>
※新しいデータ形式(teriのタイプ)のスレッド
<P>
EOF
}
##############################################################################
sub html_index_foot
{
my ($itaname, $sokonum, $infofile, $ttlt) = @_;
my $sss = $sokonum	;
my $sss0 = $sss . '000000';
my $sss9 = $sss . '999999';
my $NOWTIME = time;
if($sss9 > $NOWTIME){$sss9 = $NOWTIME;}

my $kikan = int($sss9) - int($sss0);
$kikan /= 60;#分
$kikan /= 60;#時間
$kikan /= 24;#日
my $speed = sprintf('%5.02f',$ttlt/$kikan)	;

if(open(INFOFILE, '>', $infofile))
{
print INFOFILE "$ssvv\t$itaname\t$sss\t$ttlt\t$speed\n";
	close(INFOFILE);
}


print MINDEXFILE<<EOF;
<P>
<HR>
スレッド数 = $ttlt<BR>
スレッド立てスピード = $speed / day
<HR>
問題等、なんかあったら<A HREF="http://soko.disk.io/"><font color="green">倉庫番 ★</font></A>へお願いします。
</BODY>
</HTML>
EOF
}
##############################################################################
sub html_head
{
	my	$itaname  = $_[0]	;
	my	$itakname = $kname{$itaname}	;

print PINDEXFILE<<EOF;

<HTML>
<HEAD>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=Shift_JIS">
<TITLE>$chanName 過去ログ倉庫 $itakname 板</TITLE>
</HEAD>
<BODY TEXT="#000000" BGCOLOR="#FFFFFF" link="#0000FF" alink="#FF0000" vlink="#660099" background="ba.gif">
<CENTER>
<h1>$chanName 過去ログ倉庫</h1><P>
<h2>$itakname 板</h2><P>
</CENTER>

<A HREF="$chanHome">$chanName に戻る。</A>
<P>
<A HREF="/kakolog.html">過去ログ倉庫めにゅー に戻る。($ssvvサーバ)</A>
<P>
<A HREF="/$itaname/index.html">$itakname＠$chanName に戻る。</A>
<P>
<A HREF="subject.txt">subject.txt</A>
<TABLE BORDER=2>
<TR><TD>倉庫番号</TD><TD>スレッド数</TD><TD>スピード</TD><TD align=center>.txt</TD></TR>
EOF

}
##############################################################################
sub html_foot
{
print PINDEXFILE<<EOF;
</TABLE>
倉庫番号 <A HREF="index3.html">旧倉庫。No2</A><BR>
倉庫番号 <A HREF="index9.html">999999999 以前</A><BR>
<P>
</CENTER>
<HR>
問題等、なんかあったら<A HREF="http://soko.disk.io/"><font color="green">倉庫番 ★</font></A>へお願いします。
</BODY>
</HTML>
EOF
}
##############################################################################
sub getLastUpdateP
{
	local $_ = stat($_[0])			;
	my @flt = localtime($_ ? $_->mtime : 0)	;
	return {
		xupdate => strftime('%Y%m%d%H%M%S', @flt),
		lupdate => strftime('%Y/%m/%d %T', @flt)
	};
}
##############################################################################
sub getDatNum
{
	my $bbx = $_[0]	;
	my $datnum = 0	;
	my	$folder = "$DATAREA/$bbx/oyster/$_[1]/"		;
	if(!opendir(DIR, $folder)) {return 0;}
	my	@dirs = grep(!/^\./ && -f "$folder$_", readdir(DIR));
	closedir DIR	;

	foreach my $ccccc (@dirs)
	{
		if($ccccc ne 'index.html' && $ccccc =~ /\.dat$/) {$datnum ++;}
	}
	return $datnum	;
}
##############################################################################
1;

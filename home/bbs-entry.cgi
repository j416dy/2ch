use strict 'vars';
use File::stat;
use POSIX qw(:errno_h strftime);
use BBSD;

#########################################################
sub bbs_entry
{
	use vars qw($BBSCGI)		;	#グローバルー
	$BBSCGI = '2010/10/28'		;	#最終更新日

	use vars qw($FOX)		;	#グローバルー
	use vars qw(@FOX_K998)		;	#グローバルー 規c制リスト(●)
	use vars qw(@FOX_K999)		;	#グローバルー 規制リスト(ISP)
	use vars qw(@FOX_Ro54)		;	#グローバルー 規制リスト(Rock54)
	use vars qw(@FOX_KABUU)		;	#グローバルー 特別株主優待銘柄リスト
	use vars qw(@FOX_774)		;	#グローバルー 名無しリスト(vip)

						#県名ルックアップ
	use vars qw(%FOX_KEN_ASAHI)	;	#グローバルー asahi-net
	use vars qw(%FOX_KEN_DION)	;	#グローバルー dion

	# 最初にumask(0)を宣言しておく(最後まで有効)
	umask(0);

	unless(defined($FOX))
	{
#		$FOX = 20	;
		$FOX = {}	;
		@FOX_K998 = ()	;
		@FOX_K999 = ()	;
		@FOX_Ro54 = ()	;
		&initFOX	;		#広告関係は最初に一回読み込んで、
		srand(time)	;		#乱数

		@FOX_KABUU = ()	;
		&readKABUU()	;
	}
	&bbs_entryXXX			;
}
#############################################################################
#専門板?
#############################################################################
sub IsSenmon
{
	my ($GB) = @_	;

	if($ENV{'SERVER_NAME'} !~ /2ch.net/)		{return 1;}
	if($ENV{SERVER_NAME} =~ /hayabusa/)		{return 0;}
	if($GB->{FORM}->{bbs} =~ /plus$/)		{return 0;}
	if($GB->{FORM}->{bbs} =~ /saloon$/)		{return 0;}
	if($GB->{FORM}->{bbs} =~ /anime/)		{return 0;}
	if($GB->{FORM}->{bbs} eq 'morningcoffee')	{return 0;}
	if($GB->{FORM}->{bbs} eq 'news')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'anime4vip')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'news4vip')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'news4viptasu')	{return 0;}
	if($GB->{FORM}->{bbs} eq 'campus')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'ghard')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'poverty')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'wcomic')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'soccer')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'ms')			{return 0;}
	if($GB->{FORM}->{bbs} eq 'campus')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'streaming')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'mmo')			{return 0;}
	if($GB->{FORM}->{bbs} eq 'slot')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'comic')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'skate')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'keiba')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'giin')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'seiji')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'famicom')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'shar')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'mog2')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'download')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'livemarket2')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'livemarket1')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'base')		{return 0;}

	return 1	;
}
#############################################################################
# IPv6接続かどうかをチェックする
# はじめのほうで使うので、bbs-entry.cgi に入れることにする
# $GBの初期化時に呼ばれる
# 引数はなし
#############################################################################
sub IsIPv6
{
	my $saddr = $ENV{'SERVER_ADDR'};
	use Net::IP qw(:PROC);

	return ip_is_ipv6($saddr);
}
#########################################################
#
#########################################################
sub foxSamba24Init
{
	my ($ita) = @_	;

	$FOX->{BOOK} = "."	;
	if(-e "/md/tmp/book")	{$FOX->{BOOK} = "/md/tmp"	;}

	$FOX->{SambaOffset_KEITAI} = 10			;
	$FOX->{SambaOffset_P22CH}  = 10			;

#	if($FOX->{$ita}->{"BBS_BE_TYPE2"})	{return 120;}

	if($ita eq 'newsplus')			{return	128;}

#return 10		;

	if($ita eq 'liveplus')			{return  20;}
	if($ita =~ /ogame/)			{return  20;}
	if($ita =~ /bgame/)			{return  60;}
	if($ita eq 'news')			{return  20;}
	if($ENV{SERVER_NAME} =~ /hayabusa/)	{return  20;}

	if($ENV{SERVER_NAME} !~ /2ch\.net/ && $ENV{SERVER_NAME} !~ /bbspink\.com/)	{ return 600; }

	if($ENV{SERVER_NAME} =~ /bbspink\.com/)	{return  20;}

	return 40		;
}
#######################################################################
#
#######################################################################
sub foxViva
{
	my ($GB, $tane) = @_		;

	my $Samba = "VivaSamba24"	;
	my $span  = 180			;	#規制秒数

$tane =~ s/\./-/g;
$tane =~ s/\//~/g;
	my $sFile = "$FOX->{BOOK}/book/$tane.cgi";
	my $remo = $GB->{HOST29}	;	#いわゆるリモホ
	my $ipip = $ENV{REMOTE_ADDR}	;

	my $isViva			;

	# 携帯はするー
	if($GB->{KEITAI})	{return 0;}

	# 雪だるまでは、良くわかんないので今のところなし、その後実装よろしく
	# 　　→ 実装しますた
	if(IsSnowmanServer)
	{
		my $errmsg = bbsd_db($GB->{FORM}{bbs}, 'chkid', 'vivaSamba', $tane, $span, 0xFFFF, 0xFFFF, 'dummy');
		if (&bbsd_TimeoutCheck($GB, $errmsg))		{return 0;}
		if ((split /,/, $errmsg)[0])
		{
			$errmsg = bbsd_db($GB->{FORM}{bbs}, 'peekid', 'vivaSambaIP', "$tane:$ipip", $span, 0xFFFF, 0xFFFF, 'dummy');
			if (&bbsd_TimeoutCheck($GB, $errmsg))	{return 0;}
			if (!(split /,/, $errmsg)[0])		{$isViva = 1;}
		}
		if (!$isViva)
		{
			bbsd_db($GB->{FORM}{bbs}, 'chkid', 'vivaSambaIP', "$tane:$ipip", $span, 0xFFFF, 0xFFFF, 'dummy');
		}
	}
	else
	{
		if(-e $sFile)
		{
			my ($prsize, $prmtime) = (local $_=stat($sFile)) ? ($_->size, $_->mtime) : (0, 0);
			my $ctime = time;
			my $keika = $ctime - $prmtime;

#$GB->{FORM}->{'MESSAGE'} .= "<hr>二回目以降、　今=$ipip ";

			if(open(SMB,"$sFile"))
			{
				my @mdx = <SMB>	;
				close(SMB)	;
#$GB->{FORM}->{'MESSAGE'} .= "前=$mdx[0] $keika sec経過<br>";
				if($ipip ne $mdx[0] && $keika < $span)	{$isViva = 1;}
			}
		}
		if(!$isViva && open(LOG,"> $sFile"))	{print LOG "$ipip";close(LOG)	;}
	}

	if($isViva)
	{
		print "Content-type: text/html; charset=shift_jis\n\n";
		print <<EOF;
<html><head><title>ＥＲＲＯＲ！</title><meta http-equiv="Content-Type" content="text/html; charset=shift_jis"></head>
<body><!-- 2ch_X:error -->
ＥＲＲＯＲ - Viva Samba カーニバル !<br>
<br>
ということだ。<br><br>
<br><hr><font color=green>FOX ★</font></body>
</html>
EOF
		exit;
	}

	return 0;
}
#################################################################################################
#	トラックバック受信
#################################################################################################
sub foxTrackBackIn
{
	my ($GB) = @_				;

	if(!$ENV{PATH_INFO})		{return 0;}	#PATH_INFOがないとTBACKじゃない
	if($ENV{REQUEST_METHOD} ne 'POST') {return 0;}	#POSTのみ受け入れ

	use CGI					;
	my $cgi = new CGI			;

	my $ver = "0.11"			;
	my $refer = $ENV{HTTP_REFERER}		;
	my $who = $cgi->param('who')		;
	my $mac = $cgi->param('themacallan')	;
	my $raddr = $who || $ENV{REMOTE_ADDR}	;
#$ENV{'REMOTE_ADDR'}<>$GB->{MARU}<>$ENV{'HTTP_USER_AGENT'}
#my $rhost = gethostbyaddr(pack('C4',split(/\./, $raddr)), 2) || $raddr;


if($refer =~ m#^http://(?:[-\w]+\.)?(?:2ch\.net|bbspink\.com)/#)
{
	if($who eq '')		{&TBackEnd("発信元不明");}
	if($mac ne "18")	{&TBackEnd("飲みすぎ");}
	$ENV{'REMOTE_ADDR'} = $raddr		;
	$ENV{'HTTP_USER_AGENT'} = $cgi->param('ua');
	$GB->{FORM}->{sid} = $cgi->param('mm');
}
	my ($d0,$bbs,$key,$d3) = split(/\//,$ENV{PATH_INFO})	;
	if($bbs eq '')			{&TBackEnd("板名なし");}
	if($bbs =~ /\W/)		{&TBackEnd("板名だめ");}
	if($bbs eq 'sec2ch')		{&TBackEnd("この板は受け付けない");}
	if($bbs eq 'saku')		{&TBackEnd("この板は受け付けない");}
	if($bbs eq 'saku2ch')		{&TBackEnd("この板は受け付けない");}
	if($bbs eq 'news4vip')		{&TBackEnd("この板は受け付けない");}
	if($bbs eq 'maru')		{&TBackEnd("この板は受け付けない");}
	if($key eq '')			{&TBackEnd("keyなし");}
	if($key =~ /\D/)		{&TBackEnd("keyだめ");}
	# 924 はトラックバック受信だめ(にしなくてもとりあえずここでは問題ない)
	#if($key =~ /^924/)		{&TBackEnd("keyだめ");}

	my $url = $cgi->param('url')	;
	#$url =~ tr/+/ /		;
	$url =~ tr/\t/ /		;
	$url =~ s/\r\n?|\n/<br>/g	;
	# \x00 ∈ [[:cntrl:]]
	$url =~ s/[[:cntrl:]]//g	;
	if($url eq '')			{&TBackgoThre("http://$ENV{SERVER_NAME}/test/read.cgi/$bbs/$key/l50");}
	if($url !~ /^http\:\/\//)	{&TBackgoThre("http://$ENV{SERVER_NAME}/test/read.cgi/$bbs/$key/l50");}
	if($url =~ /\|| /)		{&TBackgoThre("http://$ENV{SERVER_NAME}/test/read.cgi/$bbs/$key/l50");}
	if($url =~ /<|>/)		{&TBackgoThre("http://$ENV{SERVER_NAME}/test/read.cgi/$bbs/$key/l50");}
	if($url =~ /　/)		{&TBackgoThre("http://$ENV{SERVER_NAME}/test/read.cgi/$bbs/$key/l50");}

	if(!TBackgoodUrl($url))		{&TBackgoThre("http://$ENV{SERVER_NAME}/test/read.cgi/$bbs/$key/l50");}

	my $ttl = $cgi->param('title')		;
	my $bnm = $cgi->param('blog_name')	;
	my $exc = $cgi->param('excerpt')	;

#	$exc = substr($exc, 0, 200)		;

if(!($refer =~ m#^http://(?:[-\w]+\.)?(?:2ch\.net|bbspink\.com)/#))
{
	use Jcode	;
	$ttl = Jcode::convert( $ttl, 'sjis' )	;
	$bnm = Jcode::convert( $bnm, 'sjis' )	;
	$exc = Jcode::convert( $exc, 'sjis' )	;
}
	# \r もカットする必要があることに注意
	foreach ($ttl, $bnm, $exc) {
		# s/"/&quot;/g;
		s/</&lt;/g;
		s/>/&gt;/g;
		tr/\t/ /;
		# [\x00\n\r] ⊂ [[:cntrl:]]
		s/[[:cntrl:]]//g;
	}
	$exc =~ s/&lt;br&gt;/<br>/g;

	my $tb = "【トラックバック来たよ】 (ver. $ver) <br>"		;
	if($ttl)	{$tb .= "[タイトル] $ttl <br>";}
	if($bnm)	{$tb .= "[発ブログ] $bnm <br>";}
	$tb .= "$url<br>"			;
#	if($refer)	{$tb .= "( ref= $refer ) <br><br>";}
	if($exc)	{$tb .= "[＝要約＝]<br>$exc <br><br> ";}


	$GB->{FORM}->{'FROM'}		= "TBACK ★"	;
	$GB->{FORM}->{'mail'}		= "sage"	;
	$GB->{FORM}->{'MESSAGE'}	= $tb		;
	$GB->{FORM}->{'subject'}	= ""		;
	$GB->{FORM}->{'time'}		= $GB->{NOWTIME} - 100;
	$GB->{FORM}->{'bbs'}		= $bbs		;
	$GB->{FORM}->{'key'}		= $key		;

	$GB->{TBACK} = 1		;	# 1=TrackBack 0=通常処理
	$GB->{CAP} = 1			;	# トラックバックも名前の最後が★

#&DispError2($GB,"FOX ★","<font color=green>FOX ★</font>TBACK(201)<br><br>r=$raddr<br>r=$refer<br>");

	return $raddr			;
}
##############################################################################
sub TBackgoodUrl
{

	my $x = $_[0]	;

if($x =~ /unko\.2ch\.net/)		{return 0;}
if($x =~ /ezbbs\.net\/01\/sample0/)	{return 0;}
if($x =~ /news4vip/)			{return 0;}

	$x =~ /^http\:\/\/([\w|\:\!\#\$\%\=\&\-\^\`\\\|\@\~\[\{\]\}\;\+\*\,\.\?]+)\/([\w|\:\!\#\$\%\=\&\-\^\`\\\|\@\~\[\{\]\}\;\+\*\,\.\?\/]+)/	;

	my $u = $1	;
	my $v = $2	;

	if($u eq '')	{return 0;}
	if($v eq '')	{return 0;}

	if($u eq /ime.st$/)		{return 0;}
	if($u eq /ime.nu$/)		{return 0;}
	if($u eq /pinktower.com$/)	{return 0;}

	if($u =~ /\.2ch.net/)		{return 1;}
	if($u =~ /\.bbspink.com/)	{return 1;}
	if($u =~ /\.ddo.jp/)		{return 1;}
	if($u =~ /\.goo.ne.jp/)		{return 1;}
	if($u =~ /\.hatena.ne.jp/)	{return 1;}
	if($u =~ /\.livedoor.com/)	{return 1;}
	if($u =~ /\.livedoor.jp/)	{return 1;}
	if($u =~ /\.yahoo.co.jp/)	{return 1;}
	if($u =~ /\.cocolog-nifty.com/)	{return 1;}
	if($u =~ /yaplog.jp/)		{return 1;}
	if($u =~ /jugem.jp/)		{return 1;}
	if($u =~ /blogzine.jp/)		{return 1;}
	if($u =~ /\.kakiko.com/)	{return 1;}

	if($ENV{SERVER_NAME} =~ /qb6/)	{return 1;}

	return 0	;


	use LWP::UserAgent;

	my $ua = LWP::UserAgent->new();
	$ua->timeout(3);
	my $request = HTTP::Request->new('GET', $x);
	my $response = $ua->request($request) ;
	my $response_body = $response->content();
	my $response_code = $response->code();

	my $db_content = $response->content();

	if($response_code > 300)	{return 0;}


	return 0	;
}
##############################################################################
sub TBackEnd
{
#&TBackerrEnd;

print "Content-type: text/html; charset=shift_jis\n\n";
print "<HTML lang=\"ja\">"	;
print "<HEAD>\n"		;
print "<META http-equiv=\"Content-Type\" content=\"text/html; charset=Shift_JIS\">\n";
print "</HEAD>\n"		;
print "<BODY>\n"		;

print "tb.cgi-----------<br>\n"	;
print "| $_[0]<br>\n"		;
print "tb.cgi-----------<br>\n"	;
print "<br><br><br><hr>\n";
print "PATH_INFO=[$ENV{PATH_INFO}]<br>\n"	;
print "</BODY>\n";
print "</HTML>\n";
exit;
}
##############################################################################
sub TBackgoThre
{
my $ttt = $_[0];

print "Content-type: text/html; charset=shift_jis\n\n";
print <<EOF;
<HTML lang="ja">
<HEAD>
<META http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<title>トラックバック@２ちゃんねる</title>
<META content=10;URL="$ttt" http-equiv=refresh>
</HEAD>
<BODY>
ここだ
<a href="$ttt">$ttt</a>
</BODY>
</HTML>
EOF
exit;
}
##############################################################################
sub TBacksuperEnd
{
print "Content-type: text/xml\n\n"	;
print <<EOF;
<?xml version="1.0" encoding="utf-8"?>
<response>
<error>0</error>
</response>
EOF
exit;
}
##############################################################################
sub TBackerrEnd
{
print "Content-type: text/xml\n\n"	;
print <<EOF;
<?xml version="1.0" encoding="utf-8"?>
<response>
<error>1</error>
</response>
EOF
exit;
}
#################################################################################################
#	トラックバック送信
#################################################################################################
sub foxTrackBack
{
	my ($GB) = @_			;

	# 924 はトラックバック送信無効(にはとりあえずしないでおこう)
	#if($GB->{FORM}->{'key'} =~ /^924/)	{return 0;}

	if($GB->{TBACK})			{return 0;}
	if($GB->{FORM}->{bbs} eq 'news4vip')	{return 0;}


	if($GB->{FORM}->{'MESSAGE'} !~ /トラックバック:http\:\/\/([\w|\:\!\#\$\%\=\&\-\^\`\\\|\@\~\[\{\]\}\;\+\*\,\.\?\/]+)/)	{return 0;}
	my $target = "http://$1"	;
if($target =~ /\.2ch\.net|\.bbspink\.com|\.kakiko\.com/)
	{$target =~ s/read\.cgi/bbs\.cgi/;}
	my $url = "http://$ENV{SERVER_NAME}/test/read.cgi/$GB->{FORM}->{bbs}/$GB->{FORM}->{'key'}/l50"	;

	if($target =~ /$GB->{FORM}->{bbs}/ && $target =~ /$GB->{FORM}->{'key'}/)
	{&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：同一スレッドにはトラックバックできません。");}

	my $dattemp = "";
	my $firstlog = "";
	if(IsSnowmanServer == BBSD->{REMOTE})
	{
		# 雪だるまでは、HTTP経由で入手する
		use LWP::UserAgent;

		my $ua = LWP::UserAgent->new(agent => 'bbs.cgi', timeout => 3, max_redirect => 0);
		my $res = $ua->get("http://127.0.0.1/$GB->{FORM}{bbs}/dat/$GB->{FORM}{key}.dat", Host => $ENV{SERVER_NAME});
		if ($res->is_error)
		{
			&DispError2($GB, 'ＥＲＲＯＲ！', 'ＥＲＲＯＲ：>>1の取得に失敗しました。');
		}
		$firstlog = (split(/\n/, $res->content, 2))[0];
	}
	else
	{
		# 通常サーバでは、直接datを読む
		$dattemp = $GB->{DATPATH} . $GB->{FORM}->{'key'} . ".dat";
		open(RDAT, $dattemp)	;
		$firstlog = <RDAT>	;
		close(RDAT)		;
		chomp($firstlog)	;
	}
	my ($name,$mail,$time,$message,$subject) = split(/<>/,$firstlog);

	use LWP::UserAgent;
	use HTTP::Request::Common qw(POST);

	my %formdata;
	$formdata{'title'} = $subject;
	$formdata{'excerpt'} = $message;
	$formdata{'url'} = $url;
	$formdata{'blog_name'} = $FOX->{$GB->{FORM}->{bbs}}->{BBS_TITLE};
if($target =~ /\.2ch\.net|\.bbspink\.com/)
{
	$formdata{'who'} = $ENV{REMOTE_ADDR};
	$formdata{'themacallan'} = "18";
	$formdata{'mm'} = $GB->{FORM}->{sid}	;
	$formdata{'ua'} = $ENV{'HTTP_USER_AGENT'}	;
}
	my $request  = POST "$target" , \%formdata;
	$request->referer($url);

	my $ua = LWP::UserAgent->new()				;
	$ua->agent('TrackBack/1.0');  
	$ua->parse_head(0);   
	$ua->timeout(3)					;

	my $response = $ua->request($request);

	my $response_body = $response->content()		;#結果はここに入っている
	my $response_code = $response->code()			;#結果はここに入っている
	my $db_content = $response->content()			;

	# エラーチェック
	if ($response->is_error)
	{
		&DispError2($GB, "ＥＲＲＯＲ！", "ＥＲＲＯＲ：トラックバックの送信に失敗しました。($response_code)");
	}

	# $db_content =~ s/"/&quot;/g;
	$db_content =~ s/</&lt;/g;
	$db_content =~ s/>/&gt;/g;
	$db_content =~ tr/\n//d;

	if($ENV{SERVER_NAME} !~ /qb6/)	{return 1;}

	$GB->{FORM}->{'MESSAGE'} .= "<hr><font color=orange>トラックバック</font><br>";
	$GB->{FORM}->{'MESSAGE'} .= "target=$target<br>";
	$GB->{FORM}->{'MESSAGE'} .= "title=[$subject]<br>";
#	$GB->{FORM}->{'MESSAGE'} .= "excerpt=[$message]<br>";
	$GB->{FORM}->{'MESSAGE'} .= "URL=[ $url ]<br>";
	$GB->{FORM}->{'MESSAGE'} .= "blog_name=$FOX->{$GB->{FORM}->{bbs}}->{BBS_TITLE}<br>";
	$GB->{FORM}->{'MESSAGE'} .= "=====<br>[$db_content]";

	return 1;
}
#########################################################
# index.html/subback.html をさぼるサーバかどうか
# さぼる: 1、さぼらない: 0
#########################################################
sub SaborinServer
{
	my ($GB) = @_			;

	if($GB->{BBSCGI_FUNCTIONS}{SABORIN})	{return 1;}

	# news21/news22: 非常用
	#if($ENV{'SERVER_NAME'} =~ /news21/)	{return 1;}
	#if($ENV{'SERVER_NAME'} =~ /news22/)	{return 1;}

	# ex系、今は既にない
	#if($ENV{'SERVER_NAME'} =~ /ex11/)	{return 1;}
	#if($ENV{'SERVER_NAME'} =~ /ex12/)	{return 1;}
	#if($ENV{'SERVER_NAME'} =~ /ex13/)	{return 1;}
	#if($ENV{'SERVER_NAME'} =~ /ex14/)	{return 1;}
	#if($ENV{'SERVER_NAME'} =~ /ex15/)	{return 1;}
	#if($ENV{'SERVER_NAME'} =~ /ex16/)	{return 1;}
	#if($ENV{'SERVER_NAME'} =~ /ex17/)	{return 1;}
	#if($ENV{'SERVER_NAME'} =~ /ex19/)	{return 1;}
	#if($ENV{'SERVER_NAME'} =~ /ex20/)	{return 1;}
	#if($ENV{'SERVER_NAME'} =~ /ex21/)	{return 1;}

	# live系
	#if($ENV{'SERVER_NAME'} =~ /live28/)	{return 1;}

	# live22/live23/live24はここで指定しても意味ない(雪だるまだから)
	#if($ENV{'SERVER_NAME'} =~ /live22/)	{return 1;}
	#if($ENV{'SERVER_NAME'} =~ /live23/)	{return 1;}
	#if($ENV{'SERVER_NAME'} =~ /live24/)	{return 1;}

	# 板別で指定する場合
	if($GB->{FORM}->{'bbs'} =~ /live/)	{return 1;}
	if($GB->{FORM}->{'bbs'} eq "weekly")	{return 1;}

	return 0	;
}
sub Saborin
{
	my ($GB) = @_			;

#$GB->{FORM}->{'MESSAGE'} .= "<hr>当たり($ENV{'SERVER_NAME'},$GB->{FORM}->{'bbs'},$GB->{NEWTHREAD},$GB->{PID})"	;
#	return 0			;

	# 新スレの時は更新をさぼらない
	if($GB->{NEWTHREAD} ne 0)		{return 0;}

	# LAが基準値の1.2倍に達していたら、その後は更新をさぼる
	my $fact = 1.2			;# LAチェックの際の基準値に対する倍率
	# animeサーバは1倍
	if($ENV{'SERVER_NAME'} =~ /anime/)	{ $fact = 1.0; }
	# news系サーバは1倍
	if($ENV{'SERVER_NAME'} =~ /news/)	{ $fact = 1.0; }
	# ex系サーバは1倍
	if($ENV{'SERVER_NAME'} =~ /ex/)		{ $fact = 1.0; }
	# live系サーバは1倍
	if($ENV{'SERVER_NAME'} =~ /live/)	{ $fact = 1.0; }

	# LAが高いかチェック
	if(&mumumuMaxLACheck($GB->{LOADAVG}, $fact))	{return 1;}

	# 達していなかったら、該当するサーバ以外は更新をさぼらない
	elsif(!&SaborinServer($GB))		{return 0;}

	# index.html が存在しない場合はさぼらない
	# 存在する場合は次回以降チェックしない
	if (!$FOX->{ISINDEXHTML}{$GB->{FORM}{bbs}}) {
		if (!-e "../$GB->{FORM}{bbs}/index.html") {return 0;}
		$FOX->{ISINDEXHTML}{$GB->{FORM}{bbs}} = 1;
	}

	# 該当するサーバではPIDを50で割って余りがある時、その後の更新をさぼる
	if($GB->{PID} % 50)			{return 1;}
	# mod_speedycgi→speedy_backendではpidがずっと同じになる可能性があるので、
	# rand()を使うように変更(1999/2000の確率)
	# しばらく今のやつで様子見
	#if(rand(2000) > 1)			{return 1;}

	# 上記のいずれにも該当しない(更新をさぼらない)
	return 0			;
}
#######################################################################
# IsKoukokuをスキップするサーバかどうかをチェックする
#######################################################################
sub mumumuIsKoukokuSkipServer
{
	my ($GB, $server) = @_;

	if($GB->{BBSCGI_FUNCTIONS}{ISKOUKOKUSKIP})	{return 1;}

#	if($server =~ /news21/)	{return 1;}
#	if($server =~ /news22/)	{return 1;}
#	if($server =~ /ex11/)	{return 1;}
#	if($server =~ /ex13/)	{return 1;}
#	if($server =~ /ex14/)	{return 1;}
#	if($server =~ /ex15/)	{return 1;}
#	if($server =~ /ex16/)	{return 1;}
#	if($server =~ /ex19/)	{return 1;}
#	if($server =~ /ex20/)	{return 1;}
	return 0;
}
#######################################################################
# IsKoukokuを実行するかどうかをチェックする
#######################################################################
sub mumumuIsIsKoukoku
{
	my ($GB) = @_;

	# bananaサーバでは必ず実行
	if(&mumumuGetServerType() =~ /banana/)		{return 1;}
	# 該当するサーバでは実行しない
	if(&mumumuIsKoukokuSkipServer($GB, $ENV{SERVER_NAME})) {return 0;}
	# それ以外は実行
	return 1;
}
#######################################################################
# 1/100秒を取り扱う(表示する)かどうか
#######################################################################
sub IsCentiSec
{
	my ($GB) = @_;

	if($GB->{BBSCGI_FUNCTIONS}{CENTISEC})		{return 1;}

	# このへんのサーバでは表示
	#if($ENV{'SERVER_NAME'} =~ /atlanta/)		{return 1;}
	#if($ENV{'SERVER_NAME'} =~ /live/)		{return 1;}
	if($ENV{'SERVER_NAME'} =~ /hayabusa/)		{return 1;}
	if($ENV{'SERVER_NAME'} =~ /snow/)		{return 1;}

	# このへんの板では表示
	if($GB->{FORM}->{'bbs'} eq "news")		{return 1;}
	if($GB->{FORM}->{'bbs'} eq "news4vip")		{return 1;}
	if($GB->{FORM}->{'bbs'} eq "news4viptasu")	{return 1;}
	if($GB->{FORM}->{'bbs'} eq "morningcoffee")	{return 1;}
	if($GB->{FORM}->{'bbs'} eq "asaloon")		{return 1;}
	if($GB->{FORM}->{'bbs'} eq "operate2")		{return 1;}

	return 0;
}
#######################################################################
# 板別キャップかどうか
#######################################################################
sub IsItabetsuCap
{
	my ($GB) = @_;

	our %ItabetsuCapList;
	BEGIN {
		# 板別キャップの板が変わったら、ここを編集する
		%ItabetsuCapList = map +($_ => 1), (
			# plus系
			"bizplus", "dqnplus", "femnewsplus", "liveplus",
			"mnewsplus", "moeplus", "namazuplus", "news4plus",
			"news5plus", "newsplus", "owabiplus", "scienceplus",
			"ticketplus", "wildplus",
			# plus系ではないもの
			"comicnews", "gamenews",
			"musicnews", "news",
			"pcnews"
		);
	}

	if($ItabetsuCapList{$GB->{FORM}->{'bbs'}})
	{
		return 1;
	}
	return 0;
}
#######################################################################
# スレッド数を制限する板かどうか
#######################################################################
sub IsThreadLimitIta
{
	my ($GB) = @_;

	# 対象となる板たち
	our %ThreadLimitItaList;
	BEGIN {
		%ThreadLimitItaList = map +($_ => 1), (
			#実況ch
			"dancesite", "dome", "endless", "festival",
			#番組ch
			"livenhk", "liveetv",
			"liventv", "liveanb", "livetbs", "livetx", "livecx",
			#実況ch(weekly系)
			"livewkwest", "weekly",
			#野球、サッカー
			"livebase", "livefoot",
			#BS、ラジオ、スカパー(CS)、WOWOW
			"livebs", "liveradio",
			"liveskyp", "livewowow",
			#なんでも実況J、なんでも実況S
			"livejupiter", "livesaturn",
			#オリンピック実況
			"oonna", "ootoko",
			#なんでも実況V
			"livevenus",
			#テスト用
			#"operate2",
			#地震
			"eq", "eqplus"
		);
	}

	if($ThreadLimitItaList{$GB->{FORM}->{'bbs'}})
	{
		return 1;
	}
	return 0;
}
#######################################################################
# JavaScript版read.htmlを有効にするかどうかをチェックする
#######################################################################
sub IsReadHtml
{
	my ($GB) = @_;

	# とりあえずdso, life7サーバだけ有効
	#if($ENV{'SERVER_NAME'} =~ /^(?:dso|life7)\./)	{return 1;}

	# read.html ファイルの存在の有無で切り替え
	our $IsReadHtml;
	BEGIN {
		$IsReadHtml = -e 'read.html';
	}
	return $IsReadHtml;
}

=begin comment

bbsd 関連の処理は BBSD.pm に一任のためコメントアウト
#######################################################################
# 雪だるまサーバかどうかチェックする
#######################################################################
sub IsSnowManServer
{
	my ($server) = @_;

	if($ENV{SSL_X_BBSD_SERVER})   {return 1;}
	if($server =~ /live22/) {return 1;}
	if($server =~ /live23/) {return 1;}
	if($server =~ /live24/) {return 1;}
	if($server =~ /news20/) {return 1;}
	if($server =~ /snow/)   {return 1;}
	return 0;
}
#############################################################################
# 雪だるまサーバ用初期化ルーチン
# 入力: サーバ名
# ・各種変数(ぐろーばるー)の初期化
#############################################################################
sub InitSnow
{
	my ($server) = @_;

	# 環境変数 SSL_X_BBSD_SERVER(, SSL_X_BBSD_DB_SERVER) から取得
	# XXX: suExec だと渡せる環境変数に制限があるため SSL_X_ を付けた
	if ($ENV{SSL_X_BBSD_SERVER}) {
		# bbsd(書き込み・IDの種担当)の情報
		($FOX->{SNOWMAN}{BBSD}{HOST}, $FOX->{SNOWMAN}{BBSD}{PORT})
		    = $ENV{SSL_X_BBSD_SERVER} =~ /:/
			? split(/:/, $ENV{SSL_X_BBSD_SERVER})
			: ($ENV{SSL_X_BBSD_SERVER}, 2222);
		$FOX->{SNOWMAN}{BBSD}{TIMEOUT} = 3;
		# bbsd(Samba等共通DB担当)の情報
		($FOX->{SNOWMAN}{DB}{HOST}, $FOX->{SNOWMAN}{DB}{PORT})
		    = $ENV{SSL_X_BBSD_DB_SERVER}
			? $ENV{SSL_X_BBSD_DB_SERVER} =~ /:/
			    ? split(/:/, $ENV{SSL_X_BBSD_DB_SERVER})
			    : ($ENV{SSL_X_BBSD_DB_SERVER}, 2222)
			: ($FOX->{SNOWMAN}{BBSD}{HOST}, $FOX->{SNOWMAN}{BBSD}{PORT});
		$FOX->{SNOWMAN}{DB}{TIMEOUT} = 1;
	}
	# 他サーバでは違う値を設定できるようにしておく
	# live22系の場合
	elsif($server =~ /live22/)
	{
		# bbsd(書き込み・IDの種担当)の情報
		$FOX->{SNOWMAN}->{BBSD}->{HOST}    = '192.168.100.1';
		$FOX->{SNOWMAN}->{BBSD}->{PORT}    = 2222;
		$FOX->{SNOWMAN}->{BBSD}->{TIMEOUT} = 3;
		# bbsd(Samba等共通DB担当)の情報
		$FOX->{SNOWMAN}->{DB}->{HOST}      = '192.168.100.2';
		$FOX->{SNOWMAN}->{DB}->{PORT}      = 2222;
		$FOX->{SNOWMAN}->{DB}->{TIMEOUT}   = 1;
	}
	# live23系の場合
	elsif($server =~ /live23/)
	{
		# bbsd(書き込み・IDの種担当)の情報
		$FOX->{SNOWMAN}->{BBSD}->{HOST}    = '192.168.100.34';
		$FOX->{SNOWMAN}->{BBSD}->{PORT}    = 2222;
		$FOX->{SNOWMAN}->{BBSD}->{TIMEOUT} = 3;
		# bbsd(Samba等共通DB担当)の情報
		$FOX->{SNOWMAN}->{DB}->{HOST}      = '192.168.100.34';
		$FOX->{SNOWMAN}->{DB}->{PORT}      = 2222;
		$FOX->{SNOWMAN}->{DB}->{TIMEOUT}   = 1;
	}
	# live24系の場合
	elsif($server =~ /live24/)
	{
		# bbsd(書き込み・IDの種担当)の情報
		$FOX->{SNOWMAN}->{BBSD}->{HOST}    = '192.168.100.1';
		$FOX->{SNOWMAN}->{BBSD}->{PORT}    = 2223;
		$FOX->{SNOWMAN}->{BBSD}->{TIMEOUT} = 3;
		# bbsd(Samba等共通DB担当)の情報
		$FOX->{SNOWMAN}->{DB}->{HOST}      = '192.168.100.1';
		$FOX->{SNOWMAN}->{DB}->{PORT}      = 2223;
		$FOX->{SNOWMAN}->{DB}->{TIMEOUT}   = 1;
	}
	# news20系の場合
	elsif($server =~ /news20/)
	{
		# bbsd(書き込み・IDの種担当)の情報
		$FOX->{SNOWMAN}->{BBSD}->{HOST}    = '192.168.100.33';
		$FOX->{SNOWMAN}->{BBSD}->{PORT}    = 2222;
		$FOX->{SNOWMAN}->{BBSD}->{TIMEOUT} = 3;
		# bbsd(Samba等共通DB担当)の情報
		$FOX->{SNOWMAN}->{DB}->{HOST}      = '192.168.100.33';
		$FOX->{SNOWMAN}->{DB}->{PORT}      = 2222;
		$FOX->{SNOWMAN}->{DB}->{TIMEOUT}   = 1;
	}
	# snowサーバ(ローカル雪だるま)
	elsif($server =~ /snow/)
	{
		# bbsd(書き込み・IDの種担当)の情報
		$FOX->{SNOWMAN}->{BBSD}->{HOST}    = '127.0.0.1';
		$FOX->{SNOWMAN}->{BBSD}->{PORT}    = 2222;
		$FOX->{SNOWMAN}->{BBSD}->{TIMEOUT} = 3;
		# bbsd(Samba等共通DB担当)の情報
		$FOX->{SNOWMAN}->{DB}->{HOST}
			= $FOX->{SNOWMAN}->{BBSD}->{HOST};
		$FOX->{SNOWMAN}->{DB}->{PORT}
			= $FOX->{SNOWMAN}->{BBSD}->{PORT};
		$FOX->{SNOWMAN}->{DB}->{TIMEOUT}   = 1;
	}

	# タイムアウトメッセージ
	$FOX->{SNOWMAN}->{TIMEOUTMSG} = "bbsd timed out";

	return 0;
}

=end comment

=cut

#########################################################
sub bbs_entryXXX
{
	# qb5 で詰まる問題のデバッグ用
#	our $bbs_entryXXX_cmds;
#	BEGIN {
#		$bbs_entryXXX_cmds = <<'__BBS_ENTRY_XXX_CMDS_END__';
	use CGI::SpeedyCGI				;
	my $sp = CGI::SpeedyCGI->new			;
	my $spv = $sp->i_am_speedy ? 'SpeedyCGI' : '???';

	$ENV{TZ} = 'Asia/Tokyo'		;#日本
					 #$ENV はそのまま使う
	#対応シグナル
	$SIG{PIPE} = $SIG{INT} = $SIG{HUP} = $SIG{QUIT} = $SIG{TERM} = \&SigExit;

	my $GBX = {}			;

	# bbs.cgi のバージョン
	$GBX->{version} = "<a href=\"http://www.2ch.net/\">２ちゃんねる</a> "	;
	$GBX->{version} .= "BBS.CGI - $BBSCGI ($spv)"	;

	# 現在時刻を$GBに得る
	# マイクロ秒もとり、$GB->{NOWTIME}, $GB->{NOWMICROTIME} にそれぞれ代入
	&mumumuGetNowTime($GBX);

	$GBX->{PID} = $$		;#pid

	$GBX->{FORM} = {}		;#

	&foxSetDate($GBX)		;#　日付・時刻を設定（$DATEに設定)

	# foxTrackBackInの中でセットしているので、ここで定義・初期化しておく
	$GBX->{CAP} = 0			;# 0:キャップじゃない 1:キャップ

	$GBX->{TBACK} = 0		;# 1=TrackBack 0=通常処理
	$GBX->{HOST} = &foxTrackBackIn($GBX)	;

	# FORM の読み込みを foxIkinari の前でやっておく
	&foxReadForm($GBX)		;#$FORM を読み込む

	# 投稿確認画面をスキップする呪文(スキップ呪文)とフラグ
	$GBX->{KPIN1} = "kihon"		;# フォームの名前
	$GBX->{KPIN2} = "suriashi"	;# フォームの内容
	$GBX->{KPASS} = 0		;# 0:通常動作 1:投稿確認画面をパス

	# スキップ呪文を唱えているかどうかチェック
	$GBX->{KPASS} = &KPinCheck($GBX);

	# こいつらは foxIkinari でセットしているので、ここで初期化
	$GBX->{PON}  = "PON"		;# クッキーの素
	$GBX->{PONX} = "PONX"		;# クッキーの素
	$GBX->{PONOK} = 0		;# 正しい PON を送ってきたか?
	$GBX->{HAP}  = "HAP"		;# クッキーの素
	$GBX->{HAPX} = "HAPX"		;# クッキーの素
	$GBX->{HAPOK} = 0		;# 正しい HAP を送ってきたか?

	# はなもげらの呪文を変える時は、ここをいじること
#	$GBX->{PIN1} = "hana"	;$GBX->{PIN2} = "mogera";
#	$GBX->{PIN1} = "kiri"	;$GBX->{PIN2} = "tanpo"	;
#	$GBX->{PIN1} = "suka"	;$GBX->{PIN2} = "pontan";
#	$GBX->{PIN1} = "tepo"	;$GBX->{PIN2} = "don";
	$GBX->{PIN1} = "kuno"	;$GBX->{PIN2} = "ichi";

	$GBX->{PIN} = "$GBX->{PIN1}=$GBX->{PIN2}";# クッキーで使用

	if(!$GBX->{TBACK})
	{
		$GBX->{HOST} = &foxIkinari($GBX)	;
	}

	$GBX->{HOST2} = "HOST2"		;
	$GBX->{HOST3} = "HOST3"		;
	$GBX->{HOST4} = "HOST4"		;
	$GBX->{HOST5} = "HOST5"		;
	$GBX->{HOST999} = "HOST999"	;
	$GBX->{HOST29} = "HOST29"	;

	$GBX->{WHITECAP} = 0		;# 0:☆キャップじゃない 1:☆キャップ
					 # (このフラグは今のbbs.cgiでは使用せず)
	$GBX->{STRONGCAP} = 0		;# 0:強いキャップじゃない 1:強いキャップ

	$GBX->{TRIPSTRING} = ""		;# トリップ処理後文字列

	$GBX->{MARU} = ""		;# ●のセッションID(●かどうか判定可能)

	$GBX->{PATH} = "PATH"		;
	$GBX->{WPATH} = "WPATH"		;
	$GBX->{DATPATH} = "DATPATH"	;
	$GBX->{LOGPATH} = "LOGPATH"	;
	$GBX->{TEMPPATH} = "TEMPPATH"	;
	$GBX->{IMODEPATH} = "IMODEPATH"	;
	$GBX->{INDEXFILE} = "INDEXFILE"	;
	$GBX->{SUBFILE} = "SUBFILE"	;

	$GBX->{FILENUM} = "FILENUM"	;
	$GBX->{SUBLINE} = "SUBLINE"	;

	$GBX->{OUTDAT} = "OUTDAT"	;# まさに書こうとしているdat
	$GBX->{LOGDAT} = "LOGDAT"	;# まさに書こうとしているdatのログ
	$GBX->{xID} = "xID"		;# まさに書こうとしているdatのID
	$GBX->{xBE} = "xBE"		;# まさに書こうとしているdatのBE
	$GBX->{DAT1} = "DAT1"		;# そのdatの1
	$GBX->{DATLAST} = ()		;# そのdatのお尻BBS_CONTENTS_NUMBER個分
	$GBX->{DATNUM} = 0		;# そのdatの長さ = レス数
	$GBX->{NEWSUB} = ()		;# subject.txtを保持

	$GBX->{SABORIN} = 0		;# Saborinフラグ
	$GBX->{LOADAVG} = 0.0		;# 現在のロードアベレージ(一番左のやつ)
	$GBX->{MAXLOADAVG} = 0.0	;# 許容ロードアベレージ(超えたら特殊処理)

	$GBX->{IDNOTANE} = "IDNOTANE"	;
	$GBX->{KEITAI} = 0		;# 0:携帯じゃない 1:Docomo 2:au 3:SoftBank
					;# 5:emobile
	$GBX->{P22CH} = 0		;# 0:p2.2ch.net以外 1:p2.2ch.net
	$GBX->{KEITAIBROWSER} = 0	;# 0:携帯用ブラウザ以外 1:携帯用ブラウザ
	$GBX->{V931} = "0"		;# 0:vip臭くない 931:vip臭い
	$GBX->{NEWTHREAD} = 0		;
	$GBX->{JIKAN} = "JIKAN"		;

	$GBX->{base} = "base"		;
	$GBX->{NEWTHREAD} = 0		;# bby.2ch.net 新スレ通知機能
	$GBX->{BURNEDPROXY} = 0		;# 1:BBQ 登録済み、焼き済みのproxy 0:それ以外
	$GBX->{BURNEDKEITAI} = 0	;# 1:BBM 登録済み、焼き済みの携帯 0:それ以外

	# IPv6接続かどうか
	$GBX->{IPv6} = 0		;# 0:IPv6接続ではない、1: IPv6接続

	# IPv6接続だったら、IPv6フラグを立てる
	if(&IsIPv6())
	{
		$GBX->{IPv6} = 1	;
	}

	$GBX->{DEBUG} = "はじまりはじまりー<br>"	;

	$GBX->{LOADAVG} = &mumumuGetLA()	;# ロードアベレージ情報の入手

	my $maxspan = 600	;
	my $span = $GBX->{NOWTIME} - $FOX->{NOWTIME};
	if($span > $maxspan)	{$sp->shutdown_next_time;}

	&foxSetPath($GBX)		;# 各種PATH生成
	&foxReadSettings($GBX)		;# 板設定よみこみとためこみ SETTING.TXT
	&foxSetDate2($GBX)		;# 日付・時刻を設定（$DATEに設定 !!曜日)
	&foxBEset($GBX)			;# BE情報問い合わせ
#株関係
	&foxKabuInit($GBX)		;# 株関係

	$FOX->{$GBX->{FORM}->{'bbs'}}->{MD5NUMBER} = &foxCheckMD5id(
					$GBX->{FORM}->{'bbs'},
					$GBX->{MD5DATE},
					$FOX->{$GBX->{FORM}->{'bbs'}}->{MD5NUMBER},
					$FOX->{MD5DATE},
					$GBX->{WPATH});

	$FOX->{MD5DATE} = $GBX->{MD5DATE}	;

#お試し●
	$FOX->{OTAMESHIMARU} = 'eGSfQMC3U3iZy7mL'	;

#Vipクオリティ関係
	$GBX->{VIPQ2STOP} = 0		;# 1:スレスト　0:継続

require "../../test/bbs-main.cgi";
	&bbs_main($GBX)		;

&DispError2($GBX,"FOX ★","<font color=green>FOX ★　ふふふっ</font><br><br>これが表\示されるということは・・・<br>本体requireしたのにそっちへ行かないと、、、");
print "Content-type: text/html; charset=shift_jis\n\nWOWOWOWOWOW-----\n";
	return	;
#__BBS_ENTRY_XXX_CMDS_END__
#		$bbs_entryXXX_cmds = join '', map {
#			!/^\s*#/ && /;/ ? "${_}_bbs_entryXXX_debug(<<'__BBS_ENTRY_XXX_DEBUG_EOT__');\n${_}__BBS_ENTRY_XXX_DEBUG_EOT__\n" : $_;
#		} split /^/, $bbs_entryXXX_cmds if ($ENV{SERVER_NAME} =~ /^qb\d*\./);
#	}
#	_bbs_entryXXX_debug();
#	eval $bbs_entryXXX_cmds;
#	print "Content-Type: text/plain\n\n$@" if ($@);
}
# qb5 で詰まる問題のデバッグ用
sub _bbs_entryXXX_debug
{
	our $ptime;
	if (!defined $_[0]) {
		$ptime = time;
	}
	else {
		my ($time, $diff) = time;
		if (($diff = $time - $ptime) > 7 && open(local *F, '>>', "/var/tmp/bbscgi.log.$ENV{SERVER_NAME}")) {
			local ($_, $\) = ($_[0], "\n");
			chomp;
			print F strftime('[%F %T] ', localtime $time), "$_: took ${diff}s";
			close F;
		}
		$ptime = $time;
	}
}
#############################################################################
#	株関係
#############################################################################
sub IsUtai
{
	my ($ne) = @_;

	# 1% = 100
	if($ne <   30)	{return 300;}	
	if($ne <   50)	{return 150;}	
	if($ne <  100)	{return  75;}	
	if($ne <  500)	{return  50;}
	if($ne < 1000)	{return  40;}
	return 30	;
}
sub IsSpecialKabuU
{
	my ($GB,$mei) = @_	;

#if($mei eq 'supplement')	{return 0;}
#if($mei eq 'tanka')		{return 0;}
#if($mei eq 'ranking')		{return 0;}
#if($mei eq 'radio')		{return 0;}

	# 株主優待
	#株価
	#http://2pix.2ch.se/test/kabuka.so?morningcoffee
	my $host = "http://2pix.2ch.se/test/kabuka2.so?"	;
	my $path = $mei				;
	my $ua = LWP::UserAgent->new()		;
	$ua->agent('Mozilla/5.0 FOX(2ch.se)')	;
	$ua->timeout(3)				;
	my $request = HTTP::Request->new('GET', $host . $path);
	my $response = $ua->request($request) 	;#ここで GET 処理
	my $db_content = $response->content()	;

	# エラーチェック
	if ($response->is_error)
	{
		# 板の株価がとれなかったらエラー(E)とする
		return 0;
	}

	my ($name,$kabuka,$zenkabu,$ttttt) = split(/\:/,$db_content)	;
	$kabuka  = int($kabuka)		;
	$zenkabu = int($zenkabu)	;
	my $kabusu = &foxGetKabusu($GB,$mei)	;

	if($zenkabu < 1)	{return 0;}

	if($kabusu > 0)
	{
		$GB->{KABUXP} = "$mei"	;
		$GB->{KABUUP} = 1	;	#株主優待ぷち
	}

	my $rrr = int(10000 * $kabusu / $zenkabu);
	my $rrx = int($rrr/100)		;
	my $u4 = &IsUtai($kabuka)	;
	if($rrr >= $u4)
	{
		$GB->{KABUX}  .= "($mei)"	;
		return 1		;
	}
	return 0			;
}
sub foxKabuInit
{
	my ($GB) = @_;

#&DispError2($GB,"FOX ★","<font color=green>FOX ★　ふふふっ</font><br><br>$FOX_KABUU[2]");
	$GB->{KABU}   = 0	;
	$GB->{KABUX}  = "株主優待"	;
	$GB->{KABUXP}  = $GB->{FORM}->{'bbs'}	;
	$GB->{KABUU}  = 0	;
	$GB->{KABUUP} = 0	;	#株主優待プチ
	$GB->{NINNIN} = 0	;
	if($GB->{FORM}->{'FROM'} !~ /\!kab/)	{return 0;}

	$GB->{KABU} = 1	;

	$GB->{MEIGARA} = $GB->{FORM}->{'bbs'}			;
	if($GB->{MEIGARA} eq 'operate2')	{$GB->{MEIGARA} = 'news4vip';}
#	if($GB->{MEIGARA} eq 'operate2')	{$GB->{MEIGARA} = 'punk';}
	$GB->{ZENKABU} = 0					;
	$GB->{KABUKA} =	&foxGetKabuka($GB,$GB->{MEIGARA})	;
	# 株主優待
	my $kabuu =	&foxGetKabusu($GB,$GB->{MEIGARA})	;
	my $rrr = 0	;
	if($GB->{ZENKABU} > 0)	{$rrr = int(10000 * $kabuu / $GB->{ZENKABU});}
	my $rrx = int($rrr/100)	;
	$GB->{ZENKABU} = "$GB->{MEIGARA}:$kabuu/$GB->{ZENKABU}=$rrx(%)"	;
	my $u4 = &IsUtai($GB->{KABUKA})				;
	if($kabuu > 4)
	{
		$GB->{KABUUP} = 1	;	#株主優待ぷち
	}
	if($rrr >= $u4)
	{
		$GB->{KABUU} = 1	;
	}
#	else
	{
		if($GB->{FORM}->{'FROM'} =~ /\!88/)
		{
			my $abc = 0	;
			foreach(@FOX_KABUU)
			{
				if($abc >= 5)	{last;}
				if(&IsSpecialKabuU($GB,"$_"))
				{
					$GB->{KABUU} = 1;
					last;
				}
				$abc ++	;
			}
			if($GB->{FORM}->{'FROM'} =~ /\!88-/)
			{
				$GB->{FORM}->{'FROM'} =~ s/\!88\-//;
				$GB->{KABUX}  = "株主優待"	;
			}
			else
			{
				$GB->{FORM}->{'FROM'} =~ s/\!88//;
			}
		}
	}
	if($GB->{FORM}->{'FROM'} =~ /\!kab\-/)
	{
		$GB->{FORM}->{'FROM'} =~ s/\!kab\-//;
		$GB->{NINNIN} = 1	;
	}

	# 持ち株数表示
	if($GB->{FORM}->{'FROM'} =~ /\!kab\:([a-zA-Z0-9]+)/)
	{
		if($1 ne '')	{$GB->{MEIGARA} = $1}		;
	}
	$GB->{KABUSU} =	&foxGetKabusu($GB,$GB->{MEIGARA})	;

	if(!$GB->{KABUU} && $GB->{KABUUP})
	{
		$GB->{KABUX} = "株優プチ($GB->{KABUXP})"	;
	}

	return 1;
}
#############################################################################
# 現在時刻を$GBに代入する
# マイクロ秒もとり、$GB->{NOWTIME}, $GB->{NOWMICROTIME} にそれぞれ代入
#############################################################################
sub mumumuGetNowTime
{
	my ($GB) = @_;

	#$GB->{NOWTIME} = time		;	#現在時刻

	# マイクロ秒もとる
	use Time::HiRes qw( gettimeofday );
	($GB->{NOWTIME}, $GB->{NOWMICROTIME}) = gettimeofday;

	# FreeBSD 5.2.1Rなbananaサーバのperlには
	# Time::HiResが入っていないので、
	# 替わりにsyscallを使っていた
	#
	#my $tv = pack("L!L!", ());	# 2つのpackしたlong型変数
	#
	#require 'sys/syscall.ph';
	#syscall(&main::SYS_gettimeofday, $tv, undef);
	#
	#($GB->{NOWTIME}, $GB->{NOWMICROTIME}) = unpack("L!L!", $tv);

	return 0;
}
#######################################################################
# 現在のロードアベレージ情報を調べる
#######################################################################
sub mumumuGetLA
{
	use Sys::CpuLoad;

	return (Sys::CpuLoad::load())[0];
}
#######################################################################
# 基準ロードアベレージ情報を調べる
#######################################################################
sub mumumuGetMaxLA
{
	my $servertype = "";

	$servertype = &mumumuGetServerType();
	if($servertype =~ /cobra/)	{ return 12.0; } # cobra
	elsif($servertype =~ /tiger/)	{ return 10.0; } # tiger
	elsif($servertype =~ /banana/)	{ return  4.0; } # banana
	else				{ return  4.0; } # unknown
}
#######################################################################
# サーバの型を調べる (cobra/tiger/banana/unknown)
#######################################################################
sub mumumuGetServerType
{
	use Sys::Hostname;
	my $hostname = "";

	$hostname = hostname();
	if($hostname =~ /cobra/ ||
	   $hostname =~ /oyster/)	{ return "cobra"; }
	elsif($hostname =~ /tiger/)	{ return "tiger"; }
	elsif($hostname =~ /banana/)	{ return "banana"; }
	else				{ return "unknown"; }
}
#######################################################################
# 基準ロードアベレージに達しているかどうかを調べる (引数: LA, 倍率)
#######################################################################
sub mumumuMaxLACheck
{
	my ($loadavg, $fact) = @_;

	if($loadavg >= $FOX->{MAXLOADAVG} * $fact)	{return 1;}
	else						{return 0;}
}
#############################################################################
# BEのポイントに応じたランク付け
# 引数: BEのポイント
# 戻り値: 会員それぞれに応じた3文字の文字列
#############################################################################
sub GetBERank
{
	my ($user_points) = @_;

	# 100000ポイント以上は「ソリティア」
	if($user_points    >= 500000)	{ return "SOL"; }
	# 30000ポイント以上はダイヤ会員
	elsif($user_points >= 100000)	{ return "DIA"; }
	# 10000ポイント以上はプラチナ会員
	elsif($user_points >= 12000)	{ return "PLT"; }
	# 1000ポイント以上はブロンズ会員
	elsif($user_points >= 10000)	{ return "BRZ"; }
	# それ未満は一般会員
	else				{ return "2BP"; }
}
#############################################################################
# BE による「ポイント特典(ラッキー賞)」判定
# 引数: $GB
# 戻り値: 1: ポイント特典、0: はずれ
#############################################################################
sub GetBELucky
{
	my ($GB) = @_;

	# SOL / DIA / PLT は無条件で 1
        if($GB->{BEelite} eq "SOL")	{ return 1; }
        if($GB->{BEelite} eq "DIA")	{ return 1; }
        if($GB->{BEelite} eq "PLT")	{ return 1; }

	# BRZ は 1/2 の確率で 1
        if($GB->{BEelite} eq "BRZ")
	{
		if(rand(4) < 1)		{ return 1; }
		return 0;
	}

	# それ以外は常に 0
	return 0;
}
#######################################################################
# 特別株主優待を取得する
#######################################################################
sub readKABUU
{
	#http://2pix.2ch.se/compan/moke.txt
	my $host = "http://2pix.2ch.se/compan/moke.txt"	;
	my $path = ""		;
	my $ua = LWP::UserAgent->new();
	$ua->agent('Mozilla/5.0 FOX(2ch.se)');
	$ua->timeout(3);
	my $request = HTTP::Request->new('GET', $host . $path);
	my $response = $ua->request($request) ;#ここで GET 処理
	my $db_content = $response->content();

	# エラーチェック
	if ($response->is_error)
	{
		# 持ち株数がとれない時は0株とみなす
		return 0;
	}

	@FOX_KABUU = split(/\n/,$db_content)	;

	return 0			;
}
#######################################################################
# 現在株数を取得する
#######################################################################
sub foxGetKabusu
{
	my ($GB,$bn) = @_	;
#&DispError2($GB,"FOX ★","<font color=green>FOX ★　ふふふっ</font><br><br>DMDM[$GB->{FORM}->{'DMDM'}] ,MDMD[$GB->{FORM}->{'MDMD'}]");

#	my $bn = $GB->{FORM}->{'bbs'}	;
#	if($bn eq 'operate2')	{$bn="giin";}
	#持ち株
	#http://be.2ch.net/test/PXshowsecdetail.php?DMDM=onetop@gmail.com&MDMD=8d2888&BN=news
	my $host = "http://be.2ch.net/test/PXshowsecdetail.php?"	;
	my $path = "MDMD=$GB->{FORM}->{'MDMD'}&DMDM=$GB->{FORM}->{'DMDM'}&BN=$bn"		;
	my $ua = LWP::UserAgent->new();
	$ua->agent('Mozilla/5.0 FOX(2ch.se)');
	$ua->timeout(3);
	my $request = HTTP::Request->new('GET', $host . $path);
	my $response = $ua->request($request) ;#ここで GET 処理
	my $db_content = $response->content();

	# エラーチェック
	if ($response->is_error)
	{
		# 持ち株数がとれない時は0株とみなす
		return 0;

#		my $code = $response->code();
#		&DispError2($GB, "ＥＲＲＯＲ！", "ＥＲＲＯＲ：持ち株情報の取得に失敗しました。($code)");
	}

	my ($name,$kabu,$tanka,$ttttt) = split(/<>/,$db_content)	;
	my $kkk = int($kabu)		;

	return $kkk			;
}
#######################################################################
# 現在株価を取得する
#######################################################################
sub foxGetKabuka
{
	my ($GB,$ita) = @_	;

	#株価
	#http://2pix.2ch.se/test/kabuka.so?morningcoffee
	my $host = "http://2pix.2ch.se/test/kabuka2.so?"	;
	my $path = $ita				;
	my $ua = LWP::UserAgent->new()		;
	$ua->agent('Mozilla/5.0 FOX(2ch.se)')	;
	$ua->timeout(3)				;
	my $request = HTTP::Request->new('GET', $host . $path);
	my $response = $ua->request($request) 	;#ここで GET 処理
	my $db_content = $response->content()	;

	# エラーチェック
	if ($response->is_error)
	{
		# 板の株価がとれなかったらエラー(E)とする
		return "E";

#		my $code = $response->code();
#		&DispError2($GB, "ＥＲＲＯＲ！", "ＥＲＲＯＲ：持ち株情報の取得に失敗しました。($code)");
	}

	my ($name,$kabuka,$zenkabu,$ttttt) = split(/\:/,$db_content)	;
	$kabuka = int($kabuka)		;
	my $ret = "---"			;
	if($kabuka > 0)	{$ret = $kabuka;}

	$GB->{KABUKA} = $ret;
	$GB->{ZENKABU} = int($zenkabu)	;

	return $ret;
}
#######################################################################
# BEの情報を$GBにセットする
#######################################################################
sub foxBEset
{
	my ($GB) = @_	;

	$GB->{isBE}     = 0		;
	$GB->{BEelite}  = ""		;
	$GB->{BELucky}  = 0		;
	$GB->{icon}	= ""		;
###2010/7/7 beサーバ陥落
#return 1;
	##############becheck
#&DispError2($GB,"FOX ★","<font color=green>FOX ★　ふふふっ</font><br><br>DMDM[$GB->{FORM}->{'DMDM'}] ,MDMD[$GB->{FORM}->{'MDMD'}]");

	if($GB->{FORM}->{'DMDM'} eq '')	{return 0;}

#	if($GB->{FORM}->{'bbs'} eq 'news'
#		&& $GB->{JIKAN} % 2
#	)
#	{
#		if($GB->{FORM}->{'DMDM'} =~ /\@gmail.com/
#		|| $GB->{FORM}->{'DMDM'} =~ /\@yahoo.co.jp/
#		|| $GB->{FORM}->{'DMDM'} =~ /\@hotmail.co.jp/
#		)
#		{
#			&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：このbeアカウントはこの時間使えません。");
#		}
#	}

	use LWP::UserAgent;

	my $path = "d=$GB->{FORM}->{'DMDM'}&m=$GB->{FORM}->{'MDMD'}";
	my $ua = LWP::UserAgent->new();
	$ua->timeout(5);
	my $request = HTTP::Request->new('GET', 'http://be.2ch.net/test/v.php?' . $path);
	my $response = $ua->request($request) ;#ここで GET 処理
	my $response_body = $response->content();#GETの結果はここに入っている

	my $db_content = $response->content();

	# エラーチェック
	if ($response->is_error)
	{
		my $code = $response->code();
		&DispError2($GB, "ＥＲＲＯＲ！", "ＥＲＲＯＲ：Beユーザー情報の取得に失敗しました。($code)");
	}

	my ($user_points, $xxx, $icon_name) = split(/ /, $db_content);

#	if($user_points =~ /\D/ || $xxx =~ /\D/){
#		&DispError2($GB, "ＥＲＲＯＲ！", "ＥＲＲＯＲ：Beユーザー情報の取得に失敗しました。(Invalid response)");
#	}
	if($xxx eq ''){
		&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：Beユーザー情報エラー。ログインしなおしてください(e)。<a href=\"http://be.2ch.net/\">be.2ch.net</a>");
	}
	$GB->{isBE}     = 1		;
	$GB->{BEpoints} = $user_points	;
	$GB->{BExxx}    = $xxx		;
	$GB->{icon}    = $icon_name		;

	# BEの点数に応じたランク付けを行い、種別に応じた文字列を入れる
	$GB->{BEelite}  = &GetBERank($GB->{BEpoints});
	#&DispError2($GB,"root ★","BE会員ステータス: $GB->{BEelite}");
	# ラッキー賞かどうか調べる
	$GB->{BELucky}  = &GetBELucky($GB);
	#&DispError2($GB,"root ★","BEラッキー賞: $GB->{BELucky}");

	if($FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_BE_TYPE2"})
	{
		#BBE異常時はするー
		if(!$FOX->{BBE})		{return 1;}

		#BBEに問合せ
		my $addr = foxDNSquery2("$GB->{NOWTIME}.$GB->{PID}.$GB->{FORM}->{'MDMD'}.1.bbe.2ch.net")	;

		#BBEがしくったら、以後船が自爆するまでDNS問い合わせを停止
		if($addr eq "127.0.0.0")	{ $FOX->{BBE} = 0; }
		# 焼かれている場合
		elsif($addr eq '127.0.0.2')
		{

#			&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：焼かれた be は使えません！");
		}
	}

	return 1;
}
#==================================================
#　日付・時刻を設定（$DATEに設定)
#==================================================
sub foxSetDate
{
	my ($GB) = @_	;
	my @wdays = ("日", "月", "火", "水", "木", "金", "土");
	my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst);
	#日付と時間をげとする
	($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($GB->{NOWTIME});
	$GB->{DATE} = sprintf("%02d/%02d/%02d %02d:%02d:%02d",
	$year % 100, $mon + 1, $mday, $hour, $min, $sec);

	$GB->{MD5DATE} = sprintf("%04d_%02d_%02d",
	$year + 1900, $mon + 1, $mday);
	$GB->{JIKAN} = $hour;
	$GB->{MON} = $mon+1;
	$GB->{MDAY} = $mday;
}
#==================================================
#　日付・時刻を設定（$DATEに設定)
#==================================================
sub foxSetDate2
{
	my ($GB) = @_	;
	my @wdays = split(/\//,$FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_YMD_WEEKS'});
	my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst);
	#日付と時間をげとする
	($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($GB->{NOWTIME});

	my $nengo  = $FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_YMD_NAME'}	;
	my $offset = $FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_YMD_OFFSET'}	;

#2006/04/01 event
	if($GB->{FORM}->{'bbs'} eq 'news4vip' && $year eq 107 && $mon eq 1 && $mday eq 14)
	{
		$mon = 1	;
		$mday = 15	;
	}

	if($nengo)
	{
		$GB->{DATE} = sprintf("$nengo%d年,%04d/%02d/%02d(%s) %02d:%02d:%02d",
		$year + 1900 + $offset,$year + 1900, $mon + 1, $mday,$wdays[$wday], $hour, $min, $sec);
	}
	else
	{
		$GB->{DATE} = sprintf("%04d/%02d/%02d(%s) %02d:%02d:%02d",
		$year + 1900, $mon + 1, $mday,$wdays[$wday], $hour, $min, $sec);
	}
}
#==================================================
#　初期情報の取得（設定ファイル）
#==================================================
#設定ファイルを読む
sub foxReadSettings
{
	my ($GB) = @_	;
	my $ita = $GB->{FORM}->{'bbs'}	;

$GB->{DEBUG} .= "SETTING.TXT よみこみむ?  $ita<br>";
	if(defined($FOX->{$ita}))
	{
		$GB->{DEBUG} .= "SETTING.TXT 既に読み込み済みー(1)$ita<br>";
#		$GB->{FORM}->{MESSAGE} .= "<hr>SETTING.TXT 既に読み込み済みー。($GB->{PID})";
		return 0;
	}
$GB->{DEBUG} .= "SETTING.TXT よみこみー$ita<br>";

	my $m_pass = "../$GB->{FORM}->{'bbs'}/SETTING.TXT";
	unless(-e $m_pass)
	{
		my $gogo5 = "../$GB->{FORM}->{'bbs'}/";
		#設定ファイルがない（ERROR)
		&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：ユーザー設定が消失しています！3<br><a href=\"$gogo5\">こっちにあるかもです</a>");
	}

	{
		open(FILE,$m_pass);
		local $_; while (<FILE>) {
			chomp;
			/^([^=]+)=(.*)$/ or next;
			(my $m_name, $_) = ($1, $2);
			#(my $m_name, $_) = split(/=/, $_, 2);
			s/%([[:xdigit:]]{2})/pack('H2', $1)/eg;
			$FOX->{$GB->{FORM}->{'bbs'}}->{$m_name} = $_;
		}
		close(FILE);
	}
#欠落情報の補完

	if($FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_BG_PICTURE"} =~ /ba\.gif/){
		$FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_BG_PICTURE"} = "http://www2.2ch.net/ba.gif";
	}

	if($FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_TITLE_PICTURE"} =~ /2ch\.gif/){
		$FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_TITLE_PICTURE"} = "http://www2.2ch.net/2ch.gif";
	}
	if($FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_TITLE_LINK"} =~ /info\.html/){
		$FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_TITLE_LINK"} = "http://info.2ch.net/guide/";
	}

	unless($FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_THREAD_NUMBER"}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_THREAD_NUMBER"} = 20;
	}
	unless($FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_CONTENTS_NUMBER"}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_CONTENTS_NUMBER"} = 10;
	}
	unless($FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_LINE_NUMBER"}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_LINE_NUMBER"} = 30;
	}
	unless($FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_MAX_MENU_THREAD"}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_MAX_MENU_THREAD"}=100;
	}
	unless($FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_BG_COLOR"}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_BG_COLOR"}="#FFFFFF";
	}
	unless($FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_MENU_COLOR"}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_MENU_COLOR"}="#CCFFCC";
	}
	unless($FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_MAKETHREAD_COLOR"}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_MAKETHREAD_COLOR"}="#CCFFCC";
	}
	unless($FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_THREAD_COLOR"}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_THREAD_COLOR"}="#EFEFEF";
	}
	unless($FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_SUBJECT_COLOR"}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_SUBJECT_COLOR"}="#FF0000";
	}
	unless($FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_TEXT_COLOR"}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_TEXT_COLOR"}="#000000";
	}
	unless($FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_NAME_COLOR"}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_NAME_COLOR"}="#008800";
	}
	unless($FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_LINK_COLOR"}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_LINK_COLOR"}="#0000FF";
	}
	unless($FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_ALINK_COLOR"}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_ALINK_COLOR"}="#FF0000";
	}
	unless($FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_VLINK_COLOR"}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_VLINK_COLOR"}="#660099";
	}
	unless($FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_UNICODE'}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_UNICODE'}="change";
	}
	unless($FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_TITLE_COLOR"}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_TITLE_COLOR"}="#000000";
	}
	unless($FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_SUBJECT_COUNT"}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_SUBJECT_COUNT"}=64;
	}
	unless($FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_NAME_COUNT"}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_NAME_COUNT"}=64;
	}
	unless($FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_MAIL_COUNT"}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_MAIL_COUNT"}=64;
	}
	unless($FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_MESSAGE_COUNT"}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_MESSAGE_COUNT"}=4096;
	}
	unless($FOX->{$GB->{FORM}->{'bbs'}}->{'timecount'}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{'timecount'} = 15;
	}
	if($FOX->{$GB->{FORM}->{'bbs'}}->{'timecount'} < 1){
		$FOX->{$GB->{FORM}->{'bbs'}}->{"timecount"} = 1;
	}
	unless($FOX->{$GB->{FORM}->{'bbs'}}->{'timeclose'}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{'timeclose'} = 12;
	}
	unless($FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_NONAME_NAME'}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_NONAME_NAME'} = "名無しさん";
	}
	unless($FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_DISP_IP'}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_DISP_IP'} = "";
	}
	unless($FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_YMD_WEEKS'}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_YMD_WEEKS'} = "日/月/火/水/木/金/土";
	}
#	unless($FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_YMD_NAME'}){
#		$FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_YMD_NAME'} = "皇紀";
#	}
#	unless($FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_YMD_OFFSET'}){
#		$FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_YMD_OFFSET'} = 660;
#	}

# 選挙用
#$FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_NONAME_NAME'} = "名無しさん＠そうだ選挙に行こう";
#$FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_SLIP'} = "checked";

	if($FOX->{$GB->{FORM}->{'bbs'}}->{'timeclose'} > $FOX->{$GB->{FORM}->{'bbs'}}->{'timecount'}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{"timeclose"} = $FOX->{$GB->{FORM}->{'bbs'}}->{"timecount"};
	}

$GB->{DEBUG} .= "SETTING.TXT よみこみー$ita完了!!<br>";
#	$GB->{FORM}->{MESSAGE} .= "<hr>SETTING.TXT読んだ。($GB->{PID})";

	$FOX->{$GB->{FORM}->{'bbs'}}->{MD5NUMBER} = &foxInitMD5id($GB->{FORM}->{'bbs'},$GB->{MD5DATE},$GB->{WPATH});
	$FOX->{MD5DATE} = $GB->{MD5DATE}	;

	$FOX->{$GB->{FORM}->{'bbs'}}->{SAMBA24} = &foxSamba24Init($GB->{FORM}->{'bbs'});

#bbspinkは、BBS_MAIL_COUNT=16
if($ENV{SERVER_NAME} =~ /bbspink.com/)
{
$FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_MAIL_COUNT"}=16;
}

#if($GB->{FORM}->{'bbs'} eq 'operate2' || $GB->{FORM}->{'bbs'} eq 'news4vip' || $GB->{FORM}->{'bbs'} eq 'news4viptasu')
#{
#	my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime(time);
#	if($mday <= 11)
#	{
#		my $ato = (11*24 + 6)*60*60			;
#		$ato -= ((($mday*24 + $hour)*60 + $min)*60 + $sec)	;
#		if($ato < 1000000)	{$ato =~ s/(\d)(\d\d\d)(?!\d)/$1,$2/g;}
#		else			{$ato =~ s/(\d)(\d\d\d)(\d\d\d)(?!\d)/$1,$2,$3/g;}
#		$FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_NONAME_NAME'} .= "あと$ato秒";
#	}
#}
	return 1	;
}
#######################################################################
#
#######################################################################
sub foxSamba24
{
	my ($GB, $tane, $spanspan) = @_	;

	my $Samba = "Samba24-2.13"	;

	#my $spanspan = 20	;	#規制秒数
	my $kanpeki  = 3	;	#許容回数 ERR593 Nsec しかたっていません
	my $saidai   = 5	;	#限界回数 ERR599 コーヒーブレイク、以降もう書けません。

#	my $yakinFile = "./book/$tane.cgi";
	my $yakinFile = "$FOX->{BOOK}/book/$tane.cgi";
	my $memomemo = "($Samba)";

	my ($prsize,$prmtime)= ();
	my $ctime = 0;
	my $keika = 0;
	my $errmsg = "";	# bbsdに聞いた結果 
	my $statnum = 0;	# Samba DBから返ってくるステータス

	# 雪だるまでは、bbsdに問い合わせる
	if(IsSnowmanServer)
	{
		# live22x[123] という名前で来たら、Samba120秒
		if($ENV{SERVER_NAME} =~ /live22x[123]/)
		{
			$spanspan = 120;
		}

		# Samba24 DB への問い合わせ
		my $cmd = 'chkid';
		$errmsg = bbsd_db($GB->{FORM}->{'bbs'}, $cmd, 'samba24', $tane, $spanspan, $kanpeki, $saidai, 'dummy'); 
		# タイムアウトかどうかチェック
		# タイムアウトだったらSamba24はスルー扱い
		if(&bbsd_TimeoutCheck($GB, $errmsg))
		{
			return 0;
		}

		# 結果を切り出し
		($statnum, $prsize, $keika) = split(/,/, $errmsg);

		# ステータスが0なら無問題
		if($statnum == 0) {return 0;}

		# 「連投回数」を数えるので、一つ減らす必要がある
		$prsize--;
	}
	else
	{
		($prsize, $prmtime) = (local $_=stat($yakinFile)) ? ($_->size, $_->mtime) : (0, 0);
		$ctime = time;
		$keika = $ctime - $prmtime;
	}

	# 規制発動
	if($prsize > $saidai)
	{
		my $houhou = '<a href=\"http://etc6.2ch.net/event/\">イベント企画</a>板で一時間以上新しい面白いイベント考えてください。';

		print "Content-type: text/html; charset=shift_jis\n\n";
		print <<EOF;
<html><head><title>ＥＲＲＯＲ！</title><meta http-equiv="Content-Type" content="text/html; charset=shift_jis"></head>
<body><!-- 2ch_X:error -->
ＥＲＲＯＲ - 594 もうずっと書けませんよ。<br>
<br>
あなたは、規制リストに追加されました。<br><br>
【解除する方法】<br>
$houhou<br>
これ以外に解除の方法はありません。<br>

<br><hr>$memomemo</body>
</html>
EOF

		if(!IsSnowmanServer)
		{
			open(YAN1,">>$yakinFile");print YAN1 "1";close(YAN1);
		}

		exit;
	}

	# 警告表示
	if($prsize && $keika < $spanspan)
	{

		if(!IsSnowmanServer)
		{
			open(YAN1,">>$yakinFile");print YAN1 "1";close(YAN1);
		}

		# 重くやばい
		if($prsize > $kanpeki)
		{
			my ($fsec,$fmin,$fhour,$fmday,$fmon,$fyear,$fwday,$fyday,$fisdst) = localtime($ctime); $fmon ++	;$fyear += 1900	;

			print "Content-type: text/html; charset=shift_jis\n\n";
			print <<EOF;
<html><head><title>ＥＲＲＯＲ！</title><meta http-equiv="Content-Type" content="text/html; charset=shift_jis"></head>
<body><!-- 2ch_X:error -->
599 連打しないでください。もうそろそろ規制リストに入れますよ。。(￣ー￣)ニヤリッ<br>
<br><hr>$memomemo</body>
</html>
EOF
			exit;
		}

		# 軽くやばい/初犯
		print "Content-type: text/html; charset=shift_jis\n\n";
		print <<EOF;
<html><head><title>ＥＲＲＯＲ！</title><meta http-equiv="Content-Type" content="text/html; charset=shift_jis"></head>
<body><!-- 2ch_X:error -->
ＥＲＲＯＲ - 593 $spanspan sec たたないと書けません。($prsize回目、$keika sec しかたってない)<br>
<br>
120sec規制の場合 Be にログインすると回避できます(newsplusを除く)。<a href="http://be.2ch.net/">be.2ch.net</a>

<br><hr>$memomemo</body>
</html>
EOF
		exit;
	}

	if(!IsSnowmanServer)
	{
		if($prsize) {unlink("$yakinFile");}

		open(YAN1,">>$yakinFile");print YAN1 "1";close(YAN1);
		# 最初でumask(0)を宣言しているので不要
		#umask(0);
		#chmod(0666, $yakinFile);
	}

	return 0;
}
#######################################################################
# ●での単位時間当たりのスレ立て数をチェックする
# 一時ファイルの場所はSamba24と同じところを流用する
# 一時ファイル名の先頭に "." をつけることで、f22によるIP数のカウントに
# 影響が出ないようにする
#######################################################################
sub mumumuKuromaruSuretateCount
{
	my ($GB, $tcountmax) = @_;
	my $FilenoTane = $GB->{MARU};

	# ★はカウントアップなし
	if($GB->{CAP})		{return 0;}

	# ●の中身をファイル名として使用可能なものにする(/を_に変換)
	$FilenoTane =~ s/\//_/g;

	# 雪だるまではbbsdに問い合わせる
	if(IsSnowmanServer)
	{
		my $errmsg = "";
		my $statnum = 0;
		my $cmd = 'chkid';
		$errmsg = bbsd_db($GB->{FORM}->{'bbs'}, $cmd, 'kuromarusuretate', $FilenoTane, 1800, $tcountmax, $tcountmax, 'dummy');
		# タイムアウトかどうかチェック
		# タイムアウトだったらスルー扱い
		if(&bbsd_TimeoutCheck($GB, $errmsg))
		{
			return 0;
		}

		# 結果を切り出し
		$statnum = (split(/,/, $errmsg))[0];

		# $tcountmaxを超えていたら立てすぎ
		if($statnum == 3) {return 1;}
		# スルー判定
		return 0;
	}
	else
	{
		# ファイル置き場はSamba24の場所を借用する
		my $KuromaruFile = "./book/.$FilenoTane.cgi";
		# ●でのスレ立て回数
		my $tcount = 0;

		# ファイルがあるかどうか調べて、、、
		if(-e $KuromaruFile)
		{
			# あったら中身を読んで変数に入れ、カウントアップして書き込む
			# 同時刻に同じ●でのスレ立てはないと仮定し、排他制御はしない
			open(KURO,"+<$KuromaruFile");
			$tcount = <KURO>;
			$tcount++;
			truncate(KURO, 0);
			seek(KURO, 0, 0);         
			print KURO $tcount;
			close(KURO);
		}
		else
		{
			# なかったらファイルを新規に作って、1を書き込む
			$tcount = 1;
			open(KURO,">$KuromaruFile");
			print KURO $tcount;
			close(KURO);
		}

		# 最大回数に達していたら、異常を返す
		if($tcount >= $tcountmax)	{return 1;}
		# スルー判定
		return 0;
	}
}
#########################################################
#
#########################################################
sub foxCheckMD5id
{
	my ($bbs,$md5date,$num,$dateFox,$wpath) = @_	;
	my $md5datefile = "";

	if($dateFox eq $md5date)
	{
		return $num			;
	}

	# 雪だるまは/mdの下を読む
	if(IsSnowmanServer == BBSD->{REMOTE})
	{
		$md5datefile = $wpath . '/md5.cgi';
	}
	else
	{
		$md5datefile = "../$bbs/md5.cgi";
	}
	if(open(MD5FILE, $md5datefile))
	{
		my $md5line = <MD5FILE>;
		close(MD5FILE);
		my ($a, $b) = split(/<>/, $md5line, 2);
		if ($a eq $md5date) {return $b;}
	}

	return &foxCreateMD5id($bbs,$md5date,$wpath)	;
}
#########################################################
#
#########################################################
sub foxGetMD5id
{
	my ($bbs,$md5date,$num,$tane) = @_	;
	my $id = "FOX"			;

	use Digest::MD5			;
	use Digest::MD5 qw(md5_hex)	;

	my $idnum = md5_hex($tane)	;
	my $md5 = Digest::MD5->new	;
	$md5->add(substr($idnum,-4))	;
	$md5->add($bbs)			;
	$md5->add($num)			;
	$id = substr($md5->b64digest, 0, 8);

	return $id			;
}
#########################################################
#
#########################################################
sub foxInitMD5id
{
	my ($bbs,$md5date,$wpath) = @_		;
	my $md5datefile = "";

	# 雪だるまは/mdの下を読む
	if(IsSnowmanServer == BBSD->{REMOTE})
	{
		$md5datefile = $wpath . '/md5.cgi';
	}
	else
	{
		$md5datefile = "../$bbs/md5.cgi";
	}
	if(open(MD5FILE, $md5datefile))
	{
		my $md5line = <MD5FILE>	;
		close(MD5FILE)		;
		my ($a, $b) = split(/<>/, $md5line, 2);
		if($a eq $md5date)	{return $b;}
	}
	return &foxCreateMD5id($bbs,$md5date,$wpath)	;
}
#########################################################
#
#########################################################
sub foxCreateMD5id
{
	use Fcntl;

	my ($bbs,$md5date,$wpath) = @_		;
	my $md5datefile = "";

	# 雪だるまは/mdの下に作る
	if(IsSnowmanServer == BBSD->{REMOTE})
	{
		if(!(-e $wpath))	{ mkdir($wpath, 0777); }
		$md5datefile = $wpath . '/md5.cgi';
	}
	else
	{
		$md5datefile = "../$bbs/md5.cgi";
	}
	my $data = "ABCD";
	my $md5line = "";

	# 雪だるまでは、bbsdに種を問い合わせる
	if(IsSnowmanServer == BBSD->{REMOTE})
	{
		my $cmd = 'getmd5seed';
		$md5line = bbsd($bbs, $cmd, 'dummy');
		# タイムアウトかどうかチェック
		# ここは$GBがないので、適当に作る
		my $TMPGB = {};
		$TMPGB->{FORM}->{'bbs'} = $bbs;
		if(&bbsd_TimeoutCheck($TMPGB, $md5line))
		{
			&bbsd_TimeoutError($TMPGB, $cmd);
		}
	}
	# 通常サーバでは、自分で種を作る
	else
	{
		sysopen(RANDOM, '/dev/urandom', O_RDONLY) || die "cannot open /dev/urandom $!\n";
		sysread(RANDOM, $data, 16)	;
		close(RANDOM)			;
	}

	open(MD5FILE, ">$md5datefile")	;
	# 雪だるまでは、得た種をそのままの形で書く
	if(IsSnowmanServer == BBSD->{REMOTE})
	{
		print MD5FILE $md5line;
		$data = (split(/<>/,$md5line))[1];
	}
	else
	{
		print MD5FILE "$md5date<>$data"	;
	}
	close(MD5FILE)			;
	# 最初にumask(0)しているので不要
	#chmod(0777, $md5datefile)	;

	return	$data			;
}
########################################################################
# 板ごとのスレッド保持数を調べる(initFOXから船出航時に一度だけ呼ばれる)
# 戻り値: f22における保持数(得られなかった場合デフォルト(1000))
########################################################################
#sub mumumuGetHojisuu
#{
#	# デフォルト値、/_bg/f22.cgiを参照
#	my $resNumMax  = 1000;
#	my @f22 = ();
#	my @f22r = ();
#
#	# f22の設定ファイルを読み、値を調べる
#	if (-e '../_bg/f22info.cgi')
#	{
#		open(F22FILE,"../_bg/f22info.cgi");
#		@f22 = <F22FILE>;
#		close(F22FILE);
#
#		# $resNumMax の行を調べ、、、
#		@f22r = grep(/\$resNumMax /, @f22);
#
#		# 該当行があれば、えばる
#		# これにより$resNumMaxが更新される
#		if ($f22r[0] ne '')
#		{
#			eval $f22r[0];
#		}
#	}
#
#	return $resNumMax;
#}
#########################################################
#
#########################################################
sub initFOX
{
	$FOX->{NOWTIME} = time		;

	# BBxのDNSサーバが動いているかどうかフラグ
	$FOX->{BBM} = 1			;
	$FOX->{BBM2} = 1		;
	$FOX->{BBQ} = 1			;
	$FOX->{BBX} = 1			;
	$FOX->{BBN} = 1			;
	$FOX->{BBY} = 1			;
	$FOX->{BBS} = 1			;
	$FOX->{BBR} = 1			;
	$FOX->{BBE} = 1			;

	# BBY/BBS/BBR用DNSサーバIPアドレス
	# サーバ移転時は要変更
	# BBRはrock54.2ch.netと同一サーバだが別IPアドレスとなることに注意
	# (BBQ/BBM/BBX/BBN/BBEは通常のDNS検索のため、IPアドレス埋め込みはなし)
	$FOX->{DNSSERVER}->{BBY}  = "206.223.152.130"	;# a.ns.bby.2ch.net
	$FOX->{DNSSERVER}->{BBYP} = "206.223.153.130"	;# a.ns.bby.bbspink.com
	$FOX->{DNSSERVER}->{BBS}  = "207.29.247.145"	;# a.ns.bbs.2ch.net
	$FOX->{DNSSERVER}->{BBR}  = "206.223.151.68"	;# a.ns.bbr.2ch.net

=begin comment

bbsd 関連の処理は BBSD.pm に一任のためコメントアウト
	# 雪だるまサーバかどうか(雪だるまなら1、そうでなければ0)
	$FOX->{SNOWMAN}->{FLAG} = &IsSnowManServer($ENV{'SERVER_NAME'});

	# 雪だるまサーバだったら、初期化ルーチンを呼ぶ
	if($FOX->{SNOWMAN}->{FLAG})
	{
		&InitSnow($ENV{'SERVER_NAME'});
	}

=end comment

=cut

	# 特殊機能 (Saborin, IsKoukokuSkip, CentiSec 等)
	%{$FOX->{BBSCGI_FUNCTIONS}} = map +($_ => 1), split /,/, uc($ENV{SSL_X_BBSCGI_FUNCTIONS} || '');
	# Set-Cookie 有効期間
	$FOX->{COOKIEEXPIRES} = strftime '%A, %d-%b-%Y %T GMT', gmtime 86400 * (int($FOX->{NOWTIME} / 86400) + 2 * 365);

	$FOX->{MAXLOADAVG} = &mumumuGetMaxLA();# サーバ毎の許容ロードアベレージ
	$FOX->{ISKOUKOKU} = 1		;# IsKoukokuを実行するかどうか
#	$FOX->{KUROMARUTCOUNT} = 6	;# ●で一時間あたりに立てられるスレ数
	$FOX->{KUROMARUTCOUNT} = 100	;# by FOX

	#$FOX->{HOJISUU} = &mumumuGetHojisuu();# サーバごとのスレッド保持数

	# 広告ファイル名(public_html/test からの相対パス)
	# 雪だるまではbbsdに渡す

	if($ENV{'SERVER_NAME'} =~ /bbspink\.com/)
	{
		$FOX->{headadfile} = '../SAKURA.txt'	;#上の上
		$FOX->{putadfile}  = ''			;#上の下
		$FOX->{maido3adfile} = sub { '../BANANA.txt'; }		;#真ん中
	}
	else
	{
		$FOX->{headadfile} = 'headad.txt'	;#上の上
		$FOX->{putadfile}  = 'putad.txt'	;#上の下
		$FOX->{maido3adfile} = sub { "maido3ad/$_[0]"; }	;#真ん中
	}

	################################################################
	# 携帯/PHS用IPアドレスブロック関連
	################################################################
	# 使用モジュールの読み込み
	use Net::CIDR::Lite;

	################################################################
	# iモード用IPアドレスブロック関連
	################################################################
	$FOX->{IMODECIDR} = Net::CIDR::Lite->new;

	# IPアドレスブロック一覧(CIDR形式)
	# アドレスレンジが追加された場合、ここに加えていく
	# http://www.nttdocomo.co.jp/service/imode/make/content/ip/
	my @imodecidr = (
	"210.153.84.0/24",
	"210.136.161.0/24",
	"210.153.86.0/24",
	"124.146.174.0/24",
	"124.146.175.0/24",
	"202.229.176.0/24",
	"202.229.177.0/24",
	"202.229.178.0/24"
	);
	# CIDRリストをあらかじめ登録しておく
	# こうしておくことで、重い初期化はbbs.cgi出航時の1回で済む
	foreach (@imodecidr) {
		$FOX->{IMODECIDR}->add($_);
	}

	################################################################
	# iモードフルブラウザ用IPアドレスブロック関連
	################################################################
	$FOX->{IMODEFULLBROWSERCIDR} = Net::CIDR::Lite->new;

	# IPアドレスブロック一覧(CIDR形式)
	# アドレスレンジが追加された場合、ここに加えていく
	# http://www.nttdocomo.co.jp/service/imode/make/content/ip/
	my @imodefullbrowsercidr = (
	"210.153.87.0/24"
	);
	# CIDRリストをあらかじめ登録しておく
	# こうしておくことで、重い初期化はbbs.cgi出航時の1回で済む
	foreach (@imodefullbrowsercidr) {
		$FOX->{IMODEFULLBROWSERCIDR}->add($_);
	}

	################################################################
	# EZweb用IPアドレスブロック関連
	################################################################
	$FOX->{EZWEBCIDR} = Net::CIDR::Lite->new;
	
	# IPアドレスブロック一覧(CIDR形式)
	# アドレスレンジが追加された場合、ここに加えていく
	# http://www.au.kddi.com/ezfactory/tec/spec/ezsava_ip.html
	my @ezwebcidr = (
	"210.230.128.224/28",
	"121.111.227.160/27",
	"61.117.1.0/28",
	"219.108.158.0/27",
	"219.125.146.0/28",
	"61.117.2.32/29",
	"61.117.2.40/29",
	"219.108.158.40/29",
	"219.125.148.0/25",
	"222.5.63.0/25",
	"222.5.63.128/25",
	"222.5.62.128/25",
	"59.135.38.128/25",
	"219.108.157.0/25",
	"219.125.145.0/25",
	"121.111.231.0/25",
	"121.111.227.0/25",
	"118.152.214.192/26",
	"118.159.131.0/25",
	"118.159.133.0/25",
	"118.159.132.160/27",
	"111.86.142.0/26",
	"111.86.141.64/26",
	"111.86.141.128/26",
	"111.86.141.192/26",
	"118.159.133.192/26",
	"111.86.143.192/27",
	"111.86.143.224/27",
	"111.86.147.0/27",
	"111.86.142.128/26",
	"111.86.142.192/26",
	"111.86.143.0/26"
	);
	# CIDRリストをあらかじめ登録しておく
	# こうしておくことで、重い初期化はbbs.cgi出航時の1回で済む
	foreach (@ezwebcidr) {
		$FOX->{EZWEBCIDR}->add($_);
	}

	################################################################
	# au PCサイトビューアー(PCSV)用IPアドレスブロック関連
	################################################################
	$FOX->{PCSITEVIEWERCIDR} = Net::CIDR::Lite->new;

	# IPアドレスブロック一覧(CIDR形式)
	# アドレスレンジが追加された場合、ここに加えていく
	# http://www.au.kddi.com/ezfactory/tec/spec/pcsv.html
	my @pcsiteviewercidr = (
	"222.15.68.192/26",
	"59.135.39.128/27",
	"118.152.214.160/27",
	"118.152.214.128/27",
	"222.1.136.96/27",
	"222.1.136.64/27",
	"59.128.128.0/20"
	);
	# CIDRリストをあらかじめ登録しておく
	# こうしておくことで、重い初期化はbbs.cgi出航時の1回で済む
	foreach (@pcsiteviewercidr) {
		$FOX->{PCSITEVIEWERCIDR}->add($_);
	}

	################################################################
	# Y!ケータイ用IPアドレスブロック関連
	################################################################
	$FOX->{SOFTBANKCIDR} = Net::CIDR::Lite->new;
	
	# IPアドレスブロック一覧(CIDR形式)
	# アドレスレンジが追加された場合、ここに加えていく
	# http://developers.vodafone.jp/dp/tech_svc/web/ip.php
	#
	# ソフトバンクモバイルになって、URI が変更された模様
	# -- 10/30/2006 by む
	# http://developers.softbankmobile.co.jp/dp/tech_svc/web/ip.php
	#
	# 再度変更された模様
	# -- 4/28/2008 by む
	# http://creation.mb.softbank.jp/web/web_ip.html
	my @softbankcidr = (
	"123.108.237.0/27",
	"202.253.96.224/27",
	"210.146.7.192/26",
	"210.175.1.128/25"
	);
	# CIDRリストをあらかじめ登録しておく
	# こうしておくことで、重い初期化はbbs.cgi出航時の1回で済む
	foreach (@softbankcidr) {
		$FOX->{SOFTBANKCIDR}->add($_);
	}

	################################################################
	# ソフトバンクモバイル PCサイトブラウザ用IPアドレスブロック関連
	################################################################
	$FOX->{PCSITEBROWSERCIDR} = Net::CIDR::Lite->new;

	# PCサイトブラウザにて利用するIPアドレス帯域
	# ソフトバンク携帯電話のPCサイトブラウザにて
	# ウェブサーバへアクセスする際、ウェブサーバ側に通知される
	# 送信元のIPアドレスは下記の帯域内アドレスとなります。 
	my @pcsitebrowsercidr = (
	"123.108.237.224/27",
	"202.253.96.0/28"
	);
	# CIDRリストをあらかじめ登録しておく
	# こうしておくことで、重い初期化はbbs.cgi出航時の1回で済む
	foreach (@pcsitebrowsercidr) {
		$FOX->{PCSITEBROWSERCIDR}->add($_);
	}

	################################################################
	# emobile EMnet用IPアドレスブロック関連
	################################################################
	$FOX->{EMNETCIDR} = Net::CIDR::Lite->new;

	# IPアドレスブロック一覧(CIDR形式)
	# アドレスレンジが追加された場合、ここに加えていく
	# http://developer.emnet.ne.jp/ipaddress.html

	# eM60-254-209-99.emobile.ad.jp = 60.254.209.99 も EMnet なことに注意
	# http://takagi-hiromitsu.jp/diary/20080722.html
	my @emnetcidr = (
	"60.254.209.99/32",
	"117.55.1.224/27"
	);
	# CIDRリストをあらかじめ登録しておく
	# こうしておくことで、重い初期化はbbs.cgi出航時の1回で済む
	foreach (@emnetcidr) {
		$FOX->{EMNETCIDR}->add($_);
	}

	################################################################
	# AIR-EDGE PHONE用IPアドレスブロック関連
	################################################################
	$FOX->{AIREDGECIDR} = Net::CIDR::Lite->new;

	# IPアドレスブロック一覧(CIDR形式)
	# アドレスレンジが追加された場合、ここに加えていく
	# http://www.willcom-inc.com/ja/service/contents_service/create/center_info/index.html
	my @airedgecidr = (
	"61.198.128.0/24", "61.198.129.0/24", "61.198.130.0/24", "61.198.131.0/24",
	"61.198.132.0/24", "61.198.133.0/24", "61.198.134.0/24", "61.198.135.0/24",
	"61.198.136.0/24", "61.198.137.0/24", "61.198.138.100/32", "61.198.138.101/32",
	"61.198.138.102/32", "61.198.138.103/32", "61.198.139.0/29", "61.198.139.128/27",
	"61.198.139.160/28", "61.198.140.0/24", "61.198.141.0/24", "61.198.142.0/24",
	"61.198.143.0/24", "61.198.160.0/24", "61.198.161.0/24", "61.198.162.0/24",
	"61.198.163.0/24", "61.198.164.0/24", "61.198.165.0/24", "61.198.166.0/24",
	"61.198.168.0/24", "61.198.169.0/24", "61.198.170.0/24", "61.198.171.0/24",
	"61.198.172.0/24", "61.198.173.0/24", "61.198.174.0/24", "61.198.175.0/24",
	"61.198.248.0/24", "61.198.249.0/24", "61.198.250.0/24", "61.198.251.0/24",
	"61.198.252.0/24", "61.198.253.0/24", "61.198.254.0/24", "61.198.255.0/24",
	"61.204.0.0/24", "61.204.2.0/24", "61.204.3.0/25", "61.204.3.128/25",
	"61.204.4.0/24", "61.204.5.0/24", "61.204.6.0/25", "61.204.6.128/25",
	"61.204.7.0/25", "61.204.92.0/24", "61.204.93.0/24", "61.204.94.0/24",
	"61.204.95.0/24", "114.20.49.0/24", "114.20.50.0/24", "114.20.51.0/24",
	"114.20.52.0/24", "114.20.53.0/24", "114.20.54.0/24", "114.20.55.0/24",
	"114.20.56.0/24", "114.20.57.0/24", "114.20.58.0/24", "114.20.59.0/24",
	"114.20.60.0/24", "114.20.61.0/24", "114.20.62.0/24", "114.20.63.0/24",
	"114.20.64.0/24", "114.20.65.0/24", "114.20.66.0/24", "114.20.67.0/24",
	"125.28.0.0/24", "125.28.1.0/24", "125.28.15.0/24", "125.28.16.0/24",
	"125.28.17.0/24", "125.28.2.0/24", "125.28.3.0/24", "125.28.4.0/24",
	"125.28.5.0/24", "125.28.8.0/24", "210.168.246.0/24", "210.168.247.0/24",
	"210.169.92.0/24", "210.169.93.0/24", "210.169.94.0/24", "210.169.95.0/24",
	"210.169.96.0/24", "210.169.97.0/24", "210.169.98.0/24", "210.169.99.0/24",
	"211.126.192.128/25", "211.18.232.0/24", "211.18.233.0/24", "211.18.234.0/24",
	"211.18.235.0/24", "211.18.236.0/24", "211.18.237.0/24", "219.108.10.0/24",
	"219.108.11.0/24", "219.108.12.0/24", "219.108.13.0/24", "219.108.14.0/24",
	"219.108.15.0/24", "219.108.7.0/24", "219.108.8.0/24", "219.108.9.0/24",
	"221.119.0.0/24", "221.119.1.0/24", "221.119.2.0/24", "221.119.3.0/24",
	"221.119.4.0/24", "221.119.6.0/24", "221.119.7.0/24", "221.119.8.0/24",
	"221.119.9.0/24"
	);
	# CIDRリストをあらかじめ登録しておく
	# こうしておくことで、重い初期化はbbs.cgi出航時の1回で済む
	foreach (@airedgecidr) {
		$FOX->{AIREDGECIDR}->add($_);
	}

	################################################################
	# AIR-EDGE MEGAPLUS用IPアドレスブロック関連
	################################################################
	$FOX->{MEGAPLUSCIDR} = Net::CIDR::Lite->new;

	# IPアドレスブロック一覧(CIDR形式)
	# アドレスレンジが追加された場合、ここに加えていく
	#
	# 【BBQ 7本目】公開串登録所 【ピンポイント規制】
	# http://qb5.2ch.net/test/read.cgi/sec2chd/1123932393/908-918
	# により、現在は222.13.35.0/24を登録
	#
	# リモートIPアドレスがこのレンジだった場合、foxSetHost で、
	# Client_IP ヘッダを読み、いわゆる漏れ串の動作をさせる
	my @megapluscidr = (
	"222.13.35.0/24"
	);
	# CIDRリストをあらかじめ登録しておく
	# こうしておくことで、重い初期化はbbs.cgi出航時の1回で済む
	foreach (@megapluscidr) {
		$FOX->{MEGAPLUSCIDR}->add($_);
	}

	################################################################
	# ibisBrowser用IPアドレスブロック関連
	################################################################
	$FOX->{IBISBROWSERCIDR} = Net::CIDR::Lite->new;

	# IPアドレスブロック一覧(CIDR形式)
	# アドレスレンジが追加された場合、ここに加えていく
	# http://ibis.ne.jp/support/browserIP.jsp
	my @ibisbrowsercidr = (
	"59.106.88.0/24"
	);
	# CIDRリストをあらかじめ登録しておく
	# こうしておくことで、重い初期化はbbs.cgi出航時の1回で済む
	foreach (@ibisbrowsercidr) {
		$FOX->{IBISBROWSERCIDR}->add($_);
	}

	################################################################
	# jig Browser用IPアドレスブロック関連
	################################################################
	$FOX->{JIGBROWSERCIDR} = Net::CIDR::Lite->new;

	# IPアドレスブロック一覧(CIDR形式)
	# アドレスレンジが追加された場合、ここに加えていく
	# http://br.jig.jp/pc/ip_br.html
	my @jigbrowsercidr = (
	"59.106.23.169/32", "59.106.23.170/31", "59.106.23.172/31",
	"82.48.6.10/31", "82.48.6.12/30",
	"112.78.114.208/32",
	"112.78.207.6/31", "112.78.207.8/29", "112.78.207.16/29",
	"112.78.207.24/31", "112.78.207.38/31", "112.78.207.40/29",
	"112.78.207.48/29", "112.78.207.56/31",
	"112.78.215.70/31", "112.78.215.72/29", "112.78.215.80/29",
	"112.78.215.88/31",
	"112.78.215.166/31", "112.78.215.168/29", "112.78.215.176/29",
	"112.78.215.184/31", "112.78.215.198/31", "112.78.215.200/29",
	"112.78.215.208/29", "112.78.215.216/31", "112.78.215.230/31",
	"112.78.215.232/29", "112.78.215.240/29", "112.78.215.248/31",
	"182.48.5.134/31", "182.48.5.136/29", "182.48.5.144/29",
	"182.48.5.152/31", "182.48.5.166/31", "182.48.5.168/29",
	"182.48.5.176/29", "182.48.5.184/31", "182.48.5.198/31",
	"182.48.5.200/29", "182.48.5.208/29", "182.48.5.216/31",
	"182.48.5.230/31", "182.48.5.232/29",
	"182.48.6.6/31", "182.48.6.8/29",
	"202.181.98.160/32", "202.181.98.179/32", "202.181.98.196/32",
	"210.188.205.81/32", "210.188.205.83/32",
	"219.94.177.6/31", "219.94.177.8/29", "219.94.177.16/29",
	"219.94.177.24/31",
	"219.94.182.230/31", "219.94.182.232/29", "219.94.182.240/29",
	"219.94.182.248/31",
	"219.94.183.102/31", "219.94.183.104/29", "219.94.183.112/29",
	"219.94.183.120/31",
	"219.94.184.70/31", "219.94.184.72/30", "219.94.184.76/32"
	);
	# CIDRリストをあらかじめ登録しておく
	# こうしておくことで、重い初期化はbbs.cgi出航時の1回で済む
	foreach (@jigbrowsercidr) {
		$FOX->{JIGBROWSERCIDR}->add($_);
	}

	################################################################
	# ソフトバンクモバイル iPhone用IPアドレスブロック関連
	################################################################
	# 2ch特化型サーバ・ロケーション構築作戦 Part29
	# http://qb5.2ch.net/test/read.cgi/operate/1212665493/850-852
	# とりあえず仮対応 -- 2008/7/15 by む
	# http://qb5.2ch.net/test/read.cgi/operate/1267711917/639
	# 126.230.0.0/15 と 126.232.0.0/13 を追加 -- 2010/4/10 by む
	$FOX->{IPHONECIDR} = Net::CIDR::Lite->new;
	my @iphonecidr = (
	"126.230.0.0/15",
	"126.232.0.0/13",
	"126.240.0.0/12"
	);
	# CIDRリストをあらかじめ登録しておく
	# こうしておくことで、重い初期化はbbs.cgi出航時の1回で済む
	foreach (@iphonecidr) {
		$FOX->{IPHONECIDR}->add($_);
	}

	#雪だるまサーバでは、これらの広告は読まなくていい
	if(!IsSnowmanServer)
	{
		local $/;
		if (open(ADFILE, $FOX->{headadfile})) {
			$FOX->{headad} = <ADFILE>;
			close(ADFILE);
		}

		if($ENV{'SERVER_NAME'} =~ /2ch\.net/)
		{
			if (open(ADFILE, $FOX->{putadfile})) {
				$FOX->{putad} = <ADFILE>;
				close(ADFILE);
			}
		}
	}

	#フッター（下の広告）
	$FOX->{footad} = ''	;
	$FOX->{topad} = ''	;
	$FOX->{lastad} = ' ページのおしまいだよ。。と';

	#掲示板一覧表の表示
	#雪だるまではこれではなく、bbsdが表示しているので注意
	$FOX->{links} = '<Center><a href="http://menu.2ch.net/bbstable.html" Target=_blank>■<b>掲示板一覧</b>■</a></Center>';

	#２ちゃんねる特別リンク
	#雪だるまではこれではなく、bbsdが表示しているので注意
	$FOX->{specialad} = ' | <a href="http://irc.2ch.net">チャット</a>';

	# 以下のものは雪だるまでも読まないとだめ

	#規制用ファイル(●)
	if(open(ADFILE, 'proxy998.cgi'))
	{
		@FOX_K998 = <ADFILE>	;
		close(ADFILE)		;
	}

	#規制用ファイル(プロバイダ)
	if(open(ADFILE, 'proxy999.cgi'))
	{
		@FOX_K999 = <ADFILE>	;
		close(ADFILE)		;
	}

	#規制用ファイル(Rock54)
	if(open(ADFILE, '../_bg/Rock54.txt'))
	{
#		@FOX_Ro54 = <ADFILE>	;
		@FOX_Ro54 = map { eval {
			no warnings;
			my @a = (split /<>/)[5..7];
			[qr/$a[0]/, @a[1..2]];
		}; } <ADFILE>;
		close(ADFILE)		;
	}

	local $_;
	#名無しリスト(4vip)
	if(open(ADFILE, '/md/tmp/nanashi.txt')
	 ||open(ADFILE, 'nanashi.txt'))
	{
		while (<ADFILE>)
		{
			chomp		;
			push(@FOX_774, $_);      # 最後に要素を追加する
		}
		close(ADFILE)		;
	}
	# 選挙用
	#@FOX_774 = (
	#	"名無しさん＠そうだ選挙に行こう(a)",
	#	"名無しさん＠そうだ選挙に行こう(a)"
	#);

	#県名ルックアップ asahi-net
	%FOX_KEN_ASAHI = ()		;
	if(open(ADFILE,"./_KEN-ASAHI.txt"))
	{
		while (<ADFILE>)
		{
			chomp		;
			my ($p,$r,$x) = split(/ /)	;
#if(open(LX,">> HOST29.000")){print LX "(READ asahi) $p = $r\n";close(LX);}
			next if ($r =~ /\D/)		;
			$FOX_KEN_ASAHI{$p} = int($r)	;
		}
		close(ADFILE)		;
	}
#if(open(LX,">> HOST29.000")){print LX "(READ asahi) v116 = $FOX_KEN_ASAHI{v116}\n";close(LX);}

	#県名ルックアップ dion
	%FOX_KEN_DION = ()		;
	if(open(ADFILE,"./_KEN-DION.txt"))
	{
		while (<ADFILE>)
		{
			chomp			;
			my ($p,$r,$x) = split(/\t/)	;
			if ($r !~ /\D/ && $r > 0)
			{
#if(open(LX,">> HOST29.000")){print LX "(READ dion) $p = $r\n";close(LX);}
				$FOX_KEN_DION{$p} = int($r)	;
			}
		}
		close(ADFILE)		;
	}

	return 1			;
}
#==================================================
#シグナル対処関数
#==================================================
sub SigExit
{
	exit(0);
}
#==================================================
#　初期情報を取得（ＰＯＳＴ）
#==================================================
sub foxReadForm
{
	my ($GB) = @_;
	my $FORM = $GB->{FORM};

	# UTF-8 -> Shift JIS -- for POST by XMLHttpRequest
	use Jcode;
	my $jcode = $#ARGV >= 0 && $ARGV[0] eq 'UTF-8' ? new Jcode : undef;

	# to avoid "Use of uninitialized value" warnings (except key)
	$FORM->{$_} = '' foreach (qw/subject FROM mail bbs time MESSAGE submit/);

	#環境変数からＰＯＳＴのでーたをもらう～
	if(!$GB->{TBACK} && $ENV{REQUEST_METHOD} eq 'POST')	#TBACK 時は読まない
	{
		use Fcntl qw(F_GETFL F_SETFL O_NONBLOCK);
		local $/;
		$ENV{CONTENT_LENGTH} > 65535
			and &DispError2($GB,'ＥＲＲＯＲ！','ＥＲＲＯＲ：文長杉！');

		# POST データ送信に時間をかける DoS 攻撃に対し robust に
		my ($timeout, $len, $fdset, $stdin, $ptime) = (8, $ENV{CONTENT_LENGTH}, '', '', time);
		vec($fdset, fileno STDIN, 1) = 1;
		fcntl(STDIN, F_SETFL, O_NONBLOCK | fcntl(STDIN, F_GETFL, 0));
		while ($len && $timeout > 0) {
			my ($l, $s, $t);
			select($fdset, undef, undef, $timeout)
				# sysread() の方がいいけど SpeedyCGI だとダメ
				and $l = read(STDIN, $s, $len)
				or last;
			$len -= $l;
			$stdin .= $s;
			$timeout -= ($t = time) - $ptime;
			$ptime = $t;
		}
		# DoS と思われる場合はとりあえず記録
		if (!vec($fdset, fileno STDIN, 1) && open(local *F, '>>', "/var/tmp/dos.post.$ENV{SERVER_NAME}")) {
			local $\ = "\n";
			print F strftime('[%F %T] ', localtime $ptime), $ENV{REMOTE_ADDR},
				' <> ', map "$_=$ENV{$_}, ", grep /^HTTP_/, keys %ENV;
			close F;
			&DispError2($GB,'ＥＲＲＯＲ！','ＥＲＲＯＲ：内容が無いよう！');
		}

		foreach (split(/&/, $stdin)) {
			(my $name, $_) = split(/=/, $_, 2);
			next unless (defined $_);
			$_ = $jcode->set(\$_, 'utf8')->sjis if (ref $jcode);
			tr/+/ /;
			s/%([[:xdigit:]]{2})/pack('H2', $1)/eg;
			# トリップキーは "as is" で
			if ($name eq 'FROM') {
				require "jcode.pl";
				&jcode::tr(\$_, '＃', '#');
				($_, $GB->{TRIPKEY}) = split(/#/, $_, 2);
			}
			# s/"/&quot;/g;
			s/</&lt;/g;
			s/>/&gt;/g;
			tr/\t/ /;
			s/\r\n?|\n/<br>/g;
			# 余計な空白追加を抑制......だが芋掘りに影響？
			# s/(?<=[\x80-\xFF])<br>/ <br>/g;
			s/<br>/ <br> /g;
			# \x00 ∈ [[:cntrl:]]
			s/[[:cntrl:]]//g;

			$FORM->{$name} = $_;
		}
	}

	#１行データからは改行を削ってタグを閉じます
	$FORM->{'subject'} =~ s/ ?<br> ?//g;
	$FORM->{'subject'} =~ s/&(?!(?:quo|[lg])t;)/&amp;/g;

	$FORM->{'FROM'} =~ s/ ?<br> ?//g;
	$FORM->{'mail'} =~ s/ ?<br> ?//g;
	$FORM->{'mail'} =~ s/"/&quot;/g;

	$FORM->{'bbs'} =~ s/\W//g;
	$FORM->{'key'} =~ s/\D//g if (defined $FORM->{'key'});
	$FORM->{'time'} =~ s/\D//g;

	$FORM->{'FROM'} =~ s/&r/&amp;r/g;
# BadTripCheck で殺しているので不要
#	$FORM->{'FROM'} =~ s/usubon//g;
	$FORM->{'mail'} =~ s/&r/&amp;r/g;

	# foxIkinariの処理と互換にする (セキュリティ上も本文の " は危険)
	# $FORM->{'MESSAGE'} =~ s/"/&quot;/g; <- foreach ループ内に統合

####cookie
{
	#// クッキー取得
	foreach (split(/[&,;]\s*/, $ENV{HTTP_COOKIE} || '')) {
		(my $key, $_) = split(/=/, $_, 2);
		$GB->{COOKIES}{$key} = $_ if (defined $_ && !exists $GB->{COOKIES}{$key});
	}
	$FORM->{'DMDM'} = $GB->{COOKIES}{DMDM} || '';
	$FORM->{'MDMD'} = $GB->{COOKIES}{MDMD} || '';

#&DispError2($GB,"FOX ★","<font color=green>FOX ★　ふふふっ</font><br><br>DMDM[$FORM->{'DMDM'}] ,MDMD[$FORM->{'MDMD'}]");
}
#でも　直接指定があったら上書き
if($FORM->{'BEmailad'} && $FORM->{'BEcode32'})
{
	$FORM->{'DMDM'} = $FORM->{'BEmailad'};
	$FORM->{'MDMD'} = $FORM->{'BEcode32'};
}
#####
#爆撃対策
if($ENV{HTTP_USER_AGENT} =~ /巫女/)
{
	$FORM->{'FROM'} = "fusianasan $FORM->{'FROM'}";
}
if($ENV{HTTP_USER_AGENT} =~ /Sirangana/)
{
	$FORM->{'FROM'} = "fusianasan $FORM->{'FROM'}";
}
if($ENV{HTTP_USER_AGENT} =~ /Mirage\.Core/)
{
	$FORM->{'FROM'} = "fusianasan $FORM->{'FROM'}";
}
if($ENV{HTTP_USER_AGENT} eq '')
{
	$FORM->{'FROM'} = "fusianasan $FORM->{'FROM'}";
}
if($ENV{HTTP_USER_AGENT} eq '.')
{
	$FORM->{'FROM'} = "fusianasan $FORM->{'FROM'}";
}
#####
}
#==================================================
#　エラー画面（エラー処理）
#==================================================
sub DispError2
{
	my ($GB, $title, $topic) = @_;

	if($GB->{TBACK} && $ENV{SERVER_NAME} !~ /qb6/){&TBackerrEnd;}	#TBACK は XML

	print "Content-type: text/html; charset=shift_jis\n\n";
	#-----------------------------------------------------------------------
print <<EOF;
<html>
<head>
<title>$title</title>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
</head>
<body bgcolor="#FFFFFF"><!-- 2ch_X:error -->
<font size=+1 color=#FF0000><b>$topic</b></font>
<ul>
<br>ホスト<b>$GB->{HOST}</B><br><b>$GB->{FORM}->{'subject'} </b><br>
名前： <b>$GB->{FORM}->{'FROM'}</b><br>E-mail： $GB->{FORM}->{'mail'}<br>
内容：<br>$GB->{FORM}->{'MESSAGE'}<br><br>
</ul>
<a href="http://ula.cc/2ch/sec2ch.html">★ アクセス規制中でも書ける板たち ★</a><br><br>
<hr>
こちらでリロードしてください。<a href="../$GB->{FORM}->{'bbs'}/index.html"> GO! </a><br>
アクセス規制・プロキシー制限等規制は、<a href="http://2ch.tora3.net/">２ちゃんねるビューア</a>
を使うと回避できます。<p>
自分で解決してみよう! <a href="http://www.2ch.net/help.html">書き込めない時の早見表\</a><br>
分からないことがあったら<a href="http://info.2ch.net/guide/">２ちゃんねるガイド</a>へ。。。<br><br>

<p>
</body>
</html>
EOF
#<font color=red>途中経過</font><br>
#$GB->{DEBUG}
#----------------------------------------<br>
#PATH =[$GB->{PATH}]<br>
#DATPATH =[$GB->{DATPATH}]<br>
#TEMPPATH =[$GB->{TEMPPATH}]<br>
#IMODEPATH =[$GB->{IMODEPATH}]<br>
#INDEXFILE =[$GB->{INDEXFILE}]<br>
#SUBFILE =[$GB->{SUBFILE}]<br>
#----------------------------------------<br>
#PID=$GB->{PID}<br>
#time=$GB->{NOWTIME}<br>
#$GB->{version}#sid=$GB->{FORM}->{sid}<br>
#maru=$GB->{MARU}<br>

	#-----------------------------------------------------------------------
	exit;
}
#==================================================
#　携帯用規約表示&エラー画面（エラー処理）
#==================================================
sub DispError3
{
	my ($GB, $title, $topic) = @_;

	if (defined $GB->{TRIPKEY}) {
		$_ = $GB->{TRIPKEY};
		s/&/&amp;/g;
		s/</&lt;/g;
		s/>/&gt;/g;
		s/[[:cntrl:]]/'&#' . ord($&) . ';'/eg;
		$GB->{FORM}{FROM} .= "#$_";
	}
	$GB->{FORM}{FROM} =~ s/"/&quot;/g;
	print "Content-type: text/html; charset=shift_jis\n\n";
	#-----------------------------------------------------------------------
print <<EOF;
<html>
<head>
<title>$title</title>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
</head>
<body bgcolor=white><!-- 2ch_X:error -->
<a href="http://2ch.net/">２ちゃんねる</a><br>
<font color=red>$topic</font><br>
<hr>
<font color=red>投稿確認</font><br>
・投稿者は、投稿に関して発生する責任が全て投稿者に帰すことを承諾します。<br>
・投稿者は、話題と無関係な広告の投稿に関して、相応の費用を支払うことを承諾します<br>
・投稿者は、投稿された内容及びこれに含まれる知的財産権、（著作権法第21条ないし第28条に規定される権利も含む） その他の権利につき（第三者に対して再許諾する権利を含みます。）、掲示板運営者に対し、無償で譲渡することを 承諾します。ただし、投稿が別に定める削除ガイドラインに該当する場合、投稿に関する知的財産権その他の権利、 義務は一定期間投稿者に留保されます。<br>
・掲示板運営者は、投稿者に対して日本国内外において無償で非独占的に複製、公衆送信、 頒布及び翻訳する権利を投稿者に許諾します。また、投稿者は掲示板運営者が指定する第三者に対して、一切の権利（第三者に対して再許諾する権利を含みます）を許諾しないことを承諾します。<br>
・投稿者は、掲示板運営者あるいはその指定する者に対して、著作者人格権を一切行使しないことを承諾します。<br>
<hr>
同意した時だけ、戻って再投稿してください。(仮)<br><hr>
開発中↓<br>
<input type=checkbox >同意する<br>
名前：<input type=text size=15 name="FROM" value="$GB->{FORM}->{'FROM'}"><br>
E-ma：<input type=text size=15 name="mail" value="$GB->{FORM}->{'mail'}"><br>
<textarea name="MESSAGE" rows=5>
$GB->{FORM}->{'MESSAGE'}
</textarea>
</body>
</html>
EOF
#<font color=red>途中経過</font><br>
#$GB->{DEBUG}
#----------------------------------------<br>
#PATH =[$GB->{PATH}]<br>
#DATPATH =[$GB->{DATPATH}]<br>
#TEMPPATH =[$GB->{TEMPPATH}]<br>
#IMODEPATH =[$GB->{IMODEPATH}]<br>
#INDEXFILE =[$GB->{INDEXFILE}]<br>
#SUBFILE =[$GB->{SUBFILE}]<br>
#----------------------------------------<br>
#PID=$GB->{PID}<br>
#time=$GB->{NOWTIME}<br>
#$GB->{version}#sid=$GB->{FORM}->{sid}<br>
#maru=$GB->{MARU}<br>

	#-----------------------------------------------------------------------
	exit;
}
#############################################################################
# 投稿確認画面をチェックする呪文を唱えているかどうか調べる
# この呪文は namazuplus で使用している
# 引数: $GB
# 戻り値: 0: 唱えていない(通常)、1: 唱えている
#############################################################################
sub KPinCheck
{
	my ($GB) = @_;

	# 「基本はすり足」の呪文を唱えている
	if(($GB->{FORM}->{$GB->{KPIN1}} || '') eq $GB->{KPIN2})	{return 1;}

	# それ以外
	return 0;
}
#############################################################################
# 「いきなり」チェックするルーチン
# 歴史的事情がたくさんあるようなので、更新時には注意すること
#############################################################################
sub foxIkinari
{
	my ($GB) = @_;

	if($ENV{PATH_INFO})	{return "127.0.0.101";}

	# 最近の素のIE8はUAがとても長いので、256ではきつすぎ
	if(length($ENV{'HTTP_USER_AGENT'}) > 384)
	{
		print "Content-type: text/html; charset=shift_jis\n\n";
print <<EOF;
<html><head><title>書きこみました。</title><meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS"></head><body>書きこみが終わりました。<br><br>画面を切り替えるまでしばらくお待ち下さい。<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}</body></html>
EOF
		exit;
	}
	if($ENV{'HTTP_USER_AGENT'} =~ />>/)
	{
		print "Content-type: text/html; charset=shift_jis\n\n";
print <<EOF;
<html><head><title>書きこみました。</title><meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS"></head><body>書きこみが終わりました。<br><br>画面を切り替えるまでしばらくお待ち下さい。<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}</body></html>
EOF
		exit;
	}

	my $HOST = gethostbyaddr(pack('C4',split(/\./, $ENV{'REMOTE_ADDR'})), 2) || $ENV{'REMOTE_ADDR'};

	if($ENV{'HTTP_VIA'} || $ENV{'HTTP_X_FORWARDED_FOR'} || $ENV{'HTTP_FORWARDED'})
	{
		unless($HOST =~/jp$/ || $HOST =~/edu$/)
		{
			print "Content-type: text/html; charset=shift_jis\n\n";
print <<EOF;
<html><head><title>書きこみました。</title><meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS"></head><body>書きこみが終わりました。<br><br>画面を切り替えるまでしばらくお待ち下さい。</body></html>
EOF

			exit;
		}
	}

	# 携帯からの書き込みはスルー
	# まだこの時点ではIsIP4Mobileは使えない
	# もともとこうなっていたわけだけど、UAではやりたくないなぁ

	# こいつらはリファラもクッキーも正しく扱えないことにしている
	if($ENV{'HTTP_USER_AGENT'} =~ /DoCoMo|J-PHONE|Vodafone|SoftBank|UP.Browser|KDDI/)	{
		return $HOST;
	}

	# 味ぽん4機種はリファラは吐かないけど、クッキーは食べる
	if($ENV{'HTTP_USER_AGENT'} !~ /AH-J3001V|AH-J3002V|AH-J3003S|WX220J/)
	{
		# リファラチェック(いきなり)
		#if($ENV{'HTTP_REFERER'} !~ /^http:\/\/$ENV{'HTTP_HOST'}\//)
		if($ENV{'HTTP_REFERER'} !~ m#^http://(?:[-\w]+\.)?(?:2ch\.net|bbspink\.com|ula\.cc|u\.la|s2ch\.net|orz\.2ch\.io)/#)
		{
			print "Content-type: text/html; charset=shift_jis\n\n";
			print <<EOF;
<html><head><title>ＥＲＲＯＲ！</title><meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS"></head><body>ＥＲＲＯＲ：referer情報が変です。(ref1)$ENV{'HTTP_REFERER'}</body></html>
EOF
			exit;
		}
	}

	my $hap = time	;
	$hap /= 60	;
	$hap /= 60	;
	$hap /= 24	;
	$hap = int($hap)	;

	$hap += (($hap % 12000) * 1000)	;

	# PON と HAP を保持しておく
	$GB->{PON}  = $HOST;
	$GB->{PONX} = "PON=$HOST";
	$GB->{HAP}  = $hap;
	$GB->{HAPX} = "HAP=$hap";

	# PON がなければ、とりあえず再発行する
	if(($GB->{COOKIES}{PON} || '') ne $GB->{PON})
	{
		# PON を発行する(次回に有効になる)
		print "Set-Cookie: $GB->{PONX}; expires=$FOX->{COOKIEEXPIRES}; path=/\n";
	}
	else
	{
		# PON を持っていた
		$GB->{PONOK} = 1;
	}

	# Mozilla/4.0 ではない場合、HAP は有効期限内とみなす
	# (そうなっていた)
	if($ENV{'HTTP_USER_AGENT'} !~ /Mozilla\/4\.0/)
	{
		$GB->{HAPOK} = 1;
	}

	# HAP がない場合 or 変わっていたら再発行する
	if(($GB->{COOKIES}{HAP} || '') ne $GB->{HAP})
	{
		# 新しい HAP を発行する(次回に有効になる)
		print "Set-Cookie: $GB->{HAPX}; expires=$FOX->{COOKIEEXPIRES}; path=/\n";
	}
	else
	{
		# HAP は有効期限内だった(前の HAP と一致した)
		$GB->{HAPOK} = 1;
	}

	# 法的な投稿確認画面の表示 & exit;
	&HoutekiToukouKakunin($GB);

	# 特殊ケース(なぜそうしているかはよくわからないけど)
	if($GB->{FORM}->{'bbs'} =~ /style\=/){exit;}

	return $HOST;
}
#############################################################################
# 法的な投稿確認画面の表示
#############################################################################
sub HoutekiToukouKakunin
{
	my ($GB) = @_;

	# スキップの呪文を唱えている場合はスルー
	if($GB->{KPASS})	{return 0;}

	# 新規スレッド作成画面(BBS_PASSWORD_CHECK)の際の対策
	#   foxReadSettings の前なので、SETTING.TXT の内容は
	#   まだここでは参照できない
	# スレタイがなくて、
	if(!($GB->{FORM}->{'subject'} ne ""))
	{
		# かつ、キー情報が定義されていない場合には、
		if(!defined($GB->{FORM}->{'key'}))
		{
			# ここは素通りさせ、foxSetInformation でチェックする
			# これで &newbbs が呼ばれる or
			# 「サブジェクトが存在しません」エラーになることになる
			return 0;
		}
	}

	# はなもげら Cookie が有効かどうか
	my $isvalidPIN = ($GB->{COOKIES}{$GB->{PIN1}} || '') eq $GB->{PIN2};

	# PON と HAP が有効じゃないとだめ(必須)
	if($GB->{PONOK} && $GB->{HAPOK})
	{
		# はなもげらの呪文を唱えている
		if(($GB->{FORM}{$GB->{PIN1}} || '') eq $GB->{PIN2})	{return 0;}
		# はなもげらクッキーを持っている(期限時間内に投稿したことがある)
		if($isvalidPIN)	{return 0;}
	}

	# フォームの時間をセットする(表示部分で使用している)
	$GB->{FORM}->{'time'} = time;

	# <br> とかが出ないように、一時的に foxReadForm で加工したやつを戻す
	my %form;
	foreach (qw/subject FROM mail MESSAGE/) {
		$form{$_} = $GB->{FORM}{$_};
		$form{$_} =~ s/&(?!(?:quo|[lg])t;)/&amp;/g if ($_ ne 'subject');
		$form{$_} =~ s/"/&quot;/g;
	}
	if (defined $GB->{TRIPKEY}) {
		$_ = $GB->{TRIPKEY};
		s/&/&amp;/g;
		s/</&lt;/g;
		s/>/&gt;/g;
		s/[[:cntrl:]]/'&#' . ord($&) . ';'/eg;
		$GB->{FORM}{FROM} .= "#$_";
		s/"/&quot;/g;
		$form{FROM} .= "#$_";
	}
	$form{MESSAGE} =~ s/ ?<br> ?/&#10;/g;

	# ヘッダを表示して、、、
	print "Content-type: text/html; charset=shift_jis\n\n";

	# 投稿確認画面を表示する
	my @kakuningamen0 = (
	qq|<html><!-- 2ch_X:cookie -->|,
	qq|<head>|
	);
	&PutLines(*STDOUT, @kakuningamen0);

	# ウイルス爆撃(DoS)対応(comic6だけタイトルを変えてみる)
	my $kakunintitle = qq|<title>■ 書き込み確認 ■</title>|;
	if($ENV{SERVER_NAME} =~ /comic6/)
	{
		$kakunintitle = qq|<title>■ 書き込みの確認 ■</title>|;
	}
	&Put1Line(*STDOUT, $kakunintitle);

	my $submitButton = $isvalidPIN ? '確認して書き込む' : '上記全てを承諾して書き込む';

	my @kakuningamen = (
	qq|<META http-equiv="Content-Type" content="text/html; charset=x-sjis">|,
	qq|<meta name="viewport" content="width=device-width,initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.6,user-scalable=yes" />|,
	qq|</head>|,

	qq|<body bgcolor=#EEEEEE>|,
	qq|<font size=+1 color=#FF0000><b>書きこみ＆クッキー確認</b></font>|,
	qq|<ul><br><br>|,
	qq|<b>$GB->{FORM}->{'subject'} </b><br>|,
	qq|名前： $GB->{FORM}->{'FROM'}<br>|,
	qq|E-mail： $GB->{FORM}->{'mail'}<br>|,
	qq|内容：<br>$GB->{FORM}->{'MESSAGE'}<br><br></ul>|,
	# この文面ははなもげら Cookie がない時だけ出す
	!$isvalidPIN ? (
		qq|<b>|,
		qq|投稿確認<br>|,
		qq|・投稿者は、投稿に関して発生する責任が全て投稿者に帰すことを承諾します。<br>|,
		qq|・投稿者は、話題と無関係な広告の投稿に関して、相応の費用を支払うことを承諾します<br>|,
		qq|・投稿者は、投稿された内容及びこれに含まれる知的財産権、（著作権法第21条ないし第28条に規定される権利も含む）|,
		qq|その他の権利につき（第三者に対して再許諾する権利を含みます。）、掲示板運営者に対し、無償で譲渡することを|,
		qq|承諾します。ただし、投稿が別に定める削除ガイドラインに該当する場合、投稿に関する知的財産権その他の権利、|,
		qq|義務は一定期間投稿者に留保されます。<br>|,
		qq|・掲示板運営者は、投稿者に対して日本国内外において無償で非独占的に複製、公衆送信、|,
		qq#頒布及び翻訳する権利を投稿者に許諾します。また、投稿者は掲示板運営者が指定する第三者に対して、一切の権利（第三者に対して再許諾する権利を含みます）を許諾しないことを承諾します。<br>#,
		qq|・投稿者は、掲示板運営者あるいはその指定する者に対して、著作者人格権を一切行使しないことを承諾します。<br>|,
		qq|<br>|,
		qq|</b>|
	) : (),
	# "<pre>Cookie:\n", join("\n", map("$_=$GB->{COOKIES}{$_}", keys %{$GB->{COOKIES}})), "\n</pre>",
	qq|<form method=POST action="../test/bbs.cgi?guid=ON">|,
	qq|<input type=hidden name=subject value="$form{subject}">|,
	qq|<input TYPE=hidden NAME=FROM value="$form{FROM}">|,
	qq|<input TYPE=hidden NAME=mail value="$form{mail}">|,
	qq|<input type=hidden name=MESSAGE value="$form{MESSAGE}">|,
	qq|<input type=hidden name=bbs value=$GB->{FORM}->{'bbs'}>|,
	qq|<input type=hidden name=time value=$GB->{FORM}->{'time'}>|,
	defined $GB->{FORM}{key} ? qq|<input type=hidden name=key value=$GB->{FORM}{key}>| : qq||,
	!$isvalidPIN ? qq|<input type=hidden name="$GB->{PIN1}" value="$GB->{PIN2}">| : qq||,
	qq|<br>|,
	qq|<input type=submit value="$submitButton" name="submit"><br>|,
	qq|</form>|,
	qq|変更する場合は|, $#ARGV >= 0 && $ARGV[0] eq 'UTF-8' ? qq|キャンセルして| : qq|戻るボタンで戻って|, qq|書き直して下さい。<br><br>|,
	qq|現在、荒らし対策でクッキーを設定していないと書きこみできないようにしています。<br>|,
	qq|<font size=-1>(cookieを設定するとこの画面はでなくなります。)</font><br>|,
	qq|</body>|,
	qq|</html>|,
	#qq|<!-- $ENV{'HTTP_COOKIE'} ++ SPID=$CSPID -->|
	);
	&PutLines(*STDOUT, @kakuningamen);

	# 画面出したら exit してしまう
	exit;

	# return はしないけど、一応
	return 0;
}
#############################################################################
#	BBY/BBS/BBR
#############################################################################
sub foxDNSquery
{
	my ($host, $nameserver) = @_	;
#	$host .= "bbs.timeout.peko.2ch.net.";

	use Net::DNS;
	my $res = Net::DNS::Resolver->new(recurse => 0,
					  nameservers => [$nameserver]); 
	$res->bgsend($host)	; 

	return 1		;
}
#############################################################################
#	BBQ/BBM/BBX/BBN/BBE
#############################################################################
sub foxDNSquery2
{
	my ($host) = @_	;
#	$host .= "bbs.timeout.peko.2ch.net.";

	use Net::DNS;
	my $res = Net::DNS::Resolver->new;
	$res->tcp_timeout(3);
	$res->udp_timeout(3);
	$res->retry(4);
 	my $query = $res->query($host)	;

	if($query)
	{
		my @ans = $query->answer;
		foreach(@ans)
		{
			return $_->address	;
		}
	}
	if($res->errorstring  eq 'query timed out') {return "127.0.0.0";}

	return "127.0.0.1";
}
##########################################################################
# IPアドレスから該当するリモートホスト名を得る
# 逆引きがなければIPアドレスをそのまま返す
# IPv4/IPv6共通で使えるはず
#
# 引数: IPアドレス文字列(REMOTE_ADDRとかそういうの)
# 戻り値: リモートホスト名(逆引きが存在しない場合はIPアドレス)
##########################################################################
sub GetRemoteHostName
{
	my ($ipaddr) = @_;

	use Net::IP;
	use Net::DNS;

	# ホスト名を入れる変数
	my $hostname = undef;

	my $ip = new Net::IP($ipaddr);
	my $res = Net::DNS::Resolver->new;

	# 逆引きに使える形にする
	my $rev = $ip->reverse_ip();

	$res->tcp_timeout(2);
	$res->udp_timeout(2);
	$res->retry(3);

	# PTRレコードを検索する
	my $ans = $res->search($rev, 'PTR');

	if ($ans)
	{
		foreach my $rr ($ans->answer)
		{
			if ($rr->type eq 'PTR')
			{
				$hostname = $rr->ptrdname;
				last;
			}
		}
	}

	if ($hostname eq undef)
	{
		$hostname = $ipaddr;
	}

	return $hostname;
}
#############################################################################
# 初期情報の設定
# 各種PATH生成
#############################################################################
sub foxSetPath
{
	my ($GB) = @_	;

	$GB->{PATH} = "../$GB->{FORM}{bbs}/";
	# 雪だるまサーバだけワークエリアを別にとる
	if(IsSnowmanServer == BBSD->{REMOTE})
	{
		# ユーザ名をgetpwuidでとってくる
		my $name = getpwuid($>);
		$GB->{WPATH} = "/md/$name/$GB->{FORM}{bbs}/";
	}
	else
	{
		$GB->{WPATH} = $GB->{PATH};
	}
	$GB->{DATPATH} = "$GB->{PATH}dat/";
	$GB->{LOGPATH} = "../../test/ggg/$GB->{FORM}{bbs}dat/";
	$GB->{TEMPPATH} = "$GB->{PATH}html/";
	$GB->{IMODEPATH} = "$GB->{PATH}i/";
	$GB->{INDEXFILE} = "$GB->{PATH}index.html";
	$GB->{SUBFILE} = "$GB->{PATH}subback.html";

	# 雪だるまサーバでは芋のディレクトリを作らない
	if(IsSnowmanServer != BBSD->{REMOTE})
	{
		my $ggg = "../../test/ggg/";
		unless(-e $ggg){
			# 最初にumask(0)しているので不要
			#umask(0);
			mkdir($ggg,0777);
		}
	}

$GB->{DEBUG} .= "各種ＰＡＴＨ生成 PATH=$GB->{PATH}<br>";
}

=begin comment

bbsd 関連の処理は BBSD.pm に一任のためコメントアウト
#############################################################################
# 書き込み・IDの種処理用のbbsdを呼び出す
#############################################################################
sub bbsd
{
#	my (@Argv) = @_;

#	return &bbsd_main(0, @Argv);
	return &bbsd_main(0, @_);
}
#############################################################################
# DB処理用のbbsdを呼び出す
#############################################################################
sub bbsd_db
{
#	my (@Argv) = @_;

#	return &bbsd_main(1, @Argv);
	return &bbsd_main(1, @_);
}
#############################################################################
# bbsdとの間の通信を行う
# フラグ: 0: 書き込み・IDの種の処理、1: DB処理
#############################################################################
sub bbsd_main
{
#	my ($flag, @Argv) = @_;
	my $flag = shift;

	use Socket;

	# 問い合わせ先IPアドレス、ポート番号、タイムアウト値
	my $BBSD_HOST    = undef;
	my $BBSD_PORT    = undef;
	my $BBSD_TIMEOUT = undef;

	# フラグにより呼ぶホストのパラメータを変更する
	if (!$flag)
	{
		$BBSD_HOST    = inet_aton($FOX->{SNOWMAN}->{BBSD}->{HOST});
		$BBSD_PORT    = $FOX->{SNOWMAN}->{BBSD}->{PORT};
		$BBSD_TIMEOUT = $FOX->{SNOWMAN}->{BBSD}->{TIMEOUT};
	}
	else
	{
		$BBSD_HOST    = inet_aton($FOX->{SNOWMAN}->{DB}->{HOST});
		$BBSD_PORT    = $FOX->{SNOWMAN}->{DB}->{PORT};
		$BBSD_TIMEOUT = $FOX->{SNOWMAN}->{DB}->{TIMEOUT};
	}

	my ($rfd, $str) = ('', '');
	my $sin = sockaddr_in($BBSD_PORT, $BBSD_HOST);
	socket(SOCK, AF_INET, SOCK_DGRAM, 0) || return "$!";
#	send(SOCK, join("\x8", @Argv), 0, $sin) || (close(SOCK), return "$!");
	send(SOCK, join("\x8", @_), 0, $sin) || (close(SOCK), return "$!");
	vec($rfd, fileno(SOCK), 1) = 1;
	if (select($rfd, undef, undef, $BBSD_TIMEOUT))
	{
		recv(SOCK, $str, 16384, 0) || (close(SOCK), return "$!");
	}
	else
	{
		$str = $FOX->{SNOWMAN}->{TIMEOUTMSG};
	}
	close(SOCK);
	return $str;
}

=end comment

=cut

#############################################################################
# bbsdのタイムアウトかどうかチェック
# 入力: $GB, bbsdの戻り値
#############################################################################
sub bbsd_TimeoutCheck
{
	my ($GB, $errmsg) = @_;

	if($errmsg eq (local $! = ETIMEDOUT))
	{
		return 1;
	}

	# それ以外は戻り
	return 0;
}
#############################################################################
# bbsdのタイムアウトエラーの処理
# 入力: $GB, メッセージに出力するためのコマンド名
#############################################################################
sub bbsd_TimeoutError
{
	my ($GB, $cmd) = @_;

	&DispError2($GB, 'ＥＲＲＯＲ！', "ＥＲＲＯＲ：バックエンドサーバとの通信がタイムアウトしました($cmd)。書き込みが反映されていないかもしれません。");

	# ここから戻ることはない(が、一応)
	return 0;
}
#############################################################################
# 指定したファイルハンドルに1行出力する
# 使い方: &Put1Line(*FILE, $str);
#############################################################################
sub Put1Line
{
	local (*FD) = shift;

	print FD @_;

	return 0;
}
#############################################################################
# 指定したファイルハンドルに複数行出力する
# 使い方: &PutLines(*FILE, @str);
#############################################################################
sub PutLines
{
	local (*FD) = shift;

	print FD @_;

	return 0;
}
#############################################################################
# end of bbs.entry.cgi
#############################################################################
1;
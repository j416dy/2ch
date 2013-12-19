use strict 'vars';
use File::stat;
use POSIX qw(:errno_h strftime);
use BBSD;

#########################################################
sub bbs_entry
{
	use vars qw($BBSCGI)		;	#�O���[�o���[
	$BBSCGI = '2010/10/28'		;	#�ŏI�X�V��

	use vars qw($FOX)		;	#�O���[�o���[
	use vars qw(@FOX_K998)		;	#�O���[�o���[ �Kc�����X�g(��)
	use vars qw(@FOX_K999)		;	#�O���[�o���[ �K�����X�g(ISP)
	use vars qw(@FOX_Ro54)		;	#�O���[�o���[ �K�����X�g(Rock54)
	use vars qw(@FOX_KABUU)		;	#�O���[�o���[ ���ʊ���D�Җ������X�g
	use vars qw(@FOX_774)		;	#�O���[�o���[ ���������X�g(vip)

						#�������b�N�A�b�v
	use vars qw(%FOX_KEN_ASAHI)	;	#�O���[�o���[ asahi-net
	use vars qw(%FOX_KEN_DION)	;	#�O���[�o���[ dion

	# �ŏ���umask(0)��錾���Ă���(�Ō�܂ŗL��)
	umask(0);

	unless(defined($FOX))
	{
#		$FOX = 20	;
		$FOX = {}	;
		@FOX_K998 = ()	;
		@FOX_K999 = ()	;
		@FOX_Ro54 = ()	;
		&initFOX	;		#�L���֌W�͍ŏ��Ɉ��ǂݍ���ŁA
		srand(time)	;		#����

		@FOX_KABUU = ()	;
		&readKABUU()	;
	}
	&bbs_entryXXX			;
}
#############################################################################
#����?
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
# IPv6�ڑ����ǂ������`�F�b�N����
# �͂��߂̂ق��Ŏg���̂ŁAbbs-entry.cgi �ɓ���邱�Ƃɂ���
# $GB�̏��������ɌĂ΂��
# �����͂Ȃ�
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
	my $span  = 180			;	#�K���b��

$tane =~ s/\./-/g;
$tane =~ s/\//~/g;
	my $sFile = "$FOX->{BOOK}/book/$tane.cgi";
	my $remo = $GB->{HOST29}	;	#�����郊���z
	my $ipip = $ENV{REMOTE_ADDR}	;

	my $isViva			;

	# �g�т͂���[
	if($GB->{KEITAI})	{return 0;}

	# �Ⴞ��܂ł́A�ǂ��킩��Ȃ��̂ō��̂Ƃ���Ȃ��A���̌������낵��
	# �@�@�� �������܂���
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

#$GB->{FORM}->{'MESSAGE'} .= "<hr>���ڈȍ~�A�@��=$ipip ";

			if(open(SMB,"$sFile"))
			{
				my @mdx = <SMB>	;
				close(SMB)	;
#$GB->{FORM}->{'MESSAGE'} .= "�O=$mdx[0] $keika sec�o��<br>";
				if($ipip ne $mdx[0] && $keika < $span)	{$isViva = 1;}
			}
		}
		if(!$isViva && open(LOG,"> $sFile"))	{print LOG "$ipip";close(LOG)	;}
	}

	if($isViva)
	{
		print "Content-type: text/html; charset=shift_jis\n\n";
		print <<EOF;
<html><head><title>�d�q�q�n�q�I</title><meta http-equiv="Content-Type" content="text/html; charset=shift_jis"></head>
<body><!-- 2ch_X:error -->
�d�q�q�n�q - Viva Samba �J�[�j�o�� !<br>
<br>
�Ƃ������Ƃ��B<br><br>
<br><hr><font color=green>FOX ��</font></body>
</html>
EOF
		exit;
	}

	return 0;
}
#################################################################################################
#	�g���b�N�o�b�N��M
#################################################################################################
sub foxTrackBackIn
{
	my ($GB) = @_				;

	if(!$ENV{PATH_INFO})		{return 0;}	#PATH_INFO���Ȃ���TBACK����Ȃ�
	if($ENV{REQUEST_METHOD} ne 'POST') {return 0;}	#POST�̂ݎ󂯓���

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
	if($who eq '')		{&TBackEnd("���M���s��");}
	if($mac ne "18")	{&TBackEnd("���݂���");}
	$ENV{'REMOTE_ADDR'} = $raddr		;
	$ENV{'HTTP_USER_AGENT'} = $cgi->param('ua');
	$GB->{FORM}->{sid} = $cgi->param('mm');
}
	my ($d0,$bbs,$key,$d3) = split(/\//,$ENV{PATH_INFO})	;
	if($bbs eq '')			{&TBackEnd("���Ȃ�");}
	if($bbs =~ /\W/)		{&TBackEnd("������");}
	if($bbs eq 'sec2ch')		{&TBackEnd("���̔͎󂯕t���Ȃ�");}
	if($bbs eq 'saku')		{&TBackEnd("���̔͎󂯕t���Ȃ�");}
	if($bbs eq 'saku2ch')		{&TBackEnd("���̔͎󂯕t���Ȃ�");}
	if($bbs eq 'news4vip')		{&TBackEnd("���̔͎󂯕t���Ȃ�");}
	if($bbs eq 'maru')		{&TBackEnd("���̔͎󂯕t���Ȃ�");}
	if($key eq '')			{&TBackEnd("key�Ȃ�");}
	if($key =~ /\D/)		{&TBackEnd("key����");}
	# 924 �̓g���b�N�o�b�N��M����(�ɂ��Ȃ��Ă��Ƃ肠���������ł͖��Ȃ�)
	#if($key =~ /^924/)		{&TBackEnd("key����");}

	my $url = $cgi->param('url')	;
	#$url =~ tr/+/ /		;
	$url =~ tr/\t/ /		;
	$url =~ s/\r\n?|\n/<br>/g	;
	# \x00 �� [[:cntrl:]]
	$url =~ s/[[:cntrl:]]//g	;
	if($url eq '')			{&TBackgoThre("http://$ENV{SERVER_NAME}/test/read.cgi/$bbs/$key/l50");}
	if($url !~ /^http\:\/\//)	{&TBackgoThre("http://$ENV{SERVER_NAME}/test/read.cgi/$bbs/$key/l50");}
	if($url =~ /\|| /)		{&TBackgoThre("http://$ENV{SERVER_NAME}/test/read.cgi/$bbs/$key/l50");}
	if($url =~ /<|>/)		{&TBackgoThre("http://$ENV{SERVER_NAME}/test/read.cgi/$bbs/$key/l50");}
	if($url =~ /�@/)		{&TBackgoThre("http://$ENV{SERVER_NAME}/test/read.cgi/$bbs/$key/l50");}

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
	# \r ���J�b�g����K�v�����邱�Ƃɒ���
	foreach ($ttl, $bnm, $exc) {
		# s/"/&quot;/g;
		s/</&lt;/g;
		s/>/&gt;/g;
		tr/\t/ /;
		# [\x00\n\r] �� [[:cntrl:]]
		s/[[:cntrl:]]//g;
	}
	$exc =~ s/&lt;br&gt;/<br>/g;

	my $tb = "�y�g���b�N�o�b�N������z (ver. $ver) <br>"		;
	if($ttl)	{$tb .= "[�^�C�g��] $ttl <br>";}
	if($bnm)	{$tb .= "[���u���O] $bnm <br>";}
	$tb .= "$url<br>"			;
#	if($refer)	{$tb .= "( ref= $refer ) <br><br>";}
	if($exc)	{$tb .= "[���v��]<br>$exc <br><br> ";}


	$GB->{FORM}->{'FROM'}		= "TBACK ��"	;
	$GB->{FORM}->{'mail'}		= "sage"	;
	$GB->{FORM}->{'MESSAGE'}	= $tb		;
	$GB->{FORM}->{'subject'}	= ""		;
	$GB->{FORM}->{'time'}		= $GB->{NOWTIME} - 100;
	$GB->{FORM}->{'bbs'}		= $bbs		;
	$GB->{FORM}->{'key'}		= $key		;

	$GB->{TBACK} = 1		;	# 1=TrackBack 0=�ʏ폈��
	$GB->{CAP} = 1			;	# �g���b�N�o�b�N�����O�̍Ōオ��

#&DispError2($GB,"FOX ��","<font color=green>FOX ��</font>TBACK(201)<br><br>r=$raddr<br>r=$refer<br>");

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
<title>�g���b�N�o�b�N@�Q�����˂�</title>
<META content=10;URL="$ttt" http-equiv=refresh>
</HEAD>
<BODY>
������
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
#	�g���b�N�o�b�N���M
#################################################################################################
sub foxTrackBack
{
	my ($GB) = @_			;

	# 924 �̓g���b�N�o�b�N���M����(�ɂ͂Ƃ肠�������Ȃ��ł�����)
	#if($GB->{FORM}->{'key'} =~ /^924/)	{return 0;}

	if($GB->{TBACK})			{return 0;}
	if($GB->{FORM}->{bbs} eq 'news4vip')	{return 0;}


	if($GB->{FORM}->{'MESSAGE'} !~ /�g���b�N�o�b�N:http\:\/\/([\w|\:\!\#\$\%\=\&\-\^\`\\\|\@\~\[\{\]\}\;\+\*\,\.\?\/]+)/)	{return 0;}
	my $target = "http://$1"	;
if($target =~ /\.2ch\.net|\.bbspink\.com|\.kakiko\.com/)
	{$target =~ s/read\.cgi/bbs\.cgi/;}
	my $url = "http://$ENV{SERVER_NAME}/test/read.cgi/$GB->{FORM}->{bbs}/$GB->{FORM}->{'key'}/l50"	;

	if($target =~ /$GB->{FORM}->{bbs}/ && $target =~ /$GB->{FORM}->{'key'}/)
	{&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F����X���b�h�ɂ̓g���b�N�o�b�N�ł��܂���B");}

	my $dattemp = "";
	my $firstlog = "";
	if(IsSnowmanServer == BBSD->{REMOTE})
	{
		# �Ⴞ��܂ł́AHTTP�o�R�œ��肷��
		use LWP::UserAgent;

		my $ua = LWP::UserAgent->new(agent => 'bbs.cgi', timeout => 3, max_redirect => 0);
		my $res = $ua->get("http://127.0.0.1/$GB->{FORM}{bbs}/dat/$GB->{FORM}{key}.dat", Host => $ENV{SERVER_NAME});
		if ($res->is_error)
		{
			&DispError2($GB, '�d�q�q�n�q�I', '�d�q�q�n�q�F>>1�̎擾�Ɏ��s���܂����B');
		}
		$firstlog = (split(/\n/, $res->content, 2))[0];
	}
	else
	{
		# �ʏ�T�[�o�ł́A����dat��ǂ�
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

	my $response_body = $response->content()		;#���ʂ͂����ɓ����Ă���
	my $response_code = $response->code()			;#���ʂ͂����ɓ����Ă���
	my $db_content = $response->content()			;

	# �G���[�`�F�b�N
	if ($response->is_error)
	{
		&DispError2($GB, "�d�q�q�n�q�I", "�d�q�q�n�q�F�g���b�N�o�b�N�̑��M�Ɏ��s���܂����B($response_code)");
	}

	# $db_content =~ s/"/&quot;/g;
	$db_content =~ s/</&lt;/g;
	$db_content =~ s/>/&gt;/g;
	$db_content =~ tr/\n//d;

	if($ENV{SERVER_NAME} !~ /qb6/)	{return 1;}

	$GB->{FORM}->{'MESSAGE'} .= "<hr><font color=orange>�g���b�N�o�b�N</font><br>";
	$GB->{FORM}->{'MESSAGE'} .= "target=$target<br>";
	$GB->{FORM}->{'MESSAGE'} .= "title=[$subject]<br>";
#	$GB->{FORM}->{'MESSAGE'} .= "excerpt=[$message]<br>";
	$GB->{FORM}->{'MESSAGE'} .= "URL=[ $url ]<br>";
	$GB->{FORM}->{'MESSAGE'} .= "blog_name=$FOX->{$GB->{FORM}->{bbs}}->{BBS_TITLE}<br>";
	$GB->{FORM}->{'MESSAGE'} .= "=====<br>[$db_content]";

	return 1;
}
#########################################################
# index.html/subback.html �����ڂ�T�[�o���ǂ���
# ���ڂ�: 1�A���ڂ�Ȃ�: 0
#########################################################
sub SaborinServer
{
	my ($GB) = @_			;

	if($GB->{BBSCGI_FUNCTIONS}{SABORIN})	{return 1;}

	# news21/news22: ���p
	#if($ENV{'SERVER_NAME'} =~ /news21/)	{return 1;}
	#if($ENV{'SERVER_NAME'} =~ /news22/)	{return 1;}

	# ex�n�A���͊��ɂȂ�
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

	# live�n
	#if($ENV{'SERVER_NAME'} =~ /live28/)	{return 1;}

	# live22/live23/live24�͂����Ŏw�肵�Ă��Ӗ��Ȃ�(�Ⴞ��܂�����)
	#if($ENV{'SERVER_NAME'} =~ /live22/)	{return 1;}
	#if($ENV{'SERVER_NAME'} =~ /live23/)	{return 1;}
	#if($ENV{'SERVER_NAME'} =~ /live24/)	{return 1;}

	# �ʂŎw�肷��ꍇ
	if($GB->{FORM}->{'bbs'} =~ /live/)	{return 1;}
	if($GB->{FORM}->{'bbs'} eq "weekly")	{return 1;}

	return 0	;
}
sub Saborin
{
	my ($GB) = @_			;

#$GB->{FORM}->{'MESSAGE'} .= "<hr>������($ENV{'SERVER_NAME'},$GB->{FORM}->{'bbs'},$GB->{NEWTHREAD},$GB->{PID})"	;
#	return 0			;

	# �V�X���̎��͍X�V�����ڂ�Ȃ�
	if($GB->{NEWTHREAD} ne 0)		{return 0;}

	# LA����l��1.2�{�ɒB���Ă�����A���̌�͍X�V�����ڂ�
	my $fact = 1.2			;# LA�`�F�b�N�̍ۂ̊�l�ɑ΂���{��
	# anime�T�[�o��1�{
	if($ENV{'SERVER_NAME'} =~ /anime/)	{ $fact = 1.0; }
	# news�n�T�[�o��1�{
	if($ENV{'SERVER_NAME'} =~ /news/)	{ $fact = 1.0; }
	# ex�n�T�[�o��1�{
	if($ENV{'SERVER_NAME'} =~ /ex/)		{ $fact = 1.0; }
	# live�n�T�[�o��1�{
	if($ENV{'SERVER_NAME'} =~ /live/)	{ $fact = 1.0; }

	# LA���������`�F�b�N
	if(&mumumuMaxLACheck($GB->{LOADAVG}, $fact))	{return 1;}

	# �B���Ă��Ȃ�������A�Y������T�[�o�ȊO�͍X�V�����ڂ�Ȃ�
	elsif(!&SaborinServer($GB))		{return 0;}

	# index.html �����݂��Ȃ��ꍇ�͂��ڂ�Ȃ�
	# ���݂���ꍇ�͎���ȍ~�`�F�b�N���Ȃ�
	if (!$FOX->{ISINDEXHTML}{$GB->{FORM}{bbs}}) {
		if (!-e "../$GB->{FORM}{bbs}/index.html") {return 0;}
		$FOX->{ISINDEXHTML}{$GB->{FORM}{bbs}} = 1;
	}

	# �Y������T�[�o�ł�PID��50�Ŋ����ė]�肪���鎞�A���̌�̍X�V�����ڂ�
	if($GB->{PID} % 50)			{return 1;}
	# mod_speedycgi��speedy_backend�ł�pid�������Ɠ����ɂȂ�\��������̂ŁA
	# rand()���g���悤�ɕύX(1999/2000�̊m��)
	# ���΂炭���̂�ŗl�q��
	#if(rand(2000) > 1)			{return 1;}

	# ��L�̂�����ɂ��Y�����Ȃ�(�X�V�����ڂ�Ȃ�)
	return 0			;
}
#######################################################################
# IsKoukoku���X�L�b�v����T�[�o���ǂ������`�F�b�N����
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
# IsKoukoku�����s���邩�ǂ������`�F�b�N����
#######################################################################
sub mumumuIsIsKoukoku
{
	my ($GB) = @_;

	# banana�T�[�o�ł͕K�����s
	if(&mumumuGetServerType() =~ /banana/)		{return 1;}
	# �Y������T�[�o�ł͎��s���Ȃ�
	if(&mumumuIsKoukokuSkipServer($GB, $ENV{SERVER_NAME})) {return 0;}
	# ����ȊO�͎��s
	return 1;
}
#######################################################################
# 1/100�b����舵��(�\������)���ǂ���
#######################################################################
sub IsCentiSec
{
	my ($GB) = @_;

	if($GB->{BBSCGI_FUNCTIONS}{CENTISEC})		{return 1;}

	# ���̂ւ�̃T�[�o�ł͕\��
	#if($ENV{'SERVER_NAME'} =~ /atlanta/)		{return 1;}
	#if($ENV{'SERVER_NAME'} =~ /live/)		{return 1;}
	if($ENV{'SERVER_NAME'} =~ /hayabusa/)		{return 1;}
	if($ENV{'SERVER_NAME'} =~ /snow/)		{return 1;}

	# ���̂ւ�̔ł͕\��
	if($GB->{FORM}->{'bbs'} eq "news")		{return 1;}
	if($GB->{FORM}->{'bbs'} eq "news4vip")		{return 1;}
	if($GB->{FORM}->{'bbs'} eq "news4viptasu")	{return 1;}
	if($GB->{FORM}->{'bbs'} eq "morningcoffee")	{return 1;}
	if($GB->{FORM}->{'bbs'} eq "asaloon")		{return 1;}
	if($GB->{FORM}->{'bbs'} eq "operate2")		{return 1;}

	return 0;
}
#######################################################################
# �ʃL���b�v���ǂ���
#######################################################################
sub IsItabetsuCap
{
	my ($GB) = @_;

	our %ItabetsuCapList;
	BEGIN {
		# �ʃL���b�v�̔��ς������A������ҏW����
		%ItabetsuCapList = map +($_ => 1), (
			# plus�n
			"bizplus", "dqnplus", "femnewsplus", "liveplus",
			"mnewsplus", "moeplus", "namazuplus", "news4plus",
			"news5plus", "newsplus", "owabiplus", "scienceplus",
			"ticketplus", "wildplus",
			# plus�n�ł͂Ȃ�����
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
# �X���b�h���𐧌�������ǂ���
#######################################################################
sub IsThreadLimitIta
{
	my ($GB) = @_;

	# �ΏۂƂȂ����
	our %ThreadLimitItaList;
	BEGIN {
		%ThreadLimitItaList = map +($_ => 1), (
			#����ch
			"dancesite", "dome", "endless", "festival",
			#�ԑgch
			"livenhk", "liveetv",
			"liventv", "liveanb", "livetbs", "livetx", "livecx",
			#����ch(weekly�n)
			"livewkwest", "weekly",
			#�싅�A�T�b�J�[
			"livebase", "livefoot",
			#BS�A���W�I�A�X�J�p�[(CS)�AWOWOW
			"livebs", "liveradio",
			"liveskyp", "livewowow",
			#�Ȃ�ł�����J�A�Ȃ�ł�����S
			"livejupiter", "livesaturn",
			#�I�����s�b�N����
			"oonna", "ootoko",
			#�Ȃ�ł�����V
			"livevenus",
			#�e�X�g�p
			#"operate2",
			#�n�k
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
# JavaScript��read.html��L���ɂ��邩�ǂ������`�F�b�N����
#######################################################################
sub IsReadHtml
{
	my ($GB) = @_;

	# �Ƃ肠����dso, life7�T�[�o�����L��
	#if($ENV{'SERVER_NAME'} =~ /^(?:dso|life7)\./)	{return 1;}

	# read.html �t�@�C���̑��݂̗L���Ő؂�ւ�
	our $IsReadHtml;
	BEGIN {
		$IsReadHtml = -e 'read.html';
	}
	return $IsReadHtml;
}

=begin comment

bbsd �֘A�̏����� BBSD.pm �Ɉ�C�̂��߃R�����g�A�E�g
#######################################################################
# �Ⴞ��܃T�[�o���ǂ����`�F�b�N����
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
# �Ⴞ��܃T�[�o�p���������[�`��
# ����: �T�[�o��
# �E�e��ϐ�(����[�΂�[)�̏�����
#############################################################################
sub InitSnow
{
	my ($server) = @_;

	# ���ϐ� SSL_X_BBSD_SERVER(, SSL_X_BBSD_DB_SERVER) ����擾
	# XXX: suExec ���Ɠn������ϐ��ɐ��������邽�� SSL_X_ ��t����
	if ($ENV{SSL_X_BBSD_SERVER}) {
		# bbsd(�������݁EID�̎�S��)�̏��
		($FOX->{SNOWMAN}{BBSD}{HOST}, $FOX->{SNOWMAN}{BBSD}{PORT})
		    = $ENV{SSL_X_BBSD_SERVER} =~ /:/
			? split(/:/, $ENV{SSL_X_BBSD_SERVER})
			: ($ENV{SSL_X_BBSD_SERVER}, 2222);
		$FOX->{SNOWMAN}{BBSD}{TIMEOUT} = 3;
		# bbsd(Samba������DB�S��)�̏��
		($FOX->{SNOWMAN}{DB}{HOST}, $FOX->{SNOWMAN}{DB}{PORT})
		    = $ENV{SSL_X_BBSD_DB_SERVER}
			? $ENV{SSL_X_BBSD_DB_SERVER} =~ /:/
			    ? split(/:/, $ENV{SSL_X_BBSD_DB_SERVER})
			    : ($ENV{SSL_X_BBSD_DB_SERVER}, 2222)
			: ($FOX->{SNOWMAN}{BBSD}{HOST}, $FOX->{SNOWMAN}{BBSD}{PORT});
		$FOX->{SNOWMAN}{DB}{TIMEOUT} = 1;
	}
	# ���T�[�o�ł͈Ⴄ�l��ݒ�ł���悤�ɂ��Ă���
	# live22�n�̏ꍇ
	elsif($server =~ /live22/)
	{
		# bbsd(�������݁EID�̎�S��)�̏��
		$FOX->{SNOWMAN}->{BBSD}->{HOST}    = '192.168.100.1';
		$FOX->{SNOWMAN}->{BBSD}->{PORT}    = 2222;
		$FOX->{SNOWMAN}->{BBSD}->{TIMEOUT} = 3;
		# bbsd(Samba������DB�S��)�̏��
		$FOX->{SNOWMAN}->{DB}->{HOST}      = '192.168.100.2';
		$FOX->{SNOWMAN}->{DB}->{PORT}      = 2222;
		$FOX->{SNOWMAN}->{DB}->{TIMEOUT}   = 1;
	}
	# live23�n�̏ꍇ
	elsif($server =~ /live23/)
	{
		# bbsd(�������݁EID�̎�S��)�̏��
		$FOX->{SNOWMAN}->{BBSD}->{HOST}    = '192.168.100.34';
		$FOX->{SNOWMAN}->{BBSD}->{PORT}    = 2222;
		$FOX->{SNOWMAN}->{BBSD}->{TIMEOUT} = 3;
		# bbsd(Samba������DB�S��)�̏��
		$FOX->{SNOWMAN}->{DB}->{HOST}      = '192.168.100.34';
		$FOX->{SNOWMAN}->{DB}->{PORT}      = 2222;
		$FOX->{SNOWMAN}->{DB}->{TIMEOUT}   = 1;
	}
	# live24�n�̏ꍇ
	elsif($server =~ /live24/)
	{
		# bbsd(�������݁EID�̎�S��)�̏��
		$FOX->{SNOWMAN}->{BBSD}->{HOST}    = '192.168.100.1';
		$FOX->{SNOWMAN}->{BBSD}->{PORT}    = 2223;
		$FOX->{SNOWMAN}->{BBSD}->{TIMEOUT} = 3;
		# bbsd(Samba������DB�S��)�̏��
		$FOX->{SNOWMAN}->{DB}->{HOST}      = '192.168.100.1';
		$FOX->{SNOWMAN}->{DB}->{PORT}      = 2223;
		$FOX->{SNOWMAN}->{DB}->{TIMEOUT}   = 1;
	}
	# news20�n�̏ꍇ
	elsif($server =~ /news20/)
	{
		# bbsd(�������݁EID�̎�S��)�̏��
		$FOX->{SNOWMAN}->{BBSD}->{HOST}    = '192.168.100.33';
		$FOX->{SNOWMAN}->{BBSD}->{PORT}    = 2222;
		$FOX->{SNOWMAN}->{BBSD}->{TIMEOUT} = 3;
		# bbsd(Samba������DB�S��)�̏��
		$FOX->{SNOWMAN}->{DB}->{HOST}      = '192.168.100.33';
		$FOX->{SNOWMAN}->{DB}->{PORT}      = 2222;
		$FOX->{SNOWMAN}->{DB}->{TIMEOUT}   = 1;
	}
	# snow�T�[�o(���[�J���Ⴞ���)
	elsif($server =~ /snow/)
	{
		# bbsd(�������݁EID�̎�S��)�̏��
		$FOX->{SNOWMAN}->{BBSD}->{HOST}    = '127.0.0.1';
		$FOX->{SNOWMAN}->{BBSD}->{PORT}    = 2222;
		$FOX->{SNOWMAN}->{BBSD}->{TIMEOUT} = 3;
		# bbsd(Samba������DB�S��)�̏��
		$FOX->{SNOWMAN}->{DB}->{HOST}
			= $FOX->{SNOWMAN}->{BBSD}->{HOST};
		$FOX->{SNOWMAN}->{DB}->{PORT}
			= $FOX->{SNOWMAN}->{BBSD}->{PORT};
		$FOX->{SNOWMAN}->{DB}->{TIMEOUT}   = 1;
	}

	# �^�C���A�E�g���b�Z�[�W
	$FOX->{SNOWMAN}->{TIMEOUTMSG} = "bbsd timed out";

	return 0;
}

=end comment

=cut

#########################################################
sub bbs_entryXXX
{
	# qb5 �ŋl�܂���̃f�o�b�O�p
#	our $bbs_entryXXX_cmds;
#	BEGIN {
#		$bbs_entryXXX_cmds = <<'__BBS_ENTRY_XXX_CMDS_END__';
	use CGI::SpeedyCGI				;
	my $sp = CGI::SpeedyCGI->new			;
	my $spv = $sp->i_am_speedy ? 'SpeedyCGI' : '???';

	$ENV{TZ} = 'Asia/Tokyo'		;#���{
					 #$ENV �͂��̂܂܎g��
	#�Ή��V�O�i��
	$SIG{PIPE} = $SIG{INT} = $SIG{HUP} = $SIG{QUIT} = $SIG{TERM} = \&SigExit;

	my $GBX = {}			;

	# bbs.cgi �̃o�[�W����
	$GBX->{version} = "<a href=\"http://www.2ch.net/\">�Q�����˂�</a> "	;
	$GBX->{version} .= "BBS.CGI - $BBSCGI ($spv)"	;

	# ���ݎ�����$GB�ɓ���
	# �}�C�N���b���Ƃ�A$GB->{NOWTIME}, $GB->{NOWMICROTIME} �ɂ��ꂼ����
	&mumumuGetNowTime($GBX);

	$GBX->{PID} = $$		;#pid

	$GBX->{FORM} = {}		;#

	&foxSetDate($GBX)		;#�@���t�E������ݒ�i$DATE�ɐݒ�)

	# foxTrackBackIn�̒��ŃZ�b�g���Ă���̂ŁA�����Œ�`�E���������Ă���
	$GBX->{CAP} = 0			;# 0:�L���b�v����Ȃ� 1:�L���b�v

	$GBX->{TBACK} = 0		;# 1=TrackBack 0=�ʏ폈��
	$GBX->{HOST} = &foxTrackBackIn($GBX)	;

	# FORM �̓ǂݍ��݂� foxIkinari �̑O�ł���Ă���
	&foxReadForm($GBX)		;#$FORM ��ǂݍ���

	# ���e�m�F��ʂ��X�L�b�v�������(�X�L�b�v����)�ƃt���O
	$GBX->{KPIN1} = "kihon"		;# �t�H�[���̖��O
	$GBX->{KPIN2} = "suriashi"	;# �t�H�[���̓��e
	$GBX->{KPASS} = 0		;# 0:�ʏ퓮�� 1:���e�m�F��ʂ��p�X

	# �X�L�b�v�����������Ă��邩�ǂ����`�F�b�N
	$GBX->{KPASS} = &KPinCheck($GBX);

	# ������� foxIkinari �ŃZ�b�g���Ă���̂ŁA�����ŏ�����
	$GBX->{PON}  = "PON"		;# �N�b�L�[�̑f
	$GBX->{PONX} = "PONX"		;# �N�b�L�[�̑f
	$GBX->{PONOK} = 0		;# ������ PON �𑗂��Ă�����?
	$GBX->{HAP}  = "HAP"		;# �N�b�L�[�̑f
	$GBX->{HAPX} = "HAPX"		;# �N�b�L�[�̑f
	$GBX->{HAPOK} = 0		;# ������ HAP �𑗂��Ă�����?

	# �͂Ȃ�����̎�����ς��鎞�́A�����������邱��
#	$GBX->{PIN1} = "hana"	;$GBX->{PIN2} = "mogera";
#	$GBX->{PIN1} = "kiri"	;$GBX->{PIN2} = "tanpo"	;
#	$GBX->{PIN1} = "suka"	;$GBX->{PIN2} = "pontan";
#	$GBX->{PIN1} = "tepo"	;$GBX->{PIN2} = "don";
	$GBX->{PIN1} = "kuno"	;$GBX->{PIN2} = "ichi";

	$GBX->{PIN} = "$GBX->{PIN1}=$GBX->{PIN2}";# �N�b�L�[�Ŏg�p

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

	$GBX->{WHITECAP} = 0		;# 0:���L���b�v����Ȃ� 1:���L���b�v
					 # (���̃t���O�͍���bbs.cgi�ł͎g�p����)
	$GBX->{STRONGCAP} = 0		;# 0:�����L���b�v����Ȃ� 1:�����L���b�v

	$GBX->{TRIPSTRING} = ""		;# �g���b�v�����㕶����

	$GBX->{MARU} = ""		;# ���̃Z�b�V����ID(�����ǂ�������\)

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

	$GBX->{OUTDAT} = "OUTDAT"	;# �܂��ɏ������Ƃ��Ă���dat
	$GBX->{LOGDAT} = "LOGDAT"	;# �܂��ɏ������Ƃ��Ă���dat�̃��O
	$GBX->{xID} = "xID"		;# �܂��ɏ������Ƃ��Ă���dat��ID
	$GBX->{xBE} = "xBE"		;# �܂��ɏ������Ƃ��Ă���dat��BE
	$GBX->{DAT1} = "DAT1"		;# ����dat��1
	$GBX->{DATLAST} = ()		;# ����dat�̂��KBBS_CONTENTS_NUMBER��
	$GBX->{DATNUM} = 0		;# ����dat�̒��� = ���X��
	$GBX->{NEWSUB} = ()		;# subject.txt��ێ�

	$GBX->{SABORIN} = 0		;# Saborin�t���O
	$GBX->{LOADAVG} = 0.0		;# ���݂̃��[�h�A�x���[�W(��ԍ��̂��)
	$GBX->{MAXLOADAVG} = 0.0	;# ���e���[�h�A�x���[�W(����������ꏈ��)

	$GBX->{IDNOTANE} = "IDNOTANE"	;
	$GBX->{KEITAI} = 0		;# 0:�g�т���Ȃ� 1:Docomo 2:au 3:SoftBank
					;# 5:emobile
	$GBX->{P22CH} = 0		;# 0:p2.2ch.net�ȊO 1:p2.2ch.net
	$GBX->{KEITAIBROWSER} = 0	;# 0:�g�їp�u���E�U�ȊO 1:�g�їp�u���E�U
	$GBX->{V931} = "0"		;# 0:vip�L���Ȃ� 931:vip�L��
	$GBX->{NEWTHREAD} = 0		;
	$GBX->{JIKAN} = "JIKAN"		;

	$GBX->{base} = "base"		;
	$GBX->{NEWTHREAD} = 0		;# bby.2ch.net �V�X���ʒm�@�\
	$GBX->{BURNEDPROXY} = 0		;# 1:BBQ �o�^�ς݁A�Ă��ς݂�proxy 0:����ȊO
	$GBX->{BURNEDKEITAI} = 0	;# 1:BBM �o�^�ς݁A�Ă��ς݂̌g�� 0:����ȊO

	# IPv6�ڑ����ǂ���
	$GBX->{IPv6} = 0		;# 0:IPv6�ڑ��ł͂Ȃ��A1: IPv6�ڑ�

	# IPv6�ڑ���������AIPv6�t���O�𗧂Ă�
	if(&IsIPv6())
	{
		$GBX->{IPv6} = 1	;
	}

	$GBX->{DEBUG} = "�͂��܂�͂��܂�[<br>"	;

	$GBX->{LOADAVG} = &mumumuGetLA()	;# ���[�h�A�x���[�W���̓���

	my $maxspan = 600	;
	my $span = $GBX->{NOWTIME} - $FOX->{NOWTIME};
	if($span > $maxspan)	{$sp->shutdown_next_time;}

	&foxSetPath($GBX)		;# �e��PATH����
	&foxReadSettings($GBX)		;# �ݒ��݂��݂Ƃ��߂��� SETTING.TXT
	&foxSetDate2($GBX)		;# ���t�E������ݒ�i$DATE�ɐݒ� !!�j��)
	&foxBEset($GBX)			;# BE���₢���킹
#���֌W
	&foxKabuInit($GBX)		;# ���֌W

	$FOX->{$GBX->{FORM}->{'bbs'}}->{MD5NUMBER} = &foxCheckMD5id(
					$GBX->{FORM}->{'bbs'},
					$GBX->{MD5DATE},
					$FOX->{$GBX->{FORM}->{'bbs'}}->{MD5NUMBER},
					$FOX->{MD5DATE},
					$GBX->{WPATH});

	$FOX->{MD5DATE} = $GBX->{MD5DATE}	;

#��������
	$FOX->{OTAMESHIMARU} = 'eGSfQMC3U3iZy7mL'	;

#Vip�N�I���e�B�֌W
	$GBX->{VIPQ2STOP} = 0		;# 1:�X���X�g�@0:�p��

require "../../test/bbs-main.cgi";
	&bbs_main($GBX)		;

&DispError2($GBX,"FOX ��","<font color=green>FOX ���@�ӂӂӂ�</font><br><br>���ꂪ�\\�������Ƃ������Ƃ́E�E�E<br>�{��require�����̂ɂ������֍s���Ȃ��ƁA�A�A");
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
# qb5 �ŋl�܂���̃f�o�b�O�p
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
#	���֌W
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

	# ����D��
	#����
	#http://2pix.2ch.se/test/kabuka.so?morningcoffee
	my $host = "http://2pix.2ch.se/test/kabuka2.so?"	;
	my $path = $mei				;
	my $ua = LWP::UserAgent->new()		;
	$ua->agent('Mozilla/5.0 FOX(2ch.se)')	;
	$ua->timeout(3)				;
	my $request = HTTP::Request->new('GET', $host . $path);
	my $response = $ua->request($request) 	;#������ GET ����
	my $db_content = $response->content()	;

	# �G���[�`�F�b�N
	if ($response->is_error)
	{
		# �̊������Ƃ�Ȃ�������G���[(E)�Ƃ���
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
		$GB->{KABUUP} = 1	;	#����D�҂Ղ�
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

#&DispError2($GB,"FOX ��","<font color=green>FOX ���@�ӂӂӂ�</font><br><br>$FOX_KABUU[2]");
	$GB->{KABU}   = 0	;
	$GB->{KABUX}  = "����D��"	;
	$GB->{KABUXP}  = $GB->{FORM}->{'bbs'}	;
	$GB->{KABUU}  = 0	;
	$GB->{KABUUP} = 0	;	#����D�҃v�`
	$GB->{NINNIN} = 0	;
	if($GB->{FORM}->{'FROM'} !~ /\!kab/)	{return 0;}

	$GB->{KABU} = 1	;

	$GB->{MEIGARA} = $GB->{FORM}->{'bbs'}			;
	if($GB->{MEIGARA} eq 'operate2')	{$GB->{MEIGARA} = 'news4vip';}
#	if($GB->{MEIGARA} eq 'operate2')	{$GB->{MEIGARA} = 'punk';}
	$GB->{ZENKABU} = 0					;
	$GB->{KABUKA} =	&foxGetKabuka($GB,$GB->{MEIGARA})	;
	# ����D��
	my $kabuu =	&foxGetKabusu($GB,$GB->{MEIGARA})	;
	my $rrr = 0	;
	if($GB->{ZENKABU} > 0)	{$rrr = int(10000 * $kabuu / $GB->{ZENKABU});}
	my $rrx = int($rrr/100)	;
	$GB->{ZENKABU} = "$GB->{MEIGARA}:$kabuu/$GB->{ZENKABU}=$rrx(%)"	;
	my $u4 = &IsUtai($GB->{KABUKA})				;
	if($kabuu > 4)
	{
		$GB->{KABUUP} = 1	;	#����D�҂Ղ�
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
				$GB->{KABUX}  = "����D��"	;
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

	# ���������\��
	if($GB->{FORM}->{'FROM'} =~ /\!kab\:([a-zA-Z0-9]+)/)
	{
		if($1 ne '')	{$GB->{MEIGARA} = $1}		;
	}
	$GB->{KABUSU} =	&foxGetKabusu($GB,$GB->{MEIGARA})	;

	if(!$GB->{KABUU} && $GB->{KABUUP})
	{
		$GB->{KABUX} = "���D�v�`($GB->{KABUXP})"	;
	}

	return 1;
}
#############################################################################
# ���ݎ�����$GB�ɑ������
# �}�C�N���b���Ƃ�A$GB->{NOWTIME}, $GB->{NOWMICROTIME} �ɂ��ꂼ����
#############################################################################
sub mumumuGetNowTime
{
	my ($GB) = @_;

	#$GB->{NOWTIME} = time		;	#���ݎ���

	# �}�C�N���b���Ƃ�
	use Time::HiRes qw( gettimeofday );
	($GB->{NOWTIME}, $GB->{NOWMICROTIME}) = gettimeofday;

	# FreeBSD 5.2.1R��banana�T�[�o��perl�ɂ�
	# Time::HiRes�������Ă��Ȃ��̂ŁA
	# �ւ���syscall���g���Ă���
	#
	#my $tv = pack("L!L!", ());	# 2��pack����long�^�ϐ�
	#
	#require 'sys/syscall.ph';
	#syscall(&main::SYS_gettimeofday, $tv, undef);
	#
	#($GB->{NOWTIME}, $GB->{NOWMICROTIME}) = unpack("L!L!", $tv);

	return 0;
}
#######################################################################
# ���݂̃��[�h�A�x���[�W���𒲂ׂ�
#######################################################################
sub mumumuGetLA
{
	use Sys::CpuLoad;

	return (Sys::CpuLoad::load())[0];
}
#######################################################################
# ����[�h�A�x���[�W���𒲂ׂ�
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
# �T�[�o�̌^�𒲂ׂ� (cobra/tiger/banana/unknown)
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
# ����[�h�A�x���[�W�ɒB���Ă��邩�ǂ����𒲂ׂ� (����: LA, �{��)
#######################################################################
sub mumumuMaxLACheck
{
	my ($loadavg, $fact) = @_;

	if($loadavg >= $FOX->{MAXLOADAVG} * $fact)	{return 1;}
	else						{return 0;}
}
#############################################################################
# BE�̃|�C���g�ɉ����������N�t��
# ����: BE�̃|�C���g
# �߂�l: ������ꂼ��ɉ�����3�����̕�����
#############################################################################
sub GetBERank
{
	my ($user_points) = @_;

	# 100000�|�C���g�ȏ�́u�\���e�B�A�v
	if($user_points    >= 500000)	{ return "SOL"; }
	# 30000�|�C���g�ȏ�̓_�C�����
	elsif($user_points >= 100000)	{ return "DIA"; }
	# 10000�|�C���g�ȏ�̓v���`�i���
	elsif($user_points >= 12000)	{ return "PLT"; }
	# 1000�|�C���g�ȏ�̓u�����Y���
	elsif($user_points >= 10000)	{ return "BRZ"; }
	# ���ꖢ���͈�ʉ��
	else				{ return "2BP"; }
}
#############################################################################
# BE �ɂ��u�|�C���g���T(���b�L�[��)�v����
# ����: $GB
# �߂�l: 1: �|�C���g���T�A0: �͂���
#############################################################################
sub GetBELucky
{
	my ($GB) = @_;

	# SOL / DIA / PLT �͖������� 1
        if($GB->{BEelite} eq "SOL")	{ return 1; }
        if($GB->{BEelite} eq "DIA")	{ return 1; }
        if($GB->{BEelite} eq "PLT")	{ return 1; }

	# BRZ �� 1/2 �̊m���� 1
        if($GB->{BEelite} eq "BRZ")
	{
		if(rand(4) < 1)		{ return 1; }
		return 0;
	}

	# ����ȊO�͏�� 0
	return 0;
}
#######################################################################
# ���ʊ���D�҂��擾����
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
	my $response = $ua->request($request) ;#������ GET ����
	my $db_content = $response->content();

	# �G���[�`�F�b�N
	if ($response->is_error)
	{
		# �����������Ƃ�Ȃ�����0���Ƃ݂Ȃ�
		return 0;
	}

	@FOX_KABUU = split(/\n/,$db_content)	;

	return 0			;
}
#######################################################################
# ���݊������擾����
#######################################################################
sub foxGetKabusu
{
	my ($GB,$bn) = @_	;
#&DispError2($GB,"FOX ��","<font color=green>FOX ���@�ӂӂӂ�</font><br><br>DMDM[$GB->{FORM}->{'DMDM'}] ,MDMD[$GB->{FORM}->{'MDMD'}]");

#	my $bn = $GB->{FORM}->{'bbs'}	;
#	if($bn eq 'operate2')	{$bn="giin";}
	#������
	#http://be.2ch.net/test/PXshowsecdetail.php?DMDM=onetop@gmail.com&MDMD=8d2888&BN=news
	my $host = "http://be.2ch.net/test/PXshowsecdetail.php?"	;
	my $path = "MDMD=$GB->{FORM}->{'MDMD'}&DMDM=$GB->{FORM}->{'DMDM'}&BN=$bn"		;
	my $ua = LWP::UserAgent->new();
	$ua->agent('Mozilla/5.0 FOX(2ch.se)');
	$ua->timeout(3);
	my $request = HTTP::Request->new('GET', $host . $path);
	my $response = $ua->request($request) ;#������ GET ����
	my $db_content = $response->content();

	# �G���[�`�F�b�N
	if ($response->is_error)
	{
		# �����������Ƃ�Ȃ�����0���Ƃ݂Ȃ�
		return 0;

#		my $code = $response->code();
#		&DispError2($GB, "�d�q�q�n�q�I", "�d�q�q�n�q�F���������̎擾�Ɏ��s���܂����B($code)");
	}

	my ($name,$kabu,$tanka,$ttttt) = split(/<>/,$db_content)	;
	my $kkk = int($kabu)		;

	return $kkk			;
}
#######################################################################
# ���݊������擾����
#######################################################################
sub foxGetKabuka
{
	my ($GB,$ita) = @_	;

	#����
	#http://2pix.2ch.se/test/kabuka.so?morningcoffee
	my $host = "http://2pix.2ch.se/test/kabuka2.so?"	;
	my $path = $ita				;
	my $ua = LWP::UserAgent->new()		;
	$ua->agent('Mozilla/5.0 FOX(2ch.se)')	;
	$ua->timeout(3)				;
	my $request = HTTP::Request->new('GET', $host . $path);
	my $response = $ua->request($request) 	;#������ GET ����
	my $db_content = $response->content()	;

	# �G���[�`�F�b�N
	if ($response->is_error)
	{
		# �̊������Ƃ�Ȃ�������G���[(E)�Ƃ���
		return "E";

#		my $code = $response->code();
#		&DispError2($GB, "�d�q�q�n�q�I", "�d�q�q�n�q�F���������̎擾�Ɏ��s���܂����B($code)");
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
# BE�̏���$GB�ɃZ�b�g����
#######################################################################
sub foxBEset
{
	my ($GB) = @_	;

	$GB->{isBE}     = 0		;
	$GB->{BEelite}  = ""		;
	$GB->{BELucky}  = 0		;
	$GB->{icon}	= ""		;
###2010/7/7 be�T�[�o�ח�
#return 1;
	##############becheck
#&DispError2($GB,"FOX ��","<font color=green>FOX ���@�ӂӂӂ�</font><br><br>DMDM[$GB->{FORM}->{'DMDM'}] ,MDMD[$GB->{FORM}->{'MDMD'}]");

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
#			&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F����be�A�J�E���g�͂��̎��Ԏg���܂���B");
#		}
#	}

	use LWP::UserAgent;

	my $path = "d=$GB->{FORM}->{'DMDM'}&m=$GB->{FORM}->{'MDMD'}";
	my $ua = LWP::UserAgent->new();
	$ua->timeout(5);
	my $request = HTTP::Request->new('GET', 'http://be.2ch.net/test/v.php?' . $path);
	my $response = $ua->request($request) ;#������ GET ����
	my $response_body = $response->content();#GET�̌��ʂ͂����ɓ����Ă���

	my $db_content = $response->content();

	# �G���[�`�F�b�N
	if ($response->is_error)
	{
		my $code = $response->code();
		&DispError2($GB, "�d�q�q�n�q�I", "�d�q�q�n�q�FBe���[�U�[���̎擾�Ɏ��s���܂����B($code)");
	}

	my ($user_points, $xxx, $icon_name) = split(/ /, $db_content);

#	if($user_points =~ /\D/ || $xxx =~ /\D/){
#		&DispError2($GB, "�d�q�q�n�q�I", "�d�q�q�n�q�FBe���[�U�[���̎擾�Ɏ��s���܂����B(Invalid response)");
#	}
	if($xxx eq ''){
		&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�FBe���[�U�[���G���[�B���O�C�����Ȃ����Ă�������(e)�B<a href=\"http://be.2ch.net/\">be.2ch.net</a>");
	}
	$GB->{isBE}     = 1		;
	$GB->{BEpoints} = $user_points	;
	$GB->{BExxx}    = $xxx		;
	$GB->{icon}    = $icon_name		;

	# BE�̓_���ɉ����������N�t�����s���A��ʂɉ����������������
	$GB->{BEelite}  = &GetBERank($GB->{BEpoints});
	#&DispError2($GB,"root ��","BE����X�e�[�^�X: $GB->{BEelite}");
	# ���b�L�[�܂��ǂ������ׂ�
	$GB->{BELucky}  = &GetBELucky($GB);
	#&DispError2($GB,"root ��","BE���b�L�[��: $GB->{BELucky}");

	if($FOX->{$GB->{FORM}->{'bbs'}}->{"BBS_BE_TYPE2"})
	{
		#BBE�ُ펞�͂���[
		if(!$FOX->{BBE})		{return 1;}

		#BBE�ɖ⍇��
		my $addr = foxDNSquery2("$GB->{NOWTIME}.$GB->{PID}.$GB->{FORM}->{'MDMD'}.1.bbe.2ch.net")	;

		#BBE������������A�Ȍ�D����������܂�DNS�₢���킹���~
		if($addr eq "127.0.0.0")	{ $FOX->{BBE} = 0; }
		# �Ă���Ă���ꍇ
		elsif($addr eq '127.0.0.2')
		{

#			&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�Ă��ꂽ be �͎g���܂���I");
		}
	}

	return 1;
}
#==================================================
#�@���t�E������ݒ�i$DATE�ɐݒ�)
#==================================================
sub foxSetDate
{
	my ($GB) = @_	;
	my @wdays = ("��", "��", "��", "��", "��", "��", "�y");
	my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst);
	#���t�Ǝ��Ԃ����Ƃ���
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
#�@���t�E������ݒ�i$DATE�ɐݒ�)
#==================================================
sub foxSetDate2
{
	my ($GB) = @_	;
	my @wdays = split(/\//,$FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_YMD_WEEKS'});
	my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst);
	#���t�Ǝ��Ԃ����Ƃ���
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
		$GB->{DATE} = sprintf("$nengo%d�N,%04d/%02d/%02d(%s) %02d:%02d:%02d",
		$year + 1900 + $offset,$year + 1900, $mon + 1, $mday,$wdays[$wday], $hour, $min, $sec);
	}
	else
	{
		$GB->{DATE} = sprintf("%04d/%02d/%02d(%s) %02d:%02d:%02d",
		$year + 1900, $mon + 1, $mday,$wdays[$wday], $hour, $min, $sec);
	}
}
#==================================================
#�@�������̎擾�i�ݒ�t�@�C���j
#==================================================
#�ݒ�t�@�C����ǂ�
sub foxReadSettings
{
	my ($GB) = @_	;
	my $ita = $GB->{FORM}->{'bbs'}	;

$GB->{DEBUG} .= "SETTING.TXT ��݂��݂�?  $ita<br>";
	if(defined($FOX->{$ita}))
	{
		$GB->{DEBUG} .= "SETTING.TXT ���ɓǂݍ��ݍς݁[(1)$ita<br>";
#		$GB->{FORM}->{MESSAGE} .= "<hr>SETTING.TXT ���ɓǂݍ��ݍς݁[�B($GB->{PID})";
		return 0;
	}
$GB->{DEBUG} .= "SETTING.TXT ��݂��݁[$ita<br>";

	my $m_pass = "../$GB->{FORM}->{'bbs'}/SETTING.TXT";
	unless(-e $m_pass)
	{
		my $gogo5 = "../$GB->{FORM}->{'bbs'}/";
		#�ݒ�t�@�C�����Ȃ��iERROR)
		&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F���[�U�[�ݒ肪�������Ă��܂��I3<br><a href=\"$gogo5\">�������ɂ��邩���ł�</a>");
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
#�������̕⊮

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
		$FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_NONAME_NAME'} = "����������";
	}
	unless($FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_DISP_IP'}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_DISP_IP'} = "";
	}
	unless($FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_YMD_WEEKS'}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_YMD_WEEKS'} = "��/��/��/��/��/��/�y";
	}
#	unless($FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_YMD_NAME'}){
#		$FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_YMD_NAME'} = "�c�I";
#	}
#	unless($FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_YMD_OFFSET'}){
#		$FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_YMD_OFFSET'} = 660;
#	}

# �I���p
#$FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_NONAME_NAME'} = "���������񁗂������I���ɍs����";
#$FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_SLIP'} = "checked";

	if($FOX->{$GB->{FORM}->{'bbs'}}->{'timeclose'} > $FOX->{$GB->{FORM}->{'bbs'}}->{'timecount'}){
		$FOX->{$GB->{FORM}->{'bbs'}}->{"timeclose"} = $FOX->{$GB->{FORM}->{'bbs'}}->{"timecount"};
	}

$GB->{DEBUG} .= "SETTING.TXT ��݂��݁[$ita����!!<br>";
#	$GB->{FORM}->{MESSAGE} .= "<hr>SETTING.TXT�ǂ񂾁B($GB->{PID})";

	$FOX->{$GB->{FORM}->{'bbs'}}->{MD5NUMBER} = &foxInitMD5id($GB->{FORM}->{'bbs'},$GB->{MD5DATE},$GB->{WPATH});
	$FOX->{MD5DATE} = $GB->{MD5DATE}	;

	$FOX->{$GB->{FORM}->{'bbs'}}->{SAMBA24} = &foxSamba24Init($GB->{FORM}->{'bbs'});

#bbspink�́ABBS_MAIL_COUNT=16
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
#		$FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_NONAME_NAME'} .= "����$ato�b";
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

	#my $spanspan = 20	;	#�K���b��
	my $kanpeki  = 3	;	#���e�� ERR593 Nsec ���������Ă��܂���
	my $saidai   = 5	;	#���E�� ERR599 �R�[�q�[�u���C�N�A�ȍ~���������܂���B

#	my $yakinFile = "./book/$tane.cgi";
	my $yakinFile = "$FOX->{BOOK}/book/$tane.cgi";
	my $memomemo = "($Samba)";

	my ($prsize,$prmtime)= ();
	my $ctime = 0;
	my $keika = 0;
	my $errmsg = "";	# bbsd�ɕ��������� 
	my $statnum = 0;	# Samba DB����Ԃ��Ă���X�e�[�^�X

	# �Ⴞ��܂ł́Abbsd�ɖ₢���킹��
	if(IsSnowmanServer)
	{
		# live22x[123] �Ƃ������O�ŗ�����ASamba120�b
		if($ENV{SERVER_NAME} =~ /live22x[123]/)
		{
			$spanspan = 120;
		}

		# Samba24 DB �ւ̖₢���킹
		my $cmd = 'chkid';
		$errmsg = bbsd_db($GB->{FORM}->{'bbs'}, $cmd, 'samba24', $tane, $spanspan, $kanpeki, $saidai, 'dummy'); 
		# �^�C���A�E�g���ǂ����`�F�b�N
		# �^�C���A�E�g��������Samba24�̓X���[����
		if(&bbsd_TimeoutCheck($GB, $errmsg))
		{
			return 0;
		}

		# ���ʂ�؂�o��
		($statnum, $prsize, $keika) = split(/,/, $errmsg);

		# �X�e�[�^�X��0�Ȃ疳���
		if($statnum == 0) {return 0;}

		# �u�A���񐔁v�𐔂���̂ŁA����炷�K�v������
		$prsize--;
	}
	else
	{
		($prsize, $prmtime) = (local $_=stat($yakinFile)) ? ($_->size, $_->mtime) : (0, 0);
		$ctime = time;
		$keika = $ctime - $prmtime;
	}

	# �K������
	if($prsize > $saidai)
	{
		my $houhou = '<a href=\"http://etc6.2ch.net/event/\">�C�x���g���</a>�ňꎞ�Ԉȏ�V�����ʔ����C�x���g�l���Ă��������B';

		print "Content-type: text/html; charset=shift_jis\n\n";
		print <<EOF;
<html><head><title>�d�q�q�n�q�I</title><meta http-equiv="Content-Type" content="text/html; charset=shift_jis"></head>
<body><!-- 2ch_X:error -->
�d�q�q�n�q - 594 ���������Ə����܂����B<br>
<br>
���Ȃ��́A�K�����X�g�ɒǉ�����܂����B<br><br>
�y����������@�z<br>
$houhou<br>
����ȊO�ɉ����̕��@�͂���܂���B<br>

<br><hr>$memomemo</body>
</html>
EOF

		if(!IsSnowmanServer)
		{
			open(YAN1,">>$yakinFile");print YAN1 "1";close(YAN1);
		}

		exit;
	}

	# �x���\��
	if($prsize && $keika < $spanspan)
	{

		if(!IsSnowmanServer)
		{
			open(YAN1,">>$yakinFile");print YAN1 "1";close(YAN1);
		}

		# �d����΂�
		if($prsize > $kanpeki)
		{
			my ($fsec,$fmin,$fhour,$fmday,$fmon,$fyear,$fwday,$fyday,$fisdst) = localtime($ctime); $fmon ++	;$fyear += 1900	;

			print "Content-type: text/html; charset=shift_jis\n\n";
			print <<EOF;
<html><head><title>�d�q�q�n�q�I</title><meta http-equiv="Content-Type" content="text/html; charset=shift_jis"></head>
<body><!-- 2ch_X:error -->
599 �A�ł��Ȃ��ł��������B�������낻��K�����X�g�ɓ���܂���B�B(�P�[�P)�j�����b<br>
<br><hr>$memomemo</body>
</html>
EOF
			exit;
		}

		# �y����΂�/����
		print "Content-type: text/html; charset=shift_jis\n\n";
		print <<EOF;
<html><head><title>�d�q�q�n�q�I</title><meta http-equiv="Content-Type" content="text/html; charset=shift_jis"></head>
<body><!-- 2ch_X:error -->
�d�q�q�n�q - 593 $spanspan sec �����Ȃ��Ə����܂���B($prsize��ځA$keika sec ���������ĂȂ�)<br>
<br>
120sec�K���̏ꍇ Be �Ƀ��O�C������Ɖ���ł��܂�(newsplus������)�B<a href="http://be.2ch.net/">be.2ch.net</a>

<br><hr>$memomemo</body>
</html>
EOF
		exit;
	}

	if(!IsSnowmanServer)
	{
		if($prsize) {unlink("$yakinFile");}

		open(YAN1,">>$yakinFile");print YAN1 "1";close(YAN1);
		# �ŏ���umask(0)��錾���Ă���̂ŕs�v
		#umask(0);
		#chmod(0666, $yakinFile);
	}

	return 0;
}
#######################################################################
# ���ł̒P�ʎ��ԓ�����̃X�����Đ����`�F�b�N����
# �ꎞ�t�@�C���̏ꏊ��Samba24�Ɠ����Ƃ���𗬗p����
# �ꎞ�t�@�C�����̐擪�� "." �����邱�ƂŁAf22�ɂ��IP���̃J�E���g��
# �e�����o�Ȃ��悤�ɂ���
#######################################################################
sub mumumuKuromaruSuretateCount
{
	my ($GB, $tcountmax) = @_;
	my $FilenoTane = $GB->{MARU};

	# ���̓J�E���g�A�b�v�Ȃ�
	if($GB->{CAP})		{return 0;}

	# ���̒��g���t�@�C�����Ƃ��Ďg�p�\�Ȃ��̂ɂ���(/��_�ɕϊ�)
	$FilenoTane =~ s/\//_/g;

	# �Ⴞ��܂ł�bbsd�ɖ₢���킹��
	if(IsSnowmanServer)
	{
		my $errmsg = "";
		my $statnum = 0;
		my $cmd = 'chkid';
		$errmsg = bbsd_db($GB->{FORM}->{'bbs'}, $cmd, 'kuromarusuretate', $FilenoTane, 1800, $tcountmax, $tcountmax, 'dummy');
		# �^�C���A�E�g���ǂ����`�F�b�N
		# �^�C���A�E�g��������X���[����
		if(&bbsd_TimeoutCheck($GB, $errmsg))
		{
			return 0;
		}

		# ���ʂ�؂�o��
		$statnum = (split(/,/, $errmsg))[0];

		# $tcountmax�𒴂��Ă����痧�Ă���
		if($statnum == 3) {return 1;}
		# �X���[����
		return 0;
	}
	else
	{
		# �t�@�C���u�����Samba24�̏ꏊ���ؗp����
		my $KuromaruFile = "./book/.$FilenoTane.cgi";
		# ���ł̃X�����ĉ�
		my $tcount = 0;

		# �t�@�C�������邩�ǂ������ׂāA�A�A
		if(-e $KuromaruFile)
		{
			# �������璆�g��ǂ�ŕϐ��ɓ���A�J�E���g�A�b�v���ď�������
			# �������ɓ������ł̃X�����Ă͂Ȃ��Ɖ��肵�A�r������͂��Ȃ�
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
			# �Ȃ�������t�@�C����V�K�ɍ���āA1����������
			$tcount = 1;
			open(KURO,">$KuromaruFile");
			print KURO $tcount;
			close(KURO);
		}

		# �ő�񐔂ɒB���Ă�����A�ُ��Ԃ�
		if($tcount >= $tcountmax)	{return 1;}
		# �X���[����
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

	# �Ⴞ��܂�/md�̉���ǂ�
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

	# �Ⴞ��܂�/md�̉���ǂ�
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

	# �Ⴞ��܂�/md�̉��ɍ��
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

	# �Ⴞ��܂ł́Abbsd�Ɏ��₢���킹��
	if(IsSnowmanServer == BBSD->{REMOTE})
	{
		my $cmd = 'getmd5seed';
		$md5line = bbsd($bbs, $cmd, 'dummy');
		# �^�C���A�E�g���ǂ����`�F�b�N
		# ������$GB���Ȃ��̂ŁA�K���ɍ��
		my $TMPGB = {};
		$TMPGB->{FORM}->{'bbs'} = $bbs;
		if(&bbsd_TimeoutCheck($TMPGB, $md5line))
		{
			&bbsd_TimeoutError($TMPGB, $cmd);
		}
	}
	# �ʏ�T�[�o�ł́A�����Ŏ�����
	else
	{
		sysopen(RANDOM, '/dev/urandom', O_RDONLY) || die "cannot open /dev/urandom $!\n";
		sysread(RANDOM, $data, 16)	;
		close(RANDOM)			;
	}

	open(MD5FILE, ">$md5datefile")	;
	# �Ⴞ��܂ł́A����������̂܂܂̌`�ŏ���
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
	# �ŏ���umask(0)���Ă���̂ŕs�v
	#chmod(0777, $md5datefile)	;

	return	$data			;
}
########################################################################
# ���Ƃ̃X���b�h�ێ����𒲂ׂ�(initFOX����D�o�q���Ɉ�x�����Ă΂��)
# �߂�l: f22�ɂ�����ێ���(�����Ȃ������ꍇ�f�t�H���g(1000))
########################################################################
#sub mumumuGetHojisuu
#{
#	# �f�t�H���g�l�A/_bg/f22.cgi���Q��
#	my $resNumMax  = 1000;
#	my @f22 = ();
#	my @f22r = ();
#
#	# f22�̐ݒ�t�@�C����ǂ݁A�l�𒲂ׂ�
#	if (-e '../_bg/f22info.cgi')
#	{
#		open(F22FILE,"../_bg/f22info.cgi");
#		@f22 = <F22FILE>;
#		close(F22FILE);
#
#		# $resNumMax �̍s�𒲂ׁA�A�A
#		@f22r = grep(/\$resNumMax /, @f22);
#
#		# �Y���s������΁A���΂�
#		# ����ɂ��$resNumMax���X�V�����
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

	# BBx��DNS�T�[�o�������Ă��邩�ǂ����t���O
	$FOX->{BBM} = 1			;
	$FOX->{BBM2} = 1		;
	$FOX->{BBQ} = 1			;
	$FOX->{BBX} = 1			;
	$FOX->{BBN} = 1			;
	$FOX->{BBY} = 1			;
	$FOX->{BBS} = 1			;
	$FOX->{BBR} = 1			;
	$FOX->{BBE} = 1			;

	# BBY/BBS/BBR�pDNS�T�[�oIP�A�h���X
	# �T�[�o�ړ]���͗v�ύX
	# BBR��rock54.2ch.net�Ɠ���T�[�o������IP�A�h���X�ƂȂ邱�Ƃɒ���
	# (BBQ/BBM/BBX/BBN/BBE�͒ʏ��DNS�����̂��߁AIP�A�h���X���ߍ��݂͂Ȃ�)
	$FOX->{DNSSERVER}->{BBY}  = "206.223.152.130"	;# a.ns.bby.2ch.net
	$FOX->{DNSSERVER}->{BBYP} = "206.223.153.130"	;# a.ns.bby.bbspink.com
	$FOX->{DNSSERVER}->{BBS}  = "207.29.247.145"	;# a.ns.bbs.2ch.net
	$FOX->{DNSSERVER}->{BBR}  = "206.223.151.68"	;# a.ns.bbr.2ch.net

=begin comment

bbsd �֘A�̏����� BBSD.pm �Ɉ�C�̂��߃R�����g�A�E�g
	# �Ⴞ��܃T�[�o���ǂ���(�Ⴞ��܂Ȃ�1�A�����łȂ����0)
	$FOX->{SNOWMAN}->{FLAG} = &IsSnowManServer($ENV{'SERVER_NAME'});

	# �Ⴞ��܃T�[�o��������A���������[�`�����Ă�
	if($FOX->{SNOWMAN}->{FLAG})
	{
		&InitSnow($ENV{'SERVER_NAME'});
	}

=end comment

=cut

	# ����@�\ (Saborin, IsKoukokuSkip, CentiSec ��)
	%{$FOX->{BBSCGI_FUNCTIONS}} = map +($_ => 1), split /,/, uc($ENV{SSL_X_BBSCGI_FUNCTIONS} || '');
	# Set-Cookie �L������
	$FOX->{COOKIEEXPIRES} = strftime '%A, %d-%b-%Y %T GMT', gmtime 86400 * (int($FOX->{NOWTIME} / 86400) + 2 * 365);

	$FOX->{MAXLOADAVG} = &mumumuGetMaxLA();# �T�[�o���̋��e���[�h�A�x���[�W
	$FOX->{ISKOUKOKU} = 1		;# IsKoukoku�����s���邩�ǂ���
#	$FOX->{KUROMARUTCOUNT} = 6	;# ���ňꎞ�Ԃ�����ɗ��Ă���X����
	$FOX->{KUROMARUTCOUNT} = 100	;# by FOX

	#$FOX->{HOJISUU} = &mumumuGetHojisuu();# �T�[�o���Ƃ̃X���b�h�ێ���

	# �L���t�@�C����(public_html/test ����̑��΃p�X)
	# �Ⴞ��܂ł�bbsd�ɓn��

	if($ENV{'SERVER_NAME'} =~ /bbspink\.com/)
	{
		$FOX->{headadfile} = '../SAKURA.txt'	;#��̏�
		$FOX->{putadfile}  = ''			;#��̉�
		$FOX->{maido3adfile} = sub { '../BANANA.txt'; }		;#�^��
	}
	else
	{
		$FOX->{headadfile} = 'headad.txt'	;#��̏�
		$FOX->{putadfile}  = 'putad.txt'	;#��̉�
		$FOX->{maido3adfile} = sub { "maido3ad/$_[0]"; }	;#�^��
	}

	################################################################
	# �g��/PHS�pIP�A�h���X�u���b�N�֘A
	################################################################
	# �g�p���W���[���̓ǂݍ���
	use Net::CIDR::Lite;

	################################################################
	# i���[�h�pIP�A�h���X�u���b�N�֘A
	################################################################
	$FOX->{IMODECIDR} = Net::CIDR::Lite->new;

	# IP�A�h���X�u���b�N�ꗗ(CIDR�`��)
	# �A�h���X�����W���ǉ����ꂽ�ꍇ�A�����ɉ����Ă���
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
	# CIDR���X�g�����炩���ߓo�^���Ă���
	# �������Ă������ƂŁA�d����������bbs.cgi�o�q����1��ōς�
	foreach (@imodecidr) {
		$FOX->{IMODECIDR}->add($_);
	}

	################################################################
	# i���[�h�t���u���E�U�pIP�A�h���X�u���b�N�֘A
	################################################################
	$FOX->{IMODEFULLBROWSERCIDR} = Net::CIDR::Lite->new;

	# IP�A�h���X�u���b�N�ꗗ(CIDR�`��)
	# �A�h���X�����W���ǉ����ꂽ�ꍇ�A�����ɉ����Ă���
	# http://www.nttdocomo.co.jp/service/imode/make/content/ip/
	my @imodefullbrowsercidr = (
	"210.153.87.0/24"
	);
	# CIDR���X�g�����炩���ߓo�^���Ă���
	# �������Ă������ƂŁA�d����������bbs.cgi�o�q����1��ōς�
	foreach (@imodefullbrowsercidr) {
		$FOX->{IMODEFULLBROWSERCIDR}->add($_);
	}

	################################################################
	# EZweb�pIP�A�h���X�u���b�N�֘A
	################################################################
	$FOX->{EZWEBCIDR} = Net::CIDR::Lite->new;
	
	# IP�A�h���X�u���b�N�ꗗ(CIDR�`��)
	# �A�h���X�����W���ǉ����ꂽ�ꍇ�A�����ɉ����Ă���
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
	# CIDR���X�g�����炩���ߓo�^���Ă���
	# �������Ă������ƂŁA�d����������bbs.cgi�o�q����1��ōς�
	foreach (@ezwebcidr) {
		$FOX->{EZWEBCIDR}->add($_);
	}

	################################################################
	# au PC�T�C�g�r���[�A�[(PCSV)�pIP�A�h���X�u���b�N�֘A
	################################################################
	$FOX->{PCSITEVIEWERCIDR} = Net::CIDR::Lite->new;

	# IP�A�h���X�u���b�N�ꗗ(CIDR�`��)
	# �A�h���X�����W���ǉ����ꂽ�ꍇ�A�����ɉ����Ă���
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
	# CIDR���X�g�����炩���ߓo�^���Ă���
	# �������Ă������ƂŁA�d����������bbs.cgi�o�q����1��ōς�
	foreach (@pcsiteviewercidr) {
		$FOX->{PCSITEVIEWERCIDR}->add($_);
	}

	################################################################
	# Y!�P�[�^�C�pIP�A�h���X�u���b�N�֘A
	################################################################
	$FOX->{SOFTBANKCIDR} = Net::CIDR::Lite->new;
	
	# IP�A�h���X�u���b�N�ꗗ(CIDR�`��)
	# �A�h���X�����W���ǉ����ꂽ�ꍇ�A�����ɉ����Ă���
	# http://developers.vodafone.jp/dp/tech_svc/web/ip.php
	#
	# �\�t�g�o���N���o�C���ɂȂ��āAURI ���ύX���ꂽ�͗l
	# -- 10/30/2006 by ��
	# http://developers.softbankmobile.co.jp/dp/tech_svc/web/ip.php
	#
	# �ēx�ύX���ꂽ�͗l
	# -- 4/28/2008 by ��
	# http://creation.mb.softbank.jp/web/web_ip.html
	my @softbankcidr = (
	"123.108.237.0/27",
	"202.253.96.224/27",
	"210.146.7.192/26",
	"210.175.1.128/25"
	);
	# CIDR���X�g�����炩���ߓo�^���Ă���
	# �������Ă������ƂŁA�d����������bbs.cgi�o�q����1��ōς�
	foreach (@softbankcidr) {
		$FOX->{SOFTBANKCIDR}->add($_);
	}

	################################################################
	# �\�t�g�o���N���o�C�� PC�T�C�g�u���E�U�pIP�A�h���X�u���b�N�֘A
	################################################################
	$FOX->{PCSITEBROWSERCIDR} = Net::CIDR::Lite->new;

	# PC�T�C�g�u���E�U�ɂė��p����IP�A�h���X�ш�
	# �\�t�g�o���N�g�ѓd�b��PC�T�C�g�u���E�U�ɂ�
	# �E�F�u�T�[�o�փA�N�Z�X����ہA�E�F�u�T�[�o���ɒʒm�����
	# ���M����IP�A�h���X�͉��L�̑ш���A�h���X�ƂȂ�܂��B 
	my @pcsitebrowsercidr = (
	"123.108.237.224/27",
	"202.253.96.0/28"
	);
	# CIDR���X�g�����炩���ߓo�^���Ă���
	# �������Ă������ƂŁA�d����������bbs.cgi�o�q����1��ōς�
	foreach (@pcsitebrowsercidr) {
		$FOX->{PCSITEBROWSERCIDR}->add($_);
	}

	################################################################
	# emobile EMnet�pIP�A�h���X�u���b�N�֘A
	################################################################
	$FOX->{EMNETCIDR} = Net::CIDR::Lite->new;

	# IP�A�h���X�u���b�N�ꗗ(CIDR�`��)
	# �A�h���X�����W���ǉ����ꂽ�ꍇ�A�����ɉ����Ă���
	# http://developer.emnet.ne.jp/ipaddress.html

	# eM60-254-209-99.emobile.ad.jp = 60.254.209.99 �� EMnet �Ȃ��Ƃɒ���
	# http://takagi-hiromitsu.jp/diary/20080722.html
	my @emnetcidr = (
	"60.254.209.99/32",
	"117.55.1.224/27"
	);
	# CIDR���X�g�����炩���ߓo�^���Ă���
	# �������Ă������ƂŁA�d����������bbs.cgi�o�q����1��ōς�
	foreach (@emnetcidr) {
		$FOX->{EMNETCIDR}->add($_);
	}

	################################################################
	# AIR-EDGE PHONE�pIP�A�h���X�u���b�N�֘A
	################################################################
	$FOX->{AIREDGECIDR} = Net::CIDR::Lite->new;

	# IP�A�h���X�u���b�N�ꗗ(CIDR�`��)
	# �A�h���X�����W���ǉ����ꂽ�ꍇ�A�����ɉ����Ă���
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
	# CIDR���X�g�����炩���ߓo�^���Ă���
	# �������Ă������ƂŁA�d����������bbs.cgi�o�q����1��ōς�
	foreach (@airedgecidr) {
		$FOX->{AIREDGECIDR}->add($_);
	}

	################################################################
	# AIR-EDGE MEGAPLUS�pIP�A�h���X�u���b�N�֘A
	################################################################
	$FOX->{MEGAPLUSCIDR} = Net::CIDR::Lite->new;

	# IP�A�h���X�u���b�N�ꗗ(CIDR�`��)
	# �A�h���X�����W���ǉ����ꂽ�ꍇ�A�����ɉ����Ă���
	#
	# �yBBQ 7�{�ځz���J���o�^�� �y�s���|�C���g�K���z
	# http://qb5.2ch.net/test/read.cgi/sec2chd/1123932393/908-918
	# �ɂ��A���݂�222.13.35.0/24��o�^
	#
	# �����[�gIP�A�h���X�����̃����W�������ꍇ�AfoxSetHost �ŁA
	# Client_IP �w�b�_��ǂ݁A������R����̓����������
	my @megapluscidr = (
	"222.13.35.0/24"
	);
	# CIDR���X�g�����炩���ߓo�^���Ă���
	# �������Ă������ƂŁA�d����������bbs.cgi�o�q����1��ōς�
	foreach (@megapluscidr) {
		$FOX->{MEGAPLUSCIDR}->add($_);
	}

	################################################################
	# ibisBrowser�pIP�A�h���X�u���b�N�֘A
	################################################################
	$FOX->{IBISBROWSERCIDR} = Net::CIDR::Lite->new;

	# IP�A�h���X�u���b�N�ꗗ(CIDR�`��)
	# �A�h���X�����W���ǉ����ꂽ�ꍇ�A�����ɉ����Ă���
	# http://ibis.ne.jp/support/browserIP.jsp
	my @ibisbrowsercidr = (
	"59.106.88.0/24"
	);
	# CIDR���X�g�����炩���ߓo�^���Ă���
	# �������Ă������ƂŁA�d����������bbs.cgi�o�q����1��ōς�
	foreach (@ibisbrowsercidr) {
		$FOX->{IBISBROWSERCIDR}->add($_);
	}

	################################################################
	# jig Browser�pIP�A�h���X�u���b�N�֘A
	################################################################
	$FOX->{JIGBROWSERCIDR} = Net::CIDR::Lite->new;

	# IP�A�h���X�u���b�N�ꗗ(CIDR�`��)
	# �A�h���X�����W���ǉ����ꂽ�ꍇ�A�����ɉ����Ă���
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
	# CIDR���X�g�����炩���ߓo�^���Ă���
	# �������Ă������ƂŁA�d����������bbs.cgi�o�q����1��ōς�
	foreach (@jigbrowsercidr) {
		$FOX->{JIGBROWSERCIDR}->add($_);
	}

	################################################################
	# �\�t�g�o���N���o�C�� iPhone�pIP�A�h���X�u���b�N�֘A
	################################################################
	# 2ch�����^�T�[�o�E���P�[�V�����\�z��� Part29
	# http://qb5.2ch.net/test/read.cgi/operate/1212665493/850-852
	# �Ƃ肠�������Ή� -- 2008/7/15 by ��
	# http://qb5.2ch.net/test/read.cgi/operate/1267711917/639
	# 126.230.0.0/15 �� 126.232.0.0/13 ��ǉ� -- 2010/4/10 by ��
	$FOX->{IPHONECIDR} = Net::CIDR::Lite->new;
	my @iphonecidr = (
	"126.230.0.0/15",
	"126.232.0.0/13",
	"126.240.0.0/12"
	);
	# CIDR���X�g�����炩���ߓo�^���Ă���
	# �������Ă������ƂŁA�d����������bbs.cgi�o�q����1��ōς�
	foreach (@iphonecidr) {
		$FOX->{IPHONECIDR}->add($_);
	}

	#�Ⴞ��܃T�[�o�ł́A�����̍L���͓ǂ܂Ȃ��Ă���
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

	#�t�b�^�[�i���̍L���j
	$FOX->{footad} = ''	;
	$FOX->{topad} = ''	;
	$FOX->{lastad} = ' �y�[�W�̂����܂�����B�B��';

	#�f���ꗗ�\�̕\��
	#�Ⴞ��܂ł͂���ł͂Ȃ��Abbsd���\�����Ă���̂Œ���
	$FOX->{links} = '<Center><a href="http://menu.2ch.net/bbstable.html" Target=_blank>��<b>�f���ꗗ</b>��</a></Center>';

	#�Q�����˂���ʃ����N
	#�Ⴞ��܂ł͂���ł͂Ȃ��Abbsd���\�����Ă���̂Œ���
	$FOX->{specialad} = ' | <a href="http://irc.2ch.net">�`���b�g</a>';

	# �ȉ��̂��̂͐Ⴞ��܂ł��ǂ܂Ȃ��Ƃ���

	#�K���p�t�@�C��(��)
	if(open(ADFILE, 'proxy998.cgi'))
	{
		@FOX_K998 = <ADFILE>	;
		close(ADFILE)		;
	}

	#�K���p�t�@�C��(�v���o�C�_)
	if(open(ADFILE, 'proxy999.cgi'))
	{
		@FOX_K999 = <ADFILE>	;
		close(ADFILE)		;
	}

	#�K���p�t�@�C��(Rock54)
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
	#���������X�g(4vip)
	if(open(ADFILE, '/md/tmp/nanashi.txt')
	 ||open(ADFILE, 'nanashi.txt'))
	{
		while (<ADFILE>)
		{
			chomp		;
			push(@FOX_774, $_);      # �Ō�ɗv�f��ǉ�����
		}
		close(ADFILE)		;
	}
	# �I���p
	#@FOX_774 = (
	#	"���������񁗂������I���ɍs����(a)",
	#	"���������񁗂������I���ɍs����(a)"
	#);

	#�������b�N�A�b�v asahi-net
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

	#�������b�N�A�b�v dion
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
#�V�O�i���Ώ��֐�
#==================================================
sub SigExit
{
	exit(0);
}
#==================================================
#�@���������擾�i�o�n�r�s�j
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

	#���ϐ�����o�n�r�s�̂Ł[�������炤�`
	if(!$GB->{TBACK} && $ENV{REQUEST_METHOD} eq 'POST')	#TBACK ���͓ǂ܂Ȃ�
	{
		use Fcntl qw(F_GETFL F_SETFL O_NONBLOCK);
		local $/;
		$ENV{CONTENT_LENGTH} > 65535
			and &DispError2($GB,'�d�q�q�n�q�I','�d�q�q�n�q�F�������I');

		# POST �f�[�^���M�Ɏ��Ԃ������� DoS �U���ɑ΂� robust ��
		my ($timeout, $len, $fdset, $stdin, $ptime) = (8, $ENV{CONTENT_LENGTH}, '', '', time);
		vec($fdset, fileno STDIN, 1) = 1;
		fcntl(STDIN, F_SETFL, O_NONBLOCK | fcntl(STDIN, F_GETFL, 0));
		while ($len && $timeout > 0) {
			my ($l, $s, $t);
			select($fdset, undef, undef, $timeout)
				# sysread() �̕����������� SpeedyCGI ���ƃ_��
				and $l = read(STDIN, $s, $len)
				or last;
			$len -= $l;
			$stdin .= $s;
			$timeout -= ($t = time) - $ptime;
			$ptime = $t;
		}
		# DoS �Ǝv����ꍇ�͂Ƃ肠�����L�^
		if (!vec($fdset, fileno STDIN, 1) && open(local *F, '>>', "/var/tmp/dos.post.$ENV{SERVER_NAME}")) {
			local $\ = "\n";
			print F strftime('[%F %T] ', localtime $ptime), $ENV{REMOTE_ADDR},
				' <> ', map "$_=$ENV{$_}, ", grep /^HTTP_/, keys %ENV;
			close F;
			&DispError2($GB,'�d�q�q�n�q�I','�d�q�q�n�q�F���e�������悤�I');
		}

		foreach (split(/&/, $stdin)) {
			(my $name, $_) = split(/=/, $_, 2);
			next unless (defined $_);
			$_ = $jcode->set(\$_, 'utf8')->sjis if (ref $jcode);
			tr/+/ /;
			s/%([[:xdigit:]]{2})/pack('H2', $1)/eg;
			# �g���b�v�L�[�� "as is" ��
			if ($name eq 'FROM') {
				require "jcode.pl";
				&jcode::tr(\$_, '��', '#');
				($_, $GB->{TRIPKEY}) = split(/#/, $_, 2);
			}
			# s/"/&quot;/g;
			s/</&lt;/g;
			s/>/&gt;/g;
			tr/\t/ /;
			s/\r\n?|\n/<br>/g;
			# �]�v�ȋ󔒒ǉ���}��......�������@��ɉe���H
			# s/(?<=[\x80-\xFF])<br>/ <br>/g;
			s/<br>/ <br> /g;
			# \x00 �� [[:cntrl:]]
			s/[[:cntrl:]]//g;

			$FORM->{$name} = $_;
		}
	}

	#�P�s�f�[�^����͉��s������ă^�O����܂�
	$FORM->{'subject'} =~ s/ ?<br> ?//g;
	$FORM->{'subject'} =~ s/&(?!(?:quo|[lg])t;)/&amp;/g;

	$FORM->{'FROM'} =~ s/ ?<br> ?//g;
	$FORM->{'mail'} =~ s/ ?<br> ?//g;
	$FORM->{'mail'} =~ s/"/&quot;/g;

	$FORM->{'bbs'} =~ s/\W//g;
	$FORM->{'key'} =~ s/\D//g if (defined $FORM->{'key'});
	$FORM->{'time'} =~ s/\D//g;

	$FORM->{'FROM'} =~ s/&r/&amp;r/g;
# BadTripCheck �ŎE���Ă���̂ŕs�v
#	$FORM->{'FROM'} =~ s/usubon//g;
	$FORM->{'mail'} =~ s/&r/&amp;r/g;

	# foxIkinari�̏����ƌ݊��ɂ��� (�Z�L�����e�B����{���� " �͊댯)
	# $FORM->{'MESSAGE'} =~ s/"/&quot;/g; <- foreach ���[�v���ɓ���

####cookie
{
	#// �N�b�L�[�擾
	foreach (split(/[&,;]\s*/, $ENV{HTTP_COOKIE} || '')) {
		(my $key, $_) = split(/=/, $_, 2);
		$GB->{COOKIES}{$key} = $_ if (defined $_ && !exists $GB->{COOKIES}{$key});
	}
	$FORM->{'DMDM'} = $GB->{COOKIES}{DMDM} || '';
	$FORM->{'MDMD'} = $GB->{COOKIES}{MDMD} || '';

#&DispError2($GB,"FOX ��","<font color=green>FOX ���@�ӂӂӂ�</font><br><br>DMDM[$FORM->{'DMDM'}] ,MDMD[$FORM->{'MDMD'}]");
}
#�ł��@���ڎw�肪��������㏑��
if($FORM->{'BEmailad'} && $FORM->{'BEcode32'})
{
	$FORM->{'DMDM'} = $FORM->{'BEmailad'};
	$FORM->{'MDMD'} = $FORM->{'BEcode32'};
}
#####
#�����΍�
if($ENV{HTTP_USER_AGENT} =~ /�ޏ�/)
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
#�@�G���[��ʁi�G���[�����j
#==================================================
sub DispError2
{
	my ($GB, $title, $topic) = @_;

	if($GB->{TBACK} && $ENV{SERVER_NAME} !~ /qb6/){&TBackerrEnd;}	#TBACK �� XML

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
<br>�z�X�g<b>$GB->{HOST}</B><br><b>$GB->{FORM}->{'subject'} </b><br>
���O�F <b>$GB->{FORM}->{'FROM'}</b><br>E-mail�F $GB->{FORM}->{'mail'}<br>
���e�F<br>$GB->{FORM}->{'MESSAGE'}<br><br>
</ul>
<a href="http://ula.cc/2ch/sec2ch.html">�� �A�N�Z�X�K�����ł���������� ��</a><br><br>
<hr>
������Ń����[�h���Ă��������B<a href="../$GB->{FORM}->{'bbs'}/index.html"> GO! </a><br>
�A�N�Z�X�K���E�v���L�V�[�������K���́A<a href="http://2ch.tora3.net/">�Q�����˂�r���[�A</a>
���g���Ɖ���ł��܂��B<p>
�����ŉ������Ă݂悤! <a href="http://www.2ch.net/help.html">�������߂Ȃ����̑����\\</a><br>
������Ȃ����Ƃ���������<a href="http://info.2ch.net/guide/">�Q�����˂�K�C�h</a>�ցB�B�B<br><br>

<p>
</body>
</html>
EOF
#<font color=red>�r���o��</font><br>
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
#�@�g�їp�K��\��&�G���[��ʁi�G���[�����j
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
<a href="http://2ch.net/">�Q�����˂�</a><br>
<font color=red>$topic</font><br>
<hr>
<font color=red>���e�m�F</font><br>
�E���e�҂́A���e�Ɋւ��Ĕ�������ӔC���S�ē��e�҂ɋA�����Ƃ��������܂��B<br>
�E���e�҂́A�b��Ɩ��֌W�ȍL���̓��e�Ɋւ��āA�����̔�p���x�������Ƃ��������܂�<br>
�E���e�҂́A���e���ꂽ���e�y�т���Ɋ܂܂��m�I���Y���A�i���쌠�@��21���Ȃ�����28���ɋK�肳��錠�����܂ށj ���̑��̌����ɂ��i��O�҂ɑ΂��čċ������錠�����܂݂܂��B�j�A�f���^�c�҂ɑ΂��A�����ŏ��n���邱�Ƃ� �������܂��B�������A���e���ʂɒ�߂�폜�K�C�h���C���ɊY������ꍇ�A���e�Ɋւ���m�I���Y�����̑��̌����A �`���͈����ԓ��e�҂ɗ��ۂ���܂��B<br>
�E�f���^�c�҂́A���e�҂ɑ΂��ē��{�����O�ɂ����Ė����Ŕ�Ɛ�I�ɕ����A���O���M�A �Еz�y�і|�󂷂錠���𓊍e�҂ɋ������܂��B�܂��A���e�҂͌f���^�c�҂��w�肷���O�҂ɑ΂��āA��؂̌����i��O�҂ɑ΂��čċ������錠�����܂݂܂��j���������Ȃ����Ƃ��������܂��B<br>
�E���e�҂́A�f���^�c�҂��邢�͂��̎w�肷��҂ɑ΂��āA����Ґl�i������؍s�g���Ȃ����Ƃ��������܂��B<br>
<hr>
���ӂ����������A�߂��čē��e���Ă��������B(��)<br><hr>
�J������<br>
<input type=checkbox >���ӂ���<br>
���O�F<input type=text size=15 name="FROM" value="$GB->{FORM}->{'FROM'}"><br>
E-ma�F<input type=text size=15 name="mail" value="$GB->{FORM}->{'mail'}"><br>
<textarea name="MESSAGE" rows=5>
$GB->{FORM}->{'MESSAGE'}
</textarea>
</body>
</html>
EOF
#<font color=red>�r���o��</font><br>
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
# ���e�m�F��ʂ��`�F�b�N��������������Ă��邩�ǂ������ׂ�
# ���̎����� namazuplus �Ŏg�p���Ă���
# ����: $GB
# �߂�l: 0: �����Ă��Ȃ�(�ʏ�)�A1: �����Ă���
#############################################################################
sub KPinCheck
{
	my ($GB) = @_;

	# �u��{�͂��葫�v�̎����������Ă���
	if(($GB->{FORM}->{$GB->{KPIN1}} || '') eq $GB->{KPIN2})	{return 1;}

	# ����ȊO
	return 0;
}
#############################################################################
# �u�����Ȃ�v�`�F�b�N���郋�[�`��
# ���j�I����������񂠂�悤�Ȃ̂ŁA�X�V���ɂ͒��ӂ��邱��
#############################################################################
sub foxIkinari
{
	my ($GB) = @_;

	if($ENV{PATH_INFO})	{return "127.0.0.101";}

	# �ŋ߂̑f��IE8��UA���ƂĂ������̂ŁA256�ł͂�����
	if(length($ENV{'HTTP_USER_AGENT'}) > 384)
	{
		print "Content-type: text/html; charset=shift_jis\n\n";
print <<EOF;
<html><head><title>�������݂܂����B</title><meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS"></head><body>�������݂��I���܂����B<br><br>��ʂ�؂�ւ���܂ł��΂炭���҂��������B<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}</body></html>
EOF
		exit;
	}
	if($ENV{'HTTP_USER_AGENT'} =~ />>/)
	{
		print "Content-type: text/html; charset=shift_jis\n\n";
print <<EOF;
<html><head><title>�������݂܂����B</title><meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS"></head><body>�������݂��I���܂����B<br><br>��ʂ�؂�ւ���܂ł��΂炭���҂��������B<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}<br><br>$ENV{'HTTP_USER_AGENT'}</body></html>
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
<html><head><title>�������݂܂����B</title><meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS"></head><body>�������݂��I���܂����B<br><br>��ʂ�؂�ւ���܂ł��΂炭���҂��������B</body></html>
EOF

			exit;
		}
	}

	# �g�т���̏������݂̓X���[
	# �܂����̎��_�ł�IsIP4Mobile�͎g���Ȃ�
	# ���Ƃ��Ƃ����Ȃ��Ă����킯�����ǁAUA�ł͂�肽���Ȃ��Ȃ�

	# ������̓��t�@�����N�b�L�[�������������Ȃ����Ƃɂ��Ă���
	if($ENV{'HTTP_USER_AGENT'} =~ /DoCoMo|J-PHONE|Vodafone|SoftBank|UP.Browser|KDDI/)	{
		return $HOST;
	}

	# ���ۂ�4�@��̓��t�@���͓f���Ȃ����ǁA�N�b�L�[�͐H�ׂ�
	if($ENV{'HTTP_USER_AGENT'} !~ /AH-J3001V|AH-J3002V|AH-J3003S|WX220J/)
	{
		# ���t�@���`�F�b�N(�����Ȃ�)
		#if($ENV{'HTTP_REFERER'} !~ /^http:\/\/$ENV{'HTTP_HOST'}\//)
		if($ENV{'HTTP_REFERER'} !~ m#^http://(?:[-\w]+\.)?(?:2ch\.net|bbspink\.com|ula\.cc|u\.la|s2ch\.net|orz\.2ch\.io)/#)
		{
			print "Content-type: text/html; charset=shift_jis\n\n";
			print <<EOF;
<html><head><title>�d�q�q�n�q�I</title><meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS"></head><body>�d�q�q�n�q�Freferer��񂪕ςł��B(ref1)$ENV{'HTTP_REFERER'}</body></html>
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

	# PON �� HAP ��ێ����Ă���
	$GB->{PON}  = $HOST;
	$GB->{PONX} = "PON=$HOST";
	$GB->{HAP}  = $hap;
	$GB->{HAPX} = "HAP=$hap";

	# PON ���Ȃ���΁A�Ƃ肠�����Ĕ��s����
	if(($GB->{COOKIES}{PON} || '') ne $GB->{PON})
	{
		# PON �𔭍s����(����ɗL���ɂȂ�)
		print "Set-Cookie: $GB->{PONX}; expires=$FOX->{COOKIEEXPIRES}; path=/\n";
	}
	else
	{
		# PON �������Ă���
		$GB->{PONOK} = 1;
	}

	# Mozilla/4.0 �ł͂Ȃ��ꍇ�AHAP �͗L���������Ƃ݂Ȃ�
	# (�����Ȃ��Ă���)
	if($ENV{'HTTP_USER_AGENT'} !~ /Mozilla\/4\.0/)
	{
		$GB->{HAPOK} = 1;
	}

	# HAP ���Ȃ��ꍇ or �ς���Ă�����Ĕ��s����
	if(($GB->{COOKIES}{HAP} || '') ne $GB->{HAP})
	{
		# �V���� HAP �𔭍s����(����ɗL���ɂȂ�)
		print "Set-Cookie: $GB->{HAPX}; expires=$FOX->{COOKIEEXPIRES}; path=/\n";
	}
	else
	{
		# HAP �͗L��������������(�O�� HAP �ƈ�v����)
		$GB->{HAPOK} = 1;
	}

	# �@�I�ȓ��e�m�F��ʂ̕\�� & exit;
	&HoutekiToukouKakunin($GB);

	# ����P�[�X(�Ȃ��������Ă��邩�͂悭�킩��Ȃ�����)
	if($GB->{FORM}->{'bbs'} =~ /style\=/){exit;}

	return $HOST;
}
#############################################################################
# �@�I�ȓ��e�m�F��ʂ̕\��
#############################################################################
sub HoutekiToukouKakunin
{
	my ($GB) = @_;

	# �X�L�b�v�̎����������Ă���ꍇ�̓X���[
	if($GB->{KPASS})	{return 0;}

	# �V�K�X���b�h�쐬���(BBS_PASSWORD_CHECK)�̍ۂ̑΍�
	#   foxReadSettings �̑O�Ȃ̂ŁASETTING.TXT �̓��e��
	#   �܂������ł͎Q�Ƃł��Ȃ�
	# �X���^�C���Ȃ��āA
	if(!($GB->{FORM}->{'subject'} ne ""))
	{
		# ���A�L�[��񂪒�`����Ă��Ȃ��ꍇ�ɂ́A
		if(!defined($GB->{FORM}->{'key'}))
		{
			# �����͑f�ʂ肳���AfoxSetInformation �Ń`�F�b�N����
			# ����� &newbbs ���Ă΂�� or
			# �u�T�u�W�F�N�g�����݂��܂���v�G���[�ɂȂ邱�ƂɂȂ�
			return 0;
		}
	}

	# �͂Ȃ����� Cookie ���L�����ǂ���
	my $isvalidPIN = ($GB->{COOKIES}{$GB->{PIN1}} || '') eq $GB->{PIN2};

	# PON �� HAP ���L������Ȃ��Ƃ���(�K�{)
	if($GB->{PONOK} && $GB->{HAPOK})
	{
		# �͂Ȃ�����̎����������Ă���
		if(($GB->{FORM}{$GB->{PIN1}} || '') eq $GB->{PIN2})	{return 0;}
		# �͂Ȃ�����N�b�L�[�������Ă���(�������ԓ��ɓ��e�������Ƃ�����)
		if($isvalidPIN)	{return 0;}
	}

	# �t�H�[���̎��Ԃ��Z�b�g����(�\�������Ŏg�p���Ă���)
	$GB->{FORM}->{'time'} = time;

	# <br> �Ƃ����o�Ȃ��悤�ɁA�ꎞ�I�� foxReadForm �ŉ��H�������߂�
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

	# �w�b�_��\�����āA�A�A
	print "Content-type: text/html; charset=shift_jis\n\n";

	# ���e�m�F��ʂ�\������
	my @kakuningamen0 = (
	qq|<html><!-- 2ch_X:cookie -->|,
	qq|<head>|
	);
	&PutLines(*STDOUT, @kakuningamen0);

	# �E�C���X����(DoS)�Ή�(comic6�����^�C�g����ς��Ă݂�)
	my $kakunintitle = qq|<title>�� �������݊m�F ��</title>|;
	if($ENV{SERVER_NAME} =~ /comic6/)
	{
		$kakunintitle = qq|<title>�� �������݂̊m�F ��</title>|;
	}
	&Put1Line(*STDOUT, $kakunintitle);

	my $submitButton = $isvalidPIN ? '�m�F���ď�������' : '��L�S�Ă��������ď�������';

	my @kakuningamen = (
	qq|<META http-equiv="Content-Type" content="text/html; charset=x-sjis">|,
	qq|<meta name="viewport" content="width=device-width,initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.6,user-scalable=yes" />|,
	qq|</head>|,

	qq|<body bgcolor=#EEEEEE>|,
	qq|<font size=+1 color=#FF0000><b>�������݁��N�b�L�[�m�F</b></font>|,
	qq|<ul><br><br>|,
	qq|<b>$GB->{FORM}->{'subject'} </b><br>|,
	qq|���O�F $GB->{FORM}->{'FROM'}<br>|,
	qq|E-mail�F $GB->{FORM}->{'mail'}<br>|,
	qq|���e�F<br>$GB->{FORM}->{'MESSAGE'}<br><br></ul>|,
	# ���̕��ʂ͂͂Ȃ����� Cookie ���Ȃ��������o��
	!$isvalidPIN ? (
		qq|<b>|,
		qq|���e�m�F<br>|,
		qq|�E���e�҂́A���e�Ɋւ��Ĕ�������ӔC���S�ē��e�҂ɋA�����Ƃ��������܂��B<br>|,
		qq|�E���e�҂́A�b��Ɩ��֌W�ȍL���̓��e�Ɋւ��āA�����̔�p���x�������Ƃ��������܂�<br>|,
		qq|�E���e�҂́A���e���ꂽ���e�y�т���Ɋ܂܂��m�I���Y���A�i���쌠�@��21���Ȃ�����28���ɋK�肳��錠�����܂ށj|,
		qq|���̑��̌����ɂ��i��O�҂ɑ΂��čċ������錠�����܂݂܂��B�j�A�f���^�c�҂ɑ΂��A�����ŏ��n���邱�Ƃ�|,
		qq|�������܂��B�������A���e���ʂɒ�߂�폜�K�C�h���C���ɊY������ꍇ�A���e�Ɋւ���m�I���Y�����̑��̌����A|,
		qq|�`���͈����ԓ��e�҂ɗ��ۂ���܂��B<br>|,
		qq|�E�f���^�c�҂́A���e�҂ɑ΂��ē��{�����O�ɂ����Ė����Ŕ�Ɛ�I�ɕ����A���O���M�A|,
		qq#�Еz�y�і|�󂷂錠���𓊍e�҂ɋ������܂��B�܂��A���e�҂͌f���^�c�҂��w�肷���O�҂ɑ΂��āA��؂̌����i��O�҂ɑ΂��čċ������錠�����܂݂܂��j���������Ȃ����Ƃ��������܂��B<br>#,
		qq|�E���e�҂́A�f���^�c�҂��邢�͂��̎w�肷��҂ɑ΂��āA����Ґl�i������؍s�g���Ȃ����Ƃ��������܂��B<br>|,
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
	qq|�ύX����ꍇ��|, $#ARGV >= 0 && $ARGV[0] eq 'UTF-8' ? qq|�L�����Z������| : qq|�߂�{�^���Ŗ߂���|, qq|���������ĉ������B<br><br>|,
	qq|���݁A�r�炵�΍�ŃN�b�L�[��ݒ肵�Ă��Ȃ��Ə������݂ł��Ȃ��悤�ɂ��Ă��܂��B<br>|,
	qq|<font size=-1>(cookie��ݒ肷��Ƃ��̉�ʂ͂łȂ��Ȃ�܂��B)</font><br>|,
	qq|</body>|,
	qq|</html>|,
	#qq|<!-- $ENV{'HTTP_COOKIE'} ++ SPID=$CSPID -->|
	);
	&PutLines(*STDOUT, @kakuningamen);

	# ��ʏo������ exit ���Ă��܂�
	exit;

	# return �͂��Ȃ����ǁA�ꉞ
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
# IP�A�h���X����Y�����郊���[�g�z�X�g���𓾂�
# �t�������Ȃ����IP�A�h���X�����̂܂ܕԂ�
# IPv4/IPv6���ʂŎg����͂�
#
# ����: IP�A�h���X������(REMOTE_ADDR�Ƃ�����������)
# �߂�l: �����[�g�z�X�g��(�t���������݂��Ȃ��ꍇ��IP�A�h���X)
##########################################################################
sub GetRemoteHostName
{
	my ($ipaddr) = @_;

	use Net::IP;
	use Net::DNS;

	# �z�X�g��������ϐ�
	my $hostname = undef;

	my $ip = new Net::IP($ipaddr);
	my $res = Net::DNS::Resolver->new;

	# �t�����Ɏg����`�ɂ���
	my $rev = $ip->reverse_ip();

	$res->tcp_timeout(2);
	$res->udp_timeout(2);
	$res->retry(3);

	# PTR���R�[�h����������
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
# �������̐ݒ�
# �e��PATH����
#############################################################################
sub foxSetPath
{
	my ($GB) = @_	;

	$GB->{PATH} = "../$GB->{FORM}{bbs}/";
	# �Ⴞ��܃T�[�o�������[�N�G���A��ʂɂƂ�
	if(IsSnowmanServer == BBSD->{REMOTE})
	{
		# ���[�U����getpwuid�łƂ��Ă���
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

	# �Ⴞ��܃T�[�o�ł͈��̃f�B���N�g�������Ȃ�
	if(IsSnowmanServer != BBSD->{REMOTE})
	{
		my $ggg = "../../test/ggg/";
		unless(-e $ggg){
			# �ŏ���umask(0)���Ă���̂ŕs�v
			#umask(0);
			mkdir($ggg,0777);
		}
	}

$GB->{DEBUG} .= "�e��o�`�s�g���� PATH=$GB->{PATH}<br>";
}

=begin comment

bbsd �֘A�̏����� BBSD.pm �Ɉ�C�̂��߃R�����g�A�E�g
#############################################################################
# �������݁EID�̎폈���p��bbsd���Ăяo��
#############################################################################
sub bbsd
{
#	my (@Argv) = @_;

#	return &bbsd_main(0, @Argv);
	return &bbsd_main(0, @_);
}
#############################################################################
# DB�����p��bbsd���Ăяo��
#############################################################################
sub bbsd_db
{
#	my (@Argv) = @_;

#	return &bbsd_main(1, @Argv);
	return &bbsd_main(1, @_);
}
#############################################################################
# bbsd�Ƃ̊Ԃ̒ʐM���s��
# �t���O: 0: �������݁EID�̎�̏����A1: DB����
#############################################################################
sub bbsd_main
{
#	my ($flag, @Argv) = @_;
	my $flag = shift;

	use Socket;

	# �₢���킹��IP�A�h���X�A�|�[�g�ԍ��A�^�C���A�E�g�l
	my $BBSD_HOST    = undef;
	my $BBSD_PORT    = undef;
	my $BBSD_TIMEOUT = undef;

	# �t���O�ɂ��Ăԃz�X�g�̃p�����[�^��ύX����
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
# bbsd�̃^�C���A�E�g���ǂ����`�F�b�N
# ����: $GB, bbsd�̖߂�l
#############################################################################
sub bbsd_TimeoutCheck
{
	my ($GB, $errmsg) = @_;

	if($errmsg eq (local $! = ETIMEDOUT))
	{
		return 1;
	}

	# ����ȊO�͖߂�
	return 0;
}
#############################################################################
# bbsd�̃^�C���A�E�g�G���[�̏���
# ����: $GB, ���b�Z�[�W�ɏo�͂��邽�߂̃R�}���h��
#############################################################################
sub bbsd_TimeoutError
{
	my ($GB, $cmd) = @_;

	&DispError2($GB, '�d�q�q�n�q�I', "�d�q�q�n�q�F�o�b�N�G���h�T�[�o�Ƃ̒ʐM���^�C���A�E�g���܂���($cmd)�B�������݂����f����Ă��Ȃ���������܂���B");

	# ��������߂邱�Ƃ͂Ȃ�(���A�ꉞ)
	return 0;
}
#############################################################################
# �w�肵���t�@�C���n���h����1�s�o�͂���
# �g����: &Put1Line(*FILE, $str);
#############################################################################
sub Put1Line
{
	local (*FD) = shift;

	print FD @_;

	return 0;
}
#############################################################################
# �w�肵���t�@�C���n���h���ɕ����s�o�͂���
# �g����: &PutLines(*FILE, @str);
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
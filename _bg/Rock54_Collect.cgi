#!/usr/bin/perl --

# R54_Collect.cgi
# Rock54.txt ������Ă��鑕�u
=comment
2.00	2008/02/24	���t�ǂ��
2.01	2008/12/29	����H�Ȃ񂾂����B�B�B
2.02	2009/06/28	update���̃��X�|���X�w�b�_���������������̂ŉ��
2.03	2010/01/03	���t�ǂ��PASS���ĂȂ񂾂����H�i���j�ƁA�A�A���@�̃`�F�b�N�i��΁j
=cut

use LWP::UserAgent;
use strict;

# �������g�̖��O
my $My_name = "Rock54_Collect";
my $Version = '2.03(2010/01/03)';

# FreeBSD �ł͂������Ȃ��Ǝ~�܂����Ⴄ�݂����B�B�B
$SIG{'ALRM'} = "IGNORE";

# ����Ă������X�g��ݒu����ꏊ�B
my $Collect_PATH = '.';
my $Rock54_Text = "$Collect_PATH/Rock54.txt";

# rock54 �I��URI
my $Rock54_server_name = "rock54.2ch.net";

# rock54 �I�ւ̃��N�G�X�g
my $Collect_URI = "Rock54/_Collect/Rock54.txt";

# rock54 �I�ւ̃��N�G�X�g�i Rock54_Collect.cgi �擾�p�j
my $CollectCGI_URI = "Rock54/_Collect/Rock54_Collect.txt";

# LWP::UserAgent�I�u�W�F�N�g
my $UserAgent = LWP::UserAgent->new(
	agent           => "Monazilla/1.00 Rock54_Collect (+http://rock54.2ch.net/)",
	timeout         => 5,
);

# �t�@�C���n���h���p
my $FileHandle;

# �擾���t���O�p
my $GetList;

# HTML �e���v���[�g�B
my %Html;

# --- �����܂�̃��v���C���b�Z�[�W�̃G���e�B�e�B�w�b�_�Ƃ�
$Html{content} = <<"EOS";
Content-type: text/html; charset=Shift_JIS
Rock54-Collect-Version: %s
Rock54-Collect-Status: %s

EOS

# --- HTML�w�b�_�����isprintf�ŏo�͂��邱�Ɓj
$Html{header}  = <<"EOS";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="ja">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<meta http-equiv="Content-Style-Type" content="text/css">
<link rel="start" href="/index.html">
<style type="text/css">
<!--
	BODY       { background: #FEFEFE; color: #000; margin: 10px; }
	ADDRESS    { text-align: right; }

-->
</style>
<title>Rock54_Collect $Version</title>
</head>

EOS

# --- �Ō�̂Ƃ���
$Html{footer} =<<"EOS";
<address>Rock54_Collect $Version</address>
</body>
</html>
EOS

# �����Ȃ�͂�ǂ炟
{
	$SIG{'PIPE'} = $SIG{'INT'} = $SIG{'HUP'} = $SIG{'QUIT'} = $SIG{'TERM'} = \&SigExit;
}

# �~�߂�ꂽ�Ƃ�
sub SigExit{
	Error("94", shift);
}

# �G���[
sub Error{
	my $number = shift;
	my $err    = shift;
	my %Messages = (
		'00',"�Ƃ��ķ�������(߁��)�������!!",
		'01',"�Ƃ��ķ�����������(߁��)�������!!!",

		'90',"���������n�Q���ˁB",
		'91',"�Ƃ�܂���ł���[01]�i�L�E�ցE�M�j���ް�",
		'92',"�Ƃ�܂���ł���[02]�i�L�E�ցE�M�j���ް�",
		'93',"�Ƃ�܂���ł���[03]�i�L�E�ցE�M�j���ް�",
		'94',"�Ƃ�܂���ł���[04]�i�L�E�ցE�M�j���ް�",

		'95',"�Ƃ�܂���ł���[05]�i�L�E�ցE�M�j���ް�",
		'96',"�Ƃ�܂���ł���[06]�i�L�E�ցE�M�j���ް�",
		'97',"�Ƃ�܂���ł���[07]�i�L�E�ցE�M�j���ް�",
		'98',"�Ƃ�܂���ł���[08]�i�L�E�ցE�M�j���ް�",
		'99',"---- $err",
	);
	my %Response = (
		'00','Complete',
		'01','Complete+',

		'90','Forbbiden',
		'91','Error[$err]',
		'92',"Error[write $err]",
		'93',"Error[rename $err]",
		'94',"Error[SIG $err received]",

		'95',"Error[updateCGI $err]",
		'96',"Error[renameCGI $err]",
		'97',"Error[getCGI1 $err]",
		'98',"Error[getCGI2 $err]",
		'99',"----",
	);

	$Html{message}  = sprintf $Html{content}, $Version, $Response{$number} ;
	$Html{message} .= $Html{header};

	$Html{message} .= <<"EOS";
<body>
<h1>Rock54_Collect</h1>
<p>$Messages{$number}</p>
$Html{footer}
EOS
#	$| = 1; # ���ꗬ�����~�߂Ă݂�B
	print $Html{message};
	exit;
}

################################################################################
# ��������B
MAIN:
{
	# �Ăяo�����l�̃`�F�b�N���낢��B
	$ENV{REMOTE_HOST} eq ''               and
#	$ENV{REMOTE_ADDR} ne '206.223.147.35' and # banana238
	$ENV{REMOTE_ADDR} ne '206.223.151.67' and # tiger509
#	$ENV{REMOTE_ADDR} ne '192.168.1.21'   and # baila6.jp�p
		Error('90');

	 Error('90') unless $ENV{HTTP_USER_AGENT} eq "Monazilla/1.00 Rock54_Summon (+http://rock54.2ch.net/)"
		or $ENV{HTTP_USER_AGENT} eq "Monazilla/1.00 Rock54_Cron (+http://rock54.2ch.net/)";

	# ���� Rock54.txt �����ɍs���B
	# $UserAgent->default_header('Authorization' => 'Basic Q29sbGVjdDpkZWNjaURvbg==');
	# BASIC�F��
	$UserAgent->credentials("$Rock54_server_name:80", "Entrance Rock54", "Collect", "borracho");

	my $Response = $UserAgent->get("http://$Rock54_server_name/$Collect_URI");
	# ����荞�ݐ���
	if ($Response->is_success) {
		my $Get_Rock54list = $Response->content;

		# �����ŏ�������
		open   $FileHandle, ">$Rock54_Text.tmp" or Error('92', $!); # �擾�Ɏ��s
		print  $FileHandle $Get_Rock54list;
		close  $FileHandle;

		# ���O������������B
		rename "$Rock54_Text.tmp", $Rock54_Text or Error('93', $!); # ���O�ύX�Ɏ��s
		$GetList = 1; # �擾�n�j
	}
	else {
		Error('91',$Response->status_line); # �擾�Ɏ��s
	}

	# Rock54_Collect.cgi �̍X�V��񂪗L��΂�������ɍs���B
	if ($ENV{QUERY_STRING} eq 'update') {
		# ���� Rock54_Collect.cgi �����ɍs���B
		my $Response = $UserAgent->get("http://$Rock54_server_name/$CollectCGI_URI");

		# ����荞�ݐ���
		if ($Response->is_success) {
			my $Get_Rock54_CollectCGI = $Response->content;

			# �����ŏ�������
			open  $FileHandle, ">$Collect_PATH/$My_name.txt" or Error('95', $!); # �擾�Ɏ��s;
			print $FileHandle $Get_Rock54_CollectCGI;
			close $FileHandle;

			# ���݂̃p�[�~�b�V�������擾
			my $CGI_Permission = (stat "$Collect_PATH/$My_name.cgi")[2];

			# ���@�e�X�g
			my $Perl_Response = system 'perl', '-wc', "./$My_name.txt";
			Error('98', $Perl_Response) if $Perl_Response;

			# ���O��������
			rename "$Collect_PATH/$My_name.txt", "$Collect_PATH/$My_name.cgi" or Error('96', $!); # ���O�ύX�Ɏ��s
			chmod $CGI_Permission, "$Collect_PATH/$My_name.cgi"; # �p�[�~�b�V���������킹��B
			$GetList = 2; # �擾�n�j
		}
		else {
			# ����荞�݂Ɏ��s�����牽�����Ȃ��B
			Error('97',$Response->status_line); # �擾�Ɏ��s
		}
	}

	Error('00') if $GetList == 1; # ���X�g�̂ݎ擾����
	Error('01') if $GetList == 2; # ���X�g�{���t�ǂ�擾����

	# �����܂��B
	exit;
}

__END__

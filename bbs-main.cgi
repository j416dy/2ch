use strict 'vars';
use File::stat;
use POSIX qw(:errno_h strftime);
use BBSD;

# �Â��̂� old �ɓ��ꂽ���[ by ��
# �����ł� by ��

# 070320  �g�тƌg�їp�u���E�U(ibis/jig)�ł͕ςȃz�X�g���K���Ȃ� by ��
# 070425  jig�u���E�U��CIDR�u���b�N�ǉ� by ��
# 070719  Willcom/EZweb/i���[�h��CIDR�u���b�N�ǉ� by ��
# 070903  Willcom��CIDR�u���b�N�ǉ� by ��
# 071009  Y!�P�[�^�C��CIDR�u���b�N�ǉ��E�ύX by ��
# 071110  jig�u���E�U��CIDR�u���b�N�ǉ� by ��
# 071114  jig�u���E�U��CIDR�u���b�N�ǉ� by ��
# 071208  �Ǘ��l�̍�ƕ����𐮌`(���e�͕ύX����)
#         ibisBrowser�Q�[�g�E�F�C�p�VIP�A�h���X��o�^
#         Willcom��CIDR�u���b�N�ǉ�
#         �u�֘A�y�[�W�v�̃����N���\���� by ��
# 071209  ibisBrowser(Windows Mobile��)�ɑΉ� by ��
# 071211  be�̃A�C�R������B by ��
# 080209  ibisBrowser�Q�[�g�E�F�C�p�VIP�A�h���X��o�^ by ��
# 080214  c-others��c�ɓ������ꂽ���Ƃɔ������C by ��
#         EZweb�̃A�h���X�����W�����������ƂɑΉ� by ��
# 080216  ����P2�̐悪����������˂��܂����� by ��
# 080218  tiger2514(�Ȃ܂��̐���)��area47�\�����u�n��v�ɐݒ� by ��
# 080219  headline/BBY��DNS��V�T�[�o�Ɉڍs by ��
# 080221  stats/BBS��DNS��V�T�[�o�Ɉڍs by ��
# 080227  Willcom��CIDR�u���b�N�ǉ� by ��
# 080301  foxDNSquery���u���b�N���Ȃ�$res->bgsend�ɕύX by ��
# 080313  rock54/BBR��DNS��V�T�[�o�Ɉڍs by ��
# 080314  BBY/BBS/BBR��DNS�T�[�oIP�A�h���X��initFOX�Œ�` by ��
# 080429  SoftBank��PC�T�C�g�u���E�U�ɑΉ�(jig, ibis�Ɠ�������) by ��
# 080601  DoCoMo��i���[�hID�ɖ{�i�Ή� by ��
# 080601a i���[�hID�ւ̑Ή����t�@�C��(BBM/BBR/BBN) by ��
# 080602  i���[�h�t���u���E�U����̏������݂ɑΉ�  by ��
# 080603  ibis/jig�u���E�U��i���[�hID�Ή����ɑΉ� by ��
# 080618  Willcom��CIDR�u���b�N�ǉ� by ��
# 080711  ����p2��IP�A�h���X�ǉ� by ��
# 080714  126.240.0.0/12 ��������iPhone����̏������݂Ƃ���(ShikibetsuMark) by ��
# 080714a ��L���f�̌�AUA�o�R�𕜊�(ShikibetsuMark) by ��
# 080718  i���[�h�AEZweb��CIDR�u���b�N�ǉ� by ��
# 080723  �w�b�_�[���������Ă݂� by ��
# 080727  IPv6�ɑΉ��ABBQ��BBX�AfoxSetHost�̋����ۂ����蕔���͂Ƃ肠�����X�L�b�v by ��
# 080727a IPv6�X�����ċK���̔���� /48 �ōs���AIPv6����ID�� 48 + 16 + 64 bit �Ő��� by ��
# 080728  IPv6����ID�� ��48 + ��64 + ��64 bit �Ő��� by ��
# 080728a IPv6����ID�� ��48 + ��64 + �S128bit �Ő��� by ��
# 080728b IPv6�X�����ċK���̔���� /64 �ɖ߂��Ă݂� by ��
# 080729  GetRemoteHostName: ��ڂ� PTR ���R�[�h���������珈����ł��؂� by ��
# 080807  ula.cc/u.la/s2ch.net ���珑���Ȃ��Ȃ��������C�� by ��
# 080906  musicnews ���ʃL���b�v�� by ��
# 080911  schiphol�̔ʃL���b�v�p�~ by ��
# 080913  �ʃL���b�v���ǂ�����IsItabetsuCap�Ŕ��� by ��
# 080913  news�̃|�C���g��10000�ȏ�ɕύX by ��
# 080930  poverty�̃|�C���g��3000�ȏ�ɕύX by ��
# 081001  Willcom��CIDR�u���b�N�ǉ� by ��
# 090112  ibisBrowser����docomo�g�т̎���7����ID����Ȃ��Ƃ���(�o�O���) by ��
# 090225  jig�u���E�U��CIDR�u���b�N�ǉ� by ��
# 090324  ibisBrowser(SoftBank��)�ɑΉ� by ��
# 090330  �}�C�N���b�̎擾�� syscall ���� Time::HiRes �ɕύX by ��
# 090401  jig�u���E�U��CIDR�u���b�N�ǉ� by ��
# 090426  EZweb��CIDR�u���b�N���ŐV�łɕύX(�ǉ��ƍ폜) by ��
# 090605  jig�u���E�U��CIDR�u���b�N�ǉ��E�폜 by ��
# 090619  �g���b�v�V�������� by Sun
# 090731  emobile EMnet�ɑΉ��A�g�ш����ɁBBBM2�̑Ή��͕ʓr�K�v by ��
# 090781  emobile EMnet��BBM2�ɑΉ� by ��
# 081220  i���[�h��CIDR�u���b�N�ǉ� by ��
# 100105  Set-Cookie �L�����Ԃ̕ύX by Sun
# 100219  EZweb��CIDR�u���b�N���ŐV�łɕύX(�ǉ�) by ��
# 100320  jig�u���E�U��CIDR�u���b�N�ǉ� by ��
# 100402  stats.2ch.net (a.ns.bbs.2ch.net) ��IP�A�h���X�ύX�ɑΉ� by ��
# 100410  iPhone(panda)��CIDR�u���b�N�ǉ� by ��
# 100414  headline.2ch.net (a.ns.bby.2ch.net) ��IP�A�h���X�ύX�ɑΉ� by ��
# 100420  Y!�P�[�^�C��CIDR�u���b�N�폜�APC�T�C�g�u���E�U��CIDR�u���b�N�ύX by ��
# 100516  �Ȃ܂��̐��Ƃ�tiger2514����banana3104�ɕύX by ��
# 100517  ����p2��IP�A�h���X�ꕔ�ύX by ��
# 100526  jig�u���E�U��CIDR�u���b�N�ǉ� by ��
# 100531  live28�f�r���[�ɑΉ��A������̃X���b�h�������� live23/live24 �Ɠ����� by ��
# 100601  live28�ł�Saborin�L�� by ��
# 100602  ������̃X���b�h�����E�l�̔����ʂɈڍs by ��
# 100603  �X���b�h�����E�l��ݒ肷��̔�����T�u���[�`���� by ��
# 100606  Saborin�̍X�V�����PID�ɂ����̂���rand()�ɂ����̂ɕύX by ��
# 100617  hayabusa�T�[�o��1/100�b�܂ŕ\�� by ��
# 100619  live*�T�[�o��1/100�b�\������ by ��
# 100724  au��PC�T�C�g�r���[�A�[��IP�A�h���X�����W����̓��e�̓G���[�ɂ��� by ��
# 100914  orz.2ch.io����̓��e������ by garnet
# 100918  EZweb��CIDR�u���b�N���ŐV�łɕύX(�ǉ�) by ��
# 101005  jig�u���E�U��CIDR�u���b�N���ŐV�łɕύX(�ǉ��E�폜) by ��
# 101014  Willcom��CIDR�u���b�N���ŐV�łɕύX(�ǉ��E�폜) by ��
# 101028  jig�u���E�U��CIDR�u���b�N���ŐV�łɕύX(�ǉ�) by ��

#############################################################################
#	BE ��ICON��\������@sssp://
#############################################################################
sub dispIconSssp
{
	my ($GB) = @_;

	if($GB->{icon} eq '')	{return 0;}

	if($GB->{NINNIN})	{return 0;}	#���D�X�e���X��off

#	if(!$GB->{NEWTHREAD})	{return 0;}	#�X�����Ď��ȊO��off

	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_OVERSEA_PROXY'} eq "checked")	{return 1;}

#	if($GB->{FORM}->{'bbs'} eq "operate2")	{return 1;}
	if($GB->{FORM}->{'bbs'} eq "news")	{return 1;}
	if($GB->{FORM}->{'bbs'} eq "poverty")	{return 1;}
	if($GB->{FORM}->{'bbs'} eq "news4vip")	{return 1;}

	return 0	;
}
#############################################################################
#	�g�ъe�Ђ̃T�[�o�𐔂��邼
#############################################################################
sub countKeitaiServer
{
	my ($GB) = @_	;


	return 1	;

	if($ENV{'SERVER_NAME'} !~ /gimpo/)	{return 0;}
	if(!$GB->{KEITAI})			{return 0;}

	my $cname = "dc"		;
	if($GB->{KEITAI} eq 2)		{ $cname = "au"; }
	elsif($GB->{KEITAI} eq 3)	{ $cname = "sb"; }
	elsif($GB->{KEITAI} eq 5)	{ $cname = "em"; }

	my $fff = "./cname/" . $cname . "/"	;
	if(!(-e $fff))	{mkdir($fff,0777);}
	if(!(-e $fff))	{return 0;}

	my $remo = $GB->{HOST29}	; #�����郊���z
	my $ipip = $ENV{REMOTE_ADDR}	;
	$fff .= "$ipip.txt"		;

	if(open(LX,">> $fff")){print LX "$remo\t\t\t\t\t\t\t\t\n";close(LX);}

	return 1	;
}
#############################################################################
# docomo�g�т�i���[�hID����ADNS�₢���킹�p��������쐬����
# ����: i���[�hID������
# �߂�l: DNS�₢���킹�p������
#############################################################################
sub MakeImodeIDforDNS
{
	my ($imodeid) = @_;
	my $komojiflag = $imodeid;

	$komojiflag =~ tr/0-9A-Za-z/00000000000000000000000000000000000011111111111111111111111111/; 
	$imodeid = $imodeid . '-' . $komojiflag;

	return $imodeid;
}
#############################################################################
# �}���`�o�C�g(���{�ꓙ)�������Ȃ��@�p���
#############################################################################
sub NoJapanese
{
	my ($GB) = @_	;

	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_4WORLD'} eq "checked")
	{
		my $a = $GB->{FORM}->{'MESSAGE'} . $GB->{FORM}->{'mail'} . $GB->{FORM}->{'FROM'} . $GB->{FORM}->{'subject'}	;
		if($a =~ /[^a-zA-Z0-9\.\, #_<>\(\)\?\/\&\;\!\:\=\'\+\-\*\~\%\@\"\[\]\+]/)	{&DispError2($GB,"�d�q�q�n�q�I","���{��͎󂯕t���Ă��܂���");	}
	}
#	return	0	;

	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_4WORLD'} eq "kanji")
	{
		my $a = $GB->{FORM}->{'MESSAGE'}	;
#		$a =~ s/[\x88-\x9F\xE0-\xFF][\x9F-\xFF]//g	;
		$a =~ s/[\x88-\x9F\xE0-\xFF][\x80-\xFF]//g	;
		$a =~ s/<br>//g				;
		$a =~ s/ //g				;
		$a =~ s/�@//g				;
		if($a ne '')	{&DispError2($GB,"�d�q�q�n�q�I","���������󂯕t���Ă��܂���");	}
	}
	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_4WORLD'} eq "hira")
	{
		my $a = $GB->{FORM}->{'MESSAGE'}	;
		$a =~ s/[\x82][\x9E-\xFF]//g	;
		$a =~ s/<br>//g				;
		$a =~ s/ //g				;
		$a =~ s/�@//g				;
		if($a ne '')	{&DispError2($GB,"�d�q�q�n�q�I","�Ђ炪�Ȃ����󂯕t���Ă��܂���");	}
	}
	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_4WORLD'} eq "kata")
	{
		my $a = $GB->{FORM}->{'MESSAGE'}	;
		$a =~ s/&gt;&gt;[0-9\-,]+//g		;	# >>23�Ƃ�
		$a =~ s/[\x81][\x48-\x49]//g		;	# �H�@�Ɓ@�I
		$a =~ s/[\x81][\x5B-\x5C]//g		;	# �[�@�Ɓ@�\
		$a =~ s/[\x83][\x40-\x9F]//g		;
		$a =~ s/<br>//g				;
		$a =~ s/ //g				;
		$a =~ s/�@//g				;
		if($a ne '')	{&DispError2($GB,"�d�q�q�n�q�I","�J�^�J�i�����󂯕t���Ă��܂���");	}
	}
	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_4WORLD'} eq "senji")
	{
		my $a = $GB->{FORM}->{'MESSAGE'} . $GB->{FORM}->{'subject'}	;
		$a =~ s/&gt;&gt;[0-9\-,]+//g		;	# >>23�Ƃ�
		$a =~ s/!vip2:stop://g			;	# !vip2:stop:!vip2:heal:
		$a =~ s/!vip2:heal://g			;	# !vip2:stop:
		$a =~ s/(\x81[\x40-\xFF]|\x83[\x40-\x9F]|[\x88-\x9F][\x40-\xFF]|[\xE0-\xFF][\x40-\xFF])+//g; #(���낢��L��|�J�^�J�i|����aA|����bB)+
#		$a =~ s/http:\/\/[a-zA-Z0-9.,_\/]+//g	;	#URL ���@���V
		$a =~ s/h?ttps?:\/\/[a-zA-Z0-9.,_\/+-]+//g;	# +- �_�P�ǉ��Bh ���L�g 
		$a =~ s/<br>//g				;
		$a =~ s/ //g				;
		$a =~ s/�@//g				;
		if($a ne '')	{&DispError2($GB,"�d�q�q�n�q�I","�����ƃJ�^�J�i�����󂯕t���Ă��܂���");	}
	}

#$GB->{FORM}->{'MESSAGE'} .= "<hr>$FOX->{$GB->{FORM}->{bbs}}->{'BBS_RAWIP_CHECK'} // PREN=$GB->{COOKIES}{PREN}";

	return	0	;
}
#############################################################################
# �ێ�c�[���΍�  by �� http://web1.nazca.co.jp/despair/hosyu/
#############################################################################
sub antiHosyu
{
	my ($GB) = @_			;
	if($GB->{FORM}->{'FROM'} =~ /��2d\.AlKjN5I/)
	{
		&DispError2($GB,"�d�q�q�n�q�I","ktkr");
	}
	return 0	;
}
#############################################################################
# �g�тł̋K�񌩂��@�g��DB�̎��� by ��
#############################################################################
sub useBBM2
{
	my ($GB) = @_			;

#return 0	;

	if($GB->{KEITAI})	{return 1;}	#�g��
#	if($GB->{P22CH})	{return 1;}	#P2

	return 0	;
}
sub GooMorningKeitai
{
	my ($GB) = @_			;

	#BBM�ُ펞�͂���[
	if(!$FOX->{BBM2})	{return 0;}

	if(!&useBBM2($GB))	{return 0;}

	my $au = &NotifyUlaBbmPOST($GB)	;
	if($au eq 'ZZZ:700')	{return 0;}
	if($au eq 'ZZZ:701')	{&DispError3($GB,"�d�q�q�n�q�I","�͂��߂܂��āB<BR>701[$au]");}
	if($au eq 'ZZZ:702')	{&DispError3($GB,"�d�q�q�n�q�I","����A�v���Ԃ�B<BR>702[$au]");}
	if($au eq 'ZZZ:703')	{&DispError3($GB,"�d�q�q�n�q�I","����΂��B<BR>703[$au]");}
	if($au eq 'ZZZ:704')	{&DispError3($GB,"�d�q�q�n�q�I","���܂��B<BR>704[$au]");}
	if($au eq 'ZZZ:705')	{&DispError3($GB,"�d�q�q�n�q�I","�҂�ۂ�B<BR>705[$au]");}
	if($au =~ /ZZZ:710/)	{&DispError3($GB,"�d�q�q�n�q�I","�� ������2.0�B<BR>710[$au]");}
	&DispError3($GB,"�d�q�q�n�q�I","�������ܒ������B<BR>?[$au]");
	$FOX->{BBM2} = 0	;
}
sub NotifyUlaBbmPOST
{
	my ($GB) = @_;

	my(%pm, $ua, $response) = ()		;
	my $host = "http://bbm2.2ch.net/test/z.so?"	;
	$pm{'srv'}	= $ENV{'SERVER_NAME'}		;
	$pm{'tane'}	= $GB->{IDNOTANE}		;
	$pm{'ua'}	= $ENV{'HTTP_USER_AGENT'}	;
	$pm{'subject'}	= $GB->{FORM}->{'subject'}	;
	$pm{'FROM'}	= $GB->{FORM}->{'FROM'}		;
	$pm{'mail'}	= $GB->{FORM}->{'mail'}		;
	$pm{'bbs'}	= $GB->{FORM}->{bbs}		;
	$pm{'key'}	= $GB->{FORM}->{key}		;
	$pm{'newt'}	= $GB->{NEWTHREAD}		;
	$pm{'MESSAGE'}	= $GB->{FORM}->{'MESSAGE'}	;

	$ua = LWP::UserAgent->new()		;
	$ua->agent('Mozilla/5.0 FOX(2ch.bbs)')	;
	$ua->timeout(5);
	$response = $ua -> post($host, \%pm);
	my $db_content = $response->content();

	# �G���[�`�F�b�N
	if ($response->is_error)
	{
		return "�ʐM�G���[";
	}
	chomp($db_content);
	return $db_content;
}
#############################################################################
#�@�`���̋@�\ 2.0
#############################################################################
sub VipQ2ON
{
	my ($GB) = @_			;

#	if($GB->{FORM}->{bbs} eq 'operate2')		{return 1;}
	if($GB->{FORM}->{bbs} eq 'news')		{return 1;}
#	if($GB->{FORM}->{bbs} eq 'anime4vip')		{return 1;}
	if($GB->{FORM}->{bbs} eq 'news4vip')		{return 1;}
	if($GB->{FORM}->{bbs} eq 'news4viptasu')	{return 1;}
	if($GB->{FORM}->{bbs} eq 'campus')		{return 1;}

	return 0			;
}
sub VipQ2
{
	my ($GB) = @_			;

	if(!VipQ2ON($GB))	{return 0;}

	my @lx = split(/\n/,$GB->{FORM}->{'MESSAGE'})	;
	$lx[0] =~ /\!vip2\:(\S+)\:/	;
	my $command = $1		;

#	if($command eq '')	{return 0;}

#	$GB->{FORM}->{'MESSAGE'} .= "<br>---<br>lx=$lx[0]<br>com=$command<br>";
#	$GB->{FORM}->{'MESSAGE'} .= "<br>---<br>com=$command<br>";

	if($command eq 'stop')	{return &VipQ2Stop($GB);}
	if($command eq 'heal')	{return &VipQ2Heal($GB);}

	return 0			;
}
sub VipQ2Heal
{
	my ($GB) = @_			;
	my $MP = 100			;
	my $MX = 2000			;
	my $IP = $ENV{REMOTE_ADDR}	;

	$GB->{FORM}->{'MESSAGE'} .= "<br>---<br>";

#	my $fff = "../$GB->{FORM}->{bbs}/vip2"	;
	my $fff = "/md/tmp/book"	;
	if(!(-e $fff))	{mkdir($fff,0777);}
	if(!(-e $fff))	{return 0;}
	$fff .= "/$GB->{FORM}->{'key'}.cgi"	;

	my @dmg = ()		;
	my @vipdata = ()	;
	my $alldamege= 0	;

	if(open(DMG,"$fff"))
	{
		@dmg = <DMG>	;
		close(DMG)	;
	}

	foreach(@dmg)
	{
		@vipdata = split(/	/, $_);
		$alldamege = $alldamege + $vipdata[3];
	}

	my $pay = 350	;
	if(!&wasteBE($GB,$pay))	{return 0;}

	if(   $alldamege < -300)	{$MP = int(rand(100))+50;}
	elsif($alldamege < -100)	{$MP = int(rand(100))+50;}
	elsif($alldamege <    0)	{$MP = int(rand(200))+50;}
	elsif($alldamege <  500)	{$MP = int(rand(300))+50;}
	else				{$MP = int(rand(200))+50;}

	$MP += 10	;
	$GB->{FORM}->{'MESSAGE'} .= "MP$pay�g���ĉ񕜂̎�����������!<font color=blue>���~</font> $MP�񕜂����B<br>";

	if(open(STP,">> $fff"))
	{
		print STP "$GB->{FORM}->{'DMDM'}\t$GB->{FORM}->{'MDMD'}\t$IP\t-$MP\n";
		close(STP)	;
	}
	my $dn = @dmg + 1	;

#	my $td = $MP * $dn	;
	my $td = $alldamege - $MP	;

	$GB->{FORM}->{'MESSAGE'} .= "���̃X����$dn��ڂɉ񕜂̎������󂯂� ($td/$MX)<br>";

	return 1;
}
sub VipQ2Stop
{
	my ($GB) = @_			;
	my $MP = 150	;	#100			;
	my $MX = 2000	;	#1000			;
	my $PLUSATK = 0			;
	my $IP = $ENV{REMOTE_ADDR}	;

	if($GB->{P22CH})	{$IP = $GB->{HOST2}	;}	#IP from p2

	if($GB->{FORM}->{bbs} eq 'news4vip')		{$MX = 1000;}
	if($GB->{FORM}->{bbs} eq 'news4viptasu')	{$MX = int(rand(1000));}
	if($GB->{FORM}->{bbs} eq 'anime4vip')		{$MX = int(rand(1000));}

	$GB->{NINNIN} = 0		;		#saku�̎���be�\��

	$GB->{FORM}->{'MESSAGE'} .= "<br>---<br>";
	if($GB->{BEpoints} < 8000)	{$GB->{FORM}->{'MESSAGE'} .= "���K����m�̂ӂ��̍U��<br>";}
	elsif($GB->{BEelite} eq 'BRZ'){$GB->{FORM}->{'MESSAGE'} .= "�v�`�q�[���[�̂�����Ƃ����U�� <br>"; $PLUSATK = 5;}
	elsif($GB->{BEelite} eq 'PLT'){$GB->{FORM}->{'MESSAGE'} .= "�܂ق���������̂�߂̍U�� <br>"; $PLUSATK = 10;}
	elsif($GB->{BEelite} eq 'DIA'){$GB->{FORM}->{'MESSAGE'} .= "�O�����h�v���[�X�g�̂��Ȃ�̍U�� <br>"; $PLUSATK = 15;}
	elsif($GB->{BEelite} eq 'SOL'){$GB->{FORM}->{'MESSAGE'} .= "�^�̗E�҂̂������̍U�� <br>"; $PLUSATK = 20;}

#	my $fff = "../$GB->{FORM}->{bbs}/vip2"	;
	my $fff = "/md/tmp/book"	;
	if(!(-e $fff))	{mkdir($fff,0777);}
	if(!(-e $fff))	{return 0;}
	$fff .= "/$GB->{FORM}->{'key'}.cgi"	;

	my @dmg = ()		;

	if(open(DMG,"$fff"))
	{
		@dmg = <DMG>	;
		close(DMG)	;
	}

	foreach(@dmg)
	{
#		if($_ =~ /$GB->{FORM}->{'MDMD'}/ && $GB->{BEpoints} < 8000)
#		if($_ =~ /$GB->{FORM}->{'MDMD'}/ && !$GB->{KABUU})
#		if($_ =~ /$GB->{FORM}->{'MDMD'}/ && !$GB->{KABUU} && $GB->{FORM}->{bbs} ne 'news4viptasu')
		if($_ =~ /$GB->{FORM}->{'MDMD'}/)
		{
			$GB->{FORM}->{'MESSAGE'} .= "���������B<br>";
			return 0	;
		}
	}
	foreach(@dmg)
	{
#		if($_ =~ /$IP/ && $GB->{BEpoints} < 8000)
#		if($_ =~ /$IP/ && !$GB->{KABUU})
#		if($_ =~ /$IP/ && !$GB->{KABUU} && $GB->{FORM}->{bbs} ne 'news4viptasu')
		if($_ =~ /$IP/)
		{
			$GB->{FORM}->{'MESSAGE'} .= "���������Q�B<br>";
			return 0	;
		}
	}

	my @vipdata = ()	;
	my $alldamege= 0	;

	foreach(@dmg)
	{
		@vipdata = split(/	/, $_);
		$alldamege = $alldamege + $vipdata[3];
	}

	my $mpmp = $MP + int(rand(300))	;
	if(!&wasteBE($GB,$mpmp))	{return 0;}

	$GB->{FORM}->{'MESSAGE'} .= "MP$mpmp�g���Ăւ��ۂ��̎������������B<font color=red>���~</font> �i�X���̃_���[�W $alldamege�j <br>";

	if(open(STP,">> $fff"))
	{
		print STP "$GB->{FORM}->{'DMDM'}\t$GB->{FORM}->{'MDMD'}\t$IP\t$MP\n";
		close(STP)	;
	}
	my $dn = @dmg + 1	;

#	my $td = $MP * $dn	;
	my $td = $alldamege + $MP	;

	$GB->{FORM}->{'MESSAGE'} .= "���̃X����$dn��ڂ̃_���[�W���󂯂� ($td/$MX)<br>";
#	$GB->{FORM}->{'MESSAGE'} .= "($GB->{BEelite})<br>";
	if($GB->{KABUU})
	{
		if(open(STP,">> $fff"))
		{
			print STP "$GB->{FORM}->{'DMDM'}\t$GB->{FORM}->{'MDMD'}\t$IP\t$MP\n";
			close(STP)	;
		}
		$td += $MP		;
		$dn++			;
		$GB->{FORM}->{'MESSAGE'} .= "�������� �΂���!! ����ɂ��̃X����$dn��ڂ̃_���[�W���󂯂� ($td/$MX)<br>";
	}
	my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($GB->{NOWTIME});
	if($sec < 10)
	{
		if(open(STP,">> $fff"))
		{
			print STP "$GB->{FORM}->{'DMDM'}\t$GB->{FORM}->{'MDMD'}\t$IP\t$MP\n";
			close(STP)	;
		}
		$td += $MP		;$dn++	;
		$GB->{FORM}->{'MESSAGE'} .= "�ڂ��������͂��܂���!! ����ɂ��̃X����$dn��ڂ̃_���[�W���󂯂� ($td/$MX)<br>";
	}

	if($PLUSATK > 0)
	{
		if(open(STP,">> $fff"))
		{
			$MP = $PLUSATK;

			print STP "$GB->{FORM}->{'DMDM'}\t$GB->{FORM}->{'MDMD'}\t$IP\t$MP\n";
			close(STP)	;
			$td += $MP	;
			$dn++		;
			$GB->{FORM}->{'MESSAGE'} .= "�ǉ��U��!! ����ɂ��̃X����$dn��ڂ̃_���[�W���󂯂� ($td/$MX)<br>";
		}		
	}

	if($td >= $MX)
	{
		&VipQ2Saku($GB,$GB->{FORM}->{bbs},$GB->{FORM}->{key})	;
		$GB->{FORM}->{'MESSAGE'} .= "���̃X���́E�E�E<br><br>��~���܂����B<br>";
		$GB->{VIPQ2STOP} = 1	;	#�X���X�g
	}

	return 1;
}
sub gotoBobon
{
	my ($GB,$log,$ipip,$mes) = @_	;

	if($ipip =~ /[^0-9\.]/)	{return 0;}
#�g��
#</b>�c�̖���(�֓�)<b><><>2008/09/29(��) 17:04:10.76 xN47qM/8O<>��������<>���񂱂��ꂽ
#<>wb35proxy04.ezweb.ne.jp(05001018144926_mi.ezweb.ne.jp)<>59.135.38.174<> (2dec14b8c0e2be97b74d845f3be5ced0 hardkitayo@yahoo.co.jp)<>KDDI-SH31 UP.Browser/6.2.0.10.3.5 (GUI) MMP/2.0 
#P2
#</b>�l�\��(��ʌ�)<b><><>2008/09/29(��) 16:28:58.51 UZXBNes+P<>�ynews�z�j���[�X����^�p���13<>�p�X�ύX�ɂ��saku�������Ɓg�܂��́hIP���炳��邩��A�C������I
#<>cw43.razil.jp(462143)219.182.232.16<>210.135.98.43<> (85c00438802bac3606f3a3edbd96bbe9 iressa01@yahoo.co.jp)<>Monazilla/1.00 (P2/p2.2ch.net; p2-client-ip: 
	$log =~ /\((\S+)\)[0-9\.]*<>[0-9\.]+<>/	;
	my $yaki = $1	;

	my $rhost = gethostbyaddr(pack('c4',split(/\./, $ipip)), 2) || $ipip;
	if($rhost =~ /docomo.ne.jp$/)	{return "�Ă��Ă�����Ă��� docomo[$yaki]";}
	if($rhost =~ /ezweb.ne.jp$/)	{return "�Ă��Ă�����Ă��� AU[$yaki]";}
	if($rhost =~ /jp-\w.ne.jp$/)	{return "�Ă��Ă�����Ă��� softbank[$yaki]";}
	if($rhost =~ /vodafone.ne.jp$/)	{return "�Ă��Ă�����Ă��� softbank[$yaki]";}
	if($rhost =~ /\.razil.jp$/)	{return "�Ă��Ă�����Ă��� P2[$yaki]";}
	if($rhost =~ /\.maido3.com$/)	{return "����͏Ă��Ȃ�1";}
	if($rhost =~ /\.ibis.ne.jp$/)	{return "ibis�͂܂��Ή����Ă��Ȃ��̂�";}
	if($rhost =~ /\.jig.jp$/)	{return "jig�͂܂��Ή����Ă��Ȃ��̂�";}


	my $bburl = "http://qb6.2ch.net/test/asokin/kiri.cgi?ox=$ipip&key=$mes&cow=274";
	my $ua = LWP::UserAgent->new();
	$ua->agent('Mozilla/5.0 FOX(2ch.se)');
	$ua->timeout(3);
	my $request = HTTP::Request->new('GET', $bburl);
	my $response = $ua->request($request) ;#������ GET ����

	return "���";
}
sub VipQ2Saku
{
	my ($GB,$bbs,$key) = @_	;

#$GB->{FORM}->{'MESSAGE'} .= "VipQ2Saku<br>";
	my $logdat = "../../test/ggg/" . $bbs . "dat/" . $key . ".cgi";
	if(!open(LXX,"$logdat"))	{return 0;}
#$GB->{FORM}->{'MESSAGE'} .= "���O����<br>";
	my @lxx = <LXX>	;
	close(LXX)	;

	my $gxx = $lxx[0]	;
#(0a9a9eea0582eb7fad96dcbb0333de29 yakin@80.kg)<>
	$gxx =~ / \(([0-9a-z]+) (\S+)\)<>/;
	my $gx1 = $1	;
	my $gx2 = $2	;

	if($gx1 && $gx2)
	{
		my $sp = 300		;		# ��{�l
		$sp += int(rand(800))	;		# �����_�����Z
		if($GB->{KABUU})	{$sp *= 5;}	# ����D�҉��Z

		if(&wasteBEx($GB,$gx2,$gx1,$sp))
		{
			$GB->{FORM}->{'MESSAGE'} .= "<font size=+1 face=\"Arial\" color=red><b>$sp</b></font> saku����<br>";
		}
		else
		{#�p�X���[�h�ύX�œ�������|�C���g����Ȃ��Ƃ��̓{�{������
			my $bxx = $lxx[0]		;
			$bxx =~ /<>([0-9\.]+)<>/	;
			my $ipip = $1			;
			my $rr = &gotoBobon($GB,$bxx,$ipip,"vip2:saku:($bbs)")	;
			$GB->{FORM}->{'MESSAGE'} .= "<font color=red>�i�P�[�P�j�j�����b</font> ($rr)<br>";
		}
	}
#������?
#$GB->{FORM}->{'MESSAGE'} .= "������?<br>";
	my $mxx = $lxx[0]	;
#����� ��<><>2007/12/24(��) 03:47:54.75 5vawQ6AY0<>���ꂽ��<>
#���̈ꎞ��~�̃e�X�g<>KD125055017119.ppp-bb.dion.ne.jp[tjuTdvdhyupQ06ao]<>125.55.17.119<>tjuTdvdhyupQ06ao ( )<>Monazilla/1.00 (JaneView/0.1.12.1)
#[tjuTdvdhyupQ06ao]

	my ($d1,$d2,$d3,$d4,$d5,$d6,$d7,$d8,$d9) = split(/<>/,$mxx)	;
	$d6 =~ /\[([a-zA-Z0-9]+)\]/;
	my $mx1 = $1	;
	my $mx2 = $1	;
#&DispError2($GB,"�d�q�q�n�q�I","d6=[$mx1][$d6][$mxx]");
#&DispError2($GB,"�d�q�q�n�q�I","d6=[$mx1][$d6]");
	if(length($mx1) eq 16)
	{
		$mx1 =~ s/\//\)/g;
		$mx1 =~ s/\./\(/g;
		my $logdat = "../../test/ggg/" . $bbs . "dat/" . $mx1 . ".cgi";
		if(open(YAKI,"> $logdat"))
		{
			print YAKI "$mx2";
			close(YAKI)	;
		}
$GB->{FORM}->{'MESSAGE'} .= "<br><font color=red>���́��͂��΂炭�̊ԃX�����Ăł��Ȃ��Ȃ�܂����B</font><br><br>";
	}
	return 0;
}
sub VipQ2MaruyakiON
{
	my ($GB) = @_	;

	if($GB->{FORM}->{bbs} ne 'news')	{return 1;}
	if($GB->{FORM}->{bbs} ne 'news4vip')	{return 1;}
	if($GB->{FORM}->{bbs} ne 'news4viptasu'){return 1;}

	return 0	;
}
sub VipQ2MaruyakiCheck
{
	my ($GB) = @_	;

	if(!VipQ2MaruyakiON($GB))		{return 0;}
	if(!$GB->{MARU})			{return 0;}
	my $mx1	= $GB->{MARU}	;
	$mx1 =~ s/\//\)/g;
	$mx1 =~ s/\./\(/g;

	my $logdat = "../../test/ggg/" . $GB->{FORM}->{bbs} . "dat/" . $mx1 . ".cgi";

	if(-e $logdat)
	{
		my ($prsize,$prmtime)= ();
		($prsize, $prmtime) = (local $_=stat($logdat)) ? ($_->size, $_->mtime) : (0, 0);
		my $ctime = 0;
		$ctime = time;
		my $keika = $ctime - $prmtime	;
		my $ato = 6*60*60 - $keika	;
		if($ato > 0)
		{
			&DispError2($GB,"�d�q�q�n�q�I","���́��͂��΂炭�̊ԃX�����Ăł��܂���B[����$ato�b](saku�S��)");
		}
		else
		{
			unlink($logdat)		;
		}
	}
	
}
sub wasteBE()
{
	my ($GB,$mp) = @_	;
	return &wasteBEx($GB,$GB->{FORM}->{'DMDM'},$GB->{FORM}->{'MDMD'},$mp);
}
sub wasteBEx()
{
	my ($GB,$DMDM,$MDMD,$mp) = @_	;

	use LWP::UserAgent;
	use HTTP::Request;
	use HTTP::Status;

	my $path = "d=$DMDM&m=$MDMD";
	my $ua = LWP::UserAgent->new();
	$ua->timeout(3);
	my $request = HTTP::Request->new('GET', 'http://be.2ch.net/test/v.php?' . $path);
	my $response = $ua->request($request) ;#������ GET ����
	my $response_body = $response->content();#GET�̌��ʂ͂����ɓ����Ă���

	my $db_content = $response->content();

	my ($user_points, $xxx) = split(/ /, $db_content);

	if($xxx eq '')
	{
		$GB->{FORM}->{'MESSAGE'} .= "���O�C�����ĂȂ��ł��B<br>";
		return 0		;
	}
	my $BEpoints = $user_points	;
	my $BExxx    = $xxx		;
	if($BEpoints < $mp)
	{
		$GB->{FORM}->{'MESSAGE'} .= "MP������܂���B($mp/$BEpoints)";
		return 0		;
	}
	my $uiui = &rulaPayCost($DMDM,$MDMD,$BExxx,$mp);
	if($uiui eq '�ʐM�G���[')
	{
		&DispError2($GB,"�d�q�q�n�q�I","be�T�[�o���E�E�E");
	}
	if($uiui =~ /insufficient points/)
	{
		$GB->{FORM}->{'MESSAGE'} .= '�}�����ł���B�B�B<br>';
		return 0		;
	}
	return 1;
}
#########################################
#	BE �|�C���g����
#########################################
sub rulaPayCost
{
	my ($DMDM,$MDMD,$xxx,$ccc) = @_	;

#http://be.2ch.net/test/delp.php?delp=1&i=570402296&d=1&poi=uirou1289&b=1

	my $path = "delp=$ccc&i=$xxx&d=1&b=1&poi=uirou1289";
	my $ua = LWP::UserAgent->new();
	$ua->agent('Mozilla/5.0 Rula');
	$ua->timeout(5);
	my $request = HTTP::Request->new('GET', 'http://be.2ch.net/test/delp.php?' . $path);
$request -> header('Cookie' => "DMDM=$DMDM; MDMD=$MDMD; FOX=ehehe; ");
	my $response = $ua->request($request) 		;#������ GET ����
	my $response_code = $response->code()		;#���ʂ͂����ɓ����Ă���
	my $response_body = $response->content()	;#GET�̌��ʂ͂����ɓ����Ă���

	# �G���[�`�F�b�N
	if ($response->is_error)
	{
		return "�ʐM�G���[";
	}

	return $response_body	;
}
#############################################################################
#	�����z -> �s���{����
#############################################################################
sub area47
{
	my ($GB) = @_;

	my @kenmei = ()	;

	@kenmei = (
'����','�k�C��','�X��','��茧','�{�錧','�H�c��','�R�`��','������','��錧','�Ȗ،�',
'�Q�n��','��ʌ�','��t��','�����s','�_�ސ쌧','�V����','�x�R��','�ΐ쌧','���䌧','�R����',
'���쌧','�򕌌�','�É���','���m��','�O�d��','���ꌧ','���s�{','���{','���Ɍ�','�ޗǌ�',
'�a�̎R��','���挧','������','���R��','�L����','�R����','������','���쌧','���Q��','���m��',
'������','���ꌧ','���茧','�F�{��','�啪��','�{�茧','��������','���ꌧ','��p','�s����softbank',
'���k�n��','�֓��n��','�����n��','�֐��n��','�l���n��','�����n��','��B�n��','�����{','�����{','CATV-infoweb',
'��','��','62','63','64','dion�R','�c�ɂ��ł�','catv?','����','�`�x�b�g������',
'�k���n��','�R�A�n��','�����l��','73','74','75','76','�X�������J','�L���`������������','�������S��������',
'USA','�J�i�_','82','83','84','85','86','87','�ɐ�','�n��',
'�`��')	;

if($GB->{FORM}->{bbs} eq 'news12345')
{
	@kenmei = (
'���l','������','���쌧','�Q�n��','�{�錧','���ꌧ','�{�茧','���ꌧ','��錧','���m��',
'���R��','���{','�H�c��','��ʌ�','���m��','�V����','�啪��','��������','�É���','���茧',
'���쌧','���Q��','���挧','�_�ސ쌧','�O�d��','���Ɍ�','���s�{','�����s','���ꌧ','�ޗǌ�',
'�a�̎R��','������','�F�{��','�R�`��','�ΐ쌧','�x�R��','������','��t��','���䌧','�򕌌�',
'������','�k�C��','�R����','�R����','��茧','�L����','�Ȗ،�','�X��','��p','���',
'�֓��n��','�����n��','�֐��n��','�l���n��','�����n��','��B�n��','�����{','�����{','���k�n��','CATV-infoweb',
'��','��','62','63','64','�v����','�c�ɂ��ł�','�]��','����','����',
'�k���n��','�R�A�n��','�����l��','73','74','75','76','�X�������J','�l�u���X�J�B','�R�l�`�J�b�g�B',
'USA','�J�i�_','82','83','84','85','86','87','88','�n��',
'�`��')	;
}
if($GB->{FORM}->{bbs} eq 'campus')
{
	@kenmei = (
'���l','������','���쌧','�Q�n��','�{�錧','���ꌧ','�{�茧','���ꌧ','��錧','���m��',
'���R��','���{','�H�c��','��ʌ�','���m��','�V����','�啪��','��������','�É���','���茧',
'���쌧','���Q��','���挧','�_�ސ쌧','�O�d��','���Ɍ�','���s�{','�����s','���ꌧ','�ޗǌ�',
'�a�̎R��','������','�F�{��','�R�`��','�ΐ쌧','�x�R��','������','��t��','���䌧','�򕌌�',
'������','�k�C��','�R����','�R����','��茧','�L����','�Ȗ،�','�X��','��p','���',
'�֓��n��','�����n��','�֐��n��','�l���n��','�����n��','��B�n��','�����{','�����{','���k�n��','CATV-infoweb',
'��','��','62','63','64','�v����','�c�ɂ��ł�','�]��','����','����',
'�k���n��','�R�A�n��','�����l��','73','74','75','76','77','�l�u���X�J�B','�R�l�`�J�b�g�B',
'USA','�J�i�_','82','83','84','85','86','87','88','�n��',
'�`��')	;
}
if($GB->{FORM}->{bbs} eq 'newsnewsnews')
{
	@kenmei = (
'�Ζ�','�������','���','��񂱂���','�������܂ڂ�','���肽���','��������','����','�Ȃ��Ƃ�','���傤��',
'����ɂႭ','���܂ނ�','���������','���񂶂�','�����܂�','���ɂ���','�Ԃ�','���Ԃ炸��','������傤','�ق��Ƃ�',
'���΃����[','����','�͂�؂�','���X�J�c','�����ӂ�','�����i','������','�����₫','����������','����',
'���߂ڂ�','�Ȃ�','�ǂ낦��','���т���','���݂��\��','�ӂ�','������','���ǂ�','�݂���','����',
'����','�Ƃ���','�����ۂ�','�n�h��','�J�{�X','���̂܂��','���|','�A��','�΂Ȃ�','�L���`',
'����','���]','���','�̉�','���ԍ]','�C��','�K���]','����','�t��','�E�C�O����',
'�킽����','�w�','62','63','64','��','�c�ɂ��ł�','�v�[�A����','���','�Ζk��',
'��','�`������','�~���I��','73','74','75','76','77','�ɔJ��','�Ïl��',
'USA','�J�i�_','82','83','84','85','86','87','88','�n��',
'�|��')	;
}

	my $xkenban = &area47s0($GB)	;
	my $kenban = int($xkenban)	;
	if($kenban >90000)	{return "";}
	if($kenban < 1)
	{
		if($xkenban)	{return $xkenban;}
		$kenban = 0	;
	}
	if($kenban > 90)	{$kenban = 90;}

	return $kenmei[$kenban]	;
}
sub area47s0
{
	my ($GB) = @_;
	my $remo = $GB->{HOST29}; #�����郊���z

#return "���͂�";

	#P2�̎��̓��b�N�A�b�v
	if($GB->{P22CH})
	{
		my $p2r = "";
		#return "�A�C�_�z�B";X-P2-Mobile-Serial-BBM
		if($ENV{HTTP_USER_AGENT} =~ /p2-client-ip: (\d+\.\d+\.\d+\.\d+)/)
		{
			$p2r = $1;

			# �����[�g�z�X�g�����L�^����(�K���������悤��)
			$remo = gethostbyaddr(pack('C4',split(/\./, $p2r)), 2) || $p2r;
		}
		else
		{
			&DispError2($GB,"�d�q�q�n�q�I","�i���֎~");
		}
		##�g�ьŗL�ԍ��擾
		if(&mumumuIsIP4EZWeb($p2r))
		{
			my $ser = $ENV{HTTP_X_P2_MOBILE_SERIAL_BBM}	;
#if(open(LX,">> HOST29.000")){print LX "(P2:AU)$remo($ser)\n";close(LX);}
if($ser eq ''){&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�[���ŗL���𑗐M���Ă��������B");}
		}
		elsif(&mumumuIsIP4IMode($p2r))
		{
			my $ser = $ENV{HTTP_X_P2_MOBILE_SERIAL_BBM}	;
#if(open(LX,">> HOST29.000")){print LX "(P2:Docomo)$remo($ser)\n";close(LX);}
if($ser eq ''){&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�[���ŗL���𑗐M���Ă��������B");}
		}
		elsif(&mumumuIsIP4Vodafone($p2r))
		{
			my $ser = $ENV{HTTP_X_P2_MOBILE_SERIAL_BBM}	;
#if(open(LX,">> HOST29.000")){print LX "(P2:SB)$remo($ser)\n";close(LX);}
if($ser eq ''){&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�[���ŗL���𑗐M���Ă��������B");}
		}
	}

	if($remo =~ /\.go\.jp$/)		{return "�ɐ�";}
	if($remo =~ /\.tw$/)			{return "��";}
	if($remo =~ /\.cn$/)			{return "��";}
	if($remo =~ /\.kr$/)			{return "��";}
	if($remo =~ /\.kp$/)			{return "��";}
	if($remo =~ /\.de$/)			{return "��";}
	if($remo =~ /\.us$/)			{return "��";}
	if($remo =~ /\.fr$/)			{return "��";}
	if($remo =~ /\.uk$/)			{return "�p";}
	if($remo =~ /\.is$/)			{return "�A�C�X�����h";}
	if($remo =~ /\.au$/)			{return "��";}
	if($remo =~ /\.ca$/)			{return "��";}
	if($remo =~ /\.br$/)			{return "�u���W��";}
	if($remo =~ /\d+\.\d+\.\d+\.\d+$/)	{return "�A���r�A";}

	# SB
	if($remo =~ /jp-.\.ne\.jp/)
	{
		#J�t�H�������{
		if($remo =~ /jp-d\.ne\.jp/){return "�k�C��";}
		if($remo =~ /jp-h\.ne\.jp/){return "���k�E�V��";}
		if($remo =~ /jp-t\.ne\.jp/){return "�֓��E�b�M�z";}
		#J�t�H�������{
		if($remo =~ /jp-k\.ne\.jp/){return "�֐�";}
		if($remo =~ /jp-r\.ne\.jp/){return "�k��";}
		if($remo =~ /jp-s\.ne\.jp/){return "�l��";}
		if($remo =~ /jp-n\.ne\.jp/){return "����";}
		if($remo =~ /jp-q\.ne\.jp/){return "��B�E����";}
		#�i�t�H�����C jp-c.ne.jp
		if($remo =~ /jp-c\.ne\.jp/){return "���C";}
		return 77;
	}
	# AU
	if($remo =~ /\.ezweb\.ne\.jp/)
	{
		if($GB->{IDNOTANE} =~ /^0500101/)	{return "�֓�";}
		if($GB->{IDNOTANE} =~ /^0500103/)	{return "���C";}
		if($GB->{IDNOTANE} =~ /^0500401/)	{return "�֓��E�b�M�z";}
		if($GB->{IDNOTANE} =~ /^0500403/)	{return "���C";}
		if($GB->{IDNOTANE} =~ /^0500405/)	{return "-����";}
		if($GB->{IDNOTANE} =~ /^050/)	{return "���C�E�֓�";}
		if($GB->{IDNOTANE} =~ /^0700/)	{return "�֐��E�k��";}
		if($GB->{IDNOTANE} =~ /^0701/)	{return "��B";}
		if($GB->{IDNOTANE} =~ /^07022/)	{return "�R�z";}
		if($GB->{IDNOTANE} =~ /^0702/)	{return "�����E�l��";}
		if($GB->{IDNOTANE} =~ /^0703/)	{return "�V���E���k";}
		if($GB->{IDNOTANE} =~ /^0704/)	{return "�k���n��";}
		if($GB->{IDNOTANE} =~ /^0705/)	{return "�k�C��";}
		if($GB->{IDNOTANE} =~ /^0706/)	{return "�l��";}
		if($GB->{IDNOTANE} =~ /^0707/)	{return "��B�E����";}
		if($GB->{IDNOTANE} =~ /^070/)	{return "au-�֓��ȊO";}
#if(open(LX,">> HOST29.000")){print LX "(AU)$remo($GB->{IDNOTANE})\n";close(LX);}
		return 78;
	}
	if($remo =~ /proxy(\d+)\.docomo\.ne\.jp/)
	{
		my $ppp = $1			;
		return 79			;
	}
	#�g�т̓X���[
	if($GB->{KEITAI})
	{
		return 78;
	}

	if($remo =~ /s(\d+)\.a(\d+)\.ap\.plala\.or\.jp$/)
	{
		my $pll = int($2);
		if($pll eq 48)	{return 68;}
		return $pll;
	}
#	if($remo =~ /ap(\d+)\.ftth\.ucom\.ne\.jp$/)		{return 32;}
	if($remo =~ /\.eonet\.ne\.jp$/)				{return 53;}
	if($remo =~ /\.megaegg\.ne\.jp$/)			{return 55;}
	if($remo =~ /w\d+.eacc.dti.ne.jp$/)			{return 57;}
	if($remo =~ /e\d+.eacc.dti.ne.jp$/)			{return 58;}
	if($remo =~ /\.freed\.dti\.ne\.jp$/)			{return 60;}
	if($remo =~ /\.air-[a-z\d+-]+\.dti\.ne\.jp$/)		{return 60;}

	if($remo =~ /\.sec\.nifty\.com$/)			{return 69;}
	if($remo =~ /\.iij4u\.or\.jp$/)				{return 69;}
	if($remo =~ /\.bbexcite\.jp$/)				{return 69;}
	if($remo =~ /\.doubleroute\.jp$/)			{return 69;}
	if($remo =~ /\.prin\.ne\.jp$/)				{return 69;}
	if($remo =~ /\.ucom\.ne\.jp$/)				{return 69;}
	if($remo =~ /\.valley\.ne\.jp$/)			{return 69;}
	if($remo =~ /\.t-com\.ne\.jp$/)				{return 69;}
	if($remo =~ /\.yournet\.ne\.jp$/)			{return 69;}
	if($remo =~ /\.tiki\.ne\.jp$/)				{return 69;}
	if($remo =~ /\.atfreed\.alpha-net\.ne\.jp$/)		{return 61;}
	if($remo =~ /\.du\.alpha-net\.ne\.jp$/)			{return 61;}
	if($remo =~ /\.point\.ne\.jp$/)				{return 51;}
	if($remo =~ /userreverse\.dion\.ne\.jp$/)		{return 65;}

	# namazuplus�p(89 = �n��)
	if($remo =~ /banana3104\.maido3\.com$/)			{return 89;}

	if($remo =~ /(\S+)\.(ppp|ppp\-bb)\.dion\.ne\.jp$/)
	{
		my $ken = $1	;
		my $kenban = &area47dion($GB,$remo,$ken);
		if($kenban)	{return $kenban;}
	}
	if($remo =~ /(\S+)\.asahi-net\.or\.jp$/)
	{
		my $ken = $1	;
		my $kenban = &area47asahinet($remo,$ken);
		if($kenban)	{return $kenban;}
	}
	if($remo =~ /(\S+)\.rev\.home\.ne\.jp$/)
	{
		my $ken = $1	;
		my $kenban = &area47home($remo,$ken);
		if($kenban)	{return $kenban;}
	}
	if($remo =~ /(\S+)\.2iij\.net$/)
	{
		my $ken = $1	;
		my $kenban = &area472iij($remo,$ken);
		if($kenban)	{return $kenban;}
	}
	if($remo =~ /\.(\S+)\.ocn\.ne\.jp$/)
	{
		my $ken = $1	;
		my $kenban = &area47ocn($remo,$ken);
		if($kenban)	{return $kenban;}
	}
	if($remo =~ /\.([\w-]+)\d\d\.ap\.so-net\.ne\.jp$/)
	{
		my $ken = $1	;
		my $kenban = &area47sonet($remo,$ken);
		if($kenban)	{return $kenban;}
	}
	if($remo =~ /-([a-z]+)-\d+\.[a-z\d\-]+\.enjoy\.ne\.jp$/)
	{
		my $ken = $1	;
		if(length($ken) eq 3)
		{
			my $kenban = &area47mesh($remo,$ken);
			if($kenban)	{return $kenban;}
		}
		elsif(length($ken) eq 4)
		{
			my $kenban = &area47sonet($remo,$ken);
			if($kenban)	{return $kenban;}
		}
	}
	if($remo =~ /\.([a-z\d\-]+)\.enjoy\.ne\.jp$/)
	{
		my $ken = $1	;
		if(length($ken) eq 3)
		{
			my $kenban = &area47mesh($remo,$ken);
			if($kenban)	{return $kenban;}
		}
		elsif(length($ken) eq 4)
		{
			my $kenban = &area47sonet($remo,$ken);
			if($kenban)	{return $kenban;}
		}
	}
	if($remo =~ /(\S+)\.ppp\.infoweb\.ne\.jp$/)
	{
		my $ken = $1	;
		my $kenban = &area47infoweb($remo,$ken);
		if($kenban)	{return $kenban;}
	}
	if($remo =~ /(\S+)\.odn\.(ad|ne)\.jp$/)
	{
		my $ken = $1	;
		my $kenban = &area47odn($GB,$remo,$ken);
		if($kenban)	{return $kenban;}
	}
	if($remo =~ /\.([a-z\-]+)\.nttpc\.ne\.jp$/)
	{
		my $ken = $1	;
		my $kenban = &area47nttpc($remo,$ken);
		if($kenban)	{return $kenban;}
	}
	if($remo =~ /\.([a-z]+)\.sannet\.ne\.jp$/)
	{
		my $ken = $1	;
		my $kenban = &area47dti($remo,$ken);
		if($kenban)	{return $kenban;}
	}
	if($remo =~ /\.([a-z]+)\.acca\.dti\.ne\.jp$/)
	{
		my $ken = $1	;
		my $kenban = &area47dti($remo,$ken);
		if($kenban)	{return $kenban;}
	}
	if($remo =~ /\.([a-z]+)-ip\.dti\.ne\.jp$/)
	{
		my $ken = $1	;
		my $kenban = &area47dti($remo,$ken);
		if($kenban)	{return $kenban;}
	}
	if($remo =~ /\.([a-z]+)\.[a-z]+\.alpha-net\.ne\.jp$/)
	{
		my $ken = $1	;
		my $kenban = &area47dti($remo,$ken);
		if($kenban)	{return $kenban;}
	}
	if($remo =~ /([a-z]+)\d+-p\d+\.[a-z]+\.hi-ho\.ne\.jp$/)
	{
		my $ken = $1	;
		my $kenban = &area47hiho($remo,$ken);
		if($kenban)	{return $kenban;}
	}
	if($remo =~ /\.(\S+)\.mesh\.ad\.jp$/)
	{
		my $ken = $1	;
		my $kenban = &area47mesh($remo,$ken);
		if($kenban)	{return $kenban;}
	}
	if($remo =~ /(\S+)\.ppp\.u-netsurf\.ne\.jp$/)
	{
		my $ken = $1	;
		my $kenban = &area47unetsurf($remo,$ken);
		if($kenban)	{return $kenban;}
	}
	if($remo =~ /softbank(\d\d\d\d\d\d)\d+\.bbtec\.net$/)
	{
		my $ken = $1	;
		my $kenban = &area47sb($remo,$ken);
		if($kenban)	{return $kenban;}
	}
	if($remo =~ /\.zaq\.ne\.jp$/)
	{
		my $ken = $1	;
		my $kenban = &area47zaq($remo,$ken);
		if($kenban)	{return $kenban;}
	}
	if($remo =~ /\.([a-zA-Z\d]+)\.vectant\.ne\.jp$/)
	{
		my $ken = $1	;
		my $kenban = &area47vectant($remo,$ken);
		if($kenban)	{return $kenban;}
	}
	if($remo =~ /\.([\w-]+)\.ac\.jp$/)
	{
		my $ken = $1	;
		my $kenban = &area47ac($remo,$ken);
		if($kenban)	{return $kenban;}
	}
#	#catv
	{
		my $kenban = &area47catv($remo);
		if($kenban)	{return $kenban;}
	}
	return 99999;
}
sub area47dion
{
	my ($GB,$remo,$ken) = @_;

	if($ken =~ /^(KD\d\d\d\d\d\d\d\d\d)\d+/)	{$ken = $1;}
	elsif($ken =~ /^(KHP\d\d\d\d\d\d\d\d\d)\d+/)	{$ken = $1;}
	elsif($ken =~ /^([a-zA-Z]+\d\d\d)\d+/)		{$ken = $1;}

	my $r = int($FOX_KEN_DION{$ken})	;

	if(1 <= $r && $r <= 48)
	{
#if(open(LX,">> HOST29.000")){print LX "(ooo)$remo($ken) = $r\n";close(LX);}
		return $r	;
	}

	#���̓X���[
	if($GB->{MARU})			{return 65;}

#if(open(LX,">> HOST29.000")){print LX "(xxx)$remo($ken) = $r\n";close(LX);}
#&DispError2($GB,"�d�q�q�n�q�I","�udion.ne.jp�v�͂����Ȃ��̂�!!<br><a href=\"http://qb5.2ch.net/test/read.cgi/operate/1175759037/l5n\">������</a>fusianasan���Č����񍐂��ăl");

	return 65;
}
sub area47asahinet
{
	my ($remo,$ken) = @_;

	if($ken =~ /^([a-z]\d\d\d)\d+\.ppp/)	{$ken = $1;}

	my $r = int($FOX_KEN_ASAHI{$ken})	;

	if(1 <= $r && $r <= 48)
	{
#if(open(LX,">> HOST29.000")){print LX "(ooo)$remo($ken) = $r\n";close(LX);}
		return $r	;
	}
#if(open(LX,">> HOST29.000")){print LX "(xxx)$remo($ken) = $r\n";close(LX);}

	return 69;
}
sub area47home
{
	my ($remo,$ken) = @_;

	if($ken =~ /^61-27-/)		{return 1;}	#�k�C��
	if($ken =~ /^61-25-140-/)	{return 8;}	#���
	if($ken =~ /^61-26-231-/)	{return 8;}	#���
	if($ken =~ /^59-171-144-/)	{return 10;}	#�Q�n
	if($ken =~ /^61-24-20-/)	{return 10;}	#�Q�n
	if($ken =~ /^59-171-106-/)	{return 11;}	#���
	if($ken =~ /^61-21-248-/)	{return 11;}	#���
	if($ken =~ /^61-21-253-/)	{return 11;}	#���
	if($ken =~ /^61-23-223-/)	{return 11;}	#���
	if($ken =~ /^203-165-84-/)	{return 11;}	#���
	if($ken =~ /^203-165-244-/)	{return 11;}	#���
	if($ken =~ /^210-20-165-/)	{return 11;}	#���
	if($ken =~ /^210-20-196-/)	{return 11;}	#���
	if($ken =~ /^61-23-72-/)	{return 12;}	#��t
	if($ken =~ /^61-23-94-/)	{return 12;}	#��t
	if($ken =~ /^61-24-24-/)	{return 12;}	#��t
	if($ken =~ /^203-165-164-/)	{return 12;}	#��t
	if($ken =~ /^210-194-64-/)	{return 12;}	#��t
	if($ken =~ /^210-194-66-/)	{return 12;}	#��t
	if($ken =~ /^59-171-201-/)	{return 13;}	#����
	if($ken =~ /^60-62-121-/)	{return 13;}	#����
	if($ken =~ /^61-23-157-/)	{return 13;}	#����
	if($ken =~ /^61-23-171-/)	{return 13;}	#����
	if($ken =~ /^61-24-32-/)	{return 13;}	#����
	if($ken =~ /^61-26-3-/)		{return 13;}	#����
	if($ken =~ /^61-26-36-/)	{return 13;}	#����
	if($ken =~ /^61-26-50-/)	{return 13;}	#����
	if($ken =~ /^61-26-232-/)	{return 13;}	#����
	if($ken =~ /^124-144-94-/)	{return 13;}	#����
	if($ken =~ /^125-14-111-/)	{return 13;}	#����
	if($ken =~ /^125-14-81-/)	{return 13;}	#����
	if($ken =~ /^125-14-240-/)	{return 13;}	#����
	if($ken =~ /^203-165-104-/)	{return 13;}	#����
	if($ken =~ /^203-165-204-/)	{return 13;}	#����
	if($ken =~ /^203-165-232-/)	{return 13;}	#����
	if($ken =~ /^210-20-66-/)	{return 13;}	#����
	if($ken =~ /^210-194-120-/)	{return 13;}	#����
	if($ken =~ /^210-194-152-/)	{return 13;}	#����
	if($ken =~ /^203-165-96-/)	{return 13;}	#����
	if($ken =~ /^61-21-73-/)	{return 14;}	#�_�ސ�
	if($ken =~ /^59-171-234-/)	{return 14;}	#�_�ސ�
	if($ken =~ /^61-24-194-/)	{return 14;}	#�_�ސ�
	if($ken =~ /^61-24-194-/)	{return 14;}	#�_�ސ�
	if($ken =~ /^61-26-205-/)	{return 14;}	#�_�ސ�
	if($ken =~ /^61-26-246-/)	{return 14;}	#�_�ސ�
	if($ken =~ /^61-26-253-/)	{return 14;}	#�_�ސ�
	if($ken =~ /^124-144-103-/)	{return 14;}	#�_�ސ�
	if($ken =~ /^125-14-212-/)	{return 14;}	#�_�ސ�
	if($ken =~ /^124-144-137-/)	{return 14;}	#�_�ސ�
	if($ken =~ /^210-20-154-/)	{return 14;}	#�_�ސ�
	if($ken =~ /^210-194-19-/)	{return 14;}	#�_�ސ�
	if($ken =~ /^210-194-62-/)	{return 14;}	#�_�ސ�
	if($ken =~ /^210-194-184-/)	{return 14;}	#�_�ސ�
	if($ken =~ /^210-194-240-/)	{return 14;}	#�_�ސ�
	if($ken =~ /^60-62-34-/)	{return 15;}	#�V��
	if($ken =~ /^125-15-201-/)	{return 25;}	#����
#	if($ken =~ /^61-27-136-/)	{return 31;}	#����
	if($ken =~ /^60-62-47-/)	{return 31;}	#����
	if($ken =~ /^61-22-30-/)	{return 35;}	#�R��
	if($ken =~ /^61-22-45-/)	{return 35;}	#�R��
	if($ken =~ /^61-22-39-/)	{return 40;}	#����
	if($ken =~ /^61-22-235-/)	{return 40;}	#����
	if($ken =~ /^61-26-232-/)	{return 40;}	#����

#	if(open(LX,">> HOST29.000")){print LX "(home)$remo($ken)\n";close(LX);}
#&DispError2($GB,"�d�q�q�n�q�I","�uhome.ne.jp�v�͂����Ȃ��̂�!!<br><a href=\"http://qb5.2ch.net/test/read.cgi/operate/1173710224/l5n\">������</a>fusianasan���Č����񍐂��ăl");
	return 69;
}
sub area47sb
{
	my ($remo,$ken) = @_;

	if($ken eq '126068')	{return 1;}	#�k�C��
	if($ken eq '218127')	{return 1;}	#�k�C��
	if($ken eq '219041')	{return 1;}	#�k�C��
	if($ken eq '219168')	{return 1;}	#�k�C��
	if($ken eq '219181')	{return 1;}	#�k�C��
	if($ken eq '221023')	{return 1;}	#�k�C��
	if($ken eq '221030')	{return 1;}	#�k�C��
	if($ken eq '221032')	{return 1;}	#�k�C��
	if($ken eq '221036')	{return 1;}	#�k�C��
	if($ken eq '221046')	{return 1;}	#�k�C��
	if($ken eq '221062')	{return 1;}	#�k�C��
	if($ken eq '221029')	{return 2;}	#�X
	if($ken eq '221054')	{return 2;}	#�X
	if($ken eq '219053')	{return 3;}	#���
	if($ken eq '219173')	{return 3;}	#���
	if($ken eq '221033')	{return 3;}	#���
	if($ken eq '221039')	{return 3;}	#���
	if($ken eq '221053')	{return 3;}	#���
	if($ken eq '221054')	{return 3;}	#���
	if($ken eq '126098')	{return 4;}	#�{��
	if($ken eq '218112')	{return 4;}	#�{��
	if($ken eq '219057')	{return 4;}	#�{��E�H�c
	if($ken eq '219171')	{return 4;}	#�{��
	if($ken eq '219208')	{return 4;}	#�{��
	if($ken eq '221020')	{return 4;}	#�{��
	if($ken eq '221026')	{return 4;}	#�{��
	if($ken eq '221105')	{return 4;}	#�H�c
	if($ken eq '221058')	{return 5;}	#�{��
	if($ken eq '219051')	{return 7;}	#�����E�{��
	if($ken eq '219057')	{return 7;}	#����
	if($ken eq '219172')	{return 7;}	#����
	if($ken eq '221044')	{return 7;}	#����
	if($ken eq '060100')	{return 8;}	#���
	if($ken eq '218137')	{return 8;}	#���
	if($ken eq '219006')	{return 8;}	#���
	if($ken eq '220005')	{return 8;}	#���
	if($ken eq '220006')	{return 8;}	#���
	if($ken eq '221040')	{return 8;}	#���
	if($ken eq '221043')	{return 8;}	#���
	if($ken eq '060091')	{return 9;}	#�Ȗ�
	if($ken eq '126096')	{return 9;}	#�Ȗ�
	if($ken eq '219055')	{return 9;}	#�Ȗ�
	if($ken eq '219056')	{return 9;}	#�Ȗ�
	if($ken eq '219192')	{return 9;}	#�Ȗ�
	if($ken eq '220004')	{return 9;}	#�Ȗ�
	if($ken eq '221027')	{return 9;}	#�Ȗ�
	if($ken eq '221031')	{return 9;}	#�Ȗ�
	if($ken eq '220003')	{return 11;}	#�Q�n
	if($ken eq '220007')	{return 11;}	#�Q�n
	if($ken eq '060086')	{return 11;}	#���
	if($ken eq '218128')	{return 11;}	#���
	if($ken eq '218118')	{return 11;}	#���
	if($ken eq '218119')	{return 11;}	#���
	if($ken eq '218177')	{return 11;}	#���
	if($ken eq '219012')	{return 11;}	#���
	if($ken eq '219013')	{return 11;}	#���
	if($ken eq '219014')	{return 11;}	#���
	if($ken eq '219058')	{return 11;}	#��ʁE�Q�n
	if($ken eq '219181')	{return 11;}	#���
	if($ken eq '219182')	{return 11;}	#���
	if($ken eq '219183')	{return 11;}	#���
	if($ken eq '219193')	{return 11;}	#���
	if($ken eq '219194')	{return 11;}	#���
	if($ken eq '219199')	{return 11;}	#���
	if($ken eq '219201')	{return 11;}	#���
	if($ken eq '219214')	{return 11;}	#���
	if($ken eq '219200')	{return 11;}	#���
	if($ken eq '221018')	{return 11;}	#���
	if($ken eq '220001')	{return 11;}	#���
	if($ken eq '060088')	{return 12;}	#��t
	if($ken eq '060089')	{return 12;}	#��t
	if($ken eq '060101')	{return 12;}	#��t
	if($ken eq '126064')	{return 12;}	#��t
	if($ken eq '126112')	{return 12;}	#��t
	if($ken eq '218135')	{return 12;}	#��t
	if($ken eq '218178')	{return 12;}	#��t
	if($ken eq '218180')	{return 12;}	#��t
	if($ken eq '219010')	{return 12;}	#��t
	if($ken eq '219011')	{return 12;}	#��t
	if($ken eq '219016')	{return 12;}	#��t
	if($ken eq '219174')	{return 12;}	#��t
	if($ken eq '219176')	{return 12;}	#��t
	if($ken eq '219189')	{return 12;}	#��t
	if($ken eq '219190')	{return 12;}	#��t
	if($ken eq '219191')	{return 12;}	#��t
	if($ken eq '221022')	{return 12;}	#��t
	if($ken eq '221025')	{return 12;}	#��t
	if($ken eq '221038')	{return 12;}	#��t
	if($ken eq '221056')	{return 12;}	#��t
	if($ken eq '060076')	{return 13;}	#����
	if($ken eq '060081')	{return 13;}	#����
	if($ken eq '060085')	{return 13;}	#����
	if($ken eq '126065')	{return 13;}	#����
	if($ken eq '126080')	{return 13;}	#����
	if($ken eq '218130')	{return 13;}	#����
	if($ken eq '218132')	{return 13;}	#����
	if($ken eq '218133')	{return 13;}	#����
	if($ken eq '218134')	{return 13;}	#����
	if($ken eq '218138')	{return 13;}	#����
	if($ken eq '218176')	{return 13;}	#����
	if($ken eq '219000')	{return 13;}	#����
	if($ken eq '219001')	{return 13;}	#����
	if($ken eq '219002')	{return 13;}	#����
	if($ken eq '219003')	{return 13;}	#����
	if($ken eq '219004')	{return 13;}	#����
	if($ken eq '219005')	{return 13;}	#����
	if($ken eq '219007')	{return 13;}	#����
	if($ken eq '219008')	{return 13;}	#����
	if($ken eq '219009')	{return 13;}	#����
	if($ken eq '219011')	{return 13;}	#����
	if($ken eq '219015')	{return 13;}	#����
	if($ken eq '219018')	{return 13;}	#����
	if($ken eq '219017')	{return 13;}	#����
	if($ken eq '219019')	{return 13;}	#����
	if($ken eq '219036')	{return 13;}	#����
	if($ken eq '219037')	{return 13;}	#����
	if($ken eq '219169')	{return 13;}	#����
	if($ken eq '219176')	{return 13;}	#����
	if($ken eq '219184')	{return 13;}	#����
	if($ken eq '219185')	{return 13;}	#����
	if($ken eq '219186')	{return 13;}	#����
	if($ken eq '219187')	{return 13;}	#����
	if($ken eq '219188')	{return 13;}	#����
	if($ken eq '219195')	{return 13;}	#����
	if($ken eq '219196')	{return 13;}	#����
	if($ken eq '219197')	{return 13;}	#����
	if($ken eq '219198')	{return 13;}	#����
	if($ken eq '219215')	{return 13;}	#����
	if($ken eq '219218')	{return 13;}	#����
	if($ken eq '221016')	{return 13;}	#����
	if($ken eq '221021')	{return 13;}	#����
	if($ken eq '221028')	{return 13;}	#����
	if($ken eq '221034')	{return 13;}	#����
	if($ken eq '221041')	{return 13;}	#����
	if($ken eq '221106')	{return 13;}	#����
	if($ken eq '221108')	{return 13;}	#����
	if($ken eq '060082')	{return 14;}	#�_�ސ�
	if($ken eq '060083')	{return 14;}	#�_�ސ�
	if($ken eq '126067')	{return 14;}	#�_�ސ�
	if($ken eq '219204')	{return 14;}	#�_�ސ�
	if($ken eq '218139')	{return 14;}	#�_�ސ�
	if($ken eq '218140')	{return 14;}	#�_�ސ�
	if($ken eq '218141')	{return 14;}	#�_�ސ�
	if($ken eq '218144')	{return 14;}	#�_�ސ�
	if($ken eq '219035')	{return 14;}	#�_�ސ�
	if($ken eq '219038')	{return 14;}	#�_�ސ�
	if($ken eq '219039')	{return 14;}	#�_�ސ�
	if($ken eq '219042')	{return 14;}	#�_�ސ�
	if($ken eq '219043')	{return 14;}	#�_�ސ�
	if($ken eq '219044')	{return 14;}	#�_�ސ�
	if($ken eq '219045')	{return 14;}	#�_�ސ�
	if($ken eq '219046')	{return 14;}	#�_�ސ�
	if($ken eq '219052')	{return 14;}	#�_�ސ�
	if($ken eq '219175')	{return 14;}	#�_�ސ�
	if($ken eq '219177')	{return 14;}	#�_�ސ�
	if($ken eq '219178')	{return 14;}	#�_�ސ�
	if($ken eq '219179')	{return 14;}	#�_�ސ�
	if($ken eq '219180')	{return 14;}	#�_�ސ�
	if($ken eq '219202')	{return 14;}	#�_�ސ�
	if($ken eq '219205')	{return 14;}	#�_�ސ�
	if($ken eq '219206')	{return 13;}	#�_�ސ�E����
	if($ken eq '219207')	{return 14;}	#�_�ސ�
	if($ken eq '221017')	{return 14;}	#�_�ސ�
	if($ken eq '221019')	{return 14;}	#�_�ސ�
	if($ken eq '221037')	{return 14;}	#�_�ސ�
	if($ken eq '219040')	{return 15;}	#�V��
	if($ken eq '219058')	{return 15;}	#�V��
	if($ken eq '220008')	{return 15;}	#�V��
	if($ken eq '221052')	{return 15;}	#�V��
	if($ken eq '221060')	{return 15;}	#�V��
	if($ken eq '220021')	{return 16;}	#�x�R
	if($ken eq '220052')	{return 16;}	#�x�R
	if($ken eq '219213')	{return 17;}	#�ΐ�
	if($ken eq '221071')	{return 17;}	#�ΐ�
	if($ken eq '221081')	{return 17;}	#�ΐ�
	if($ken eq '221093')	{return 17;}	#�ΐ�
	if($ken eq '221095')	{return 17;}	#�ΐ�
	if($ken eq '219061')	{return 18;}	#����
	if($ken eq '220024')	{return 18;}	#����
	if($ken eq '220010')	{return 19;}	#�R���E�É�
	if($ken eq '220009')	{return 20;}	#����
	if($ken eq '126069')	{return 22;}	#�É�
	if($ken eq '218131')	{return 22;}	#�É�
	if($ken eq '218143')	{return 22;}	#�É�
	if($ken eq '219047')	{return 22;}	#�É�
	if($ken eq '219048')	{return 22;}	#�É�
	if($ken eq '220023')	{return 22;}	#�É��E��
	if($ken eq '220000')	{return 22;}	#�É�
	if($ken eq '220002')	{return 22;}	#�É�
	if($ken eq '221024')	{return 22;}	#�É��E�O�d
	if($ken eq '060096')	{return 23;}	#��
	if($ken eq '220031')	{return 23;}	#��
	if($ken eq '221035')	{return 23;}	#��
	if($ken eq '221045')	{return 23;}	#��
	if($ken eq '218122')	{return 23;}	#���m
	if($ken eq '218142')	{return 23;}	#���m
	if($ken eq '218179')	{return 23;}	#���m
	if($ken eq '219032')	{return 23;}	#���m
	if($ken eq '219033')	{return 23;}	#���m
	if($ken eq '219049')	{return 23;}	#���m
	if($ken eq '219050')	{return 23;}	#���m�E�O�d
	if($ken eq '219170')	{return 23;}	#���m
	if($ken eq '219203')	{return 23;}	#���m
	if($ken eq '219209')	{return 23;}	#���m
	if($ken eq '219210')	{return 23;}	#���m
	if($ken eq '220028')	{return 23;}	#���m
	if($ken eq '220029')	{return 23;}	#���m
	if($ken eq '220002')	{return 23;}	#���m
	if($ken eq '220030')	{return 23;}	#���m
	if($ken eq '221057')	{return 23;}	#���m
	if($ken eq '221059')	{return 23;}	#���m
	if($ken eq '221107')	{return 23;}	#���m
	if($ken eq '219054')	{return 24;}	#�O�d
	if($ken eq '220026')	{return 24;}	#�O�d
	if($ken eq '220027')	{return 24;}	#�O�d�E���m
	if($ken eq '218129')	{return 25;}	#����
	if($ken eq '220051')	{return 25;}	#����
	if($ken eq '221075')	{return 25;}	#����
	if($ken eq '218121')	{return 26;}	#���s
	if($ken eq '218123')	{return 26;}	#���s
	if($ken eq '219025')	{return 26;}	#���s
	if($ken eq '219029')	{return 26;}	#���s
	if($ken eq '219030')	{return 26;}	#���s�E����
	if($ken eq '219092')	{return 26;}	#���s
	if($ken eq '220041')	{return 26;}	#���s
	if($ken eq '220037')	{return 26;}	#���s
	if($ken eq '220046')	{return 26;}	#���s
	if($ken eq '220047')	{return 26;}	#���s
	if($ken eq '221055')	{return 26;}	#���s
	if($ken eq '2210920')	{return 26;}	#���s
	if($ken eq '060105')	{return 27;}	#���
	if($ken eq '218121')	{return 27;}	#���
	if($ken eq '218126')	{return 27;}	#���
	if($ken eq '218129')	{return 27;}	#���
	if($ken eq '218136')	{return 27;}	#���
	if($ken eq '218181')	{return 27;}	#���
	if($ken eq '218182')	{return 27;}	#���
	if($ken eq '219020')	{return 27;}	#���
	if($ken eq '219021')	{return 27;}	#���
	if($ken eq '219023')	{return 27;}	#���
	if($ken eq '219024')	{return 27;}	#���
	if($ken eq '219062')	{return 27;}	#���
	if($ken eq '220011')	{return 27;}	#���
	if($ken eq '220012')	{return 27;}	#���
	if($ken eq '220013')	{return 27;}	#���
	if($ken eq '220018')	{return 27;}	#���
	if($ken eq '220032')	{return 27;}	#���
	if($ken eq '220033')	{return 27;}	#���
	if($ken eq '220034')	{return 27;}	#���
	if($ken eq '220035')	{return 27;}	#���
	if($ken eq '220036')	{return 27;}	#���
	if($ken eq '220038')	{return 27;}	#���
	if($ken eq '220042')	{return 27;}	#���
	if($ken eq '060110')	{return 28;}	#����
	if($ken eq '218124')	{return 28;}	#����
	if($ken eq '218125')	{return 28;}	#����
	if($ken eq '218154')	{return 28;}	#����
	if($ken eq '219022')	{return 28;}	#����
	if($ken eq '219026')	{return 28;}	#����
	if($ken eq '219027')	{return 28;}	#����
	if($ken eq '220014')	{return 28;}	#����
	if($ken eq '220015')	{return 28;}	#����
	if($ken eq '220016')	{return 28;}	#����
	if($ken eq '220017')	{return 28;}	#����
	if($ken eq '220039')	{return 28;}	#����
	if($ken eq '220040')	{return 28;}	#����
	if($ken eq '220044')	{return 28;}	#����
	if($ken eq '221064')	{return 28;}	#����
	if($ken eq '221092')	{return 28;}	#����
	if($ken eq '218183')	{return 29;}	#�ޗǁE���s
	if($ken eq '126070')	{return 29;}	#�ޗ�
	if($ken eq '220043')	{return 29;}	#�ޗ�
	if($ken eq '221072')	{return 29;}	#�ޗ�
	if($ken eq '220050')	{return 30;}	#�a�̎R
	if($ken eq '060120')	{return 31;}	#����
	if($ken eq '221079')	{return 32;}	#����
	if($ken eq '060118')	{return 33;}	#���R
	if($ken eq '126087')	{return 33;}	#���R
	if($ken eq '218115')	{return 33;}	#���R
	if($ken eq '219063')	{return 33;}	#���R
	if($ken eq '220056')	{return 33;}	#���R
	if($ken eq '221084')	{return 33;}	#���R�E�L��
	if($ken eq '221094')	{return 33;}	#���R�E�L��
	if($ken eq '221097')	{return 33;}	#���R
	if($ken eq '221100')	{return 33;}	#���R
	if($ken eq '060116')	{return 34;}	#�L��
	if($ken eq '218120')	{return 34;}	#�L��
	if($ken eq '219060')	{return 34;}	#�L���E����
	if($ken eq '220019')	{return 34;}	#�L��
	if($ken eq '220020')	{return 34;}	#�L��
	if($ken eq '220025')	{return 34;}	#�L��
	if($ken eq '220053')	{return 34;}	#�L��
	if($ken eq '219034')	{return 35;}	#�R��
	if($ken eq '221063')	{return 35;}	#�R��
	if($ken eq '221085')	{return 35;}	#�R��
	if($ken eq '221086')	{return 36;}	#����
	if($ken eq '219028')	{return 37;}	#����
	if($ken eq '219211')	{return 37;}	#����
	if($ken eq '220045')	{return 37;}	#����
	if($ken eq '221080')	{return 37;}	#����
	if($ken eq '221096')	{return 37;}	#����
	if($ken eq '221076')	{return 38;}	#���Q
	if($ken eq '220048')	{return 38;}	#���Q
	if($ken eq '221089')	{return 39;}	#���m
	if($ken eq '126071')	{return 40;}	#����
	if($ken eq '126071')	{return 40;}	#����
	if($ken eq '060122')	{return 40;}	#����
	if($ken eq '218114')	{return 40;}	#����
	if($ken eq '218116')	{return 40;}	#����
	if($ken eq '218117')	{return 40;}	#����
	if($ken eq '219212')	{return 40;}	#����
	if($ken eq '220054')	{return 40;}	#����
	if($ken eq '220058')	{return 40;}	#����
	if($ken eq '220059')	{return 40;}	#����
	if($ken eq '220060')	{return 40;}	#����
	if($ken eq '220061')	{return 40;}	#����
	if($ken eq '221098')	{return 40;}	#����
	if($ken eq '221078')	{return 40;}	#����
	if($ken eq '221098')	{return 40;}	#����
	if($ken eq '221101')	{return 40;}	#����
	if($ken eq '220020')	{return 41;}	#����E����
	if($ken eq '221067')	{return 41;}	#����
	if($ken eq '220055')	{return 42;}	#����
	if($ken eq '221083')	{return 43;}	#�F�{
	if($ken eq '221088')	{return 43;}	#�F�{
	if($ken eq '220022')	{return 43;}	#�F�{
	if($ken eq '060125')	{return 44;}	#�啪
	if($ken eq '218113')	{return 44;}	#�啪
	if($ken eq '220062')	{return 44;}	#�啪
	if($ken eq '221077')	{return 45;}	#�{��
	if($ken eq '220063')	{return 46;}	#������
	if($ken eq '221065')	{return 46;}	#������
	if($ken eq '221074')	{return 46;}	#������
	if($ken eq '221082')	{return 46;}	#������
	if($ken eq '221087')	{return 46;}	#������
	if($ken eq '221091')	{return 46;}	#������
	if($ken eq '219031')	{return 47;}	#����
	if($ken eq '220057')	{return 47;}	#����
	if($ken eq '220049')	{return 42;}	#�����l��(���m)

#&DispError2($GB,"�d�q�q�n�q�I","�u�s����softbank�v�͂����Ȃ��̂�!!<br><a href=\"http://qb5.2ch.net/test/read.cgi/operate/1173710224/\">������</a>fusianasan���Č����񍐂��ăl");

	return 49;
#	if(open(LX,">> HOST29.000")){print LX "$remo($ken)\n";close(LX);}
	return 0			;
}
sub area47hiho
{
	my ($remo,$ken) = @_;

	if($ken eq 'west')	{return 57;}
	if($ken eq 'east')	{return 58;}
	if($ken eq 'nrm')	{return 51;}
	if($ken eq 'tky')	{return 13;}
	if($ken eq 'osk')	{return 27;}
	if($ken eq 'stm')	{return 11;}
	if($ken eq 'kwg')	{return 11;}
	if($ken eq 'kng')	{return 14;}
	if($ken eq 'ykh')	{return 14;}
	if($ken eq 'shg')	{return 25;}
	if($ken eq 'oky')	{return 33;}
	if($ken eq 'fks')	{return 7;}
	if($ken eq 'aic')	{return 23;}
	if($ken eq 'kgw')	{return 37;}
	if($ken eq 'hkd')	{return 1;}
	if($ken eq 'chb')	{return 12;}
	if($ken eq 'myg')	{return 4;}
	if($ken eq 'kyt')	{return 26;}
	if($ken eq 'gmm')	{return 10;}
	if($ken eq 'amr')	{return 2;}
	if($ken eq 'fkk')	{return 40;}
	if($ken eq 'mie')	{return 24;}
	if($ken eq 'hrs')	{return 34;}
	if($ken eq 'tcg')	{return 9;}
	if($ken eq 'ngs')	{return 42;}
	if($ken eq 'hyg')	{return 28;}
	if($ken eq 'akt')	{return 5;}
	if($ken eq 'szk')	{return 22;}
	if($ken eq 'ngt')	{return 15;}
	if($ken eq 'smn')	{return 32;}
	if($ken eq 'ymn')	{return 19;}
	if($ken eq 'okn')	{return 47;}
	if($ken eq 'fki')	{return 18;}
	if($ken eq 'ibr')	{return 8;}
	if($ken eq 'kch')	{return 39;}
	if($ken eq 'gif')	{return 21;}
	if($ken eq 'tks')	{return 36;}
	if($ken eq 'wky')	{return 30;}
	if($ken eq 'nar')	{return 29;}
	if($ken eq 'iwt')	{return 3;}
	if($ken eq 'ngn')	{return 20;}
	if($ken eq 'isk')	{return 17;}
	if($ken eq 'myz')	{return 45;}
	if($ken eq 'ymt')	{return 6;}
	if($ken eq 'saga')	{return 41;}
	if($ken eq 'yamaguchi')	{return 35;}
	if($ken eq 'oita')	{return 44;}
	if($ken eq 'toyama')	{return 16;}
	if($ken eq 'shiga')	{return 25;}
	if($ken eq 'kagoshima')	{return 46;}
	if($ken eq 'ehime')	{return 38;}
	if($ken eq 'kumamoto')	{return 43;}
	if($ken eq 'tottori')	{return 31;}
#nrm1-p59.tepco.hi-ho.ne.jp(nrm)
	if($ken eq 'snj')	{return 13;}	#
	if($ken eq 'snt')	{return 13;}	#
	if($ken eq 'wdb')	{return 13;}	#
	if($ken eq 'hoj')	{return 13;}	#
	if($ken eq 'edg')	{return 60;}	#

#	if(open(LX,">> HOST29.000")){print LX "(hiho)$remo($ken)\n";close(LX);}
	return 0			;
}
sub area47infoweb
{
	my ($remo,$ken) = @_;


	if($remo =~ /oyma(\d+|\d+n\d+)\.catv.ppp.infoweb.ne.jp$/)	{return 9;}	#�Ȗ،�(09)
	if($remo =~ /fnbs(\d+|\d+n\d+)\.catv.ppp.infoweb.ne.jp$/)	{return 12;}	#��t��(12)
	if($remo =~ /nkno(\d+|\d+n\d+)\.catv.ppp.infoweb.ne.jp$/)	{return 13;}	#�����s(13)
	if($remo =~ /ohta(\d+|\d+n\d+)\.catv.ppp.infoweb.ne.jp$/)	{return 13;}	#
	if($remo =~ /ktsk(\d+|\d+n\d+)\.catv.ppp.infoweb.ne.jp$/)	{return 13;}	#
	if($remo =~ /hcou(\d+|\d+n\d+)\.catv.ppp.infoweb.ne.jp$/)	{return 13;}	#
	if($remo =~ /tkbn(\d+|\d+n\d+)\.catv.ppp.infoweb.ne.jp$/)	{return 13;}	#
	if($remo =~ /odwr(\d+|\d+n\d+)\.catv.ppp.infoweb.ne.jp$/)	{return 14;}	#�_�ސ쌧(14)
	if($remo =~ /youx(\d+|\d+n\d+)\.catv.ppp.infoweb.ne.jp$/)	{return 21;}	#�򕌌�(21)
	if($remo =~ /ymgt(\d+|\d+n\d+)\.catv.ppp.infoweb.ne.jp$/)	{return 21;}	#�򕌌�(21)
	if($remo =~ /hmmt(\d+|\d+n\d+)\.catv.ppp.infoweb.ne.jp$/)	{return 22;}	#�É���(22)
	if($remo =~ /aksi(\d+|\d+n\d+)\.catv.ppp.infoweb.ne.jp$/)	{return 28;}	#���Ɍ�(28)
	if($remo =~ /kkgw(\d+|\d+n\d+)\.catv.ppp.infoweb.ne.jp$/)	{return 28;}	#
	if($remo =~ /kihn(\d+|\d+n\d+)\.catv.ppp.infoweb.ne.jp$/)	{return 28;}	#

	if($ken =~ /\.dup$/)	{return 61;}
	if($ken =~ /\.do$/)	{return 60;}
#	if($ken =~ /catv/)	{return 59;}

	if($ken =~ /\.(\w+)\.nt\./)	{$ken = $1;}
	elsif($ken =~ /\.(\w+)\.te\./)	{$ken = $1;}
	elsif($ken =~ /ea([a-z]+)\d+\.adsl$/)	{$ken = $1;}
	elsif($ken =~ /ac([a-z]+)\d+\.adsl$/)	{$ken = $1;}
	elsif($ken =~ /tc([a-z]+)\d+\.adsl$/)	{$ken = $1;}
	elsif($ken =~ /ct([a-z]+)\d+\.adsl$/)	{$ken = $1;}
	elsif($ken =~ /th([a-z]+)\d+\.adsl$/)	{$ken = $1;}
	elsif($ken =~ /st([a-z]+)\d+\.adsl$/)	{$ken = $1;}
	elsif($ken =~ /\.([a-z]+)\.fnt\.ftth$/)	{$ken = $1;}
	elsif($ken =~ /[a-z][a-z]([a-z]+)\d+\.adsl$/)	{$ken = $1;}

	if($ken =~ /air/i)	{return 60;}

	if($ken eq 'tkyo')	{return 13;}
	if($ken eq 'tckw')	{return 13;}
	if($ken eq 'atgi')	{return 13;}
	if($ken eq 'oska')	{return 27;}
	if($ken eq 'sitm')	{return 11;}
	if($ken eq 'urwa')	{return 11;}
	if($ken eq 'kngw')	{return 14;}
	if($ken eq 'ykhm')	{return 14;}
	if($ken eq 'siga')	{return 25;}
	if($ken eq 'okym')	{return 33;}
	if($ken eq 'fksm')	{return 7;}
	if($ken eq 'aich')	{return 23;}
	if($ken eq 'ngya')	{return 23;}
	if($ken eq 'kgwa')	{return 37;}
	if($ken eq 'tkmt')	{return 37;}
	if($ken eq 'ymgc')	{return 35;}
	if($ken eq 'hkid')	{return 1;}
	if($ken eq 'spro')	{return 1;}
	if($ken eq 'chba')	{return 12;}
	if($ken eq 'mygi')	{return 4;}
	if($ken eq 'sndi')	{return 4;}
	if($ken eq 'kyto')	{return 26;}
	if($ken eq 'gnma')	{return 10;}
	if($ken eq 'aomr')	{return 2;}
	if($ken eq 'fkok')	{return 40;}
	if($ken eq 'ooit')	{return 44;}
	if($ken eq 'miex')	{return 24;}
	if($ken eq 'hrsm')	{return 34;}
	if($ken eq 'tcgi')	{return 9;}
	if($ken eq 'ngsk')	{return 42;}
	if($ken eq 'hygo')	{return 28;}
	if($ken eq 'kube')	{return 28;}
	if($ken eq 'akta')	{return 5;}
	if($ken eq 'szok')	{return 22;}
	if($ken eq 'yizu')	{return 22;}
	if($ken eq 'nigt')	{return 15;}
	if($ken eq 'oknw')	{return 47;}
	if($ken eq 'fkui')	{return 18;}
	if($ken eq 'ibrk')	{return 8;}
	if($ken eq 'tyma')	{return 16;}
	if($ken eq 'kuch')	{return 39;}
	if($ken eq 'gifu')	{return 21;}
	if($ken eq 'tksm')	{return 36;}
	if($ken eq 'shga')	{return 25;}
	if($ken eq 'kgsm')	{return 46;}
	if($ken eq 'nara')	{return 29;}
	if($ken eq 'iwte')	{return 3;}
	if($ken eq 'ngno')	{return 20;}
	if($ken eq 'iskw')	{return 17;}
	if($ken eq 'knzw')	{return 17;}
	if($ken eq 'saga')	{return 41;}
	if($ken eq 'ehme')	{return 38;}
	if($ken eq 'kmmt')	{return 43;}
	if($ken eq 'ttri')	{return 31;}
	if($ken eq 'smne')	{return 32;}
	if($ken eq 'ymns')	{return 19;}
	if($ken eq 'wkym')	{return 30;}
	if($ken eq 'ymgt')	{return 6;}
	if($ken eq 'myzk')	{return 45;}

#	if(open(LX,">> HOST29.000")){print LX "$remo($ken)\n";close(LX);}
	return 0			;
}
sub area47mesh
{
	my ($remo,$ken) = @_;

	if($ken eq 'tky')	{return 13;}
	if($ken eq 'osk')	{return 27;}
	if($ken eq 'stm')	{return 11;}
	if($ken eq 'kng')	{return 14;}
	if($ken eq 'sig')	{return 25;}
	if($ken eq 'oky')	{return 33;}
	if($ken eq 'fks')	{return 7;}
	if($ken eq 'aic')	{return 23;}
	if($ken eq 'kgw')	{return 37;}
	if($ken eq 'ygc')	{return 35;}
	if($ken eq 'hkd')	{return 1;}
	if($ken eq 'chb')	{return 12;}
	if($ken eq 'myg')	{return 4;}
	if($ken eq 'kyt')	{return 26;}
	if($ken eq 'gnm')	{return 10;}
	if($ken eq 'aom')	{return 2;}
	if($ken eq 'fko')	{return 40;}
	if($ken eq 'oit')	{return 44;}
	if($ken eq 'mie')	{return 24;}
	if($ken eq 'hrs')	{return 34;}
	if($ken eq 'tcg')	{return 9;}
	if($ken eq 'ngs')	{return 42;}
	if($ken eq 'hyg')	{return 28;}
	if($ken eq 'szo')	{return 22;}
	if($ken eq 'nig')	{return 15;}
	if($ken eq 'ymn')	{return 19;}
	if($ken eq 'okn')	{return 47;}
	if($ken eq 'iba')	{return 8;}
	if($ken eq 'koc')	{return 39;}
	if($ken eq 'gif')	{return 21;}
	if($ken eq 'fki')	{return 18;}
	if($ken eq 'tks')	{return 36;}
	if($ken eq 'kgs')	{return 46;}
	if($ken eq 'wky')	{return 30;}
	if($ken eq 'nra')	{return 29;}
	if($ken eq 'iwa')	{return 3;}
	if($ken eq 'ngn')	{return 20;}
	if($ken eq 'isk')	{return 17;}
	if($ken eq 'sag')	{return 41;}
	if($ken eq 'ygt')	{return 6;}
	if($ken eq 'kmm')	{return 43;}
	if($ken eq 'myz')	{return 45;}
	if($ken eq 'tym')	{return 16;}
	if($ken eq 'ttr')	{return 31;}
	if($ken eq 'aki')	{return 5;}
	if($ken eq 'smn')	{return 32;}
	if($ken eq 'shiga')	{return 25;}
	if($ken eq 'ehm')	{return 38;}

#	if(open(LX,">> HOST29.000")){print LX "(mesh)$remo($ken)\n";close(LX);}
	return 0			;
}
sub area47zaq
{
	my ($remo,$ken) = @_;

	#���s�{
	if($remo =~ /zaq3d2e6[89a-f]..\.zaq.ne.jp/)	{return 26;}
	if($remo =~ /zaq3dc06[c-f]..\.zaq.ne.jp/)	{return 26;}
	if($remo =~ /zaqd37c8[0-5]..\.zaq.ne.jp/)	{return 26;}
	if($remo =~ /zaqd37c8[67]..\.zaq.ne.jp/)	{return 26;}
	if($remo =~ /zaqd37cc[0-9a-c]..\.zaq.ne.jp/)	{return 26;}
	if($remo =~ /zaqd37cc[d-f]..\.zaq.ne.jp/)	{return 26;}
	if($remo =~ /zaqd38730..\.zaq.ne.jp/)		{return 26;}
	if($remo =~ /zaqd3873[1-7]..\.zaq.ne.jp/)	{return 26;}

	#���Ɍ�
	if($remo =~ /zaq3d2e7...\.zaq.ne.jp/)		{return 28;}
	if($remo =~ /zaq3d2ec[0-7]..\.zaq.ne.jp/)	{return 28;}
	if($remo =~ /zaq3d2ec[89a-f]..\.zaq.ne.jp/)	{return 28;}
	if($remo =~ /zaq3d2ef...\.zaq.ne.jp/)		{return 28;}
	if($remo =~ /zaq3d738[0-9a]..\.zaq.ne.jp/)	{return 28;}
	if($remo =~ /zaq3d738b..\.zaq.ne.jp/)		{return 28;}
	if($remo =~ /zaq3d739...\.zaq.ne.jp/)		{return 28;}
	if($remo =~ /zaq3dc04[0-9]..\.zaq.ne.jp/)	{return 28;}
	if($remo =~ /zaq3dc0(4[a-f]|5.)..\.zaq.ne.jp/)	{return 28;}
	if($remo =~ /zaq3dcd8...\.zaq.ne.jp/)		{return 28;}
	if($remo =~ /zaq3dcdb[89a]..\.zaq.ne.jp/)	{return 28;}
	if($remo =~ /zaq3dcdb[b-f]..\.zaq.ne.jp/)	{return 28;}
	if($remo =~ /zaq7d04[ab]...\.zaq.ne.jp/)	{return 28;}
	if($remo =~ /zaq7d04c...\.zaq.ne.jp/)		{return 28;}
	if($remo =~ /zaqd37c(0[89a-f]|1.)..\.zaq.ne.jp/){return 28;}
	if($remo =~ /zaqd37c7[0-9a-d]..\.zaq.ne.jp/)	{return 28;}
	if($remo =~ /zaqd37c9[0-5]..\.zaq.ne.jp/)	{return 28;}
	if($remo =~ /zaqd37c9[67]..\.zaq.ne.jp/)	{return 28;}
	if($remo =~ /zaqd37c9[89ab]..\.zaq.ne.jp/)	{return 28;}
	if($remo =~ /zaqd3875[89a-f]..\.zaq.ne.jp/)	{return 28;}
	if($remo =~ /zaqdb73f[01]..\.zaq.ne.jp/)	{return 28;}
	if($remo =~ /zaqdb73f[2-9a-f]..\.zaq.ne.jp/)	{return 28;}

	#���ꌧ
	if($remo =~ /zaqd378b[4-7]..\.zaq.ne.jp/)	{return 25;}	#�c��͂��ׂđ��{
	#from whois & LogCounter(zaq.txt)
	return 27;
}
sub area47sonet
{
	my ($remo,$ken) = @_;

	if($ken =~ /freedc$/)	{return 901;}
	elsif($ken =~ /ah$/)	{return 901;}
	elsif($ken =~ /te$/)	{$ken =~ s/te$//;}
	elsif($ken =~ /nt$/)	{$ken =~ s/nt$//;}
	elsif($ken =~ /ac$/)	{$ken =~ s/ac$//;}
	elsif($ken =~ /ea$/)	{$ken =~ s/ea$//;}
	elsif($ken =~ /us$/)	{$ken =~ s/us$//;}
	elsif($ken =~ /ff$/)	{$ken =~ s/ff$//;}

	if($ken eq 'tubems')	{return 52;}
	if($ken eq 'west')	{return 57;}
	if($ken eq 'east')	{return 58;}
	if($ken eq 'wpdabw')	{return 60;}

	if($ken eq 'tkyo')	{return 13;}
	if($ken eq 'toky')	{return 13;}
	if($ken eq 'ntky')	{return 13;}
	if($ken eq 'osak')	{return 27;}
	if($ken eq 'sitm')	{return 11;}
	if($ken eq 'uraw')	{return 11;}
	if($ken eq 'ykhm')	{return 14;}
	if($ken eq 'kngw')	{return 14;}
	if($ken eq 'siga')	{return 25;}
	if($ken eq 'okym')	{return 33;}
	if($ken eq 'fksm')	{return 7;}
	if($ken eq 'aici')	{return 23;}
	if($ken eq 'ngya')	{return 23;}
	if($ken eq 'kagw')	{return 37;}
	if($ken eq 'ymgc')	{return 35;}
	if($ken eq 'hkid')	{return 1;}
	if($ken eq 'sppr')	{return 1;}
	if($ken eq 'chib')	{return 12;}
	if($ken eq 'miyg')	{return 4;}
	if($ken eq 'sndi')	{return 4;}
	if($ken eq 'kyot')	{return 26;}
	if($ken eq 'gunm')	{return 10;}
	if($ken eq 'aomr')	{return 2;}
	if($ken eq 'fkok')	{return 40;}
	if($ken eq 'oita')	{return 44;}
	if($ken eq 'mie')	{return 24;}
	if($ken eq 'mie-')	{return 24;}
	if($ken eq 'hrsm')	{return 34;}
	if($ken eq 'tocg')	{return 9;}
	if($ken eq 'kobe')	{return 28;}
	if($ken eq 'hyog')	{return 28;}
	if($ken eq 'akit')	{return 5;}
	if($ken eq 'szok')	{return 22;}
	if($ken eq 'nigt')	{return 15;}
	if($ken eq 'ymns')	{return 19;}
	if($ken eq 'oknw')	{return 47;}
	if($ken eq 'fuki')	{return 18;}
	if($ken eq 'ibrk')	{return 8;}
	if($ken eq 'toym')	{return 16;}
	if($ken eq 'koci')	{return 39;}
	if($ken eq 'gifu')	{return 21;}
	if($ken eq 'tksm')	{return 36;}
	if($ken eq 'kgsm')	{return 46;}
	if($ken eq 'wkym')	{return 30;}
	if($ken eq 'nara')	{return 29;}
	if($ken eq 'iwat')	{return 3;}
	if($ken eq 'ngno')	{return 20;}
	if($ken eq 'iskw')	{return 17;}
	if($ken eq 'saga')	{return 41;}
	if($ken eq 'ymgt')	{return 6;}
	if($ken eq 'ehim')	{return 38;}
	if($ken eq 'kmmt')	{return 43;}
	if($ken eq 'myzk')	{return 45;}
	if($ken eq 'totr')	{return 31;}
	if($ken eq 'shiga')	{return 25;}
	if($ken eq 'ngsk')	{return 42;}
	if($ken eq 'shimane')	{return 32;}

	if($ken eq 'w032bw')	{return 60;}
	if($ken eq 'onenum')	{return 61;}
	if($ken eq 'tubehm')	{return 72;}


#	if(open(LX,">> HOST29.000")){print LX "(sonet)$remo($ken)\n";close(LX);}
	return 0			;
}
sub area47dti
{
	my ($remo,$ken) = @_;

	if($ken eq 'airedge')	{return 60;}
	if($ken eq 'west')	{return 57;}
	if($ken eq 'east')	{return 58;}
	if($ken eq 'otemachi')	{return 13;}
	if($ken eq 'iidabashi')	{return 13;}
	if($ken eq 'tokyo')	{return 13;}
	if($ken eq 'tachikawa')	{return 13;}
	if($ken eq 'osaka')	{return 27;}
	if($ken eq 'ohsaka')	{return 27;}
	if($ken eq 'saitama')	{return 11;}
	if($ken eq 'soka')	{return 11;}
	if($ken eq 'kuki')	{return 11;}
	if($ken eq 'urawa')	{return 11;}
	if($ken eq 'kanagawa')	{return 14;}
	if($ken eq 'yokohama')	{return 14;}
	if($ken eq 'kawasaki')	{return 14;}
	if($ken eq 'siga')	{return 25;}
	if($ken eq 'otsu')	{return 25;}
	if($ken eq 'okayama')	{return 33;}
	if($ken eq 'fukusima')	{return 7;}
	if($ken eq 'fukushima')	{return 7;}
	if($ken eq 'aichi')	{return 23;}
	if($ken eq 'nagoya')	{return 23;}
	if($ken eq 'yokkaichi')	{return 23;}
	if($ken eq 'kagawa')	{return 37;}
	if($ken eq 'takamatsu')	{return 37;}
	if($ken eq 'yamaguchi')	{return 35;}
	if($ken eq 'hokkaido')	{return 1;}
	if($ken eq 'sapporo')	{return 1;}
	if($ken eq 'osaka')	{return 27;}
	if($ken eq 'chiba')	{return 12;}
	if($ken eq 'ichikawa')	{return 12;}
	if($ken eq 'miyagi')	{return 4;}
	if($ken eq 'sendai')	{return 4;}
	if($ken eq 'kyoto')	{return 26;}
	if($ken eq 'gunma')	{return 10;}
	if($ken eq 'maebashi')	{return 10;}
	if($ken eq 'aomori')	{return 2;}
	if($ken eq 'fukuoka')	{return 40;}
	if($ken eq 'kurume')	{return 40;}
	if($ken eq 'oita')	{return 44;}
	if($ken eq 'mie')	{return 24;}
	if($ken eq 'hiroshima')	{return 34;}
	if($ken eq 'hirosima')	{return 34;}
	if($ken eq 'tochigi')	{return 9;}
	if($ken eq 'totigi')	{return 9;}
	if($ken eq 'utsunomiya'){return 9;}
	if($ken eq 'nagasaki')	{return 42;}
	if($ken eq 'hyogo')	{return 28;}
	if($ken eq 'kobe')	{return 28;}
	if($ken eq 'akita')	{return 5;}
	if($ken eq 'shizuoka')	{return 22;}
	if($ken eq 'niigata')	{return 15;}
	if($ken eq 'shimane')	{return 32;}
	if($ken eq 'yamanashi')	{return 19;}
	if($ken eq 'kofu')	{return 19;}
	if($ken eq 'okinawa')	{return 47;}
	if($ken eq 'fukui')	{return 18;}
	if($ken eq 'ibaraki')	{return 8;}
	if($ken eq 'toyama')	{return 16;}
	if($ken eq 'kochi')	{return 39;}
	if($ken eq 'gifu')	{return 21;}
	if($ken eq 'tokushima')	{return 36;}
	if($ken eq 'shiga')	{return 25;}
	if($ken eq 'kagoshima')	{return 46;}
	if($ken eq 'wakayama')	{return 30;}
	if($ken eq 'nara')	{return 29;}
	if($ken eq 'iwate')	{return 3;}
	if($ken eq 'nagano')	{return 20;}
	if($ken eq 'ishikawa')	{return 17;}
	if($ken eq 'kanazawa')	{return 17;}
	if($ken eq 'saga')	{return 41;}
	if($ken eq 'yamagata')	{return 6;}
	if($ken eq 'ehime')	{return 38;}
	if($ken eq 'matsuyama')	{return 38;}
	if($ken eq 'kumamoto')	{return 43;}
	if($ken eq 'miyazaki')	{return 45;}
	if($ken eq 'tottori')	{return 31;}

#	if(open(LX,">> HOST29.000")){print LX "$remo($ken)\n";close(LX);}
	return 0			;
}
sub area47odn
{
	my ($GB,$remo,$ken) = @_;

	if($ken =~ /^([A-Z0-9]+)[a-z]+-/)	{$ken = $1;}

	if($ken eq 'AH1')	{return 60;}	# ��
	if($ken eq 'TEP')	{return 51;}	# �֓��n��
	if($ken eq 'CEP')	{return 52;}	# �����n��
	if($ken eq 'EAO')	{return 57;}	# �����{
	if($ken eq 'EAT')	{return 58;}	# �����{
	if($ken eq 'SAP')	{return 1;}	# �k�C��
	if($ken eq 'SOD')	{return 1;}	# �k�C��
	if($ken eq 'OKI')	{return 2;}	# �X
	if($ken eq 'MRN')	{return 3;}	# ���
	if($ken eq 'AOB')	{return 4;}	# �{��
	if($ken eq 'NKD')	{return 5;}	# �H�c
	if($ken eq 'IMZ')	{return 6;}	# �R�`
	if($ken eq 'HNZ')	{return 7;}	# ����
	if($ken eq 'FKH')	{return 7;}	# ����
	if($ken eq 'AKA')	{return 8;}	# ���
	if($ken eq 'HRD')	{return 9;}	# �Ȗ�
	if($ken eq 'KKR')	{return 10;}	# �Q�n
	if($ken eq 'SKN')	{return 11;}	# ���
	if($ken eq 'FNA')	{return 12;}	# ��t
	if($ken eq 'OFS')	{return 13;}	# ����
	if($ken eq 'HDO')	{return 14;}	# �_�ސ�
	if($ken eq 'NGN')	{return 15;}	# �V��
	if($ken eq 'TYN')	{return 16;}	# �x�R
	if($ken eq 'KNZ')	{return 17;}	# �ΐ�
	if($ken eq 'KNN')	{return 17;}	# �ΐ�
	if($ken eq 'FKN')	{return 18;}	# ����
	if($ken eq 'KFN')	{return 19;}	# �R��
	if($ken eq 'SYD')	{return 20;}	# ����
	if($ken eq 'GFN')	{return 21;}	# ��
	if($ken eq 'SDD')	{return 22;}	# �É�
	if($ken eq 'SSJ')	{return 23;}	# ���m
	if($ken eq 'YKM')	{return 24;}	# �O�d
	if($ken eq 'OTU')	{return 25;}	# ����
	if($ken eq 'KYN')	{return 26;}	# ���s
	if($ken eq 'KYO')	{return 26;}	# ���s
	if($ken eq 'NWT')	{return 27;}	# ���
	if($ken eq 'OSA')	{return 27;}	# ���
	if($ken eq 'KBM')	{return 28;}	# ����
	if($ken eq 'DAJ')	{return 29;}	# �ޗ�
	if($ken eq 'WKN')	{return 30;}	# �a�̎R
	if($ken eq 'TTN')	{return 31;}	# ����
	if($ken eq 'SMN')	{return 32;}	# ����
	if($ken eq 'IMM')	{return 33;}	# ���R
	if($ken eq 'NIH')	{return 34;}	# �L��
	if($ken eq 'YGN')	{return 35;}	# �R��
	if($ken eq 'TKN')	{return 36;}	# ����
	if($ken eq 'TMN')	{return 37;}	# ����
	if($ken eq 'TKH')	{return 37;}	# ����
	if($ken eq 'MYN')	{return 38;}	# ���Q
	if($ken eq 'KCN')	{return 39;}	# ���m
	if($ken eq 'FKC')	{return 40;}	# ����
	if($ken eq 'TGS')	{return 41;}	# ����
	if($ken eq 'SCO')	{return 42;}	# ����
	if($ken eq 'OBY')	{return 43;}	# �F�{
	if($ken eq 'OMC')	{return 44;}	# �啪
	if($ken eq 'MZN')	{return 45;}	# �{��
	if($ken eq 'KMI')	{return 46;}	# ������
	if($ken eq 'YRM')	{return 47;}	# ����
	if($ken eq 'ATU')	{return 61;}	# �_�C�A���A�b�v
	if($ken eq 'TYO')	{return 61;}	# �_�C�A���A�b�v
	if($ken eq 'CBC')	{return 61;}	# �_�C�A���A�b�v
	if($ken eq 'TBT')	{return 61;}	# �_�C�A���A�b�v
	if($ken eq 'KAJ')	{return 61;}	# �_�C�A���A�b�v
	if($ken eq 'PAX')	{return 61;}	# �_�C�A���A�b�v
	if($ken eq 'RIF')	{return 61;}	# �_�C�A���A�b�v
	if($ken eq 'NIG')	{return 61;}	# �_�C�A���A�b�v

#	if(open(LX,">> HOST29.000")){print LX "(odn)$remo($ken)\n";close(LX);}
&DispError2($GB,"�d�q�q�n�q�I","�u���ł�v�͂����Ȃ��̂�!!<br><a href=\"http://qb5.2ch.net/test/read.cgi/operate/1173710224/\">������</a>fusianasan���Č����񍐂��ăl");

	if($ken eq 'NOT')	{return 66;}

#	if(open(LX,">> HOST29.000")){print LX "(odn)$remo($ken)\n";close(LX);}
	return 66;
}
sub area47unetsurf
{
	my ($remo,$ken) = @_;

	if($ken =~ /[a-zA-Z]+-([a-z][a-z])\.[\d-]+/)	{$ken = $1;}

	if($ken =~ /\.at$/)	{return 13;}
	if($ken eq 'es')	{return 58;}
	if($ken eq 'os')	{return 57;}
	if($ken eq 'tk')	{return 58;}

#	if(open(LX,">> HOST29.000")){print LX "(unetsurf)$remo($ken)\n";close(LX);}
	return 0;
}
sub area472iij
{
	my ($remo,$ken) = @_;

	if($ken =~ /[a-zA-Z]+([a-z][a-z])\./)	{$ken = $1;}

#	if(open(LX,">> HOST29.000")){print LX "(2iij)$remo($ken)\n";close(LX);}
	return 90;
}
sub area47ac
{
	my ($remo,$ken) = @_;

	if($ken eq 'hokkyodai')		{return 1;}
	if($ken eq 'hit')		{return 1;}
	if($ken eq 'midorigaoka')	{return 1;}
	if($ken eq 'hokusei')		{return 1;}
	if($ken eq 'hokudai')		{return 1;}
	if($ken eq 'iwate-pu')		{return 1;}
	if($ken eq 'ichinoseki')	{return 3;}
	if($ken eq 'ichinoseki')	{return 3;}
	if($ken eq 'tohoku')		{return 4;}
	if($ken eq 'shokei')		{return 4;}
	if($ken eq 'seiwa')		{return 4;}
	if($ken eq 'tohoku-gakuin')	{return 4;}
	if($ken eq 'sendai-ct')		{return 4;}
	if($ken eq 'akita-nct')		{return 5;}
	if($ken eq 'yamagata-u')	{return 6;}
	if($ken eq 'u-aizu')		{return 7;}
	if($ken eq 'fmu')		{return 7;}
	if($ken eq 'tsukuba')		{return 8;}
	if($ken eq 'ibaraki')		{return 8;}
	if($ken eq 'jichi')		{return 9;}
	if($ken eq 'utsunomiya-u')	{return 9;}
	if($ken eq 'dendai')		{return 11;}
	if($ken eq 'saitama-med')	{return 11;}
	if($ken eq 'dokkyo')		{return 11;}
	if($ken eq 'waseda')		{return 13;}
	if($ken eq 'tus')		{return 13;}
	if($ken eq 'uec')		{return 13;}
	if($ken eq 'titech')		{return 13;}
	if($ken eq 'jec')		{return 13;}
	if($ken eq 'nodai')		{return 13;}
	if($ken eq 'tuat')		{return 13;}
	if($ken eq 'jikei')		{return 13;}
	if($ken eq 'shobi')		{return 13;}
	if($ken eq 'keio')		{return 13;}
	if($ken eq 'gakushuin')		{return 13;}
	if($ken eq 'neec')		{return 13;}
	if($ken eq 'twmu')		{return 13;}
	if($ken eq 'icu')		{return 13;}
	if($ken eq 'toho-u')		{return 13;}
	if($ken eq 'kokugakuin')	{return 13;}
	if($ken eq 'u-tokyo')		{return 13;}
	if($ken eq 'nihon-u')		{return 13;}
	if($ken eq 'shobi-u')		{return 13;}
	if($ken eq 'chuo-u')		{return 13;}
	if($ken eq 'toyo')		{return 13;}
	if($ken eq 'kitasato-u')	{return 13;}
	if($ken eq 'teikyo-u')		{return 13;}
	if($ken eq 'kaiyodai')		{return 13;}
	if($ken eq 'ynu')		{return 14;}
	if($ken eq 'kanagawa-u')	{return 14;}
	if($ken eq 'toin')		{return 14;}
	if($ken eq 'niigata-u')		{return 15;}
	if($ken eq 'nagaokaut')		{return 15;}
	if($ken eq 'toyama-nct')	{return 16;}
	if($ken eq 'jaist')		{return 17;}
	if($ken eq 'fukui-nct')		{return 18;}
	if($ken eq 'shinshu-u')		{return 20;}
	if($ken eq 'iamas')		{return 21;}
	if($ken eq 'gifu-u')		{return 21;}
	if($ken eq 'shizuoka')		{return 22;}
	if($ken eq 'numazu-ct')		{return 22;}
	if($ken eq 'nig')		{return 22;}
	if($ken eq 'u-shizuoka-ken')	{return 22;}
	if($ken eq 'nitech')		{return 23;}
	if($ken eq 'nifs')		{return 23;}
	if($ken eq 'tut')		{return 23;}
	if($ken eq 'sozo')		{return 23;}
	if($ken eq 'chubu')		{return 23;}
	if($ken eq 'nanzan-u')		{return 23;}
	if($ken eq 'nagoya-u')		{return 23;}
	if($ken eq 'ims')		{return 23;}
	if($ken eq 'nibb')		{return 23;}
	if($ken eq 'tsudagakuen')	{return 24;}
	if($ken eq 'mie-u')		{return 24;}
	if($ken eq 'toba-cmt')		{return 24;}
	if($ken eq 'ritsumei')		{return 26;}
	if($ken eq 'kpu')		{return 26;}
	if($ken eq 'doshisha')		{return 26;}
	if($ken eq 'kyoto-u')		{return 26;}
	if($ken eq 'kit')		{return 26;}
	if($ken eq 'osaka-u')		{return 27;}
	if($ken eq 'kwansei')		{return 28;}
	if($ken eq 'kyoto-u')		{return 28;}
	if($ken eq 'kobedenshi')	{return 28;}
	if($ken eq 'hyo-med')		{return 28;}
	if($ken eq 'nara-su')		{return 29;}
	if($ken eq 'wakayama-u')	{return 30;}
	if($ken eq 'shimane-u')		{return 32;}
	if($ken eq 'ous')		{return 33;}
	if($ken eq 'kindai')		{return 33;}
	if($ken eq 'hiroshima-cu')	{return 34;}
	if($ken eq 'it-hiroshima')	{return 34;}
	if($ken eq 'yamaguchi-u')	{return 35;}
	if($ken eq 'tokushima-u')	{return 36;}
	if($ken eq 'shinonome')		{return 38;}
	if($ken eq 'kochi-u')		{return 39;}
	if($ken eq 'fit')		{return 40;}
	if($ken eq 'kyutech')		{return 40;}
	if($ken eq 'fukuoka-u')		{return 40;}
	if($ken eq 'kyushu-u')		{return 40;}
	if($ken eq 'nagasaki-u')	{return 41;}
	if($ken eq 'kumamoto-u')	{return 43;}
	if($ken eq 'miyazaki-u')	{return 45;}
	if($ken eq 'u-ryukyu')		{return 47;}
	if($ken eq 'kbc')		{return 47;}

#	if(open(LX,">> HOST29.001")){print LX "(ac.jp)$remo($ken)\n";close(LX);}
	return 0;
}
sub area47vectant
{
	my ($remo,$ken) = @_;

	my $we = 57		;	#e=57 w=58
	if($ken =~ /^e/)	{$we = 57;}
	if($ken =~ /^w/)	{$we = 58;}

	if($ken =~ /Bas1/)			{return $we;}
	if($ken =~ /IFL7/)			{return $we;}
	if($ken =~ /AFL/)			{return $we;}
	if($ken =~ /BFL/)			{return $we;}
	if($ken =~ /BN/)			{return $we;}
	if($ken =~ /BS/)			{return $we;}
	if($ken =~ /air/)			{return 60;}
	if($ken =~ /[A-Z]([a-z]+)FL\d+/)	{$ken = $1;}

	if($ken eq 'wide')			{return 69;}

	return &area47dti($remo,$ken)	;
}
sub area47nttpc
{
	my ($remo,$ken) = @_;

	if($ken =~ /[a-z]-([a-z]+)/)	{$ken = $1;}

	return &area47dti($remo,$ken)	;
}
sub area47ocn
{
	my ($remo,$ken) = @_	;

	$ken =~ s/\.ovcs//	;
	if($ken =~ /-/)	{return 69;}

	return &area47dti($remo,$ken)	;
}
sub area47catv
{
	my ($remo) = @_;

	if($remo =~ /\.seikyou\.ne\.jp$/)			{return 68;}
	if($remo =~ /\.wakwak\.ne\.jp$/)			{return 68;}
	if($remo =~ /\.eaccess\.ne\.jp$/)			{return 68;}
	if($remo =~ /\.highway\.ne\.jp$/)			{return 68;}
	if($remo =~ /\.bit-drive\.ne\.jp$/)			{return 68;}
	if($remo =~ /\.pwd\.ne\.jp$/)				{return 68;}
	if($remo =~ /\.([a-z\d]+)\.step\.ne\.jp$/)
	{
		my $ken = $1			;
		if($ken =~ /c5([a-z]+)/)	{$ken = $1;}
		return &area47mesh($remo,$ken)	;
	}
	if($remo =~ /\.bbiq\.jp$/)	#bbiq.jp ��B�n��
	{
		if($remo =~ /hakata03/)	{return 41;}
		return 40;
	}

if($remo =~ /\.ccnw\.ne\.jp$/)		{return 23;}	#.*.ccnw.ne.jp$ �����P�[�u���l�b�g���[�N�i���m�E�򕌁j
if($remo =~ /\.katch\.ne\.jp$/)		{return 23;}	#.*.katch.ne.jp$ KATCH-NET�i���m�j
if($remo =~ /\.enat\.org$/)		{return 21;}	#.*.enat.org$ City.Ena'T.Org�i�򕌌��b�ߎs�j
if($remo =~ /\.thn\.ne\.jp$/)		{return 22;}	#.*.thn.ne.jp$ THN CATV�C���^�[�l�b�g�T�[�r�X�i�É��j
if($remo =~ /\.kitanet\.ne\.jp$/)	{return 13;}	#.*.kitanet.ne.jp$ �k�l�b�g�C���^�[�l�b�g�T�[�r�X�i�����s�k��j
if($remo =~ /\.hot-cha\.tv$/)		{return 35;}	#.*.hot-cha.tv$ �ق�����e���r�i�R��������s�j
if($remo =~ /\.across\.or\.jp$/)	{return 22;}	#.*.across.or.jp$ �h���[���E�F�[�u�É��i�É��j
if($remo =~ /\.cty-net\.ne\.jp$/)	{return 24;}	#.*.cty-net.ne.jp$ �V�[�E�e�B�[�E���C �C���^�[�l�b�g�ڑ��T�[�r�X�i�O�d�j
if($remo =~ /\.miyazaki-catv\.ne\.jp$/)	{return 45;}	#.*.miyazaki-catv.ne.jp$ MCN �{��P�[�u���e���r�i�{��j
if($remo =~ /\.tac-net\.ne\.jp$/)	{return 23;}	#.*.tac-net.ne.jp$ �m�������P�[�u���l�b�g���[�N�i���m�j
if($remo =~ /\.orihime\.ne\.jp$/)	{return 23;}	#.*.orihime.ne.jp$ ����Ђ߂˂��Ɓi���m����{�s�j
if($remo =~ /\.starcat\.ne\.jp$/)	{return 23;}	#.*.starcat.ne.jp$ Starcat�C���^�[�l�b�g�i���m�����É��s�j
if($remo =~ /\.nmt\.ne\.jp$/)		{return 36;}	#.*.nmt.ne.jp$ NMT�l�b�g�i�����j
if($remo =~ /\.tcn-catv\.ne\.jp$/)	{return 13;}	#.*.tcn-catv.ne.jp$ �����P�[�u���l�b�g���[�N�i�����j
if($remo =~ /\.kcv\.ne\.jp$/)		{return 33;}	#.*.kcv.ne.jp$ ��߃l�b�g���[�N�i���R�j
if($remo =~ /\.csf\.ne\.jp$/)		{return 40;}	#.*.csf.ne.jp$ �P�[�u���X�e�[�V���������i�����j
if($remo =~ /\.cts-net\.ne\.jp$/)	{return 44;}	#.*.cts-net.ne.jp$ CTS�C���^�[�l�b�g�T�[�r�X�i�啪�j
if($remo =~ /\.scn-net\.ne\.jp$/)	{return 14;}	#.*.scn-net.ne.jp$ �Ó�P�[�u���l�b�g���[�N�i�_�ސ�j
if($remo =~ /\.amigo\d?\.ne\.jp$/)	{return 24;}	#.*.amigo2.ne.jp$ �A�~�[�S�C���^�[�l�b�g�T�[�r�X�i�O�d�j
if($remo =~ /\.catvy\.ne\.jp$/)		{return 6;}	#.*.catvy.ne.jp$ �P�[�u���e���r�R�`�i�R�`�j
if($remo =~ /\.ztv\.ne\.jp$/)		{return 24;}	#.*.ztv.ne.jp$ Z-LAN�i�O�d�j
if($remo =~ /\.actv\.ne\.jp$/)		{return 2;}	#.*.actv.ne.jp$ �X�P�[�u���e���r�i�X�j
if($remo =~ /\.hicat\.ne\.jp$/)		{return 34;}	#.*.hicat.ne.jp$ �L���V�e�B�P�[�u���e���r HICAT�i�L���j
if($remo =~ /\.kcn\.ne\.jp$/)		{return 53;}	#.*.kcn.ne.jp$ KCN-Net Service�i�ߋE�j
if($remo =~ /\.itscom\.jp$/)		{return 13;}	#.*.itscom.jp$ �C�b�c�E�R�~���j�P�[�V�����Y������Ёi�����E�_�ސ�j
if($remo =~ /\.246\.ne\.jp$/)		{return 13;}	#.*.246.ne.jp$ �C�b�c�E�R�~���j�P�[�V�����Y������Ёi�����E�_�ސ�j
if($remo =~ /\.aikis\.or\.jp$/)		{return 30;}	#.*.aikis.or.jp$ ���������I�B�l�b�g�i�a�̎R�j
if($remo =~ /\.coara\.or\.jp$/)		{return 40;}	#.*.coara.or.jp$ �j���[COARA�i�啪�E�����j
if($remo =~ /\.kumin\.ne\.jp$/)		{return 40;}	#.*.kumin.ne.jp$ ���[�݂�u���[�h�o���h�i�����j
if($remo =~ /\.gujo-tv\.ne\.jp$/)	{return 21;}	#.*.gujo-tv.ne.jp$ �S��L��A���i�򕌁j
if($remo =~ /\.hcvnet.jp$/)		{return 31;}	#.*.hcvnet.jp$ ������Ё@�R���s���[�^�E�T�[�r�X�i����j
if($remo =~ /\.spacelan\.ne\.jp$/)	{return 17;}	#.*.spacelan.ne.jp$ ����P�[�u���e���r�l�b�g�i�ΐ�j
if($remo =~ /\.ayu\.ne\.jp$/)		{return 14;}	#.*.ayu.ne.jp$ ���؈ɐ����P�[�u���l�b�g���[�N�i�_�ސ�j
if($remo =~ /\.cna\.ne\.jp$/)		{return 5;}	#.*.cna.ne.jp$ �H�c�P�[�u���e���r�i�H�c�j
if($remo =~ /\.catvnet\.ne\.jp$/)	{return 54;}	#.*.catvnet.ne.jp$ CATV�l�b�g���[�N�T�[�r�X�i�l���j
if($remo =~ /\.m-net\.ne\.jp$/)		{return 13;}	#.*.m-net.ne.jp$ My TV�i�����j
if($remo =~ /\.ncv\.ne\.jp$/)		{return 1;}	#.*.ncv.ne.jp$ NCV�i�k�C�����َs�j
if($remo =~ /\.adachi\.ne\.jp$/)	{return 13;}	#.*.adachi.ne.jp$ �P�[�u���e���r�����i�����j
if($remo =~ /\.wac2\.net$/)		{return 28;}	#.*.wac2.net$ �킭�킭�l�b�g���[�N�i���Ɂj
if($remo =~ /\.net3-tv\.net$/)		{return 16;}	#.*.net3-tv.net$ Net3 Internet�i�x�R�j
if($remo =~ /\.lcv\.ne\.jp$/)		{return 20;}	#.*.lcv.ne.jp$ LCV-Net�i����j
if($remo =~ /\.tontonme\.ne\.jp$/)	{return 47;}	#.*.tontonme.ne.jp$ �Ƃ�Ƃ�݁`�i����j
if($remo =~ /\.denkosekka\.ne\.jp$/)	{return 51;}	#.*.denkosekka.ne.jp$ �d���Ή΁i�����d�d�j
if($remo =~ /\.mecha\.ne\.jp$/)		{return 24;}	#.*.mecha.ne.jp$ MeCha�i�P�[�u���l�b�g�鎭�j
if($remo =~ /\.oninet\.ne\.jp$/)	{return 33;}	#.*.oninet.ne.jp$ oni�l�b�g�i���R�j
if($remo =~ /\.rmc\.ne\.jp$/)		{return 25;}	#.*.rmc.ne.jp$ Rmc�l�b�g���[�N�i����j
if($remo =~ /\.mco\.ne\.jp$/)		{return 47;}	#.*.mco.ne.jp$ �����Ղ�l�b�g�i����j
if($remo =~ /\.aitai\.ne\.jp$/)		{return 23;}	#.*.aitai.ne.jp$ Aitai net�i���m�E�򕌁j
if($remo =~ /\.ocv\.ne\.jp$/)		{return 51;}	#.*.ocv.ne.jp$ ���c�}�P�[�u���e���r�W����

if($remo =~ /\.nns\.ne\.jp$/)		{return 19;}	#*.nns.ne.jp$ ���{�l�b�g���[�N�T�[�r�X�i�R���j
if($remo =~ /\.cablenet\.ne\.jp$/)	{return 11;}	#.*.cablenet.ne.jp$ �P�[�u���l�b�g���
if($remo =~ /\.milare-tv\.ne\.jp$/)	{return 16;}	#.*.milare-tv.ne.jp$ �݂�[��TV�i�x�R�j
if($remo =~ /\.mni\.ne\.jp$/)		{return 4;}	#.*.mni.ne.jp$ �P�[�u���e���r �L���x�c(�{��)
if($remo =~ /\.gallery\.ne\.jp$/)	{return 39;}	#.*.gallery.ne.jp$ �C���^�[�l�b�gGallery�i���m�j
if($remo =~ /\.cans\.ne\.jp$/)		{return 26;}	#.*.cans.ne.jp$ �P�[�u���l�b�g���[�N���ׁ̂i���s�j
if($remo =~ /\.ict\.ne\.jp$/)		{return 24;}	#.*.ict.ne.jp$ �ɉ���P�[�u���e���r�i�O�d�j
if($remo =~ /\.ctk\.ne\.jp$/)		{return 21;}	#.*.ctk.ne.jp$ �P�[�u���e���r���i�򕌁j
if($remo =~ /\.ucatv\.ne\.jp$/)		{return 9;}	#.*.ucatv.ne.jp$ �F�s�{�P�[�u���e���r�i�Ȗ؁j
if($remo =~ /\.cncm\.ne\.jp$/)		{return 42;}	#.*.cncm.ne.jp$ ����P�[�u�����f�B�A�i����j
if($remo =~ /\.itakita\.net$/)		{return 5;}	#.*.itakita.net$ �H�c��IT��Ջ���
if($remo =~ /\.ogaki-tv\.ne\.jp$/)	{return 21;}	#.*.ogaki-tv.ne.jp$ ��_�P�[�u���e���r�i�򕌁j
if($remo =~ /\.t-net\.ne\.jp$/)		{return 13;}	#.*.t-net.ne.jp$ �����P�[�u���l�b�g���[�N�i�����j
if($remo =~ /\.fureai-ch\.ne\.jp$/)	{return 34;}	#.*.fureai-ch.ne.jp$ �ӂꂠ���`�����l���i�L���j
if($remo =~ /\.synapse\.ne\.jp$/)	{return 46;}	#.*.synapse.ne.jp$ �V�i�v�X�i�������j
if($remo =~ /\.dokidoki\.ne\.jp$/)	{return 38;}	#.*.dokidoki.ne.jp$ �}�W�J���T�C�g�E�C���^�[�l�b�g�T�[�r�X�i���Q�j
if($remo =~ /\.shizuokanet\.ne\.jp$/)	{return 22;}	#.*.shizuokanet.ne.jp$ �É��C���^�[�l�b�g�i�É��j
if($remo =~ /\.kyoto-inet\.or\.jp$/)	{return 26;}	#.*.kyoto-inet.or.jp$ ���s�A�C�l�b�gBB�i���s�j
if($remo =~ /\.wainet\.ne\.jp$/)	{return 45;}	#.*.wainet.ne.jp$ �킢Wai�l�b�g�i�{��j
if($remo =~ /\.kcn-tv\.ne\.jp$/)	{return 43;}	#.*.kcn-tv.ne.jp$ �F�{�P�[�u���l�b�g���[�N�i�F�{�j
if($remo =~ /\.d-b\.ne\.jp$/)		{return 44;}	#.*.d-b.ne.jp$ �啪�����V���C���^�[�l�b�g�i�啪�j
if($remo =~ /\.parkcity\.ne\.jp$/)	{return 13;}	#.*.parkcity.ne.jp$ ������O��P�[�u���e���r�i�����j
if($remo =~ /\.nirai\.ne\.jp$/)		{return 47;}	#.*.nirai.ne.jp$ ����P�[�u���l�b�g���[�N�i����j
if($remo =~ /\.cosmos\.ne\.jp$/)	{return 47;}	#.*.cosmos.ne.jp$ COSMOS NET COMMUNICATIONS�i����j
if($remo =~ /\.kct\.ne\.jp$/)		{return 33;}	#.*.kct.ne.jp$ �q�~�P�[�u���e���r�i���R�j
if($remo =~ /\.me-h\.ne\.jp$/)		{return 1;}	#.*.me-h.ne.jp$ ME�k�C���l�b�g���[�N�T�[�r�X�i�k�C���j
if($remo =~ /\.asagaotv\.ne\.jp$/)	{return 17;}	#.*.asagaotv.ne.jp$ ���������e���r�i�ΐ�j
if($remo =~ /\.medias\.ne\.jp$/)	{return 23;}	#.*.medias.ne.jp$ �m�����f�B�A�X�l�b�g���[�N
if($remo =~ /\.octv\.ne\.jp$/)		{return 1;}	#.*.octv.ne.jp$ �эL�V�e�B�[�P�[�u���i�k�C���j
if($remo =~ /\.wbs\.ne\.jp$/)		{return 22;}	#.*.wbs.ne.jp$ Web�É�
if($remo =~ /\.commufa\.jp$/)		{return 52;}	#.*.commufa.jp$ �R�~���t�@�i�����d�́j
if($remo =~ /\.sni\.ne\.jp$/)		{return 41;}	#.*.sni.ne.jp$ ����V���E����V���C���^�[�l�b�g�i����E����j
if($remo =~ /\.netwave\.or\.jp$/)	{return 54;}	#.*.netwave.or.jp$ Netwave�C���^�[�l�b�g�T�[�r�X�i�l���j
if($remo =~ /\.mopera\.ne\.jp$/)	{return 60;}	#.*.mopera.ne.jp$ ���y���iFOMA�̐ڑ��T�[�r�X�H�j
if($remo =~ /\.koalanet\.ne\.jp$/)	{return 12;}	#.*.koalanet.ne.jp$ �R�A���e���r�i��t�j
if($remo =~ /\.clovernet\.ne\.jp$/)	{return 23;}	#.*.clovernet.ne.jp$ �N���[�o�[�l�b�g�i���m�j
if($remo =~ /\.hottv\.ne\.jp$/)		{return 25;}	#.*.hottv.ne.jp$ �ߍ]�����P�[�u���l�b�g���[�N������Ёi���ꌧ�ߍ]�����s�j
if($remo =~ /\.tvk\.ne\.jp$/)		{return 17;}	#.*.tvk.ne.jp$ �e���r�����i�ΐ�j
if($remo =~ /\.tcn\.ne\.jp$/)		{return 36;}	#.*.tcn.ne.jp$ �����P�[�u���l�b�g���[�N�i�����j
if($remo =~ /\.ccv\.ne\.jp$/)		{return 34;}	#.*.ccv.ne.jp$ �ӂꂠ���`�����l���i�L���j
if($remo =~ /\.cnc\.jp$/)		{return 12;}	#.*.cnc.jp$ ������ЃP�[�u���l�b�g���[�N��t
if($remo =~ /\.e-catv\.ne\.jp$/)	{return 38;}	#.*.e-catv.ne.jp$ ���QCATV�i���Q�j
if($remo =~ /\.wind\.ne\.jp$/)		{return 10;}	#.*.wind.ne.jp$ �Q�n�C���^�[�l�b�g�i�Q�n�j
if($remo =~ /\.hit-5\.net$/)		{return 32;}	#.*.hit-5.net$ �_�B�킪�Ƃ��e���r�i�����j
if($remo =~ /\.yukiguni\.net$/)		{return 15;}	#.*.yukiguni.net$ �䂫���Ƀl�b�g�i�V���j
if($remo =~ /\.kct\.ad\.jp$/)		{return 33;}	#.*.kct.ad.jp$ ������Бq�~�P�[�u���e���r�i���R�j
if($remo =~ /\.ictnet\.ne\.jp$/)	{return 3;}	#.*.ictnet.ne.jp$ ���P�[�u���e���r�W�����i���j
if($remo =~ /\.chikamatsu\.ne\.jp$/)	{return 13;}	#.*.chikamatsu.ne.jp$ PS/PLAZA �n�����i�����s���c��j
if($remo =~ /\.miracle\.ne\.jp$/)	{return 55;}	#.*.miracle.ne.jp$ San-inNet�i�R�A�n���j
if($remo =~ /\.avis\.ne\.jp$/)		{return 71;}	#.*.avis.ne.jp$ �A���B�X�i����j
if($remo =~ /\.fcv\.ne\.jp$/)		{return 30;}	#.*.fcv.ne.jp$ �����P�[�u���r�W����
if($remo =~ /\.inacatv\.ne\.jp$/)	{return 20;}	#.*.inacatv.ne.jp$ �ɓ߃P�[�u���e���r�W����
if($remo =~ /\.incl\.ne\.jp$/)		{return 70;}	#.*.incl.ne.jp$ �C���N���i�k���n���j
if($remo =~ /\.c-able\.ne\.jp$/)	{return 35;}	#.*.c-able.ne.jp$ �R���P�[�u���r�W�����i�R���j
if($remo =~ /\.tees\.ne\.jp$/)		{return 23;}	#.*.tees.ne.jp$ �L���P�[�u���l�b�g���[�N�i���m���L���s�E�c���s�j

if($remo =~ /\.cty8\.com$/)		{return 16;}	#.*.cty8.com$ �P�[�u���e���r�����i�x�R�j
if($remo =~ /\.bc9\.ne\.jp$/)		{return 9;}	#.*.bc9.ne.jp$ �����P�[�u���e���r�i�Ȗ؎����s�j
if($remo =~ /\.cc9\.ne\.jp$/)		{return 9;}	#.*.cc9.ne.jp$ �Ȗ؃P�[�u���e���r�i�Ȗ؁E�Q�n�j
if($remo =~ /\.cnh\.ne\.jp$/)		{return 16;}	#.*.cnh.ne.jp$ �X���E�H��P�[�u���l�b�g�i�x�R���X���s�E�H��s�j
if($remo =~ /\.catvmics\.ne\.jp$/)	{return 23;}	#.*.catvmics.ne.jp$ �~�N�X�l�b�g���[�N�i���m������s�j
if($remo =~ /\.cts\.ne\.jp$/)		{return 13;}	#.*.cts.ne.jp$ �P�[�u���e���r�i��i�����s�i���j
if($remo =~ /\.tcat\.ne\.jp$/)		{return 11;}	#.*.tcat.ne.jp$ �e�v�R�P�[�u���e���r�i��ʁj
if($remo =~ /\.tcnet\.ne\.jp$/)		{return 16;}	#.*.tcnet.ne.jp$ �����P�[�u���l�b�g���[�N�i�x�R�������s�E�������j
if($remo =~ /\.winknet\.ne\.jp$/)	{return 28;}	#.*.winknet.ne.jp$ �P�H�P�[�u���e���r�i���Ɍ��P�H�s�j
if($remo =~ /\.usennet\.ne\.jp$/)	{return 25;}	#.*.usennet.ne.jp$ ��R�L�������i���ꌧ��R�s�j
if($remo =~ /\.ictv\.ne\.jp$/)		{return 11;}	#.*.ictv.ne.jp$ ���ԃP�[�u���e���r�i��ʌ����Ԏs�j
if($remo =~ /\.otv\.ne\.jp$/)		{return 10;}	#.*.otv.ne.jp$ �Q�n�P�[�u�����f�B�A�i�Q�n�����c�s�E�ː��s�j
if($remo =~ /\.sdx\.ne\.jp$/)		{return 11;}	#.*.sdx.ne.jp$ ��ʃf�[�^�G�N�X�`�F���W�T�[�r�X�i��ʁj
if($remo =~ /\.tcv\.jp$/)		{return 13;}	#.*.tcv.jp$ �����P�[�u���r�W����
if($remo =~ /\.h555\.net$/)		{return 28;}	#.*.h555.net$ h555.net�i���Ɍ��j
if($remo =~ /\.lan-do\.ne\.jp$/)	{return 1;}	#.*.lan-do.ne.jp$ ����P�[�u���e���r �|�e�g�i�k�C������s�j
if($remo =~ /\.bbbn\.jp$/)		{return 34;}	#.*.bbbn.jp$ BBBN�i�L�����j
if($remo =~ /\.ctb\.ne\.jp$/)		{return 44;}	#.*.ctb.ne.jp$ CTB���f�B�A�i�啪�j
if($remo =~ /\.intsurf\.ne\.jp$/)	{return 24;}	#.*.intsurf.ne.jp$ �C���g�T�[�t�i�O�d���K���s�E�������j
if($remo =~ /\.cvk\.ne\.jp$/)		{return 19;}	#.*.cvk.ne.jp$ �����b�`�s�u�i�R������A���v�X�s�j
if($remo =~ /\.omn\.ne\.jp$/)		{return 6;}	#.*.omn.ne.jp$ �j�R�j�R�P�[�u���e���r�W�����i�R�`�j
if($remo =~ /\.kcv-net\.ne\.jp$/)	{return 11;}	#.*.kcv-net.ne.jp$ ��z�P�[�u���e���r�i��ʌ���z�s�j
if($remo =~ /\.accsnet\.ne\.jp$/)	{return 8;}	#.*.accsnet.ne.jp$ ACCSnet�i��錧���Ύs�j
if($remo =~ /\.tst\.ne\.jp$/)		{return 16;}	#.*.tst.ne.jp$ �ƂȂ݉q���ʐM�e���r�i�x�R������s�E��v�s�E�v�g�s�j
if($remo =~ /\.ctt\.ne\.jp$/)		{return 16;}	#.*.ctt.ne.jp$ �P�[�u���e���r�x�R�i�x�R���x�R�s�E�M�����j
if($remo =~ /\.fctv\.ne\.jp$/)		{return 18;}	#.*.fctv.ne.jp$ ����P�[�u���e���r�i����j
if($remo =~ /\.izu\.co\.jp$/)		{return 22;}	#.*.izu.co.jp$ �ɓ��}�P�[�u���l�b�g���[�N�i�É��������j
if($remo =~ /\.icnet\.ne\.jp$/)		{return 12;}	#.*.icnet.ne.jp$ ��������P�[�u���l�b�g���[�N�i��t���s��s�j
if($remo =~ /\.kyoto-inetbb\.jp$/)	{return 26;}	#.*.kyoto-inetbb.jp$ ���s�A�C�l�b�gBB�i���s�j
if($remo =~ /\.cc22\.ne\.jp$/)		{return 34;}	#.*.cc22.ne.jp$ �ӂꂠ���`�����l���i�L���s�j
if($remo =~ /\.catv296\.ne\.jp$/)	{return 12;}	#.*.catv296.ne.jp$ �P�[�u���l�b�g296�i��t�j
if($remo =~ /\.ueda\.ne\.jp$/)		{return 20;}	#.*.ueda.ne.jp$ ��c�P�[�u���r�W�����i����j
if($remo =~ /\.toshima\.ne\.jp$/)	{return 13;}	#.*.toshima.ne.jp$ �L���P�[�u���l�b�g���[�N�i�����s�L����j
if($remo =~ /\.ii-okinawa\.ne\.jp$/)	{return 47;}	#.*.ii-okinawa.ne.jp$ ii-okinawa�i����j
if($remo =~ /\.biwa\.ne\.jp$/)		{return 25;}	#.*.biwa.ne.jp$ BIWALOBE�i����j
if($remo =~ /\.tvkumagaya\.ne\.jp$/)	{return 11;}	#.*.tvkumagaya.ne.jp$ �F�J�P�[�u���e���r�i��ʌ��F�J�s�j
if($remo =~ /\.mable\.ne\.jp$/)		{return 32;}	#.*.mable.ne.jp$ �R�A�P�[�u���r�W�����i���������]�s�j
if($remo =~ /\.tamatele\.ne\.jp$/)	{return 33;}	#.*.tamatele.ne.jp$ �ʓ��e���r�i���R���q�~�s�j
if($remo =~ /\.ccnet-ai\.ne\.jp$/)	{return 23;}	#.*.ccnet-ai.ne.jp$ CCNet�L��ǁi���m���L��s�j
if($remo =~ /\.infoaomori\.ne\.jp$/)	{return 2;}	#.*.infoaomori.ne.jp$ 7-dj.com�i�X�j
if($remo =~ /\.7-dj\.ne\.jp$/)		{return 2;}	#.*.infoaomori.ne.jp$ 7-dj.com�i�X�j

if($remo =~ /\.btvm\.ne\.jp$/)		{return 46;}	#.*.btvm.ne.jp$ BTV�P�[�u���e���r�W�����i�������j
if($remo =~ /\.kbn\.ne\.jp$/)		{return 37;}	#.*.kbn.ne.jp$ ����e���r�����ԁi����j
if($remo =~ /\.rcn\.ne\.jp$/)		{return 18;}	#.*.rcn.ne.jp$ menet�i����j
if($remo =~ /\.hearts\.ne\.jp$/)	{return 38;}	#.*.hearts.ne.jp$ HEART NET�i���Q�j
if($remo =~ /\.yct\.ne\.jp$/)		{return 33;}	#.*.yct.ne.jp$ ��|�����i���R�����c�S��|���j
if($remo =~ /\.c3-net\.ne\.jp$/)	{return 14;}	#.*.c3-net.ne.jp$ JCN�`��i�_�ސ쌧���l�s�j
if($remo =~ /\.ginga-net\.ne\.jp$/)	{return 3;}	#.*.ginga-net.ne.jp$ �k��P�[�u���e���r�i��茧�k��s�j
if($remo =~ /\.icn-net\.ne\.jp$/)	{return 3;}	#.*.icn-net.ne.jp$ ��փP�[�u���l�b�g���[�N�i��茧��֎s�j
if($remo =~ /\.canet\.ne\.jp$/)		{return 16;}	#.*.canet.ne.jp$ �ː��P�[�u���e���r�i�x�R���ː��s�E�����s�j
if($remo =~ /\.kamakuranet\.ne\.jp$/)	{return 14;}	#.*.kamakuranet.ne.jp$ ���q�P�[�u���e���r�i�_�ސ쌧���q�s�j
if($remo =~ /\.s-cnet\.ne\.jp$/)	{return 22;}	#.*.s-cnet.ne.jp$ �h���[���E�F�[�u�É��i�É����É��s�j
if($remo =~ /\.c-marinet\.ne\.jp$/)	{return 4;}	#.*.c-marinet.ne.jp$ �����P�[�u���e���r�i�{�錧�����s�E�����s�E���{���E�����l���j
if($remo =~ /\.himawarinet\.ne\.jp$/)	{return 42;}	#.*.himawarinet.ne.jp$ �Ђ܂��Ă�сi����j
if($remo =~ /\.ccsnet\.ne\.jp$/)	{return 35;}	#.*.ccsnet.ne.jp$ �V�e�B�[�P�[�u������i�R��������s�j
if($remo =~ /\.sakura-catv\.ne\.jp$/)	{return 13;}	#.*.sakura-catv.ne.jp$ ������P�[�u���e���r�i�����s�n�c��j
if($remo =~ /\.hinocatv\.ne\.jp$/)	{return 13;}	#.*.hinocatv.ne.jp$ ����P�[�u���e���r�i�����s�j
if($remo =~ /\.watv\.ne\.jp$/)		{return 9;}	#.*.watv.ne.jp$ �킽�点�e���r�i�Ȗ،������s�j
if($remo =~ /\.mctv\.ne\.jp$/)		{return 24;}	#.*.mctv.ne.jp$ MCTV����P�[�u���e���r�i�O�d������s�j
if($remo =~ /\.tmtv\.ne\.jp$/)		{return 14;}	#.*.tmtv.ne.jp$ �P�[�u���l�b�g�Â��̐X�i���l�s�s�}��j
if($remo =~ /\.ttv\.ne\.jp$/)		{return 13;}	#.*.ttv.ne.jp$ �����e���r�i�����s�����q�s�E���c�s�E�����s�E���s�j
if($remo =~ /\.sopia\.or\.jp$/)		{return 8;}	#.*.sopia.or.jp$ �\�s�A�t�H���X������Ёi��錧�����s�j
if($remo =~ /\.nice-tv\.jp$/)		{return 16;}	#.*.nice-tv.jp$ NICE TV�i�x�R�����Îs�j
if($remo =~ /\.iwamicatv\.jp$/)		{return 32;}	#.*.iwamicatv.jp$ �Ό��P�[�u���r�W�����i�������l�c�s�E�]�Îs�j
if($remo =~ /\.cac-net\.ne\.jp$/)	{return 23;}	#.*.cac-net.ne.jp$ CATV���m�i���m�����c�s�j

if($remo =~ /\.inforyoma\.or\.jp$/)	{return 39;}	#inforyoma.or.jp ���m
if($remo =~ /\.joetsu\.ne\.jp$/)	{return 15;}	#joetsu.ne.jp �V��
if($remo =~ /\.cable-net\.ne\.jp$/)	{return 25;}	#cable-net.ne.jp ����
if($remo =~ /\.icc\.ne\.jp$/)		{return 14;}	#icc.ne.jp �_�ސ�
if($remo =~ /\.bai\.ne\.jp$/)		{return 28;}	#bai.ne.jp ����
if($remo =~ /\.people-i\.ne\.jp$/)	{return 41;}	#people-i.ne.jp ����
if($remo =~ /\.fruits\.ne\.jp$/)	{return 19;}	#fruits.ne.jp �R��
if($remo =~ /\.viplt\.ne\.jp$/)		{return 70;}	#viplt.ne.jp �k��
if($remo =~ /\.taku\.ne\.jp$/)		{return 41;}	#taku.ne.jp ����
if($remo =~ /\.htv-net\.ne\.jp$/)	{return 2;}	#htv-netne.jp �X
if($remo =~ /\.gol\.ne\.jp$/)		{return 68;}	#'gol.ne.jp'
if($remo =~ /\.kinet-tv\.ne\.jp$/)	{return 26;}	#'kinet-tv.ne.jp'���s
if($remo =~ /\.cyberbb\.ne\.jp$/)	{return 68;}	#'cyberbb.ne.jp'
if($remo =~ /\.tribe\.ne\.jp$/)		{return 68;}	#'tribe.ne.jp'
if($remo =~ /\.janis\.or\.jp$/)		{return 20;}	#janis.or.jp�i����j
if($remo =~ /\.valley\.ne\.jp$/)	{return 20;}	#valley.ne.jp�i����j
if($remo =~ /\.tnc\.ne\.jp$/)		{return 22;}	#tnc.ne.jp�@�É�
if($remo =~ /\.tokai\.or\.jp$/)		{return 22;}	#tokai.or.jp�@�É�
if($remo =~ /\.chukai\.ne\.jp$/)	{return 31;}	#chukai.ne.jp�@����
if($remo =~ /\.nasicnet\.ne\.jp$/)	{return 27;}	#nasicnet.ne.jp�@���
if($remo =~ /\.namikata\.ne\.jp$/)	{return 38;}	#namikata.ne.jp�@���Q
if($remo =~ /\.bunbun\.ne\.jp$/)	{return 41;}	#bunbun.ne.jp ����
if($remo =~ /\.harenet\.ne\.jp$/)	{return 33;}	#harenet.ne.jp ���R
if($remo =~ /\.yomogi\.or\.jp$/)	{return 9;}	#yomogi.or.jp �Ȗ�
if($remo =~ /\.ttn\.ne\.jp$/)		{return 18;}	#ttn.ne.jp ����
if($remo =~ /\.rosenet\.ne\.jp$/)	{return 13;}	#rosenet.ne.jp ����
if($remo =~ /\.ctktv\.ne\.jp$/)		{return 14;}	#ctktv.ne.jp �_�ސ�
if($remo =~ /\.gctv\.ne\.jp$/)		{return 23;}	#gctv.ne.jp ���É�
if($remo =~ /\.kamon\.ne\.jp$/)		{return 34;}	#kamon.ne.jp �L��
if($remo =~ /\.canvas\.ne\.jp$/)	{return 68;}	#canvas.ne.jp ����
if($remo =~ /\.i-chubu\.ne\.jp$/)	{return 52;}	#i-chubu.ne.jp ����
if($remo =~ /\.oct-net\.ne\.jp$/)	{return 44;}	#oct-net.ne.jp �啪
if($remo =~ /\.megax\.ne\.jp$/)		{return 56;}	#megax.ne.jp ��B
if($remo =~ /\.icntv\.ne\.jp$/)		{return 12;}	#icntv.ne.jp ��t
if($remo =~ /\.cyberhome\.ne\.jp$/)	{return 68;}	#cyberhome.ne.jp ����
if($remo =~ /\.pcsitebrowser\.ne\.jp$/)	{return 60;}	#pcsitebrowser.ne.jp ��
if($remo =~ /\.nava21\.ne\.jp$/)	{return 24;}	#nava21.ne.jp �O�d
if($remo =~ /\.catv-mic\.ne\.jp$/)	{return 3;}	#catv-mic.ne.jp ���
if($remo =~ /\.edit\.ne\.jp$/)		{return 13;}	#edit.ne.jp ����
if($remo =~ /\.mto\.ne\.jp$/)		{return 33;}	#mto.ne.jp ���R
if($remo =~ /\.seaple\.ne\.jp$/)	{return 12;}	#seaple.ne.jp ��t
if($remo =~ /\.firstserver\.ne\.jp$/)	{return 27;}	#firstserver.ne.jp ���

if($remo =~ /\.anc-tv\.ne\.jp$/)	{return 20;}	#.anc-tv.ne.jp ���쌧�@20
if($remo =~ /\.attmil\.ne\.jp$/)	{return 68;}	#.attmil.ne.jp 
if($remo =~ /\.attnet\.ne\.jp$/)	{return 68;}	#.attnet.ne.jp 
if($remo =~ /\.bias\.ne\.jp$/)		{return 68;}	#.bias.ne.jp �z�X�e�B���O�T�[�r�X�H
if($remo =~ /\.bb-west\.ne\.jp$/)	{return 57;}	#.bb-west.ne.jp �֐� ���� ��B
if($remo =~ /\.cableone\.ne\.jp$/)	{return 68;}	#.cableone.ne.jp ���ꌧ 41
if($remo =~ /\.dsnw\.ne\.jp$/)		{return 41;}	#.dsnw.ne.jp �S����@�s���{���ʉ\���H
if($remo =~ /\.eagle-net\.ne\.jp$/)	{return 17;}	#.eagle-net.ne.jp �ΐ쌧�@17
if($remo =~ /\.eastcom\.ne\.jp$/)	{return 12;}	#.eastcom.ne.jp ��t���@12
if($remo =~ /\.icn-tv\.ne\.jp$/)	{return 35;}	#.icn-tv.ne.jp �R���� 35
if($remo =~ /\.em-net\.ne\.jp$/)	{return 68;}	#.em-net.ne.jp �S����
if($remo =~ /\.hachigamenet\.ne\.jp$/)	{return 41;}	#.hachigamenet.ne.jp ���ꌧ
if($remo =~ /\.hagakure\.ne\.jp$/)	{return 41;}	#.hagakure.ne.jp ���ꌧ
if($remo =~ /\.hal\.ne\.jp$/)		{return 68;}	#.hal.ne.jp �S����
if($remo =~ /\.i-younet\.ne\.jp$/)	{return 22;}	#.i-younet.ne.jp �É���
if($remo =~ /\.ip-link\.ne\.jp$/)	{return 51;}	#.ip-link.ne.jp �֓��n��
if($remo =~ /\.iprevolution\.ne\.jp$/)	{return 68;}	#.iprevolution.ne.jp �S����
if($remo =~ /\.ium\.ne\.jp$/)		{return 13;}	#.ium.ne.jp �����ۂ�(����)
if($remo =~ /\.ktv\.ne\.jp$/)		{return 10;}	#.ktv.ne.jp �Q�n��
if($remo =~ /\.matsumoto\.ne\.jp$/)	{return 20;}	#.matsumoto.ne.jp ���쌧
if($remo =~ /\.nsk\.ne\.jp$/)		{return 71;}	#.nsk.ne.jp �x�R�A����A�ΐ�
if($remo =~ /\.pikara\.ne\.jp$/)	{return 14;}	#.pikara.ne.jp �l��
if($remo =~ /\.raidway\.ne\.jp$/)	{return 68;}	#.raidway.ne.jp �_�ސ�
if($remo =~ /\.rnac\.ne\.jp$/)		{return 5;}	#.rnac.ne.jp �H�c�E���
if($remo =~ /\.rurbannet\.ne\.jp$/)	{return 12;}	#.rurbannet.ne.jp ��t
if($remo =~ /\.sensyu\.ne\.jp$/)	{return 27;}	#.sensyu.ne.jp ���
if($remo =~ /\.speednet\.ne\.jp$/)	{return 68;}	#.speednet.ne.jp ����
if($remo =~ /\.tctv\.ne\.jp$/)		{return 13;}	#.tctv.ne.jp ����
if($remo =~ /\.ttmy\.ne\.jp$/)		{return 14;}	#.ttmy.ne.jp �_�ސ�
if($remo =~ /\.tvm\.ne\.jp$/)		{return 20;}	#.tvm.ne.jp ����
if($remo =~ /\.urban\.ne\.jp$/)		{return 68;}	#.urban.ne.jp 
if($remo =~ /\.goennet\.ne\.jp$/)	{return 32;}	#.goennet.ne.jp ����
if($remo =~ /\.ictweb\.ne\.jp$/)	{return 47;}	#.ictweb.ne.jp ����

if($remo =~ /\.tns\.ne\.jp$/)		{return 68;}	#.tns.ne.jp �g���^�����Ԋ֘A�@�S����
if($remo =~ /\.warabi\.ne\.jp$/)	{return 11;}	#.warabi.ne.jp ���
if($remo =~ /\.stnet\.ne\.jp$/)		{return 68;}	#.stnet.ne.jp �S���@(�t���b�c)
if($remo =~ /\.bmobile\.ne\.jp$/)	{return 60;}	#.bmobile.ne.jp �S���@(PHS)
if($remo =~ /\.meon\.ne\.jp$/)		{return 55;}	#.meon.ne.jp �R�� ���R���E���挧
if($remo =~ /\.hinanet\.ne\.jp$/)	{return 6;}	#.hinanet.ne.jp �R�`
if($remo =~ /\.nima-cho\.ne\.jp$/)	{return 32;}	#.nima-cho.ne.jp ����
if($remo =~ /\.nus\.ne\.jp$/)		{return 19;}	#.nus.ne.jp �R��
if($remo =~ /\.tv-naruto\.ne\.jp$/)	{return 36;}	#.tv-naruto.ne.jp ����
if($remo =~ /\.access-internet\.ne\.jp$/)	{return 60;}	#.access-internet.ne.jp �\�t�g�o���N���o�C���̃T�[�r�X
if($remo =~ /\.cat-v\.ne\.jp$/)		{return 4;}	#.cat-v.ne.jp �{��
if($remo =~ /\.mct\.ne\.jp$/)		{return 46;}	#.mct.ne.jp ������
if($remo =~ /\.iam\.ne\.jp$/)		{return 68;}	#.iam.ne.jp 
if($remo =~ /\.arena\.ne\.jp$/)		{return 68;}	#.arena.ne.jp 

if($remo =~ /\.comcast\.net$/)		{return 80;}	#.comcast.net �č�
if($remo =~ /\.cilas\.net$/)		{return 68;}	#.cilas.net �S���}���V����
if($remo =~ /\.fiberbit\.net$/)		{return 68;}	#.fiberbit.net �S��
if($remo =~ /\.hawaiiantel\.net$/)	{return 80;}	#.hawaiiantel.net �A�����J �n���C
if($remo =~ /\.hinet\.net$/)		{return 68;}	#.hinet.net ��p
if($remo =~ /\.imouto\.net$/)		{return 48;}	#.imouto.net �S��
if($remo =~ /\.isao\.net$/)		{return 68;}	#.isao.net �n��ʉ\�H
if($remo =~ /\.mediatti\.net$/)		{return 68;}	#.mediatti.net catv�@�S��
if($remo =~ /\.solteria\.net$/)		{return 68;}	#.solteria.net IP-VPN�T�[�r�X�@�\�t�g�o���N�e���R���n
if($remo =~ /\.zero-isp\.net$/i)	{return 68;}	#.zero-isp.net �S���E�n�����s�\

if($remo =~ /\.ibara\.ne\.jp$/)		{return 33;}	#.ibara.ne.jp ���R
if($remo =~ /\.rak-rak\.ne\.jp$/)	{return 52;}	#.rak-rak.ne.jp �����n��
if($remo =~ /\.cypress\.ne\.jp$/)	{return 30;}	#.cypress.ne.jp �a�̎R
if($remo =~ /\.seiryu\.ne\.jp$/)	{return 21;}	#.seiryu.ne.jp �򕌌�
if($remo =~ /\.wings\.ne\.jp$/)		{return 68;}	#.wings.ne.jp �S��
if($remo =~ /\.jyaken\.ne\.jp$/)	{return 34;}	#.jyaken.ne.jp �L��
if($remo =~ /\.bb4u\.ne\.jp$/)		{return 68;}	#.bb4u.ne.jp �S���@�}���V����
if($remo =~ /\.n-cube\.ne\.jp$/)	{return 68;}	#.n-cube.ne.jp �S��
if($remo =~ /\.ont\.ne\.jp$/)		{return 5;}	#.ont.ne.jp �H�c��
if($remo =~ /\.awaikeda\.ne\.jp$/)	{return 36;}	#.awaikeda.net ����
if($remo =~ /\.ccjnet\.ne\.jp$/)	{return 34;}	#.ccjnet.ne.jp �L��
if($remo =~ /\.hotspot\.ne\.jp$/)	{return 60;}	#.hotspot.ne.jp �z�b�g�X�|�b�g
if($remo =~ /\.brew\.ne\.jp$/)		{return 60;}	#.brew.ne.jp ezweb�̃t���u���E�U

if($remo =~ /\.openmobile\.ne\.jp$/)	{return 68;}	#.openmobile.ne.jp(�S��)�\�t�g�o���N���o�C���H
if($remo =~ /\.jet\.ne\.jp$/)		{return 58;}	#.jet.ne.jp(�����{)
if($remo =~ /\.icv\.ne\.jp$/)		{return 32;}	#.icv.ne.jp(����)
if($remo =~ /\.kagacable\.ne\.jp$/)	{return 17;}	#.kagacable.ne.jp(�ΐ�)
if($remo =~ /\.icv-net\.ne\.jp$/)	{return 42;}	#.icv-net.ne.jp(����)
if($remo =~ /\.izumo\.ne\.jp$/)		{return 32;}	#.izumo.ne.jp(����)
if($remo =~ /\.ch-you\.ne\.jp$/)	{return 20;}	#.ch-you.ne.jp(����)
if($remo =~ /\.hotcn\.ne\.jp$/)		{return 1;}	#.hotcn.ne.jp(�k�C��)
if($remo =~ /\.nct\.ne\.jp$/)		{return 7;}	#.nct.ne.jp(����)
if($remo =~ /\.otc\.ne\.jp$/)		{return 47;}	#.otc.ne.jp(����)

if($remo =~ /\.shawcable\.net$/)	{return 81;}	#.shawcable.net(�J�i�_)
if($remo =~ /\.verizon\.net$/)		{return 80;}	#.verizon.net(�A�����J)
if($remo =~ /\.i-products\.net$/)	{return 68;}	#.i-products.net(�S��)ibisBrowser?
if($remo =~ /\.awaikeda\.net$/)		{return 36;}	#.awaikeda.net(����)
if($remo =~ /\.bitcat\.net$/)		{return 51;}	#.bitcat.net(bitcat�͎O��s���Y�}���V���������T�[�r�X�����C�u�h�A�ɋz�������œ����E�_�ސ�E��ʂ��ȂƎv���܂�)
if($remo =~ /\.Level3\.net$/)		{return 80;}	#.Level3.net(�A�����J)
if($remo =~ /\.edu$/)			{return 80;}	#.edu(�A�����J)

if($remo =~ /\.awacco\.ne\.jp$/)	{return 36;}	#.awacco.ne.jp(����)
if($remo =~ /\.ccnetmie\.ne\.jp$/)	{return 24;}	#.ccnetmie.ne.jp(�O�d)
if($remo =~ /\.ciaotv\.ne\.jp$/)	{return 24;}	#.ciaotv.ne.jp(�O�d)
if($remo =~ /\.firnet\.ne\.jp$/)	{return 43;}	#.firnet.ne.jp(�F�{)
if($remo =~ /\.fnj\.ne\.jp$/)		{return 68;}	#.fnj.ne.jp(�S��)
if($remo =~ /\.haginet\.ne\.jp$/)	{return 35;}	#.haginet.ne.jp(�R��)
if($remo =~ /\.i-berry\.ne\.jp$/)	{return 9;}	#.i-berry.ne.jp(�Ȗ�)
if($remo =~ /\.i-yume\.ne\.jp$/)	{return 32;}	#.i-yume.ne.jp(����)
if($remo =~ /\.icknet\.ne\.jp$/)	{return 38;}	#.icknet.ne.jp(���Q)
if($remo =~ /\.infoeddy\.ne\.jp$/)	{return 57;}	#.infoeddy.ne.jp(�����{)

if($remo =~ /\.jctv\.ne\.jp$/)		{return 36;}	#.jctv.ne.jp�@����
if($remo =~ /\.jway\.ne\.jp$/)		{return 8;}	#.jway.ne.jp�@���
if($remo =~ /\.kcb-net\.ne\.jp$/)	{return 39;}	#.kcb-net.ne.jp�@���m
if($remo =~ /\.kctvnet\.ne\.jp$/)	{return 1;}	#.kctvnet.ne.jp�@�k�C��
if($remo =~ /\.kkm\.ne\.jp$/)		{return 32;}	#.kkm.ne.jp�@����
if($remo =~ /\.nkoutokuji\.ne\.jp$/)	{return 46;}	#.koutokuji.ne.jp�@������
if($remo =~ /\.kyt-net\.ne\.jp$/)	{return 26;}	#.kyt-net.ne.jp�@���s
if($remo =~ /\.kvision\.ne\.jp$/)	{return 35;}	#.kvision.ne.jp�@�R��
if($remo =~ /\.maotv\.ne\.jp$/)		{return 22;}	#.maotv.ne.jp�@�É�
if($remo =~ /\.mcbnet\.ne\.jp$/)	{return 37;}	#.mcbnet.ne.jp�@����

if($remo =~ /\.nanmoku\.ne\.jp$/)	{return 10;} #.nanmoku.ne.jp(�Q�n)
if($remo =~ /\.nct9\.ne\.jp$/)		{return 15;} #.nct9.ne.jp(�V��)
if($remo =~ /\.netfour\.ne\.jp$/)	{return 41;} #.netfour.ne.jp(����)
if($remo =~ /\.nkansai\.ne\.jp$/)	{return 57;} #.nkansai.ne.jp(�����{)
if($remo =~ /\.octp-net\.ne\.jp$/)	{return 42;} #.octp-net.ne.jp(����)
if($remo =~ /\.okuizumo\.ne\.jp$/)	{return 32;} #.okuizumo.ne.jp(����)
if($remo =~ /\.pcm\.ne\.jp$/)		{return 25;} #.pcm.ne.jp(����)
if($remo =~ /\.qtnet\.ne\.jp$/)		{return 56;} #.qtnet.ne.jp(��B�n��)
if($remo =~ /\.ryucom\.ne\.jp$/)	{return 47;} #.ryucom.ne.jp(����)
if($remo =~ /\.sakura\.ne\.jp$/)	{return 68;} #.sakura.ne.jp(�����^���T�[�o)

if($remo =~ /\.sanuki\.ne\.jp$/)	{return 37;}	#.sanuki.ne.jp(����)
if($remo =~ /\.scatv\.ne\.jp$/)		{return 39;}	#.scatv.ne.jp(���m)
if($remo =~ /\.shiojiri\.ne\.jp$/)	{return 20;}	#.shiojiri.ne.jp(����)
if($remo =~ /\.snowman\.ne\.jp$/)	{return 1;}	#.snowman.ne.jp(�k�C��)
if($remo =~ /\.sub\.ne\.jp$/)		{return 68;}	#.sub.ne.jp(�S��)dti�@�l����
if($remo =~ /\.tvt\.ne\.jp$/)		{return 33;}	#.tvt.ne.jp(���R)
if($remo =~ /\.webone\.ne\.jp$/)	{return 1;}	#.webone.ne.jp(�k�C��)
if($remo =~ /\.yappo\.ne\.jp$/)		{return 68;}	#.yappo.ne.jp(�S��)�P�[�^�C�Q�[�g�E�F�C�T�[�r�Xbydocomo
if($remo =~ /\.leo-net\.jp$/)		{return 67;}	#.leo-net.jp
if($remo =~ /\.bb-niigata\.jp$/)	{return 15;}	#.bb-niigata.jp(�V��)

if($remo =~ /\.lbdsl\.net$/)		{return 80;} #.lbdsl.net�@�A�����J
if($remo =~ /\.cox\.net$/)		{return 80;} #.cox.net�@�A�����J
if($remo =~ /\.vrtc\.net$/)		{return 21;} #.vrtc.net�@�򕌌��b�ߎs�⑺��
if($remo =~ /\.pacbell\.net$/)		{return 80;} #.pacbell.net�@�A�����J
if($remo =~ /\.iowatelecom\.net$/)	{return 80;} #.iowatelecom.net�@�A�����J
if($remo =~ /\.ms246\.net$/)		{return 13;} #.ms246.net�@�����E�_�ސ�
if($remo =~ /\.gujocity\.net$/)		{return 21;} #.gujocity.net�@�򕌌��S�㔪��
if($remo =~ /\.gru\.net$/)		{return 80;} #.gru.net�@�A�����J
if($remo =~ /\.ovh\.net$/)		{return 80;} #.ovh.net�@�t�����X
if($remo =~ /\.axelmark\.net$/)		{return 68;} #.axelmark.net�@sv0134.dc01.axel

if($remo =~ /\.bitcat\.net$/)		{return 68;} #.bitcat.net(�S���}���V�����H)
if($remo =~ /\.dsl\.net$/)		{return 80;} #.dsl.net(�A�����J)
if($remo =~ /\.e-awa\.net$/)		{return 36;} #.e-awa.net(����)
if($remo =~ /\.e-nt\.net$/)		{return 80;} #.e-nt.net(�A�����J)
if($remo =~ /\.proxad\.net$/)		{return 80;} #.proxad.net(�t�����X)
if($remo =~ /\.arcor-ip\.net$/)		{return 80;} #.arcor-ip.net(�h�C�c)
if($remo =~ /\.fastres\.net$/)		{return 80;} #.fastres.net(�C�^���A)
if($remo =~ /\.t-dialin\.net$/)		{return 80;} #.t-dialin.net(�h�C�c)
if($remo =~ /\.nameservices\.net$/)	{return 80;} #.nameservices.net(�A�����J)
if($remo =~ /\.sbcglobal\.net$/)	{return 80;} #.sbcglobal.net(�A�����J)
if($remo =~ /\.fctv-net\.net$/)		{return 42;} #.fctv-net.jp(����)
if($remo =~ /\.kwins\.net$/)		{return 60;} #.kwins.net(���o�C��)
if($remo =~ /\.ycix\.net$/)		{return 19;} #.ycix.net(�R��)

if($remo =~ /\.nasicnet\.com$/)		{return 68;} #.nasicnet.com(�S���}���V����)
if($remo =~ /\.xiando\.com$/)		{return 68;} #.xiando.com(�C�O�Z�C�V�F��)
if($remo =~ /\.george24\.com$/)		{return 68;} #.george24.com(�S���}���V����)
if($remo =~ /\.kaga-tv\.com$/)		{return 17;} #.kaga-tv.com(�ΐ�)

if($remo =~ /\.takamori\.ne\.jp$/)	{return 20;} #.takamori.ne.jp(����)
if($remo =~ /\.hctv\.ne\.jp$/)		{return 11;} #.hctv.ne.jp(���)
if($remo =~ /\.dcn\.ne\.jp$/)		{return 51;} #.dcn.ne.jp(�֓��n��)
if($remo =~ /\.icn\.ne\.jp$/)		{return 15;} #.icn.ne.jp(�V��)
if($remo =~ /\.au-net\.ne\.jp$/)	{return 68;} #.au-net.ne.jp(�S��)
if($remo =~ /\.knc\.ne\.jp$/)		{return 1;}  #.knc.ne.jp(�k�C��)
if($remo =~ /\.coralnet\.or\.jp$/)	{return 70;} #.coralnet.or.jp(�k��)
if($remo =~ /\.mitene\.or\.jp$/)	{return 68;} #.mitene.or.jp(�S��)
if($remo =~ /\.din\.or\.jp$/)		{return 68;} #.din.or.jp(�S��)

if($remo =~ /\.zoot\.jp$/)		{return 68;} #.zoot.jp�@�S��
if($remo =~ /\.gmo-access\.jp$/)	{return 68;} #.gmo-access.jp�@�S��
if($remo =~ /\.dsn\.jp$/)		{return 68;} #.dsn.jp �S��
if($remo =~ /\.withe\.ne\.jp$/)		{return 68;} #.withe.ne.jp �}���V����
if($remo =~ /\.supercsi\.jp$/)		{return 72;} #.supercsi.jp�@�����n���H(�l����)
if($remo =~ /\.banban\.jp$/)		{return 28;} #.banban.jp(����)
if($remo =~ /\.viplt\.ne\.jp$/)		{return 71;} #.viplt.ne.jp �k�����S�����ǃt���b�c�͈̔͂͐����{

if($remo =~ /\.iwami\.or\.jp$/)		{return 28;} #.iwami.or.jp
if($remo =~ /\.optonline\.net$/)	{return 28;} #.optonline.net
if($remo =~ /\.zakkaz\.ne\.jp$/)	{return 28;} #.zakkaz.ne.jp
if($remo =~ /\.katsunuma\.ne\.jp$/)	{return 28;} #.katsunuma.ne.jp
if($remo =~ /\.tgn\.or\.jp$/)		{return 28;} #.tgn.or.jp
#.voice-factory.net
#.info.net
#.speakeasy.net
#.kagoya.net
#.qwest.net

#.ksp.or.jp
#.sala.or.jp
#.rim.or.jp
#.fureai.or.jp
#.fitweb.or.jp

#.ose.ne.jp
#.tocn.ne.jp
#.myt.ne.jp
#.hibikino.ne.jp
#.speedway.ne.jp
#.kamitv.ne.jp
#.chun2.ne.jp
#.inetpia.ne.jp
#.satsuma.ne.jp
#.aso.ne.jp
#.kiso.ne.jp
#.gotemba.ne.jp

#CCCCC
#'50���k�n��','51�֓��n��','52�����n��','53�֐��n��','54�l���n��','55�����n��','56��B�n��','57�����{','58�����{','',

	my $ken = ''; #�����̃u���b�N�Œ�`����ĂȂ�
	if($remo =~ /\.ezweb\.ne\.jp$/)	{return 60;}
	if($remo =~ /\.enjoy\.ne\.jp$/)	{return 0;}
#	if($remo =~ /\.net$/)		{if(open(LX,">> HOST29.000")){print LX "(ne.jp)$remo($ken)\n";close(LX);}}
#	if($remo =~ /\.ne\.jp$/)	{if(open(LX,">> HOST29.000")){print LX "(ne.jp)$remo($ken)\n";close(LX);}}
#	if($remo =~ /\.go\.jp$/)	{if(open(LX,">> HOST29.000")){print LX "(ne.jp)$remo($ken)\n";close(LX);}}
#	if($remo =~ /\.or\.jp$/)	{if(open(LX,">> HOST29.000")){print LX "(ne.jp)$remo($ken)\n";close(LX);}}
#{if(open(LX,">> HOST29.000")){print LX "(?????)$remo($ken)\n";close(LX);}}
	return 67	;
}
#############################################################################
#	�X���Ԃ�����(�o�C�o�C���邳��)
#############################################################################
sub bybySaruON
{
	my ($GB) = @_	;

	if($ENV{'SERVER_NAME'} =~ /hayabusa/)		{return 0;}
	if($GB->{FORM}->{bbs} eq 'goki')		{return 1;}
#return 0;

	if($GB->{FORM}->{bbs} eq 'doujin')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'dataroom')		{return 0;}
	if($ENV{'SERVER_NAME'} =~ /qb/)			{return 0;}
#	if($ENV{'SERVER_NAME'} =~ /bbspink/)		{return 0;}
	if($GB->{FORM}->{bbs} eq 'news4viptasu')	{return 0;}
#	if($GB->{FORM}->{bbs} eq 'campus')		{return 0;}
#return 1;

	if($GB->{FORM}->{bbs} eq 'aastory')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'aasaloon')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'nida')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'mona')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'kao')			{return 0;}
	if($GB->{FORM}->{bbs} eq 'nanminhis')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'eroparo')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'intro')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'warhis')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'kitchen')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'ume')			{return 0;}
	if($GB->{FORM}->{bbs} eq 'mog2')		{return 0;}
	if($GB->{FORM}->{bbs} eq 'liveanime')		{return 0;}
return 1;

	if($GB->{FORM}->{bbs} eq 'operate')		{return 1;}
return 0;
	if($GB->{FORM}->{bbs} eq 'news4vip')		{return 1;}
	if($GB->{FORM}->{bbs} eq 'morningcoffee')	{return 1;}

	if($GB->{FORM}->{bbs} eq 'ana')			{return 1;}
	if($GB->{FORM}->{bbs} eq 'doujin')		{return 1;}
	if($GB->{FORM}->{bbs} eq 'morningcoffee')	{return 1;}
return 0;

	if($GB->{FORM}->{bbs} eq 'wcomic')		{return 1;}
	if($GB->{FORM}->{bbs} eq 'kouri')		{return 1;}
	if($ENV{'SERVER_NAME'} =~ /ex/)			{return 1;}
	if($ENV{'SERVER_NAME'} =~ /game/)		{return 1;}

	return 0	;
}
sub bybySaru
{
	my ($GB) = @_	;

	local $_	;
	my $dfile = $GB->{DATPATH} . $GB->{FORM}->{'key'} . '.dat';
	my $prsize = IsSnowmanServer == BBSD->{REMOTE}
			? ($_ = bbsd($dfile, 'getfilesize', 'nolog')) !~ /\D/ ? $_ : 0
			: ($_ = stat($dfile)) ? $_->size : 0;

#if(open(UUU,">> loglog.cgi")){print UUU "$dfile=$prsize\n";close(UUU);}
	if($prsize < 2048*20)	{return 0;}

	if(!bybySaruON($GB))
	{
		$GB->{version} .= " +ByeSaru=OFF";
		return 0;
	}
	else
	{
		;
		$GB->{version} .= " +ByeSaru=ON";
	}

	#���̓X���[
	if($GB->{CAP})					{return 0;}
	#���̓X���[
#	if($GB->{MARU})					{return 0;}
	#����D�҂̓X���[
	if($GB->{KABUU})				{return 0;}
	if($GB->{KABUUP})				{return 0;}

	my $kaimadeOK = 10	; #M��܂�ok
	my $kaiChu = 18		; #N�񒆁@�����������N���A����܂��B

	my $host = $ENV{'REMOTE_ADDR'}			;	#IP
	if($GB->{P22CH})	{$host = $GB->{HOST2}	;}	#IP from p2
	$host =~ /(\d+)\.(\d+)\.(\d+)\.(\d+)/;
	$host = "$1.$2.$3"	;
	if($GB->{KEITAI})	{$host = $GB->{IDNOTANE};}	#�g�ьŗL�ԍ�

	my $remo = $GB->{HOST29}; #�����郊���z
	#p57b2fd.szoknt01.ap.so-net.ne.jp
	if($remo =~ /\.(\S+\.ap\.so-net\.ne\.jp)/)
	{
		$host = $1		;
		$host =~ s/\d/\#/g	;
#if(open(UUU,">> loglog.cgi")){print UUU "$host\n";close(UUU);}
	}
	#p7042-adsau04sappo2-acca.hokkaido. .ne.jp
	if($remo =~ /\S+-(\S+\d+\S+\S+\.\S+\.ocn\.ne\.jp)/)
	{
		$host = $1		;
		$host =~ s/\d/\#/g	;
#if(open(UUU,">> loglog.cgi")){print UUU "$host\n";close(UUU);}
	}

	# �Ⴞ��܂͂���[
	if($ENV{SERVER_NAME} =~ /^live2[34]\./)	{return 0;}

	# live�n�͂���[
#	if($ENV{'SERVER_NAME'} !~ /live/)	{return 0;}
#	if($ENV{'SERVER_NAME'} !~ /ex15/)	{return 0;}
#	if($ENV{'SERVER_NAME'} !~ /ex16/)	{return 0;}

	my ($saruPath, @saruList, %kai);
	if(IsSnowmanServer)
	{
		# �������������ꍇ�݂̂��̉� (����ȊO 0) ���Ԃ�
		# age �͖�����ăN���A�̋����ɂ��ׂ�����
		$kai{$host} = bbsd($GB->{FORM}{bbs}, 'chkthrtimecount', $GB->{FORM}{key}, $GB->{NOWTIME} % 3600, $kaiChu, $kaimadeOK + 1, $host, 'nolog');
		# �^�C���A�E�g���G���[�̏ꍇ�̓X�L�b�v
		$kai{$host} = 0 if($kai{$host} =~ /\D/);
	}
	else
	{
#		$saruPath = "./book/$GB->{FORM}->{bbs}/";
		$saruPath = "$FOX->{BOOK}/book/$GB->{FORM}->{bbs}/";
		mkdir($saruPath, 0777)		;
		$saruPath .= $GB->{FORM}->{key}	;
		$saruPath .= '.cgi'		;

		@saruList = ();
		if(open(SARU, $saruPath))
		{
			@saruList = <SARU>		;
			close(SARU)			;
		}

		%kai = ()			;
		foreach my $see (@saruList)
		{
			chomp($see)	;
			$kai{$see} ++	;
		}
		$kai{$host} ++		;
	}

	if(!$GB->{CAP} && !$GB->{MARU} && $kai{$host} > $kaimadeOK)	
	{
		&DispError2($GB,"�d�q�q�n�q�I","��͂�M���͓��e�������ł��B�o�C�o�C���邳��B<BR>�����t=�D���ȎԂ́H");
	}

#	$GB->{FORM}->{'MESSAGE'} .= "<hr>$kai{$host}";

	if(!IsSnowmanServer)
	{
		if(!open(SARU,"> $saruPath"))	{return 0;}
		print SARU "$host\n";
		my $ccc = 0;
		foreach my $see (@saruList)
		{
			chomp($see)	;
			print SARU "$see\n";
			$ccc ++		;
			if($ccc > $kaiChu)	{last;}
		}
		close(SARU)		;
	}

	return 0		;
}
########################################################################
# �������̏���(�n�k�֘A��)
########################################################################
sub EQfromWhereON
{
	my ($GB) = @_;

#	if($GB->{FORM}->{bbs} eq 'news')	{return 1;}
	if($GB->{FORM}->{bbs} eq 'eq')		{return 1;}
	if($GB->{FORM}->{bbs} eq 'eqplus')	{return 1;}
	if($GB->{FORM}->{bbs} eq 'namazuplus')	{return 1;}

	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_JP_CHECK'} eq "checked") {return 1;}

	return 0	;
}
sub EQfromWhere
{
	my ($GB) = @_;

	if(!&EQfromWhereON($GB))	{return 0;}

	my $a47 = &area47($GB)		;
	if($a47 eq '')			{return 0;}

	$GB->{FORM}->{'FROM'} = "$GB->{FORM}->{'FROM'}<\/b>($a47)<b>"	;

	return 1;
}
########################################################################
# �������̏���(vip�����_��)
########################################################################
sub NanashiReplace4vipON
{
	my ($GB) = @_;

	if($GB->{FORM}->{bbs} eq 'poverty')	{return 1;}
	if($GB->{FORM}->{bbs} eq 'news')	{return 1;}
#	if($GB->{FORM}->{bbs} eq 'anime4vip')	{return 1;}
	if($GB->{FORM}->{bbs} eq 'asaloon')	{return 1;}

#	if($GB->{FORM}->{bbs} eq 'campus')	{return 1;}
#	if($GB->{FORM}->{bbs} eq 'news4vip')	{return 1;}
#	if($GB->{FORM}->{bbs} eq 'operate2')	{return 1;}
	return 0	;
}
sub NanashiReplace4vip
{
	my ($GB) = @_;

	if(!&NanashiReplace4vipON($GB))	{return 0;}
if($GB->{FORM}->{'FROM'} ne '' || defined $GB->{TRIPKEY})
{
	#���̓X���[
	if($GB->{MARU})			{return 0;}
	if($GB->{KABUU})		{return 0;}
	if($GB->{BEelite} eq 'SOL')	{return 0;}
	if($GB->{BEelite} eq 'DIA')	{return 0;}
}
	my $fusi = ""				;
	if($GB->{FORM}->{'FROM'} =~ /fusianasan/)		{$fusi="fusianasan";}
	my $kab = ""				;
	if($GB->{FORM}->{'FROM'} =~ /(!kab[a-z\d\-\%\:]+)/)	{$kab = $1;}
	elsif($GB->{FORM}->{'FROM'} =~ /(!kab)/)		{$kab = $1;}

	$ENV{REMOTE_ADDR} =~ /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/	;
	my $kk = $1	;
	my $mm = $2	;
	my $iq = $3	;
	my $nm = $4	;

	if($GB->{KEITAI})
	{
		$GB->{IDNOTANE} =~ /\S*(\d+)\S*/	;
		$nm = $1;
	}

	my ($sec, $min, $hhh, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($GB->{NOWTIME});

	$iq *= 255	;
	$nm += $iq	;

#	my $off = (($mon*31 + $mday)*24 + $hhh)	;	#�@�����ύX
	my $off =  ($mon*31 + $mday)		;	#�@�����ύX
	$nm += $off	;

	my $sss = (scalar @FOX_774)		;
	if($sss < 1)	{return 0;}
	my $omikuji2 = $nm % $sss		;
	my $omikuji3 = $FOX_774[$omikuji2]	;

	if($GB->{FORM}->{bbs} eq 'poverty')	{$omikuji3 = $FOX->{$GB->{FORM}->{bbs}}->{'BBS_NONAME_NAME'}	;}

	my $a47 = &area47($GB)		;
#	if($GB->{FORM}->{bbs} eq 'news')
#	{
#		my $yy = ($nm % 70) + 38	;
#		$a47 = "$yy��";
#	}
	if($GB->{FORM}->{bbs} eq 'campus')
	{
		my $yy = ($nm % 20) + 25	;
		$a47 = "SS$yy";
	}

if($GB->{FORM}->{bbs} eq 'poverty')
{
	if($a47 ne '')
	{
		$omikuji3 =~ s/\(\S+\)/<\/b>\($a47\)<b>/;
	}
	else
	{
		$omikuji3 =~ s/\(\S+\)/<\/b>\(�`��\)<b>/;
	}
	$GB->{FORM}->{'FROM'} = "$fusi$kab $omikuji3"	;
	undef $GB->{TRIPKEY};
	return 1;
}
else
{
	if($a47 ne '')
	{
		$omikuji3 =~ s/\(\S+\)/\($a47\)/;
	}
	else
	{
		$omikuji3 =~ s/\(\S+\)/\(�`��\)/;
	}
}	

	$GB->{FORM}->{'FROM'} = "$fusi$kab <\/b>$omikuji3<b>"	;

#	$GB->{FORM}->{'FROM'} = "$GB->{FORM}->{'FROM'}<\/b>$omikuji3<b>"	;
#	$GB->{FORM}->{'FROM'} = "<\/b>$FOX_774[$sss]<b>"	;
	undef $GB->{TRIPKEY};
	return 1;
}
#############################################################################
# vip�L��
#############################################################################
sub vip931
{
	my ($GB) = @_	;

#	return 0	;

	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_VIP931'} ne "checked")	{return 0;}

#my $eee = $GB->{FORM}->{bbs} . "+" . $FOX->{$GB->{FORM}->{bbs}}->{'BBS_VIP931'};
#&DispError2($GB,"�d�q�q�n�q�I","checked $eee");

	#�g�т̓X���[
	if($GB->{KEITAI})			{return 0;}
	if($GB->{KEITAIBROWSER})		{return 0;}
	# �g�сE���ۂ�͂���[
	if(&IsIP4Mobile($ENV{REMOTE_ADDR}))	{return 0;}
	#���̓X���[
	if($GB->{CAP})				{return 0;}
	#���̓X���[
	if($GB->{MARU})				{return 0;}
	#����p2�̓X���[
	if($GB->{P22CH})			{return 0;}

	use LWP::UserAgent;

	my $fff = "1111222233334440"		;
	if($GB->{FORM}->{bbs} eq 'news4vip' || $GB->{FORM}->{bbs} eq 'campus')
	{
		$fff = "1111222233334441"	;
	}

	my $x = "http://cook81.2ch.net/931/vip931.so?$fff-$ENV{REMOTE_ADDR}";
	my $ua = LWP::UserAgent->new();
	$ua->timeout(3);
	my $request = HTTP::Request->new('GET', $x);
	my $response = $ua->request($request) ;
	my $response_body = $response->content();
	my $response_code = $response->code();

	# ���擾�G���[�Ȃ�L���Ȃ����Ƃɂ���
	if ($response->is_error)		{return 0;}

	$response_body =~ /VIP931\[([0-9]+)\]/;

#&DispError2($GB,"�d�q�q�n�q�I","vip�L���ł�($1,$response_code)<br><br><a target=\"_blank\" href=\"http://cook81.2ch.net/\">�ڂ������</a>");

	$GB->{V931} = $1	;

	if($GB->{V931} ne "0")
	{
		# ����̔ł�vipper�}�[�N�����ċ���
		if($GB->{FORM}->{'bbs'} eq "operate2" ||
		   $GB->{FORM}->{'bbs'} eq "sec2chd")
		{
			$GB->{FORM}->{'FROM'} = ' </b>[�@�O�ցO]<b> ' . $GB->{FORM}->{'FROM'};
			return 0;
		}
		# ����ȊO
		&DispError2($GB,"�d�q�q�n�q�I","���L���ł�($1,$response_code)<br><br><a target=\"_blank\" href=\"http://cook81.2ch.net/\">�ڂ������</a>");
	}

	return 0	;
}
#############################################################################
# P2���ǂ���
#############################################################################
sub IsP2
{
	my ($GB) = @_	;

	#����p2�̓X���[
	if($GB->{P22CH})				{return 0;}
	if($GB->{HOST999} =~ //)			{return 0;}

	if($ENV{'HTTP_USER_AGENT'} !~ /^Monazilla\/1/)	{return 0;}

	if($GB->{HOST999} =~ /lolipop\.jp/)		{return 1;}
	if($GB->{HOST999} =~ /land\.to/)		{return 1;}
	if($ENV{'HTTP_USER_AGENT'} =~ /[Pp]2/)		{return 1;}
	if($ENV{'HTTP_USER_AGENT'} =~ /[Pp]\+\+/)	{return 1;}
	return 0;
}
#############################################################################
# ����E�B���X�΍�
#############################################################################
##### Mozilla/4.0 (compatible; ICS) 
sub Saga
{
	my ($GB) = @_			;

	if($ENV{'HTTP_USER_AGENT'} =~ /Mozilla\/4\.0 \(compatible; ICS\)/)
	{
		&DispError2($GB,"FOX ��","<font color=green>FOX ���@����E�B���X</font><br><br>�������B�B�B");
	}
	return 0;
}
#############################################################################
# �R�c�E�B���X�΍�
#############################################################################
##### Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)
sub Yamada
{
	my ($GB) = @_			;

	#if($ENV{'HTTP_USER_AGENT'} !~ /Mozilla\/4\.0/){return 0;}

	my $mss = substr($GB->{FORM}->{'MESSAGE'}, 0, 30);
	# $mss =~ s/</&lt;/g; $mss =~ s/>/&gt;/g;

	#if($ENV{'SERVER_NAME'} =~ /tmp4/ && $GB->{FORM}->{'MESSAGE'} =~ /���Ƃ��/)
	{#cookie
	#if(open(ABCD,">>./yamada.txt")){print ABCD "[$ENV{'HTTP_COOKIE'}]\n";close(ABCD);}
	#if(open(ABCD,">>./yamada.txt")){print ABCD "[$ENV{'HTTP_COOKIE'}]$mss\n";close(ABCD);}
	#if(open(ABCD,">>./yamada.txt")){print ABCD "[$ENV{HTTP_ACCEPT_LANGUAGE}]$mss\n";close(ABCD);}
	if(open(ABCD,">>./yamada.txt")){print ABCD "[$ENV{'HTTP_USER_AGENT'}]\n";close(ABCD);}
	#if(open(ABCD,">>./yamada.txt")){print ABCD "[$ENV{'HTTP_USER_AGENT'}]$mss\n";close(ABCD);}
	}

if($ENV{'HTTP_COOKIE'} =~ /^NAME\=\; MAIL\=sage\; PON\=/
 && $ENV{'HTTP_USER_AGENT'} !~ /^Monazilla\/1/ 
 && $ENV{'HTTP_USER_AGENT'} !~ /Opera/
 && $ENV{'HTTP_USER_AGENT'} !~ /DDIPOCKET/
 && $ENV{HTTP_ACCEPT_LANGUAGE} eq '')
{
	#if($ENV{'SERVER_NAME'} =~ /tmp4/ && $GB->{FORM}->{'MESSAGE'} =~ /���Ƃ��/)
	{#cookie
	#if(open(ABCD,">>./yamada.txt")){print ABCD "$ENV{'HTTP_COOKIE'}\n";close(ABCD);}
	#if(open(ABCD,">>./yamada.txt")){print ABCD "[$ENV{HTTP_ACCEPT_LANGUAGE}]\n";close(ABCD);}
	if(open(ABCD,">>./yamada.txt")){print ABCD "[$ENV{'HTTP_USER_AGENT'}]\n";close(ABCD);}
	}
	{
	my $mss = substr($GB->{FORM}->{'MESSAGE'}, 0, 30); $mss =~ s/</&lt;/g; $mss =~ s/>/&gt;/g;
	my $outdat = "$GB->{FORM}->{'FROM'}<>$GB->{FORM}->{'mail'}<>$GB->{DATE}<>$mss<>$GB->{FORM}->{'subject'}<>$GB->{HOST999}<>$ENV{'REMOTE_ADDR'}<><>$ENV{'HTTP_USER_AGENT'}";
	#���t�Ǝ��Ԃ����Ƃ���
	my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($GB->{NOWTIME});
	my $fff = sprintf("../_service/Yamada%04d%02d%02d.txt",$year+1900,$mon+1,$mday)	;
	open(OUT2, ">>$fff");
	print OUT2 "$outdat\n";
	close(OUT2);
	}
&DispError2($GB,"FOX ��","<font color=green>FOX ���@�R�c�E�B���X</font><br><br>�������B�B�B");
}
}
#############################################################################
# �N�b�L�[���s
#############################################################################
sub PutCookie
{
	my ($GB) = @_;

	#�L������������
	my $exp = 24 * 60 * 60;
	$exp *= 30;	#�L���������悶��
	my ($dmy,$mdc,$monc,$yrc,$wdayc,$mc,$yc,$times);
	($dmy,$dmy,$dmy,$mdc,$monc,$yrc,$wdayc,$dmy,$dmy) = gmtime($GB->{NOWTIME} + $exp);
	$yc = ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday') [$wdayc];
	$mc = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec') [$monc];
	$yrc = $yrc+1900;
	$mdc = "0$mdc" if ($mdc < 10);
	my ($cname, $cmail);
	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_NAMECOOKIE_CHECK'} eq "checked"){
		$cname = "$GB->{FORM}->{'FROM'}";
	}
	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_MAILCOOKIE_CHECK'} eq "checked"){
		$cmail = "$GB->{FORM}->{'mail'}";
	}
	if($ENV{'HTTP_USER_AGENT'} =~ /[Mm][Aa][Cc]/ ){
		$cname =~ s/(\W)/'%' . unpack('H2', $1)/eg;
		$cmail =~ s/(\W)/'%' . unpack('H2', $1)/eg;
	}
	print "Set-Cookie: NAME=$cname; expires=$yc, $mdc-$mc-$yrc 00:00:00 GMT; path=/\n";
	print "Set-Cookie: MAIL=$cmail; expires=$yc, $mdc-$mc-$yrc 00:00:00 GMT; path=/\n";

	return 0;
}
#############################################################################
# ���e�m�F���
#############################################################################
sub ToukouKakunin
{
	my ($GB) = @_;
	my $mdc = '';

	my $msg = $GB->{FORM}->{'MESSAGE'};
	my $sbj = $GB->{FORM}->{'subject'};
	$msg =~ s/<[Bb][Rr]>/\n/g;
	$msg =~ s/&/&amp;/g;
	$msg =~ s/"/&quot;/g;
	$sbj =~ s/&/&amp;/g;
	$sbj =~ s/"/&quot;/g;

	#�m�F��ʂ��o��
	print "Content-type: text/html; charset=shift_jis\n\n";
	print <<EOF;
<html lang="ja">
<head>
<title>���e�m�F</title>
<meta http-equiv="Content-Type" content="text/html; charset=shift_jis">
<meta name="viewport" content="width=device-width,initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.6,user-scalable=yes" />
</head>
<body bgcolor="#FFFFFF">
<font size=+1 color=#FF0000><b>�������݊m�F</b></font><ul><br><br>
<b>$GB->{FORM}->{'subject'} </b><br>���O�F $GB->{FORM}->{'FROM'}<br>E-mail�F $GB->{FORM}->{'mail'}<br>���e�F<br>
$GB->{FORM}->{'MESSAGE'}<br><br>$ENV{HTTP_USER_AGENT}<br><br></ul><b>
���e�m�F(2)<br>
�E���e���ꂽ���e�̓R�s�[�A�ۑ��A���p�A�]�ړ������ꍇ������܂��B<br>
�E���e�Ɋւ��Ĕ�������ӔC�͑S�ē��e�҂ɋA���܂��B<br></b>
<form method=POST action="../test/bbs.cgi?guid=ON"><input type=hidden name="subject" value="$sbj">
<input type=hidden name=FROM  value="$GB->{FORM}->{'FROM'}">
<input type=hidden name=mail  value="$GB->{FORM}->{'mail'}">
<input type=hidden name=get value="1$mdc">
<input type=hidden name=MESSAGE value="$msg">
<br><input type=hidden name=bbs value=$GB->{FORM}->{'bbs'}>
<input type=hidden name=time value=$GB->{NOWTIME}>
<input type=hidden name=key value=$GB->{FORM}->{'key'}>
<input type=submit value="�S�ӔC�𕉂����Ƃ��������ď�������" name="submit"><br></form>
�ύX����ꍇ�͖߂�{�^���Ŗ߂��ď��������ĉ������B<font size=-1>(cookie��ݒ肷��Ƃ��̉�ʂ͂łȂ��Ȃ�܂��B)</font><br></body></html>
EOF

	return 0;
}
#############################################################################
# ���̏���
# �Z�b�V����ID�𓾂�HOST999�ɕۑ����A�����O�C���t���O�𗧂Ă�
# p2+���́u������Ⴑ�[���v�ɂ���
#############################################################################
sub ProcessMaru
{
	my ($GB) = @_;

	#���̃Z�b�V����ID�𓾂�
	$GB->{MARU} = &IsMonazilla($GB->{FORM}->{sid});

	#p2+��=p2
	if($GB->{P22CH})	{ $GB->{MARU} = ""; }

	if($GB->{MARU} eq $FOX->{OTAMESHIMARU})
	{
		if($GB->{FORM}->{'bbs'} eq 'sec2chd'
		|| $GB->{FORM}->{'bbs'} eq 'saku'
		|| $GB->{FORM}->{'bbs'} eq 'saku2ch'
		)
		{
			&endhtml($GB)		;
			$GB->{MARU} = 1		;
		}
	}


	#�Z�b�V����ID�������؂�Ȃ�ă��O�C���𑣂��ďI��
	if($GB->{MARU} eq "1")
	{
		&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�ēx���O�C�����ĂˁB�B�B");
	}

	#HOST999�Ɂ��̏�������
	if($GB->{MARU})	
	{
		$GB->{HOST999} .= "[$GB->{MARU}]";
		# ����p2�ȊO��p2+���́u������Ⴑ�[���v
		if(!$GB->{P22CH})
		{
			if($ENV{HTTP_USER_AGENT} =~ /p2\-client\-ip\:/)
			{
				&DispError2($GB,"�d�q�q�n�q�I","������Ⴑ�[��");
			}
		}
	}

#2009/05/02 07022420477712_eg[nJu0xsHmrC2U5G/K]
#	if($GB->{MARU} =~ /rC2U5G\/K$/ || $GB->{MARU} =~ /mkladyWF$/)
#	{
#		$GB->{MARU} = "";
#	}

	return 0;
}
#############################################################################
# ������1���當����2����蕥��
# ����: ������1, ������2, �t���O
# �߂�l: ������̕�����
#
# usuusubonbon �̂悤�Ȍ`���Ή�
# �t���O��1�̎��ɂ͂��炩���ߕ�����1��8�r�b�g�ڂ��}�X�N���������Ŕ�r����
#############################################################################
sub StripStr
{
	my ($str1, $str2, $flag) = @_;

	my $savestr = $str1;	# 8�r�b�g�ڂ��J�b�g����O�̕������ۑ����Ă���

	# �t���O�������Ă���A8�r�b�g�ڂ��J�b�g
	# �ꎞ�I�ɃJ�b�g���I�t by ��
	#if($flag)
	#{
	#	$str1 =~ tr/\x80-\xFF/\x00-\x7F/;
	#}

	# �����񂪂Ȃ���΂΂��΂�
	if($str1 !~ $str2)	{ return $savestr; }

	# �����񂪑��݂��Ȃ��Ȃ�܂ŕϊ����J��Ԃ��āA�A�A
	while($str1 =~ $str2)
	{
		$str1 =~ s/$str2//g;
	}

	# �������ʂ�Ԃ�
	return $str1;
}
########################################################################
# ���O���ƃ��[�����̋֎~���[�h�̏���
########################################################################
sub NGNameReplace
{
	my ($GB) = @_;

	# NG���[�h
	$GB->{FORM}->{'FROM'} =~ s/mail/ /g;
	$GB->{FORM}->{'FROM'} =~ s/MAIL/ /g;
	$GB->{FORM}->{'FROM'} =~ s/�Ǘ�/�h�Ǘ��h/g;
	$GB->{FORM}->{'FROM'} =~ s/�ǒ�/�h�ǒ��h/g;
	$GB->{FORM}->{'FROM'} =~ s/����/�h�����h/g;
	$GB->{FORM}->{'FROM'} =~ s/�폜/�h�폜�h/g;
	$GB->{FORM}->{'FROM'} =~ s/���A/�h���A�h/g;
	$GB->{FORM}->{'FROM'} =~ s/sakujyo/�hsakujyo�h/g;
	$GB->{FORM}->{'FROM'} =~ s/��/��/g;
	$GB->{FORM}->{'FROM'} =~ s/��/��/g;
	$GB->{FORM}->{'FROM'} =~ s/�R���/fusianasan/g;
	# BadTripCheck ��V�݂����̂ŕs�v by ��
	#$GB->{FORM}->{'FROM'} = &StripStr($GB->{FORM}->{'FROM'}, "usubon", 1);

	$GB->{FORM}->{'mail'} =~ s/�폜/�h�폜�h/g;
	$GB->{FORM}->{'mail'} =~ s/sakujyo/�hsakujyo�h/g;
	$GB->{FORM}->{'mail'} =~ s/��/��/g;
	$GB->{FORM}->{'mail'} =~ s/��/��/g;

	$GB->{FORM}->{'MESSAGE'}=~ s/sssp:/http:/g;;

	if(!$GB->{MARU})
	{
		$GB->{FORM}->{'FROM'} =~ s/��/��/g;
	}
	if($GB->{FORM}->{'bbs'} eq 'ihou' && $GB->{KEITAI})
	{
		$GB->{FORM}->{'FROM'} = "tasukeruyo$GB->{FORM}->{'FROM'}"	;
	}
#	if($GB->{FORM}->{'bbs'} eq 'campus' && rand(100) > 90)
#	{
#		$GB->{FORM}->{'FROM'} = "fusianasan"	;
#	}


	return 0;
}
########################################################################
# �g���b�v�̏���
# $GB->{TRIPSTRING} �ɏ������ʂ�����
########################################################################
sub ProcessTrip
{
	my ($GB, $main_message, $handle_pass) = @_;

	length $handle_pass > 1024
		and &DispError2($GB,'�d�q�q�n�q�I','�d�q�q�n�q�F�g���b�v�L�[�����I');

	if (length $handle_pass >= 12)
	{
		my $mark = substr($handle_pass, 0, 1);
		if ($mark eq '#' || $mark eq '$')
		{
			if ($handle_pass =~ m|^#([[:xdigit:]]{16})([./0-9A-Za-z]{0,2})$|)
			{
				$GB->{TRIPSTRING} = substr(crypt(pack('H*', $1), "$2.."), -10);
			}
			else
			{
				# �����̊g���p
				$GB->{TRIPSTRING} = '???';
			}
		}
		else
		{
			use Digest::SHA1 qw(sha1_base64);
			$GB->{TRIPSTRING} = substr(sha1_base64($handle_pass), 0, 12);
			$GB->{TRIPSTRING} =~ tr/+/./;
		}
	}
	else
	{
		my $change_salt = substr($handle_pass, , 1) . "H";
		$change_salt =~ tr/\x3A-\x40\x5B-\x60\x00-\x2D\x7B-\xFF/A-Ga-f./;

		$GB->{TRIPSTRING} = substr(crypt($handle_pass, $change_salt), -10);
	}
	$GB->{FORM}->{'FROM'} = "$main_message </b>��$GB->{TRIPSTRING} <b>";

	return 0;
}
########################################################################
# ���ꂽ�g���b�v�̃`�F�b�N
# $GB->{TRIPSTRING} ������Ă���ꍇ�A�G���[
########################################################################
sub BadTripCheck
{
	my ($GB) = @_;
	our %BadTripList;
	BEGIN {
		# ���ꂽ�g���b�v����������A������ҏW����
		%BadTripList = map +($_ => 1), (
			"3SHRUNYAXA"
		);
	}

	if($BadTripList{$GB->{TRIPSTRING}})
	{
		&DispError2($GB, "�d�q�q�n�q�I", "�d�q�q�n�q�F�g���b�v������Ă��܂��B");
	}
	return 0;
}
########################################################################
# �L���b�v�̏���
########################################################################
sub ProcessCap
{
	my ($GB, $mail_message, $handle_pass) = @_;

	# ���ƃL���b�v�t���O
	my $bflag = 0;
	# �L���b�v���Ԃ�o���t���O
	my $tflag = 0;
	# �L���b�v�n���h����
	my $handle = "";

	# �ʃL���b�v����?
	if(&IsItabetsuCap($GB))
	{
		$bflag = 1;
	}
	# plus/news�̐V�X���͂��Ԃ�o��
	if($GB->{NEWTHREAD} ne 0 && ($GB->{FORM}->{'bbs'} =~ /plus$/ || $GB->{FORM}->{'bbs'} eq 'news'))
	{
		$tflag = 1;
	}
	# �L���b�v���邩��?
	$handle = &FindCap($GB, $handle_pass, $bflag, $tflag);
	if($handle ne "")
	{
		# �L���b�v����������A�܂��L���b�v�t���O�𗧂Ă�
		$GB->{CAP} = 1;

		# ���ɃL���b�v�̎�ʂ��`�F�b�N����
		if($handle =~ /��$/)
		{
			# �����n���h��(���̓L���b�v)
			$GB->{STRONGCAP} = 1;
			$handle =~ s/��.*//;
		}
		elsif($handle =~ /��$/)
		{
			# �����n���h��(���L���b�v)
			# ���݂ł͒ʏ�L���b�v�Ƌ�ʂȂ�
			$GB->{WHITECAP} = 1;
			$handle =~ s/��.*//;
		}

		# ���O����Ă����� ���O���n���h�� ��
		# ���O�Ȃ��̎��� �n���h�� ��
		if($GB->{FORM}->{'FROM'})
		{
			$GB->{FORM}->{'FROM'} = "$GB->{FORM}->{'FROM'}��$handle ��";
		}
		else
		{
			$GB->{FORM}->{'FROM'} = "$handle ��";
		}
	}
	# ���[�����̕⊮ (#���O�̕�����)
	$GB->{FORM}->{'mail'} = $mail_message;

	#&DispError2($GB,"root ��","�L���b�v�t���O:$GB->{CAP} ���t���O:$GB->{WHITECAP} ���t���O:$GB->{STRONGCAP}");

	return 0;
}
########################################################################
# �L���b�v�����邩�ǂ������ׁA�������炻�̃L���b�v����Ԃ�
# ����: $GB, �L���b�v�p�X, �t���O1, �t���O2
#       �t���O1���^�̏ꍇ�A�ʃL���b�v�̏������s��
#       �t���O2���^�̏ꍇ�A�L���b�v���Ԃ肾���̏������s��
# �߂�l: �L���b�v�n���h���� �܂��� ""(�Y���Ȃ��̏ꍇ)
########################################################################
sub FindCap
{
	my ($GB, $pass, $bflag, $tflag) = @_;
	my $board = $GB->{FORM}->{'bbs'};
	my $handle_file = "../handle/";
	my $handle_name = "";

	$pass =~ s/[\.\/]//gi;
	$pass .= ".cgi";

	#bflag���^�̎��́A�ʃL���b�v�̏���
	if($bflag)
	{
		$handle_file .= $board . "/";
	}
	$handle_file .= $pass;

	# �t�@�C�������邩���ׂ�
	if(-e $handle_file)
	{
		#tflag���^�̎��́A�L���b�v�̂��Ԃ肾������
		if($tflag)
		{
			# Perl 5.7.2 �ȍ~�� utime �� undef �ł���
			my $now = $^V lt v5.7.2 ? time : undef;
			# �Ȃ񂾂����܂������Ȃ��̂łƂ肠�������ɖ߂��� by ��
			# my $now = time;

			# �Ⴞ��܂ł́Abbsd�ɂ��Ԃ肾���������˗�
			if(IsSnowmanServer == BBSD->{REMOTE})
			{
				# bbsd �� touch �ł� undef �̑���� 0
				my $cmd = 'touch';
				my $errmsg = bbsd($handle_file, $cmd, $now || 0, 'dummy'); 
				# �^�C���A�E�g���ǂ����`�F�b�N
				if(&bbsd_TimeoutCheck($GB, $errmsg))
				{
					&bbsd_TimeoutError($GB, $cmd);
				}
			}
			else
			{
				# undef �͕ϐ��łȂ����ڋL�q�łȂ��ƃ_��
				utime $now || undef, $now || undef, $handle_file;
			}
		}
		#�t�@�C�����J���Ē��g(�n���h����)�𓾂�
		open(HANDLE, $handle_file);
		$handle_name = <HANDLE>;
		close(HANDLE);
		chomp($handle_name);
	}
	return $handle_name;
}

########################################################################
# �������̏���(heaven4vip�ł���Ă���BE�|�C���g�ɂ��ϖ���������)
########################################################################
sub NanashiReplace4Heaven
{
	my ($GB) = @_;

	if($GB->{BEpoints} > 999)	{$GB->{FORM}->{'FROM'} = "<font color=#9933CC>�����H</font>"	;}
	elsif($GB->{BEpoints} > 499)	{$GB->{FORM}->{'FROM'} = "<font color=#9966CC>����</font>"	;}
	elsif($GB->{BEpoints} > 99)	{$GB->{FORM}->{'FROM'} = "<font color=#9999CC>���c</font>"	;}
	elsif($GB->{BEpoints} > 29)	{$GB->{FORM}->{'FROM'} = "<span style=\"background-color: #6600cc; color: #ffffff; padding-left: 4px; padding-right: 4px;\">�L��</span>"	;}
	elsif($GB->{BEpoints} eq 20)	{$GB->{FORM}->{'FROM'} = "<font color=#99CCCC>����</font>"	;}
	elsif($GB->{BEpoints} eq 10)	{$GB->{FORM}->{'FROM'} = "<font color=#99CCCC>�^��</font>"	;}
	elsif($GB->{BEpoints} > 9)	{$GB->{FORM}->{'FROM'} = "<font color=#99CCCC>�R�c</font>"	;}
	elsif($GB->{BEpoints} > 1)	{$GB->{FORM}->{'FROM'} = "<font color=#99FFCC>����</font>"	;}

	return 0;
}
#############################################################################
# ���O���̓`�F�b�N�A�������⊮�Ə����Aheaven4vip�̖������u������
#############################################################################
sub ProcessNanashi
{
	my ($GB) = @_;

	# ���O���̓`�F�b�N
	if($FOX->{$GB->{FORM}->{bbs}}->{'NANASHI_CHECK'})
	{
		unless($GB->{FORM}->{'FROM'})
		{
			&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F���O����Ă���B�B�B");
		}
	}

	# �������̕⊮�Ə���
	unless($GB->{FORM}->{'FROM'})
	{
		if(!$GB->{KEITAI} && $FOX->{$GB->{FORM}->{bbs}}->{'BBS_RAWIP_CHECK'} eq "checked" && $GB->{COOKIES}{PREN} ne '')
		{	# �ȑO�ɏ������񂾔̖���������
#$GB->{FORM}->{'MESSAGE'} .= "<hr>PREN=$GB->{COOKIES}{PREN} // $FOX->{$GB->{FORM}->{bbs}}->{'BBS_NONAME_NAME'}";

			my $prep = $GB->{COOKIES}{PREN}	;

#use URI::Escape;
#$prep = uri_escape($prep);
			$prep =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;

			if($prep =~ /[<>\t\n\#\&]/)	{&endhtml($GB);}
			if(length($prep) > 48)	{&endhtml($GB);}


			# NG���[�h
			$prep =~ s/mail/ /g;
			$prep =~ s/MAIL/ /g;
			$prep =~ s/�Ǘ�/�h�Ǘ��h/g;
			$prep =~ s/�ǒ�/�h�ǒ��h/g;
			$prep =~ s/����/�h�����h/g;
			$prep =~ s/�폜/�h�폜�h/g;
			$prep =~ s/���A/�h���A�h/g;
			$prep =~ s/sakujyo/�hsakujyo�h/g;
			$prep =~ s/��/��/g;
			$prep =~ s/��/��/g;
			$prep =~ s/�R���/fusianasan/g;

			if($prep ne $FOX->{$GB->{FORM}->{bbs}}->{'BBS_NONAME_NAME'})
			{
				if($prep !~ /fusianasan/ && $prep !~ /tasukeruyo/)
				{
					$GB->{FORM}->{'FROM'} = "<\/b>$prep <b>"	;
				}
				else
				{
					$GB->{FORM}->{'FROM'} = "$prep"			;
				}
			}
		}
	}
	unless($GB->{FORM}->{'FROM'})
	{
		$GB->{FORM}->{'FROM'} = $FOX->{$GB->{FORM}->{bbs}}->{'BBS_NONAME_NAME'};
		if($GB->{FORM}->{bbs} eq 'heaven4vip')
		{
			&NanashiReplace4Heaven($GB);
		}
	}

	return 0;
}
########################################################################
# tasukeruyo�̏���
########################################################################
sub Tasukeruyo
{
	my ($GB) = @_;

	if(length($GB->{FORM}->{'MESSAGE'}) == 0){
		&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�{��������܂���I");
	}

	my $user_agent = $ENV{'HTTP_USER_AGENT'};
	# $user_agent =~ s/"/&quot;/g;
	$user_agent =~ s/</&lt;/g;
	$user_agent =~ s/>/&gt;/g;
	$user_agent =~ tr/\t/ /;
	# [\x00\n\r] �� [[:cntrl:]]
	$user_agent =~ s/[[:cntrl:]]//g;
	$user_agent =~ s/(?<=[\x80-\xFF])$/ /g;
	#$user_agent =~ s/;icc[\w]{20}/;icc********************/g;
	my $tasu = "$GB->{HOST}($GB->{IDNOTANE})";
	$tasu =~ s/<([^>]+)>/<!--$1-->/g;
	&jcode::tr(\$GB->{FORM}->{'FROM'}, 't', '"');
	$GB->{FORM}->{'FROM'} =~ s/"asukeruyo/ <\/b>$tasu<b>/g;
	&jcode::tr(\$GB->{FORM}->{'FROM'}, '"', 't');
	$GB->{FORM}->{'FROM'} =~ s/(?:^|(?<=[\x20-\x7E])) </</;
	$GB->{FORM}->{'MESSAGE'} .= " <hr><font color=\"blue\">$user_agent</font>";

	$GB->{FORM}->{'FROM'} =~ s/fusianasan//g;

	return 0;
}
########################################################################
# fusianasan�̏���
########################################################################
sub Fusianasan
{
	my ($GB) = @_;

	my $fusi = $GB->{HOST}	;
	if($GB->{KEITAI})		{$fusi = $GB->{IDNOTANE};}
	if($GB->{KEITAIBROWSER})	{$fusi = $GB->{IDNOTANE};}
	if($GB->{P22CH})
	{
		$fusi = "p2-user: " . $GB->{IDNOTANE};
		$fusi .= " p2-client-ip: " . $GB->{HOST2};
	}
	$fusi =~ s/<([^>]+)>/<!--$1-->/g;
	&jcode::tr(\$GB->{FORM}->{'FROM'}, 'f', '"');
	$GB->{FORM}->{'FROM'} =~ s/"usianasan/ <\/b>$fusi<b>/g;
	&jcode::tr(\$GB->{FORM}->{'FROM'}, '"', 'f');
	$GB->{FORM}->{'FROM'} =~ s/(?:^|(?<=[\x20-\x7E])) </</;

	return 0;
}
##############################################################################
# �t�H�[�����̃`�F�b�N(���ɕςȕ����A���Ԃ��ǂ߂Ȃ�)
##############################################################################
sub FormInfoCheck
{
	my ($GB) = @_;

	#�a�a�r���ɕs���ȕ������������ꍇ���΂��΂�
	if($GB->{FORM}->{'bbs'} =~ /[^a-zA-Z0-9]/)
	{
		&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�a�a�r�����s���ł��I");
	}
	#���Ԃ��ǂݍ��߂Ȃ�������΂��΂�
	unless($GB->{FORM}->{'time'})
	{
		&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�t�H�[����񂪕s���ł��I");
	}

	return 0;
}
########################################################################
# ���t�@���̃`�F�b�N(�u���E�U�ςł����)
########################################################################
sub BraHen
{
	my ($GB) = @_;

	# �g�сE���ۂ�͂���[
	if(&IsIP4Mobile($ENV{REMOTE_ADDR}))	{return 0;}
	#���̓X���[
	if($GB->{CAP})				{return 0;}
	#���̓X���[
	if($GB->{MARU})				{return 0;}

	# UA���Ȃ��̂̓u����
	#if(!$ENV{'HTTP_USER_AGENT'})
	#{
	#	&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�u���E�U�ςł����B(ua)$ENV{'HTTP_REFERER'}");
	#}
#	if($ENV{'HTTP_USER_AGENT'} =~ /gikoNavi\/beta50/)
	if($ENV{'HTTP_USER_AGENT'} =~ /gikoNavi\/beta50\/1\.50\.2\.606/)
	{
		&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�u���E�U�ςł����-2�B(ua)$ENV{'HTTP_REFERER'}");
	}

	# *.ula.cc �̓X���[
	if($ENV{'HTTP_REFERER'} =~ /^http:\/\/\w+\.u\.la\//)	{return 0;}
	if($ENV{'HTTP_REFERER'} =~ /^http:\/\/\w+\.ula\.cc\//)	{return 0;}

	# orz.2ch.io �̓X���[
	if($ENV{'HTTP_REFERER'} =~ /^http:\/\/orz\.2ch\.io\//)	{return 0;}

	if($ENV{'HTTP_REFERER'} !~ /^http:\/\/$ENV{'HTTP_HOST'}\//)
	{
		#c���t���u���E�U����g�p�����ꍇ�ɑΉ�
		if($ENV{'HTTP_REFERER'} !~ /^http:\/\/c\.2ch\.net\//)
		{
			&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�u���E�U�ςł����B(referer1)$ENV{'HTTP_REFERER'}");
		}
	}
	if($ENV{'HTTP_HOST'} ne $ENV{'SERVER_NAME'})
	{
		&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�u���E�U�ςł����(host)�B$ENV{'HTTP_REFERER'}");
	}

	return 0;
}
########################################################################
# �X���^�C�A���O�A���A�h�A�{���̒����`�F�b�N
########################################################################
sub FieldSizeCheck
{
	my ($GB) = @_;

	#�������̓X���[
	if($GB->{STRONGCAP})			{return 0;}

	if(length($GB->{FORM}->{'subject'}) > $FOX->{$GB->{FORM}->{bbs}}->{"BBS_SUBJECT_COUNT"})
	{
		&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�T�u�W�F�N�g���������܂��I");
	}
	if(length($GB->{FORM}->{'FROM'}) > $FOX->{$GB->{FORM}->{bbs}}->{"BBS_NAME_COUNT"})
	{
		&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F���O���������܂��I");
	}
	if(length($GB->{FORM}->{'mail'}) > $FOX->{$GB->{FORM}->{bbs}}->{"BBS_MAIL_COUNT"})
	{
		&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F���[���A�h���X���������܂��I");
	}
	if(length($GB->{FORM}->{'MESSAGE'}) > $FOX->{$GB->{FORM}->{bbs}}->{"BBS_MESSAGE_COUNT"})
	{
		&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�{�����������܂��I==$FOX->{$GB->{FORM}->{bbs}}->{BBS_MESSAGE_COUNT}==");
	}
	if(length($GB->{FORM}->{'MESSAGE'}) == 0)
	{
		&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�{��������܂���I");
	}

	return 0;
}
########################################################################
# �{���̍s���ƒ�������s�̃`�F�b�N
########################################################################
sub FieldLineCheck
{
	my ($GB) = @_;

	#�������̓X���[
	if($GB->{STRONGCAP})			{return 0;}

	#�s�����s��������
	my @msg = split(/<br>/, $GB->{FORM}->{'MESSAGE'});
	my $cnt = @msg;
	if($cnt > ($FOX->{$GB->{FORM}->{bbs}}->{'BBS_LINE_NUMBER'} * 2))
	{
		&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F���s���������܂��I");
	}
	foreach(@msg)
	{
		#$cnt = tr/[\041-\177]//;
		if(length > 256)
		{
			&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F��������s������܂��I");
		}
	}

	return 0;
}
##############################################################################
# �ʂ̓��ꏈ��(sec2ch�ł͈�ʏ������݋֎~�Ƃ�plus�ł́������X�����ĉ\�Ƃ�)
##############################################################################
sub ItabetsuSpecial
{
	my ($GB) = @_;

	#�K�����͈�ʏ������݋֎~
	if($GB->{FORM}->{'bbs'} eq "sec2ch")
	{
		if(!$GB->{STRONGCAP})
		{
			&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�K�����͈�ʏ������݋֎~�ł�");
		}
	}

	#���̓��O�C���̂�
	if($GB->{FORM}->{'bbs'} =~ /maru$/)
	{
		if(!$GB->{MARU})
		{
			&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F���́����Ȃ��Ƃ����Ȃ��ł��B");
		}
	}

	#�L���b�v��p�j���[�X�ł̓L���b�v�����̂ݏ������݉\
	if($GB->{FORM}->{'bbs'} =~ /plus$/ && $GB->{FORM}->{'subject'} ne "")
	{
		if($GB->{FORM}->{'bbs'} =~ /liveplus/)
		{
			;# �������B�B�B plus �ł�������Ƃ����������ł��A�A�A
		}
		elsif(!$GB->{CAP})
		{
			&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F���̌f���́��t���̋L�҂���̂݃X���b�h�����Ă��܂�");
		}
	}

	# saku/saku2ch/sakud�͒ʏ�̃X�����ċ֎~
	if($GB->{FORM}->{'bbs'} eq "saku" || $GB->{FORM}->{'bbs'} eq "saku2ch" || $GB->{FORM}->{'bbs'} eq "sakud")
	{
		if (!$GB->{CAP})
		{
			if($GB->{FORM}->{'subject'} ne "" && $GB->{FORM}->{'bbs'} ne "sakud")
			{
				&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�����̓X���b�h���ċ֎~�ł��I�I");
			}
		}
	}

	#Be�̓��O�C���̂�
	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_BE_ID'})
	{ 
		if(!$GB->{CAP})
		{
			if($GB->{FORM}->{'DMDM'} eq '')
			{
				&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F<a href=\"http://be.2ch.net/\">be.2ch.net</a>�Ń��O�C�����ĂȂ��Ə����܂���B");
			}
		}
	}

	#IPv6��IPv6�ڑ�����(������Be�̂悤��SETTING.TXT���悳��)
	if($GB->{FORM}->{'bbs'} eq "ipv6")
	{
		# �L���b�v�ł͏�����
		if(!$GB->{CAP})
		{
			if(!$GB->{IPv6})
			{
				&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�FIPv6�Őڑ����Ă��Ȃ��Ə����܂���B");
			}
		}
	}

	return 0;
}
#############################################################################
# �e��X�����ă`�F�b�N���܂Ƃ߂čs��
#############################################################################
sub SuretateTotalCheck
{
	my ($GB) = @_;

	# �̂�т�K��
	my $violation = &Check_Speed($GB);
	if($violation)
	{
		&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�̂�т�s���܂���B<br>���̔X���b�h�������B");
	}
	# �V�X�����ċK��
	my $tatetate = &Check_SURETATE($GB);
	if($tatetate ne 0)
	{
		&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�V���̃z�X�g�ł́A���΂炭�X���b�h�����Ă��܂���B<br>�܂��̋@��ɂǂ����B�B�B<br><br><a href=http://info.2ch.net/wiki/index.php?BELucky>�X�����ċK�����</a><br><br>$GB->{FORM}->{'FROM'} ($tatetate)");
	}
	# ���X�����ă��~�b�^�[
	# ��~ by FOX
	# news �ȊO�ėL���� by �� 2006/8/3
	# ��~ by FOX �t���Ǝv�� news �������߂Ȃ̂� 2007/4/8
	# news �͌�����
#	if($GB->{FORM}->{'bbs'} eq 'news')
	{
		if($GB->{MARU})
		{
			# ���ł̒P�ʎ��Ԃ�����̃X�����Đ��𒲂ׁA
			# �������ŋK�萔�ȏゾ������A�X�����Ă͂��f�肷��
	
			my $tcount = $FOX->{KUROMARUTCOUNT};# �f�t�H���g�l(6)
	
			#�ȉ��̃T�[�o�E�ł͏��Ȃ�����
#			if($GB->{FORM}->{bbs} eq 'news')	{ $tcount = 3; }
			if(&mumumuKuromaruSuretateCount($GB, $tcount))
			{
				&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F���ŃX���b�h���ĉ߂��ł��B�܂��ɂ��Ă��������B");
			}
		}
	}
	# ���߂�Ȃ������~�b�^�[
	if (&mumumuThreadNumExceededCheck($GB))
	{
		#�X���b�h����������ꍇ�A�X�����Ă����f�肷��
		&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F���̔͍��X���b�h�吙�ł��B���߂�Ȃ����B");
	}

	# �����܂ŗ�����X���[
	return 0;
}
#############################################################################
# ���X�A���J�[�������N�ɂ���
#############################################################################
sub ResAnchor
{
	my ($GB) = @_;

	# >>nnn
	$GB->{FORM}->{'MESSAGE'} =~ s/&gt;&gt;([0-9]+)(?![-\d])/<a href="..\/test\/read.cgi\/$GB->{FORM}->{'bbs'}\/$GB->{FORM}->{'key'}\/$1" target="_blank">&gt;&gt;$1<\/a>/g;
	# >>nnn-nnn
	$GB->{FORM}->{'MESSAGE'} =~ s/&gt;&gt;([0-9]+)\-([0-9]+)/<a href="..\/test\/read.cgi\/$GB->{FORM}->{'bbs'}\/$GB->{FORM}->{'key'}\/$1-$2" target="_blank">&gt;&gt;$1-$2<\/a>/g;

	# �����̌���1.2�{�𒴂����炾��(�L���b�v�̓X���[)
	if(!$GB->{CAP})
	{
		if(length($GB->{FORM}->{'MESSAGE'}) > ($FOX->{$GB->{FORM}->{bbs}}->{"BBS_MESSAGE_COUNT"} * 1.2)){
			&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�{�����������܂��I");
		}
	}

	return 0;
}
#############################################################################
# BE�p�̕�������쐬����
# ������ĂԂ��Ƃɂ��A$GB->{xBE} �����������
#############################################################################
sub MakeBEString
{
	my ($GB) = @_;


	my $user_status = $GB->{BEelite};
	my $user_points_mark = '';
	my $xxx         = $GB->{BExxx}	;

	my $ppp         = $GB->{BEpoints};

	# BE�����N�ɉ����� # �}�[�N�̑Ή������
	#if($user_status    eq "SOL")	{ $user_points_mark = 'S<font color=red>��</font>'; }
	if($user_status    eq "SOL")	{ $user_points_mark = 'S��'; }
	elsif($user_status eq "DIA")	{ $user_points_mark = $user_status; }
	elsif($user_status eq "PLT")	{ $user_points_mark = $user_status; }
	elsif($user_status eq "BRZ")	{ $user_points_mark = $user_status; }
	else				{ $user_points_mark = $user_status; }


	if($user_points_mark ne '')
	{
		$GB->{xBE} = " BE:$xxx-$user_points_mark($ppp)";
	}

	# �u�|�C���g���T�v�̕\��
	if($FOX->{$GB->{FORM}->{bbs}}->{"BBS_BE_TYPE2"} && $GB->{NEWTHREAD})
	{
		# news poverty ����
		if($GB->{FORM}->{'bbs'} eq 'news' || $GB->{FORM}->{'bbs'} eq 'poverty')
		{
			if($GB->{BELucky})
			{
				$GB->{xBE} .= " �|�C���g���T";
			}
		}
	}

	# heaven4vip�͓��ʏ���(BE�o���Ȃ�)
	if($GB->{FORM}->{bbs} eq 'heaven4vip')	{$GB->{xBE} = "";}

	#�X�����Ď��̓X�e���X���Ȃ��Abe�������Ⴄ
	if($GB->{NEWTHREAD} && $GB->{FORM}->{bbs} eq 'news')
	{
		$GB->{NINNIN} = 0	;
	}
	#����D�҃v�`
	if($GB->{KABUUP})
	{
	    if($GB->{NINNIN} && !$FOX->{$GB->{FORM}->{bbs}}->{'BBS_BE_ID'})
	    {
			$GB->{xBE} = "";
	    }
	    else
	    {
		$GB->{xBE} .= " $GB->{KABUX}";
	    }
		return 1;
	}

	if($GB->{KABUU})
	{
#		$GB->{xBE} = ""			;
		if($GB->{NEWTHREAD})
		{
			$GB->{xBE} .= " $GB->{KABUX}";
		}
		else
		{
		    if($GB->{NINNIN} && !$FOX->{$GB->{FORM}->{bbs}}->{'BBS_BE_ID'})
		    {
			$GB->{xBE} = "";
		    }
		}
		return 1;
	}

	return 0;
}
########################################################################
# PC/�g��/���ۂ�/p2/�g�їp�u���E�U ���ʃ}�[�N�̏���
# �߂�l: ���ʃ}�[�N "" "0" "O" "o" "P" "Q"
########################################################################
sub ShikibetsuMark
{
	my ($GB) = @_;

	# BBS_SLIP=checked �ł͂Ȃ��ꍇ�͂Ȃ�
	if(!$FOX->{$GB->{FORM}->{'bbs'}}->{BBS_SLIP})	{ return ""; }

	# �����@iPhone
	# iPhone 3G�o�R�AIP�A�h���X�Ŕ��f
	if(&IsIP4iPhone($ENV{'REMOTE_ADDR'}))		{ return "i"; }
	# iPhone Wifi�o�R�A�Ƃ肠����UA�Ŕ��f�A�U�������͍̂��̂Ƃ���d���Ȃ�
	if($ENV{'HTTP_USER_AGENT'} =~ /iPhone/)		{ return "I"; }

	# �����@Docomo ��$ENV{HTTP_X_DCMGUID}
#	if($GB->{KEITAI} eq 1)
#	{
#		if($ENV{HTTP_X_DCMGUID})
#		{
#			return "I";
#		}
#		return "i";
#	}

	# �g�т� O
	if($GB->{KEITAI})		{ return "O"; }
	# ����p2�� P
	if($GB->{P22CH})		{ return "P"; }
	# AIR-EDGE PHONE�Z���^�[�o�R�̖��ۂ�� o
	if(&mumumuIsAjipon($ENV{'REMOTE_ADDR'}))
					{ return "o"; }
	# �g�їp�u���E�U�� Q
	if($GB->{KEITAIBROWSER})	{ return "Q"; }

	# ��L�̂�����ł��Ȃ����̂� 0
	return "0";
}
#############################################################################
# ID�̂Ƃ���ɕ\�����镶����ƁA���@��̈��̎���쐬����
# ID�̂Ƃ���ɕ\�����镶����� $GB->{xID} �Ɋi�[����A
# ���@��̈��� $GB->{LOGDAT} �Ɋi�[�����
#############################################################################
sub MakeIdStringAndLogdat
{
	my ($GB) = @_;

	#ID�𐶐�����
	my $idcrypt = undef;

	#IPv6�ł́u��48�v�Ɓu��64�v�Ɓu�S128�v���琶������24����ID
	if ($GB->{IPv6})
	{
		use Net::IP;
		my $ip = new Net::IP($ENV{REMOTE_ADDR});
		my $ip_number = $ip->intip();
		# ��48bit
		my $ip_number_h = $ip_number >> 80;
		# ��64bit
		my $ip_number_m = $ip_number >> 64;

		my $idcrypt_h = &foxGetMD5id(
			$GB->{FORM}->{'bbs'},				#bbs
			$GB->{MD5DATE},					#���t
			$FOX->{$GB->{FORM}->{'bbs'}}->{MD5NUMBER},	#
			$ip_number_h					#
		)	;
		my $idcrypt_m = &foxGetMD5id(
			$GB->{FORM}->{'bbs'},				#bbs
			$GB->{MD5DATE},					#���t
			$FOX->{$GB->{FORM}->{'bbs'}}->{MD5NUMBER},	#
			$ip_number_m					#
		)	;
		my $idcrypt_f = &foxGetMD5id(
			$GB->{FORM}->{'bbs'},				#bbs
			$GB->{MD5DATE},					#���t
			$FOX->{$GB->{FORM}->{'bbs'}}->{MD5NUMBER},	#
			$ip_number					#
		)	;
		$idcrypt = $idcrypt_h . '_' . $idcrypt_m . '_' . $idcrypt_f;
	}
	else
	{
		$idcrypt = &foxGetMD5id(
			$GB->{FORM}->{'bbs'},				#bbs
			$GB->{MD5DATE},					#���t
			$FOX->{$GB->{FORM}->{'bbs'}}->{MD5NUMBER},	#
			$GB->{IDNOTANE}					#
		)	;
	}

	#siberia�ŕ\������IP�A�h���X
	my $ipipip = $ENV{REMOTE_ADDR};	#$GB->{HOST29};
	#���ʃ}�[�N�𓾂� (O o P Q 0)
	my $baribari = &ShikibetsuMark($GB);

	#ID�p����������
	# siberia�͔��M��IP�A�h���X��\��
#	if($GB->{FORM}->{'bbs'} eq "siberia")
	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_DISP_IP'} eq "siberia")
	{
		$GB->{xID} = "���M��:$ipipip $baribari";
	}
	elsif($FOX->{$GB->{FORM}->{bbs}}->{'BBS_DISP_IP'} eq "sakhalin")
	{
		$GB->{xID} = "���M��:$ipipip $baribari";
		if($GB->{P22CH})	{$GB->{xID} = "���M��:$ipipip ($GB->{IDNOTANE}) $baribari";}
		if($GB->{KEITAI})	{$GB->{xID} = "���M��:$ipipip ($GB->{IDNOTANE}) $baribari";}
		if($GB->{CAP})		{$GB->{xID} = "���M��:??? $baribari";}
	}
	# ID�Ȃ��̔�
	elsif($FOX->{$GB->{FORM}->{bbs}}->{'BBS_NO_ID'} eq "checked")
	{
		$GB->{xID} = "$baribari";
	}
	# �L���b�v�Ńg���b�N�o�b�N����Ȃ��ꍇ��ID:???
	elsif($GB->{CAP} && !$GB->{TBACK})
	{
		$GB->{xID} = "ID:???$baribari";
	}
	# ����ID�̔�
	elsif($FOX->{$GB->{FORM}->{bbs}}->{'BBS_FORCE_ID'} eq "checked")
	{
		$GB->{xID} = "ID:$idcrypt$baribari";
	}
	# �C��ID�̔̓��[�������󂶂�Ȃ�����ID:???
	elsif($GB->{FORM}->{'mail'} ne "")
	{
		$GB->{xID} = "ID:???$baribari";
	}
	# �C��ID�̔Ń��[��������
	else
	{
		$GB->{xID} = "ID:$idcrypt$baribari";
	}

	# BE_TYPE2�̔ł́A���łȂ����݂̐V�X�����ɂ́��}�[�N����
	if($FOX->{$GB->{FORM}->{bbs}}->{"BBS_BE_TYPE2"} && $GB->{NEWTHREAD})
	{
		if($GB->{MARU} && !$GB->{CAP})
		{
			$GB->{xID} .= "��";
		}
	}

	# ���̏���
	if($GB->{FORM}->{'mail'} =~ /\!stock/)
	{
		my $ksu = &foxGetKabusu($GB,$GB->{FORM}->{'bbs'})	;
		if($ksu > 0)
		{
			$GB->{FORM}->{'mail'} =~ s/\!stock//	;
			my $kbkb = "��";
			if   ($ksu >= 300)	{$kbkb="�_";}
			elsif($ksu >= 119)	{$kbkb="��";}
			elsif($ksu >= 109)	{$kbkb="�~";}
			elsif($ksu >= 99)	{$kbkb="��";}
			elsif($ksu >= 90)	{$kbkb="��";}
			elsif($ksu >= 88)	{$kbkb="��";}
			elsif($ksu >= 80)	{$kbkb="�P";}
			elsif($ksu >= 77)	{$kbkb="��";}
			elsif($ksu >= 60)	{$kbkb="��";}
			elsif($ksu >= 40)	{$kbkb="��";}
			elsif($ksu >= 20)	{$kbkb="��";}
			$GB->{xID} = " <a href=\"http://2ch.se/\">$kbkb</a> " . $GB->{xID};
		}
	}

	#if(IsP2($GB))
	#{
	#	$GB->{xID} .= ' P2@';
	#	if($GB->{MARU})
	#	{
	#		$GB->{xID} .= "��$GB->{MARU}";
	#	}
	#	$GB->{xID} .= " $ENV{REMOTE_ADDR}($GB->{HOST})";
	#}

	# vip �L���̃e�X�g&�f�o�b�O
#	my $v931 = "(" . $GB->{V931} . ")";
#	$GB->{xID} .= $v931;
	# ���@��p�̈����
	&MakeLogdat($GB, $idcrypt, $baribari);


#$GB->{xID} .= " DISP_IP=[$FOX->{$GB->{FORM}->{bbs}}->{'BBS_DISP_IP'}]";
	return 0;
}
#############################################################################
# 1���j�b�g���̃��O�t�@�C��(���@��̈�)�����
# ID�Ǝ��ʃ}�[�N���K�v�Ȃ̂ŁAMakeIdStringAndLogdat ����Ă΂�邱�ƂɂȂ�
# ���@��̈��� $GB->{LOGDAT} �Ɋi�[�����
#############################################################################
sub MakeLogdat
{
	my ($GB, $idcrypt, $baribari) = @_;

	# ���@��̈��ɓ����A���b�Z�[�W�̓�30�o�C�g�𒊏o
	my $mss = substr($GB->{FORM}->{'MESSAGE'}, 0, 30);
	$mss =~ s/</&lt;/g; $mss =~ s/>/&gt;/g;

	# 1���j�b�g���̃��O�t�@�C��(���@��̈�)�����
	my $CID = ""	;
	if($ENV{HTTP_X_DCMGUID})	{$CID = "������($ENV{HTTP_X_DCMGUID})������";}


	if($GB->{NEWTHREAD})
	{
		$GB->{LOGDAT} = "$GB->{FORM}->{'FROM'}<>$GB->{FORM}->{'mail'}<>$GB->{DATE} $idcrypt$baribari<>$mss<>$GB->{FORM}->{'subject'}<>$GB->{HOST999}<>$ENV{'REMOTE_ADDR'}<>$GB->{MARU} ($GB->{FORM}->{'MDMD'} $GB->{FORM}->{'DMDM'})<>$ENV{'HTTP_USER_AGENT'}$CID $GB->{BExxx}"; #($ENV{'HTTP_COOKIE'})
	}
	else
	{
		$GB->{LOGDAT} = "$GB->{FORM}->{'FROM'}<>$GB->{FORM}->{'mail'}<>$GB->{DATE} $idcrypt$baribari<>$mss<>$GB->{FORM}->{'subject'}<>$GB->{HOST999}<>$ENV{'REMOTE_ADDR'}<>$GB->{MARU}<>$ENV{'HTTP_USER_AGENT'}$CID $GB->{BExxx}"; #($ENV{'HTTP_COOKIE'})
	}
#	$GB->{LOGDAT} = "$GB->{FORM}->{'FROM'}<>$GB->{FORM}->{'mail'}<>$GB->{DATE} $idcrypt$baribari<>$mss<>$GB->{FORM}->{'subject'}<>$GB->{HOST999}<>$ENV{'REMOTE_ADDR'}<>$GB->{MARU}<>$ENV{'HTTP_USER_AGENT'}"; #($ENV{'HTTP_COOKIE'})
#	$GB->{LOGDAT} = "$GB->{FORM}->{'FROM'}<>$GB->{FORM}->{'mail'}<>$GB->{DATE} $idcrypt$baribari<>$mss<>$GB->{FORM}->{'subject'}<>$GB->{HOST999}<>$ENV{'REMOTE_ADDR'}<>$GB->{MARU}<>$ENV{'HTTP_USER_AGENT'}$CID"; #($ENV{'HTTP_COOKIE'})

	return 0;
}
#############################################################################
# 1���j�b�g����dat�����
#############################################################################
sub MakeOutdat
{
	my ($GB) = @_;
	my $hoshos = "";
#	my $message = $GB->{FORM}->{'MESSAGE'};

#			$message =~ s/sssp\:\/\/img\.2ch\.net\/([\w|\:\!\#\$\%\=\&\-\^\`\\\|\@\~\[\{\]\}\;\+\*\,\.\?\/]+)/<img src="http:\/\/img\.2ch\.net\/$1">/g;

	if(&dispIconSssp($GB))	{$GB->{FORM}->{'MESSAGE'} = 'sssp://img.2ch.net/ico/' . $GB->{icon} .' <br> '. $GB->{FORM}->{'MESSAGE'} ;}


	# 1���j�b�g����dat�����
	$GB->{OUTDAT} = "$GB->{FORM}->{'FROM'}<>$GB->{FORM}->{'mail'}<>$GB->{DATE} $GB->{xID}$GB->{xBE}<> $GB->{FORM}->{'MESSAGE'} <>$GB->{FORM}->{'subject'}";

	# saku/saku2ch/sakud�͓��ꏈ��(HOST: �z�X�g���\���AID�EBE�\���Ȃ�)
	if($GB->{FORM}->{'bbs'} eq "saku" || $GB->{FORM}->{'bbs'} eq "saku2ch" || $GB->{FORM}->{'bbs'} eq "sakud")
	{
		if (!$GB->{CAP})
		{
			$hoshos = $GB->{HOST};
			# �g�тł͌ŗL�ԍ����\������
			if($GB->{KEITAI})
			{
				$hoshos = "$GB->{IDNOTANE} $GB->{HOST}";
			}
			if($GB->{KEITAIBROWSER})
			{
				$hoshos = "$GB->{IDNOTANE} $GB->{HOST}";
			}
			# ����p2�ł̓��[�U�ԍ��� p2-client-ip: �̏����\������
			# foxSetHost�ŁA$GB->{HOST2} �ɓ����Ă���
			elsif($GB->{P22CH})
			{
				$hoshos = "$GB->{IDNOTANE} $GB->{HOST} ($GB->{HOST2})";
			}
			$GB->{OUTDAT} = "$GB->{FORM}->{'FROM'}<>$GB->{FORM}->{'mail'}<>$GB->{DATE} HOST:$hoshos<> $GB->{FORM}->{'MESSAGE'} <>$GB->{FORM}->{'subject'}";
		}
	}

	return 0;
}
#############################################################################
# �X���b�h924�̓��t�X�V����(����)���s��
# ����: 924�X���b�h��dat�t���p�X��
#############################################################################
sub Update924
{
	my ($GB, $DATAFILE) = @_;
	# Perl 5.7.2 �ȍ~�� utime �� undef �ł���
	my $now = $^V lt v5.7.2 ? time : undef;

	# �Ⴞ��܂ł�bbsd��age�̃R�}���h�𑗂�
	if(IsSnowmanServer == BBSD->{REMOTE} || IsSnowmanServer && $GB->{FORM}{mail} !~ /sage/)
	{
		# sage�Ȃ�touch����
		if($GB->{FORM}->{'mail'} =~ /sage/)
		{
			# bbsd �� touch �ł� undef �̑���� 0
			my $cmd = 'touch';
			my $errmsg = bbsd($DATAFILE, $cmd, $now || 0, 'dummy'); 
			# �^�C���A�E�g���ǂ����`�F�b�N
			if(&bbsd_TimeoutCheck($GB, $errmsg))
			{
				&bbsd_TimeoutError($GB, $cmd);
			}
		}
		# age�����ꍇ�Aage��R�}���h�𑗂�
		else
		{
			my $cmd = 'raise';
			my $errmsg = bbsd($GB->{FORM}->{'bbs'}, $cmd, $GB->{FORM}->{'key'}, 'dummy'); 
			# �^�C���A�E�g���ǂ����`�F�b�N
			if(&bbsd_TimeoutCheck($GB, $errmsg))
			{
				&bbsd_TimeoutError($GB, $cmd);
			}
		}
	}
	else
	{
		# dat�t�@�C���ւ̒ǋL���s�킸�Atouch���������{
		# undef �͕ϐ��łȂ����ڋL�q�łȂ��ƃ_��
		utime $now || undef, $now || undef, $DATAFILE;
		# �p�[�~�b�V���������͕s�v
		#chmod(0666, $DATAFILE);
	}

	return 0;
}
#############################################################################
# dat�t�@�C����1�s���ǉ��ŏ�������
# ����: $GB�A�t�@�C�����A�f�[�^1�s��(���s�R�[�h�Ȃ�)�A�t���O
#       �t���O 0: dat�����A1:���O����
#############################################################################
sub WriteDatFile
{
	my ($GB, $filename, $filedata, $flag) = @_;
	use Fcntl; 

	# dat�̏����̏ꍇ�A�V�X���ƃ��X�ŏꍇ����
	if (!$flag)
	{
		# �V�X���̏ꍇ�Adat����������G���[
		if($GB->{NEWTHREAD})
		{
			sysopen(OUT, $filename, O_WRONLY|O_CREAT|O_EXCL, 0666)
			or &DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F��т����Ȃ̂ŁA�܂��̋@��ɂǂ����B�B�B");
		}
		# ���X�̏ꍇ�Adat�ɒǋL�ł��Ȃ�������G���[
		else
		{
			sysopen(OUT, $filename, O_WRONLY|O_APPEND, 0666)
			or &DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F���X���悤�Ƃ�����dat�ɏ����܂���ł����B��dat������������������ł��B");
		}
	}
	else
	# ���O�̏ꍇ�A��ɒǉ����[�h
	{
		sysopen(OUT, $filename, O_WRONLY|O_APPEND|O_CREAT, 0666)
		or &DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F���O�t�@�C���ɏ����܂���ł����B");
	}
	print OUT "$filedata\n";
	close(OUT);
	# �O����umask����sysopen�Ŏw�肵�Ă���̂ŁA�p�[�~�b�V���������͕s�v
	#chmod(0666, $filename);

	return 0;
}
########################################################################
#
########################################################################
#�Q���g���b�v�h�~�������火
sub GeroTrap
{
	my ($GB) = @_	;

	#�ȉ��̔͂���[
	if(&KiseiOFF($GB))			{return 0;}
#	if($GB->{FORM}->{'bbs'} eq "campus")	{return 0;}
	#TBACK�͂���[
	if($GB->{TBACK})			{return 0;}
	#�ȉ��̔͂���[
#	if($GB->{FORM}->{'bbs'} eq "siberia")	{return 0;}
	# �g�сE���ۂ�͂���[
	if(&IsIP4Mobile($ENV{REMOTE_ADDR}))	{return 0;}
	# iPhone�͂���[
	if($ENV{'HTTP_USER_AGENT'} =~ /iPhone/)	{return 0;}
	#���̓X���[
	if($GB->{CAP})				{return 0;}
	#���̓X���[
	if($GB->{MARU})				{return 0;}

	unless(
	    $ENV{'HTTP_REFERER'} eq ''
	 || $ENV{'HTTP_REFERER'} =~ /^http:\/\/[-\w]+\.2ch\.net\//
	 || $ENV{'HTTP_REFERER'} =~ /^http:\/\/\w+\.bbspink\.com\//
	 || $ENV{'HTTP_REFERER'} =~ /^http:\/\/\w+\.ula\.cc\//
	 || $ENV{'HTTP_REFERER'} =~ /^http:\/\/\w+\.u\.la\//
	 || $ENV{'HTTP_REFERER'} =~ /^http:\/\/\w+\.s2ch\.net\//
	 || $ENV{'HTTP_REFERER'} =~ /^http:\/\/orz\.2ch\.io\//
	)
	{
		&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F���Ȃ��x����Ă܂���H");
	}
	if($ENV{'HTTP_REFERER'} eq '')
	{
		&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F���t�@�����炢�����Ă�������");
	}
	return 0;
}
#�������܂�
#############################################################################
# �g�т������łȂ������`�F�b�N����
# 0: �g��/AIR-EDGE�̖��ۂ�ȊO�A1: i���[�h�A2: EZweb�A3: �{�[�_�t�H��!���C�u
# 4: AIR-EDGE PHONE�Z���^�[�o�R�̖��ۂ�
# 5: emobile EMnet
#############################################################################
sub IsIP4Mobile
{
	my ($raddr) = @_;

	# i���[�h
	if(&mumumuIsIP4IMode($raddr))		{ return 1; }
	# EZweb
	elsif(&mumumuIsIP4EZWeb($raddr))	{ return 2; }
	# Vodafone!���C�u
	elsif(&mumumuIsIP4Vodafone($raddr))	{ return 3; }
	# AIR-EDGE PHONE�Z���^�[�o�R�̖��ۂ�
	elsif(&mumumuIsAjipon($raddr))		{ return 4; }
	# emobile EMnet
	elsif(&mumumuIsIP4EMnet($raddr))	{ return 5; }
	# ��L�̂ǂ�ł��Ȃ�
	else					{ return 0; }
}
#############################################################################
# iPhone��IP�A�h���X���ǂ����`�F�b�N����
#############################################################################
sub IsIP4iPhone
{
	my ($raddr) = @_;

	# CIDR���X�g�ɊY�������邩�ǂ����`�F�b�N����
	return $FOX->{IPHONECIDR}->find($raddr);
}
#############################################################################
# i���[�h�Z���^��IP�A�h���X���ǂ����`�F�b�N����
#############################################################################
sub mumumuIsIP4IMode
{
	my ($raddr) = @_;

	# CIDR���X�g�ɊY�������邩�ǂ����`�F�b�N����
	return $FOX->{IMODECIDR}->find($raddr);
}
#############################################################################
# EZ�T�[�o��IP�A�h���X���ǂ����`�F�b�N����
#############################################################################
sub mumumuIsIP4EZWeb
{
	my ($raddr) = @_;

	# CIDR���X�g�ɊY�������邩�ǂ����`�F�b�N����
	return $FOX->{EZWEBCIDR}->find($raddr);
}
#############################################################################
# �{�[�_�t�H�����C�u�I�T�[�o��IP�A�h���X���ǂ����`�F�b�N����
#############################################################################
sub mumumuIsIP4Vodafone
{
	my ($raddr) = @_;

	# CIDR���X�g�ɊY�������邩�ǂ����`�F�b�N����
	return $FOX->{SOFTBANKCIDR}->find($raddr);
}
#############################################################################
# emobile EMnet��IP�A�h���X���ǂ����`�F�b�N����
#############################################################################
sub mumumuIsIP4EMnet
{
	my ($raddr) = @_;

	# CIDR���X�g�ɊY�������邩�ǂ����`�F�b�N����
	return $FOX->{EMNETCIDR}->find($raddr);
}
#############################################################################
# AIR-EDGE PHONE�Z���^�[��IP�A�h���X���ǂ����`�F�b�N����
#############################################################################
sub mumumuIsIP4AirEdgePhone
{
	my ($raddr) = @_;

	# CIDR���X�g�ɊY�������邩�ǂ����`�F�b�N����
	return $FOX->{AIREDGECIDR}->find($raddr);
}
#############################################################################
# AIR-EDGE MEGAPLUS��IP�A�h���X���ǂ����`�F�b�N����
#############################################################################
sub mumumuIsIP4MegaPlus
{
	my ($raddr) = @_;

	# CIDR���X�g�ɊY�������邩�ǂ����`�F�b�N����
	return $FOX->{MEGAPLUSCIDR}->find($raddr);
}
#############################################################################
# AIR-EDGE PHONE�Z���^�[�o�R�̖��ۂ񂩂ǂ������ׂ�
# AIR-EDGE PHONE�Z���^�[����̐ڑ��Ń��t�@�����Ȃ��ꍇ�ɂ̂ݐ^
#############################################################################
sub mumumuIsAjipon
{
	my ($raddr) = @_;

	if(&mumumuIsIP4AirEdgePhone($raddr) &&
	   $ENV{'HTTP_REFERER'} eq '')	{return 1;}
	else				{return 0;}
}
#############################################################################
# ����p2��IP�A�h���X���ǂ����`�F�b�N����
#############################################################################
sub mumumuIsIP4P22ch
{
	my ($raddr) = @_;
	our @P22chIPAddrs;
	BEGIN {
		# IP�A�h���X�ɕω�����������A������ҏW����
		@P22chIPAddrs = map { local $_ = $_; s/\./\\./g; qr/$_/; }
			( "210.135.100.132", "210.135.98.43",
			  "210.135.99.5",  "210.135.99.6" );
	}

	foreach(@P22chIPAddrs)
	{
		if($raddr =~ $_)	{return 1;}
	}
	return 0;
}
#############################################################################
# ���肪�g�їp�u���E�U���ǂ����`�F�b�N����
# 0: �g�їp�u���E�U����Ȃ�
# 1: ibisBrowser
# 2: jig Browser
# 3: SoftBank PC�T�C�g�u���E�U
# 4: docomo �t���u���E�U
# 5: au PC�T�C�g�r���[�A�[
# ...
#############################################################################
sub mumumuIsKeitaiBrowser
{
	my ($GB) = @_;
	my $raddr = $ENV{'REMOTE_ADDR'};

	# ibisBrowser
	if(&mumumuIsIP4ibisBrowser($raddr))	{return 1;}

	# jig Browser
	if(&mumumuIsIP4jigBrowser($raddr))	{return 2;}

	# ��W�F���k���񂩂�̎w�߂ɂ��Anewservant�������̃`�F�b�N�����Ȃ�
	if($GB->{FORM}->{'bbs'} ne "newservant")
	{
		# SoftBank PC�T�C�g�u���E�U
		if(&mumumuIsIP4pcsiteBrowser($raddr))	{return 3;}
	}

	# docomo�t���u���E�U
	if(&mumumuIsIP4imodefullBrowser($raddr))	{return 4;}

	# au PC�T�C�g�r���[�A�[
	if(&mumumuIsIP4pcsiteViewer($raddr))	{return 5;}

	# ��L�̂ǂ�ł��Ȃ�
	return 0;
}
#############################################################################
# ibisBrowser (one of �g�їp�t���u���E�U)��IP�A�h���X���ǂ����`�F�b�N����
#############################################################################
sub mumumuIsIP4ibisBrowser
{
	my ($raddr) = @_;

	# CIDR���X�g�ɊY�������邩�ǂ����`�F�b�N����
	return $FOX->{IBISBROWSERCIDR}->find($raddr);
}
#############################################################################
# jigBrowser (one of �g�їp�t���u���E�U)��IP�A�h���X���ǂ����`�F�b�N����
#############################################################################
sub mumumuIsIP4jigBrowser
{
	my ($raddr) = @_;

	# CIDR���X�g�ɊY�������邩�ǂ����`�F�b�N����
	return $FOX->{JIGBROWSERCIDR}->find($raddr);
}
#############################################################################
# PC�T�C�g�u���E�U (�\�t�g�o���N�g�уt���u���E�U)��IP�A�h���X���ǂ���
#############################################################################
sub mumumuIsIP4pcsiteBrowser
{
	my ($raddr) = @_;

	# CIDR���X�g�ɊY�������邩�ǂ����`�F�b�N����
	return $FOX->{PCSITEBROWSERCIDR}->find($raddr);
}
#############################################################################
# �t���u���E�U (�h�R���g�уt���u���E�U)��IP�A�h���X���ǂ���
#############################################################################
sub mumumuIsIP4imodefullBrowser
{
	my ($raddr) = @_;

	# CIDR���X�g�ɊY�������邩�ǂ����`�F�b�N����
	return $FOX->{IMODEFULLBROWSERCIDR}->find($raddr);
}
#############################################################################
# PC�T�C�g�r���[�A�[ (au�g�уt���u���E�U)��IP�A�h���X���ǂ���
#############################################################################
sub mumumuIsIP4pcsiteViewer
{
	my ($raddr) = @_;

	# CIDR���X�g�ɊY�������邩�ǂ����`�F�b�N����
	return $FOX->{PCSITEVIEWERCIDR}->find($raddr);
}
#############################################################################
#
#############################################################################
sub checkPragma
{
	my ($GB) = @_	;
	#�ȉ��̔͂���[
	if(&KiseiOFF($GB))			{return 0;}
	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_4WORLD'} eq "checked")	{return 0;}

	#�g�т̓X���[
	if($GB->{KEITAI})			{return 0;}
	if($GB->{KEITAIBROWSER})		{return 0;}
	#AIR-EDGE PHONE�Z���^�[����̐ڑ��̓X���[
	if(&mumumuIsIP4AirEdgePhone($ENV{'REMOTE_ADDR'}))	{return 0;}
	#news�̓X���[
	if($GB->{FORM}->{'bbs'} eq "news")	{return 0;}
	#operate/sec2chd�̓X���[
	if($GB->{FORM}->{'bbs'} eq "operate")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "sec2chd")	{return 0;}
	#���̓X���[
	if($GB->{CAP})				{return 0;}
	#���̓X���[
	if($GB->{MARU})				{return 0;}
	#mac �̓X���[
	if($ENV{HTTP_USER_AGENT} =~ /PDA/)		{return 0;}
	if($ENV{HTTP_USER_AGENT} =~ /Mac/)		{return 0;}
	if($ENV{HTTP_USER_AGENT} =~ /^Monazilla\/1/)	{return 0;}
	if($ENV{HTTP_ACCEPT_LANGUAGE} =~ /ja/)		{return 0;}
	#NetFront�� Pragma: ��f���ė��Ȃ�
	if($ENV{HTTP_USER_AGENT} =~ /NetFront/)		{return 0;}

	if($ENV{HTTP_PRAGMA})
	{
		&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�u���E�U�ςł����B$ENV{'HTTP_REFERER'}");
	}
}
#############################################################################
#
#############################################################################
sub ToolGekitai0
{
	my ($GB) = @_	;
	my $span = $FOX->{$GB->{FORM}->{'bbs'}}->{SAMBA24}	;

	#�ȉ��̔̓X���[
	if(&KiseiOFF($GB))			{return 0;}
#	if($GB->{FORM}->{'bbs'} eq "campus")	{return 0;}

	if(&IsIP4Mobile($ENV{REMOTE_ADDR}))
				{$span += $FOX->{SambaOffset_KEITAI}	;}
	if($GB->{P22CH})	{$span += $FOX->{SambaOffset_P22CH}	;}

	$GB->{version} .= " +Samba24="		;
	$GB->{version} .= $FOX->{$GB->{FORM}->{'bbs'}}->{SAMBA24};

	#���Ńg���b�N�o�b�N����Ȃ����̓X���[
	if($GB->{CAP} && !$GB->{TBACK})		{return 0;}
	#���̓X���[ => ���͐�p��samba
	if($GB->{MARU})
	{
		&foxViva($GB,$GB->{MARU})	;
		return 0;
	}

	my $tane = $ENV{'REMOTE_ADDR'}	;
	if($GB->{KEITAI} eq 1)	{$tane = $GB->{IDNOTANE};}
	if($GB->{KEITAI} eq 2)	{$tane = $GB->{IDNOTANE};}
	if($GB->{KEITAI} eq 3)	{$tane = $GB->{IDNOTANE};}
	if($GB->{KEITAI} eq 5)	{$tane = $GB->{IDNOTANE};}
	if($GB->{KEITAIBROWSER}) {$tane = $GB->{IDNOTANE};}
	if($GB->{P22CH})	{$tane = $GB->{IDNOTANE};}
	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_PROXY_CHECK'} && $GB->{BURNEDPROXY} eq 1)	{$tane = "burned";}

	&foxSamba24($GB, $tane, $span)	;
}
#############################################################################
#
#############################################################################
sub CheckDomain
{
	my ($GB) = @_	;
	my $remo = $GB->{HOST29}	; #�����郊���z
	my $ita  = $GB->{FORM}->{bbs}	;

#	&DispError2($GB,"�d�q�q�n�q�I","�C�O�h���C���K��($ita)�B");

	if($GB->{KEITAI})		{return 1;}
	if($GB->{KEITAIBROWSER})	{return 1;}
	if($ita eq 'accuse')		{return 1;}
	if($ita eq 'siberia')		{return 1;}
	if($ita eq 'world')		{return 1;}
	if($ita eq 'northa')		{return 1;}

	if($ita eq 'oversea')		{return 1;}
	if($ita eq 'wine')		{return 1;}
	if($ita eq 'bizplus')		{return 1;}
	if($ita eq 'comic')		{return 1;}
	if($ita eq 'bicycle')		{return 1;}
	if($ita eq 'airline')		{return 1;}
	if($ita eq 'baby')		{return 1;}
	if($ita eq 'space')		{return 1;}
	if($ita eq 'life')		{return 1;}
	if($ita eq 'news2')		{return 1;}
	if($ita eq 'newsplus')		{return 1;}
	if($ita eq 'sake')		{return 1;}
	if($ita eq 'ski')		{return 1;}

	if($ita eq 'operate2')		{return 1;}
	if($FOX->{$ita}->{'BBS_4WORLD'} eq "checked")
					{return 1;}

#	&DispError2($GB,"�d�q�q�n�q�I","�C�O�h���C���K��($remo)�B");
	if($remo =~ /\.jp$/)		{return 1;}
	if($remo =~ /awaikeda\.com$/)	{return 1;}
	if($remo =~ /ccccc5\.com$/)	{return 1;}
	if($remo =~ /cty8\.com$/)	{return 1;}
	if($remo =~ /george24\.com$/)	{return 1;}
	if($remo =~ /ja-hc\.com$/)	{return 1;}
	if($remo =~ /kaga-tv\.com$/)	{return 1;}
	if($remo =~ /nasicnet\.com$/)	{return 1;}
	if($remo =~ /quolia\.com$/)	{return 1;}
	if($remo =~ /tigers-net\.com$/)	{return 1;}
	if($remo =~ /tonotv\.com$/)	{return 1;}
	if($remo =~ /e-sadonet\.tv$/)	{return 1;}
	if($remo =~ /shimanto\.tv$/)	{return 1;}
	if($remo =~ /telenet\.tv$/)	{return 1;}

	my @cDom = ('ro','to','us','hr','at','biz','be','lt','ca','uk','fr','ma','nu','mx','bg','se','cz','co','pt','by','ar','br','it','ru','il','nl','cl','in','info','asia','name','tv','th','hu','pl','es');
	foreach(@cDom)
	{
		my $dom = $_			;
		my $dxx = '\.' . $_ . '$'	;
		if($remo =~ /$dxx/i)	{&DispError2($GB,"�d�q�q�n�q�I","�C�O�h���C���K��($dom)�B<a href=\"http://2ch.tora3.net/\">�Q�����˂�r���[�A</a>���g���Ə������߂܂��B");}
	}

	return 0	;
}
#############################################################################
#
#############################################################################
sub checkDenyList
{
	my ($GB) = @_	;
	my $pxck;

	#�ȉ��̔̓X���[
	if(&KiseiOFF($GB))			{return 0;}
	if($GB->{FORM}->{'bbs'} eq "pinknanmin"){return 0;}
	if($GB->{FORM}->{'bbs'} eq "servant")	{return 0;}
#	if($GB->{FORM}->{'bbs'} eq "campus")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "trafficinfo" && $GB->{KEITAI})	{return 0;}

	#���̓X���[
	if($GB->{CAP})				{return 0;}

	#���̔���
	if($GB->{MARU})
	{
		my @PIP = @FOX_K998	;
		#���K�����X�g�`�F�b�N
		foreach(@PIP)
		{
			chomp		;
			if(/^\#/)	{next;}
			if(eval { $GB->{MARU} =~ /$_/; })
			{
				# operate2/sec2chd�ł́���ID���G���[�\������
				if($GB->{FORM}->{'bbs'} eq "operate2" ||
				   $GB->{FORM}->{'bbs'} eq "housekeeping" ||
				   $GB->{FORM}->{'bbs'} eq "sec2chd")
				{
#					return 0;
					&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�A�N�Z�X�K�����ł��I�I(��=$GB->{MARU})");
				}
				else
				{
					&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�A�N�Z�X�K�����ł��I�I(��)");
				}
			}
		}
		#�K�����X�g�ɍڂ��Ă��Ȃ����̓X���[
		return 0;
	}

	#p2�K��
	if($ENV{'REMOTE_ADDR'} =~ /^61\.165\./)		{&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�A�N�Z�X�K�����ł��I�I(9)");}
	if($ENV{'REMOTE_ADDR'} =~ /^202\.181\.96\./)	{&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�A�N�Z�X�K�����ł��I�I(9)");}
	if($ENV{'REMOTE_ADDR'} =~ /^202\.222\.16\./)	{&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�A�N�Z�X�K�����ł��I�I(9)");}
	if($ENV{'REMOTE_ADDR'} =~ /^21\.240\./)		{&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�A�N�Z�X�K�����ł��I�I(9)");}
	if($ENV{'REMOTE_ADDR'} =~ /^69\.56\./)		{&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�A�N�Z�X�K�����ł��I�I(9)");}
	if($ENV{'REMOTE_ADDR'} =~ /^211\.8\.35\./)	{&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�A�N�Z�X�K�����ł��I�I(9)");}

	#�폜�n�̔́��`�F�b�N��̓X���[
	if($GB->{FORM}->{'bbs'} eq "saku")	{return 0;}
#	if($GB->{FORM}->{'bbs'} eq "sakud")	{return 0;}
#	if($GB->{FORM}->{'bbs'} eq "saku2ch")	{return 0;}
	#�ꕔ�̔̓X���[
#	if($ENV{'SERVER_NAME'} =~ /hayabusa/)	{return 0;}
#	if($GB->{FORM}->{'bbs'} eq "news")	{return 0;}
#	if($GB->{FORM}->{'bbs'} eq "neet4pink")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "siberia")	{return 0;}
#	if($GB->{FORM}->{'bbs'} eq "liveplus")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "liveanime")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "dejima")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "senji")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "operate2")	{return 0;}

	#???
	if($GB->{HOST4} eq '')
	{
		&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F���͏����܂���B");
	}

	#�g�шȊO�̓����z�̕�������`�F�b�N
	if(!($GB->{KEITAI} || $GB->{KEITAIBROWSER}))
	{
		if($GB->{HOST999} =~ /proxy/)	{&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�ςȃz�X�g�K�����I�I�@�ςȃz�X�g�ł��B");}
		if($GB->{HOST999} =~ /cache/)	{&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�ςȃz�X�g�K�����I�I�@�ςȃz�X�g�ł��B");}
		if($GB->{HOST999} =~ /^tor\./)	{&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�ςȃz�X�g�K�����I�I�@�ςȃz�X�g�ł��B");}
		if($GB->{HOST999} =~ /^tor\d+\./)	{&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�ςȃz�X�g�K�����I�I�@�ςȃz�X�g�ł��B");}
#		if($GB->{HOST999} =~ /^gw/)	{&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�ςȃz�X�g�K�����I�I�@�ςȃz�X�g�ł��B");}
	}
	#�C�O�h���C���K��
	&CheckDomain($GB)		;

	#�������݋��ۃ��X�g�Ŕ���
	my @PIP = @FOX_K999		;
	foreach(@PIP)
	{
		chomp;
		if($_ eq '')	{next;}
		if(/^\#/)	{next;}
		if(/^_2CH_/)
		{
			if($ENV{'SERVER_NAME'} !~ /2ch.net/)	{next;}
			s/^_2CH_//	;
		}
		if(/^_PINK_/)
		{
			if($ENV{'SERVER_NAME'} !~ /bbspink.com/)	{next;}
			s/^_PINK_//	;
		}
		if(/^_BBS_(\S+)_/)
		{
#&DispError2($GB,"�d�q�q�n�q�I","BBS = [$1]");
			if($GB->{FORM}->{'bbs'} ne $1)	{next;}
			s/^_BBS_\S+_//	;
		}
		if(/^_SRV_(\S+)_/)
		{
			if($ENV{'SERVER_NAME'} !~ $1)	{next;}
			s/^_SRV_\S+_//	;
		}
		if(/^_HANA_/)
		{
			if(IsSenmon($GB))		{next;}
			s/^_HANA_//	;
		}
$GB->{DEBUG} .= "���X�g�Ŕ��� ($_) <br>";
		# �啶����������ʂ���̂Œ���
		if(eval { $GB->{HOST999} =~ /$_/; })
		{# ���X�g�ɂ�����
			# ���ۂ��}�[�N������t���O
			my $deniedmark = 0;

			# accuse/operate/sec2chd �� fusianasan ���Ă�
			# �V�X���ł͂Ȃ��ꍇ�́A�A�A
			if($GB->{FORM}->{'bbs'} eq "accuse"  && $GB->{FORM}->{'FROM'} =~ /$GB->{HOST}/ && $GB->{FORM}->{'subject'} eq "") { $deniedmark = 1; }
			if($GB->{FORM}->{'bbs'} eq "operate" && $GB->{FORM}->{'FROM'} =~ /$GB->{HOST}/ && $GB->{FORM}->{'subject'} eq "") { $deniedmark = 1; }
#			if($GB->{FORM}->{'bbs'} eq "operate2" && $GB->{FORM}->{'FROM'} =~ /$GB->{HOST}/ && $GB->{FORM}->{'subject'} eq "") { $deniedmark = 1; }
#if($GB->{HOST999} =~ /ocn\.ne\.jp/)
if($GB->{HOST999} =~ /xxx\.ne\.jp/)
{
			if($GB->{FORM}->{'bbs'} eq "siberia") { $deniedmark = 0; }
			if($GB->{FORM}->{'bbs'} eq "sec2chd") { $deniedmark = 0; }
			if($GB->{FORM}->{'bbs'} eq "accuse") { $deniedmark = 0; }
}
			# ���ۂ��}�[�N�����������ŏ������݂�������
			if($deniedmark)
			{
				# [�\{}@{}@{}-] �ƈꏏ�ɏo�鎞��
				# ���������Ă���悤�ɂ���
				if($GB->{BURNEDPROXY})
				{
					$GB->{FORM}->{'FROM'} = ' </b>�S[�L�E�ցE�M]�|<b> ' . $GB->{FORM}->{'FROM'};
				}
				else
				{
					$GB->{FORM}->{'FROM'} = ' </b>[�L�E�ցE�M]<b> ' . $GB->{FORM}->{'FROM'};
				}
				return 1;
			}
			else
			{
				# ��L�̂��̈ȊO�̓G���[
				&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�A�N�Z�X�K�����ł��I�I($_)<br><a href=\"http://qb5.2ch.net/sec2chd/\">�����ō��m����Ă��܂��B</a>");
			}
		}
	}
#&DispError2($GB,"FOX ��","<font color=green>FOX ��</font>�@�ǂ�<br>");
	return	1;
}
#############################################################################
#
#############################################################################
sub foxMARUsuru
{
	my ($GB) = @_	;

	if(!$GB->{MARU})			{return 0;}
	if($GB->{MARU} eq $FOX->{OTAMESHIMARU})	{return 0;}

	if($GB->{NEWTHREAD})
	{#�X�����Ď��́��ł��`�F�b�N
		if($ENV{'SERVER_NAME'} =~ /qb/)
		{#qb�n
			return 0;
		}
		else
		{#qb�n�ȊO
			return 1;	#���ŃX���[�������Ă݂�
		}
	}
	else
	{#���X���́��ł���[
		return 1;
	}
	return 0	;
}
sub checkProxyAtAll
{
	my ($GB) = @_	;

	# news4vip�ł�BBQ�L��(�C�I�i�Y���΍�)
	#if($ENV{'SERVER_NAME'} =~ /bbspink/)	{return 0;}
	#if($GB->{FORM}->{'bbs'} eq "news4vip")	{return 0;}
	#if($GB->{FORM}->{'bbs'} eq "news")	{return 0;}
	#if($GB->{FORM}->{'bbs'} eq "campus")	{return 0;}

	# IPv6���ł�BBQ��(�܂�)�Ȃ�
	if($GB->{IPv6})				{return 0;}

	# BBQ�����version�ɒǉ�
	$GB->{version} .= " +<a href=\"http://bbq.uso800.net/\">BBQ</a>";

	# BBQ �ɕ����Ă݂�
	$GB->{BURNEDPROXY} = &checkProxyList($GB)		;

	# ����p2�ł�Proxy�̎��͑S�˂��܂���BBQ�X���[
	# http://qb5.2ch.net/test/read.cgi/operate/1202007319/757-768
	if($GB->{P22CH} && $GB->{BURNEDPROXY})
	{
		$GB->{FORM}->{'FROM'} = ' </b>[�\{}@{}@{}-]<b> ' . $GB->{FORM}->{'FROM'};
		return 0;
	}

	# ����̔ł͂˂��܂�����
	if($GB->{FORM}->{'bbs'} eq "operate2" && $GB->{BURNEDPROXY}) {$GB->{FORM}->{'FROM'} = ' </b>[�\{}@{}@{}-]<b> ' . $GB->{FORM}->{'FROM'};}
	if($GB->{FORM}->{'bbs'} eq "operate" && $GB->{BURNEDPROXY}) {$GB->{FORM}->{'FROM'} = ' </b>[�\{}@{}@{}-]<b> ' . $GB->{FORM}->{'FROM'};}
	if($GB->{FORM}->{'bbs'} eq "sec2chd" && $GB->{BURNEDPROXY}) {$GB->{FORM}->{'FROM'} = ' </b>[�\{}@{}@{}-]<b> ' . $GB->{FORM}->{'FROM'};}
	if($GB->{FORM}->{'bbs'} eq "goki" && $GB->{BURNEDPROXY}) {$GB->{FORM}->{'FROM'} = ' </b>[�\{}@{}@{}-]<b> ' . $GB->{FORM}->{'FROM'};}

	#�ȉ��̔͂���[
	if($GB->{FORM}->{'bbs'} eq "siberia" && !$GB->{NEWTHREAD})
	{
		my $bFile = "../$GB->{FORM}->{'bbs'}/BBQ/index.html";
		if(!(-e $bFile))	{return 0;}
	}
	#���Ńg���b�N�o�b�N����Ȃ����̓X���[
	if($GB->{CAP} && !$GB->{TBACK})			{return 0;}

	#���̓X���[
	#�P�ށ@2010/5/5
	#if(&foxMARUsuru($GB) && !$GB->{NEWTHREAD})	{return 0;}

	# ���肦�Ȃ��z�X�g
	#�g�шȊO�̓����z�̕�������`�F�b�N
	if(!($GB->{KEITAI} || $GB->{KEITAIBROWSER}))
	{
		if($GB->{HOST4} =~ /^ns\d?\.|mail|www|^ftp|^smtp|^news/ || $GB->{HOST2} =~ /^ns\d?\.|mail|www|^ftp|^smtp|^news/)
		{
			&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�ςȃz�X�g�K�����I�I�@�ςȃz�X�g�ł��B");
		}
	}

	#operate2/operate/sec2chd �� fusianasan �͂���[
	if($GB->{FORM}->{'bbs'} eq "operate2" && $GB->{FORM}->{'FROM'} =~ /$GB->{HOST}/ && $GB->{FORM}->{'subject'} eq "") {return 0;}
# �����p�̖��ߗ��čr�炵�����̂��߁A
# �ꎞ�I�� operate �� [�\{}@{}@{}-] �X���[���X�g�b�v -- 2006/3/17 by ��
#	if($GB->{FORM}->{'bbs'} eq "operate" && $GB->{FORM}->{'FROM'} =~ /$GB->{HOST}/ && $GB->{FORM}->{'subject'} eq "") {return 0;}
#	if($GB->{FORM}->{'bbs'} eq "sec2chd" && $GB->{FORM}->{'FROM'} =~ /$GB->{HOST}/ && $GB->{FORM}->{'subject'} eq "") {return 0;}
	if($GB->{FORM}->{'bbs'} eq "goki" && $GB->{FORM}->{'FROM'} =~ /$GB->{HOST}/ && $GB->{FORM}->{'subject'} eq "") {return 0;}
	#��ʓI�ȏ���
	if($GB->{BURNEDPROXY} eq 1)
	{
		&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F���J�o�q�n�w�x����̓��e�͎󂯕t���Ă��܂���I�I(1)");
	}
}
############################################################################
# vip�N�I���e�B�̊e�폈�����[�`���Q
############################################################################
sub ReplIQ
{
	my ($GB) = @_	;
#return 0;
	if($GB->{FORM}->{bbs} ne 'news4viptasu' && $GB->{FORM}->{bbs} ne 'heaven4vip' && $GB->{FORM}->{bbs} ne 'operate2')	{return 0;}
	$ENV{REMOTE_ADDR} =~ /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/	;
	my $kk = $1	;
	my $mm = $2	;
	my $iq = $3	;
	my $nm = $4	;
	$GB->{FORM}->{'FROM'} =~ s/(\!IQ)/ <\/b>�yIQ$iq�z<b> /;

	my $bill = $iq * 10 + int(rand(10000))	;
	if($bill < 1000000)	{$bill =~ s/(\d)(\d\d\d)(?!\d)/$1,$2/g;}
	else			{$bill =~ s/(\d)(\d\d\d)(\d\d\d)(?!\d)/$1,$2,$3/g;}

	$GB->{FORM}->{'FROM'} =~ s/(\!bill)/ <\/b>�{���̗��p�� $bill�~<b> /;


	my @omikuji = ('����','�����','����','������','�����ς�','�΂�����','�ł�','���イ����',
			'�ۂ�','�݂�[�܂�','���ɂ�','�Ă������','��������','�悾��','�€','�Ђ�',

			'�n�`�x�G','���[�����','�P�j�A','�W�����{','��','������','�R�u��','�|�j�[',
			'������','�܂�����','�J�r','������[','�Ԃ�Ԃ�','�o�P�c','����ׂ�','��d�{',
			'�����ӂ�','�͂ɂ�','�܂񂰂�','�S������','�a��','�}�J���j','���[�_�[','�������',
			'����','�悵�������','�Ӂ[����','�ψ���','����','����','�ӂ�','����',

			'�C���h�l','�͔|�}��','�����炵','�߂���','�ԁ[�����','�˂���','�o����','�K��',
			'���L�\�o��','����������','�]�E�����V','�_������S�b�h','�n�J�Z','���[�`����','��C','�n�G');
	my $omikuji2 = $nm % 64	;
	my $omikuji3 = $omikuji[$omikuji2];
	$GB->{FORM}->{'FROM'} =~ s/(\!kote)/ <\/b>�y$omikuji3�z<b> /;

	$omikuji2 = int(rand(scalar @omikuji));
	$omikuji3 = $omikuji[$omikuji2];
	if(rand(800) < 1)	{$omikuji3 = "�_";}
	if(rand(4000) < 1)	{$omikuji3 = "���_";}
	$GB->{FORM}->{'FROM'} =~ s/(\!sute)/ <\/b>�s$omikuji3�t<b> /;

	my @kz;
	my @k0 = ('����','�������W','���W','���H�W','�|���W','�f���W','�����W','�̈�W','���y�W','�x���}�[�N�W','�x���}�[�N�W','�ی��W','�X�g�[�u�W')	;
	my @k1 = ('����','���W','���H�W','�|���W','�������W','�����W','�̈�W','���y�W','�f���W','�x���}�[�N�W','�ی��W','�X�g�[�u�W','�x���}�[�N�W')	;
	my @k2 = ('����','���H�W','�|���W','�������W','���W','�̈�W','���y�W','�f���W','�����W','�ی��W','�X�g�[�u�W','�x���}�[�N�W','�x���}�[�N�W')	;
	my @k3 = ('����','�|���W','�������W','���W','���H�W','���y�W','�f���W','�����W','�̈�W','�X�g�[�u�W','�x���}�[�N�W','�x���}�[�N�W','�ی��W')	;
	my @k4 = ('����','�f���W','�����W','�̈�W','���y�W','�x���}�[�N�W','�x���}�[�N�W','�ی��W','�X�g�[�u�W','�������W','���W','���H�W','�|���W')	;
	my @k5 = ('����','�����W','�̈�W','���y�W','�f���W','�x���}�[�N�W','�ی��W','�X�g�[�u�W','�x���}�[�N�W','�������W','���W','���H�W','�|���W')	;
	my @k6 = ('����','�̈�W','���y�W','�f���W','�����W','�ی��W','�X�g�[�u�W','�x���}�[�N�W','�x���}�[�N�W','�������W','���W','���H�W','�|���W')	;
	my @k7 = ('����','���y�W','�f���W','�����W','�̈�W','�X�g�[�u�W','�x���}�[�N�W','�x���}�[�N�W','�ی��W','�|���W','�������W','���W','���H�W')	;
	my @k8 = @k0	;
	if(($GB->{JIKAN} % 8) eq 1)	{@kz = @k1;}
	if(($GB->{JIKAN} % 8) eq 2)	{@kz = @k2;}
	if(($GB->{JIKAN} % 8) eq 3)	{@kz = @k3;}
	if(($GB->{JIKAN} % 8) eq 4)	{@kz = @k4;}
	if(($GB->{JIKAN} % 8) eq 5)	{@kz = @k5;}
	if(($GB->{JIKAN} % 8) eq 6)	{@kz = @k6;}
	if(($GB->{JIKAN} % 8) eq 7)	{@kz = @k7;}
	my $kaka = $kz[0]	;
	if($kk < 60)		{$kaka = $kz[1];}
	elsif($kk < 128)	{$kaka = $kz[2];}
	elsif($kk < 150)	{$kaka = $kz[3];}
	elsif($kk < 200)	{$kaka = $kz[4];}
	elsif($kk < 205)	{$kaka = $kz[5];}
	elsif($kk < 210)	{$kaka = $kz[6];}
	elsif($kk < 215)	{$kaka = $kz[7];}
	elsif($kk < 220)	{$kaka = $kz[8];}
	$GB->{FORM}->{'FROM'} =~ s/(\!kakari)/ <\/b>$kaka<b> /;

	while($GB->{FORM}->{'FROM'} =~ /\!mibun/)
	{
		$omikuji3 = &GetMibun	;
		$GB->{FORM}->{'FROM'} =~ s/(\!mibun)/ <\/b>$omikuji3<b> /;
	}
#�{��
my $vipMax = 12	;
$GB->{VIP} = 0	;
	while($GB->{FORM}->{'MESSAGE'} =~ /\!mibun/)
	{
		if(++$GB->{VIP} > $vipMax)	{return 0;}
		if($GB->{BEpoints} > 499)	{$omikuji3 = &GetMibunBe;}
		else				{$omikuji3 = &GetMibun	;}
		$GB->{FORM}->{'MESSAGE'} =~ s/(\!mibun)/ <b>$omikuji3<\/b> /;
	}

	while($GB->{FORM}->{'MESSAGE'} =~ /\!where/)
	{
		if(++$GB->{VIP} > $vipMax)	{return 0;}
		$omikuji3 = &GetWhere	;
		$GB->{FORM}->{'MESSAGE'} =~ s/(\!where)/ <b>$omikuji3<\/b> /;
	}

	while($GB->{FORM}->{'MESSAGE'} =~ /\!card/)
	{
		if(++$GB->{VIP} > $vipMax)	{return 0;}
		$omikuji3 = &GetCard	;
		$GB->{FORM}->{'MESSAGE'} =~ s/(\!card)/ <b>$omikuji3<\/b> /;
	}

	while($GB->{FORM}->{'MESSAGE'} =~ /\!do/)
	{
		if(++$GB->{VIP} > $vipMax)	{return 0;}
		$omikuji3 = &GetDo	;
		$GB->{FORM}->{'MESSAGE'} =~ s/(\!do)/ <b>$omikuji3<\/b> /;
	}

	while($GB->{FORM}->{'MESSAGE'} =~ /\!food/)
	{
		if(++$GB->{VIP} > $vipMax)	{return 0;}
		$omikuji3 = &GetFood	;
		$GB->{FORM}->{'MESSAGE'} =~ s/(\!food)/ <b>$omikuji3<\/b> /;
	}

	while($GB->{FORM}->{'MESSAGE'} =~ /\!drink/)
	{
		if(++$GB->{VIP} > $vipMax)	{return 0;}
		$omikuji3 = &GetDrink	;
		$GB->{FORM}->{'MESSAGE'} =~ s/(\!drink)/ <b>$omikuji3<\/b> /;
	}

	while($GB->{FORM}->{'MESSAGE'} =~ /\!animal/)
	{
		if(++$GB->{VIP} > $vipMax)	{return 0;}
		$omikuji3 = &GetAnimal	;
		$GB->{FORM}->{'MESSAGE'} =~ s/(\!animal)/ <b>$omikuji3<\/b> /;
	}

	while($GB->{FORM}->{'MESSAGE'} =~ /\!jinsei/)
	{
		if(++$GB->{VIP} > $vipMax)	{return 0;}
		$omikuji3 = &GetJinsei	;
		$GB->{FORM}->{'MESSAGE'} =~ s/(\!jinsei)/ <b>$omikuji3<\/b> /;
	}
}
sub GoShip
{
	my ($GB) = @_	;

	if($GB->{FORM}->{bbs} eq 'neet4vip')		{return 1;}
	if($GB->{FORM}->{bbs} eq 'heaven4vip')		{return 1;}
	if($GB->{FORM}->{bbs} eq 'news4viptasu')	{return 1;}
	if($GB->{FORM}->{bbs} eq 'news4vip')		{return 1;}
#	if($GB->{FORM}->{bbs} eq 'morningcoffee')	{return 1;}
#	if($GB->{FORM}->{bbs} eq 'campus')		{return 1;}
	if($GB->{FORM}->{bbs} eq 'operate2')		{return 1;}

	return 0	;
}
sub ReplShip
{
	my ($GB) = @_	;
	if(!&GoShip($GB))	{return 0;}

	$ENV{REMOTE_ADDR} =~ /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/	;
	my $kk = $1	;
	my $mm = $2	;
	my $iq = $3	;
	my $nm = $4	;

	my $shipPath = "$GB->{PATH}/ship"	;
	if($GB->{FORM}->{'MESSAGE'} =~ /\!list/)
	{
		if($GB->{FORM}->{'MESSAGE'} =~ /\!list ([a-z0-9]+)/)
		{
			my $omikuji3 = &ListShip($1)	;
			$omikuji3 .= &ListShip($GB->{FORM}->{bbs})	;
			$GB->{FORM}->{'MESSAGE'} =~ s/\!list ([a-z0-9]+)/$omikuji3/;
		}
		else
		{
			my $omikuji3 = &ListShip($GB->{FORM}->{bbs})	;
			$GB->{FORM}->{'MESSAGE'} =~ s/\!list/$omikuji3/	;
		}
	}
	if($GB->{FORM}->{'MESSAGE'} =~ /\!create ([A-Za-z0-9]+)/)
	{
		my $omikuji3 = &GetShip($shipPath,$1,$iq,$GB->{BEpoints})	;
		$GB->{FORM}->{'MESSAGE'} =~ s/(\!create [A-Za-z0-9]+)/$omikuji3/;
	}
	elsif($GB->{FORM}->{'MESSAGE'} =~ /\!attack ([A-Za-z0-9@]+)/)
	{
		my $omikuji3 = &AttackShip($GB->{FORM}->{bbs},$1,$iq)	;
		$GB->{FORM}->{'MESSAGE'} =~ s/(\!attack [A-Za-z0-9@]+)/$omikuji3/;
	}
	return 0;
}
sub AttackShip
{
	my ($path,$nameXXX,$iq) = @_	;
	my ($name,$gun) = split(/@/,$nameXXX)	;
	if(!$gun)	{$gun = $path;}
	my $folder = "../$gun/ship"	;
	my $poi = 0			;
	if(!open(SHIP,"$folder/$name.ship"))
	{
		return "Attack $1 ---> Missed."	;
	}
	$poi=<SHIP>;
	chomp($poi);
	close(SHIP);

	my $hp = (255 - $iq) * 3 + int(rand(200))	;
	if(rand(3) < 1)		{$hp += 50;}
	if(rand(8) < 1)		{$hp += 500;}
	if(rand(50) < 1)	{$hp += 5000;}

	$poi -= $hp	;

	if($poi < 1)
	{
		unlink("$folder/$name.ship")	;
		return "Attack $1 ---> Success. <font color=red>����!!</font>"	;
	}

	if(open(SHIP,"> $folder/$name.ship")){print SHIP "$poi\n";close(SHIP);}

	return "<font color=blue>Attack $1 ---> Success. (-$hp)</font>"	;
}
sub ListShip
{
	my ($path) = @_		;
	$path =~ s/ //g;
	my $folder = "../$path/ship"	;
	my @ds = ()		;
	if(opendir(DIR, $folder))
	{
		@ds = grep(!/^\./ && -f "$folder/$_", readdir(DIR));
		closedir DIR	;
	}
	my $nnn = @ds		;
	my $ships = "<font color=green face=\"Arial\"><b>current ships</b></font>($nnn) $path�R<br>";
	foreach(@ds)
	{
		my $poi = 0		;
		my $name = $_		;
		$name =~ s/\.ship//	;
		if(open(SHIP,"$folder/$name.ship")){$poi=<SHIP>;chomp($poi);close(SHIP);}
	
		$ships .= "# <font color=blue>$name</font> $poi<br>"	;
	}
	return $ships	;
}
sub GetShip
{
	my ($path,$name,$iq,$be) = @_	;

	if($iq < 150)	{return '<font color=green>�m�\���Ⴍ�Č����ł��܂���ł����B</font>' . "($name)";};
	if(length($name) >16)	{return '<font color=green>�D�����������܂��B</font>' . "($name)";};

	my $folder = "$path"	;
	if(-e "$folder/$name.ship")	{return '<font color=green>�����̑D�����ɑ��݂��܂��B</font>' . "($name)";};
	my @ds = ()		;
	if(opendir(DIR, $folder))
	{
		@ds = grep(!/^\./ && -f "$folder/$_", readdir(DIR));
		closedir DIR	;
	}
	my $nnn = @ds		;
	if($nnn >= 5)
	{
		return '<font color=green>����ȏ㌚���ł��܂���B</font>' . "($name)"	;
	}
	if($name =~ /\d/)
	{
		return '<font color=green>�������g���Ȃ��Ȃ�܂����B</font>' . "($name)"	;
	}

	my $hp = 5000		;
	$hp *= int(rand(8)+1)	;
	$be *= 5		;
	if($be > 50000)	{$be = 50000;}
	$hp += $be		;

	mkdir("$path/",0777)	;
	if(open(SHIP,"> $folder/$name.ship")){print SHIP "$hp\n";close(SHIP);}
	return "<font color=blue><b>$name</b> created. (HP $hp)</font>"	;
}
sub GetMibun
{
	my @m0 = ('�j�[�g','�z��','���g','�r����','����','����','�C���m','�C����','����','�n��','�M��','���t',
		'�z��','�z��','�ނ�t','�e����','���y','�X�p�C','�E��b','�ޒ�','�p�V��','����','����','����',
		'�z��','�z��','��r','�؂���','�����t','�}�M�[','���s','�ԓ�','�j��','���','������','������',
		'�z��','�z��','�X���t','�������','�E��','�d��','����','�d��','���b','�e��','�Ǘ��l','��V���l',
		'�z��','�z��','�z��','�z��','�z��','�z��','�z��','�z��','�z��','�z��','����',
		'�z��','�z��','�z��','�z��','�z��','�z��','�z��','�z��','�z��','�z��',
		'�z��','�z��','��H','����','�w���','�b�艮','�d����','���\�t','���l��','�V��','���㊯','�����{',
		'�z��','�z��','�e��','�q��','�S�g�t','�M�����u���[','�}�t�B�A','�M�����O','���V','�����l','�s��','�����L�[',
		'�z��','�z��','������','�����}�}','����l','���m','�V��','�^�щ�','�֎g��','1,000�~����','�i�[�X','DQN',
		'���X���[','<font color=tomato>�X�[�p�[�n�J�[</font>','���[�}��','�ʉَq��','�s��','�X�g�[�J�[','�T��','�h���[�t','��l','�q�b�L�[',
		'���ێЈ�','�l���l��',
#'','','','','','','','',
		'�z��','�z��','���C�h')	;
#		'','','','','','','','','','',
	my $omikuji2 = int(rand(scalar @m0));
	my $omikuji3 = $m0[$omikuji2];
	if(rand(200) < 1)	{$omikuji3 = "��";}
	if(rand(400) < 1)	{$omikuji3 = "AV�ē�";}

	return $omikuji3	;
}
sub GetMibunBe
{
	my @m0 = ('�m��','��b','����','�i�C�g','��m','���@�g��','�V�g',
			'���m','�E','���̂���','�搶','����','����','�햱','�ꖱ',
			'�卲','�{����','���@��','�h�N�^�[','�w��','�ψ���','����','�@��',
#'','','','','','','','',
#'','','','','','','','',
		'���l','���l','���l')	;
	my $omikuji2 = int(rand(scalar @m0));
	my $omikuji3 = $m0[$omikuji2];
#	if(rand(200) < 1)	{$omikuji3 = "��";}
#	if(rand(400) < 1)	{$omikuji3 = "AV�ē�";}

	return $omikuji3	;
}
sub GetJinsei
{
	my @m0 = (
		'��','����','���C','����','�����삯','�삯����','���H','���z��',
		'���w','�C�O���w','1,000���n�����Ă�','�󂭂�����','�Ўv��','�₹��','���@','�̎�f�r���[',
		'��','�o�Y','��R�q�a��','���ɐ���','�ߕ�','���@','����','����',
		'�o���h���','���ꂨ��Ɉ���������','���z���Ƃ�','���]�ԓ��܂��','���񂱓���','���񂱂����','�G��`��','�܂����I',
		'���Ȕj�Y','�ڂ�����','�ƌ��Ă�','�󂫑��ɂ����','�܂���l','���E','2ch����','�Ђ�������',
		'�Əo����','����','����','����','����','����','����','����',
#		'����','����','����','����','����','����','����','����',
#'','','','','','','','',
		'����','���X�g��','�A�E')	;
	my $omikuji2 = int(rand(scalar @m0));
	my $omikuji3 = $m0[$omikuji2];
	if(rand(200) < 1)	{$omikuji3 = "���z����";}
	if(rand(400) < 1)	{$omikuji3 = "�O���~�[�܎��";}

	return $omikuji3	;
}
sub GetAnimal
{
	my @m0 = ('����񂳂�','��������','�R��','��','�L','��',
		'�ނ�����','�n���L�Q�j�A','�}�����X','�Ƃ�','�����炵','�͓�','�͔n','�C��',
		'�E�B���X','�d��','�G�C���A��','E.T','�����L�[','���΂���','�Z�C�E�`','������',
		'���j','�`���p���W�[','�Ȃ܂�����','�܂�ƂЂ�','���炤�[����','�肷����','�T','���낭��',
		'�c�`�m�R','�u�^','�u�^','�u�^','�u�^','�u�^','�u�^','�u�^',
		'�Ԃ�','��','�u�^')	;
	my $omikuji2 = int(rand(scalar @m0));
	my $omikuji3 = $m0[$omikuji2];
	if(rand(200) < 1)	{$omikuji3 = "�f�u";}
#	if(rand(400) < 1)	{$omikuji3 = "AV�ē�";}

	return $omikuji3	;
}
sub GetFood
{
	my @m0 = ('�L���x�c','�V��','�J�c�ǂ�','���ȏd','�I�����C�X','�[��','�^�c�^�T���h',
		'�������','������','���Ƃ�����','�','�݂݂�','����','�����i','����',
		'����','�C�J�[��','������','���肽���','������','�X�e�[�L','�}�b�N','�t�����`�t���C',
		'���܂��_','�p��','�p��','�p��','�p��','�p��','�p��','�p��',
		'�J���[�p��','�����Ƃ�','���̂�','�Ⓚ�}�O��','�p��','�p��','�p��','�p��',
#'','','','','','','','',
		'���ǂ�','��[�߂�','�킩��')	;
	my $omikuji2 = int(rand(scalar @m0));
	my $omikuji3 = $m0[$omikuji2];
	if(rand(200) < 1)	{$omikuji3 = "�s�U";}
#	if(rand(400) < 1)	{$omikuji3 = "AV�ē�";}

	return $omikuji3	;
}
sub GetDrink
{
	my @m0 = ('���X�`','�y�v�V',
		'��','�o�[�{��','�X�R�b�`','�Ē�','�A��','�e�L�[��','����','���',
		'���C��','������','�u�����f�[','�݂͂�','�g��','�ʃR�[�q�[','�r�[��','�}���K���[�^',
#'','','','','','','','',
		'�V�R��','�J','�C��')	;
	my $omikuji2 = int(rand(scalar @m0));
	my $omikuji3 = $m0[$omikuji2];

	return $omikuji3	;
}
sub GetWhere
{
	my @m0 = (
		'������','�B���','�剜','�K�i','���Z','����','�ے�','�ߏ�','�N���[�U�[','�{�[�g',
		'��','�a�̎R','����','����','���s','�ޗ�','�V��','���','�H�c','���',
		'�C�M���X','�t�����X','�h�C�c','�I�����_','�X�y�C��','�f���}�[�N','�t�B�������h','����','�؍�','�k���N',
		'���','��������','�c��','�s��','�ԉ�','������','����','�J�t�F','�v�[��','�ߏ�',
		'�x�b�g','����','�n��','��','�x�����_','��������','����','����','�n����','�G���x�[�^�[',
		'�J�U�t�X�^��','�����b�R','�䏊')	;
#		'','','','','','','','','','',
	my $omikuji2 = int(rand(scalar @m0));
	my $omikuji3 = $m0[$omikuji2];
	if(rand(200) < 1)	{$omikuji3 = '�V��';}
	if(rand(400) < 1)	{$omikuji3 = '�\�[�v';}

	return $omikuji3	;
}
sub GetDo
{
	my @m0 = (
		'�W�����v','�u�[��','����','����','����','���˂�','�ϐg','�t����','�̓�����',
		'�ǂ�ǂ�','�q���','�Z�b�N�X','���V','���i','�ώ@','��p','���`','�锇��','�铦��',
		'���肮��','����','�^�b�`','�L�X','���C�N���u','���C�N�~���N��','����','�׋�','����񂯂�','�s��',
		'��������','���񂠂�','���낿��','�؂�؂�','�ׂ�ׂ�','�ɂ�ɂ�','���񂭂�','���񂮂�','����Ƃ�','�ɂ��ɂ��',
		'����','���݂���','����')	;
#		'','','','','','','','','','',
	my $omikuji2 = int(rand(scalar @m0));
	my $omikuji3 = $m0[$omikuji2];
	if(rand(200) < 1)	{$omikuji3 = "�ؕ�";}
	if(rand(400) < 1)	{$omikuji3 = "���̌�";}

	return $omikuji3	;
}
sub GetCard
{
	my @c0 = ('&hearts;','&clubs;','&spades;','&diams;')	;
	my @c1 = ('A','2','3','4','5','6','7','8','9','10','J','Q','K')	;
	my $omikuji2 = int(rand(scalar @c0));
	my $omikuji3 = $c0[$omikuji2];
	my $omikuji4 = int(rand(scalar @c1));
	my $omikuji5 = $c1[$omikuji4];

	return $omikuji3 . $omikuji5	;
}
sub ReplKabuka
{
	my ($GB) = @_			;

	if(!$GB->{KABU})	{return 0;}

	$GB->{FORM}->{'FROM'} =~ s/!!kab(?::[a-zA-Z0-9]+|%|)//;

	if($GB->{FORM}->{'FROM'} =~ /\!kab\:[a-zA-Z0-9]+/)
	{
		$GB->{FORM}->{'FROM'} =~ s/\!kab\:[a-zA-Z0-9]+/ <\/b>�y$GB->{MEIGARA}:$GB->{KABUSU}�z<b> /;
	}
	elsif($GB->{FORM}->{'FROM'} =~ /\!kab\%/)
	{
		$GB->{FORM}->{'FROM'} =~ s/(\!kab\%)/ <\/b>����y$GB->{ZENKABU}�z<b> /;
	}
	else
	{
		$GB->{FORM}->{'FROM'} =~ s/(\!kab)/ <\/b>�����y$GB->{KABUKA}�z<b> /;
	}
	return 1;
}
sub GoOmikuji
{
	my ($GB) = @_	;

	if($GB->{MDAY} ne 1)	{return 0;}
	if($GB->{MON} eq 1)	{return 1;}

	if($ENV{SERVER_NAME} =~ /kamome/)	{return 1;}
	if($ENV{SERVER_NAME} =~ /toki/)		{return 1;}
	if($ENV{SERVER_NAME} =~ /yuzuru/)	{return 1;}
	if($ENV{SERVER_NAME} =~ /raicho/)	{return 1;}
	if($ENV{SERVER_NAME} =~ /hato/)		{return 1;}

	return 0	;
}
sub ReplOmikuji
{
	my ($GB) = @_	;
#$GB->{MDAY}\/$GB->{MDAY}
	if(!&GoOmikuji($GB))	{return 0;}
	my @omikuji = ("��g","��g","��g","��g","��g","�g","���g","���g","���g","��","�勥","�҂��g","����g","��");
	my $omikuji2 = int(rand(scalar @omikuji));
	my $omikuji3 = $omikuji[$omikuji2];
	if(rand(800) < 1)	{$omikuji3 = "�_";}
	if(rand(10000) < 1)	{$omikuji3 = "���_";}
	$GB->{FORM}->{'FROM'} =~ s/(\!omikuji)/ <\/b>�y$omikuji3�z<b> /;
	return 0;
}
sub ReplOtoshidama
{
	my ($GB) = @_	;

	if($GB->{MON} ne 1)	{return 0;}
	if($GB->{MDAY} ne 1)	{return 0;}
	my $omikuji2 = int(rand(2000));
	if(rand(400) < 1)	{$omikuji2 *= 11;}
	if(rand(1000) < 1)	{$omikuji2 *= 111;}
	my $omikuji3 = "$omikuji2�~";
	$GB->{FORM}->{'FROM'} =~ s/(\!dama)/ <\/b>�y$omikuji3�z<b> /;
	return 0;
}
#############################################################################
# ��������dat�̏���$GB�ɃZ�b�g����
# ����: $GB, �^�[�Q�b�g�ƂȂ�dat��$key
# $GB->{DATNUM}, $GB->{DAT1}, $GB->{DATLAST}[N]
#############################################################################
sub GetDatInfo
{
	my ($GB, $key) = @_;
	my $datfile = $GB->{DATPATH} . $key . ".dat";
	my $datlastnum = $FOX->{$GB->{FORM}->{bbs}}->{"BBS_CONTENTS_NUMBER"};

	if($GB->{NEWTHREAD})
	{
		# �V�X���̏ꍇ
		$GB->{DAT1} = $GB->{OUTDAT};
		$GB->{DATNUM} = 1;
		@{$GB->{DATLAST}} = ();
	}
	else
	{
		# ���X�̏ꍇ
		open(DAT,"<$datfile");
		$GB->{DAT1} = <DAT>;
		@{$GB->{DATLAST}} = <DAT>;
		$GB->{DATNUM} = $.; 
		close(DAT);
		if (@{$GB->{DATLAST}} > $datlastnum)
		{ 
			@{$GB->{DATLAST}} = splice(@{$GB->{DATLAST}}, -$datlastnum); 
		} 
	}

	return 0;
}
#############################################################################
# �ŏI�ً}��h
# ���́A$GB, dat�t�@�C����
#############################################################################
sub EmergOver1000Final
{
	use File::Copy;
	my ($GB, $dat) = @_;

	if(-w $dat)
	{
		my $tmpdat = $GB->{DATPATH} . $GB->{FORM}{key} . ".tmp";
		copy($dat, $tmpdat);
		chmod(0555, $tmpdat);
		&TryRename($tmpdat, $dat);
	}
	&DispError2($GB,"�d�q�q�n�q�I", "�d�q�q�n�q�F���̃X���b�h�ɂ͏������߂܂���B�Ō�̎�i!!");

	return 0;
}
#############################################################################
# �ً}��h
# ���́A$GB, dat�t�@�C����
#############################################################################
sub EmergOver1000
{
	my ($GB, $dat) = @_;

	chmod(0555, $dat);
	&DispError2($GB,"�d�q�q�n�q�I", "�d�q�q�n�q�F���̃X���b�h�ɂ͏������߂܂���B�ً}�ً}�ً}!!");

	return 0;
}
#############################################################################
# 1000�����̏���������
# ���́A$GB, dat�t�@�C����
# ������dat��chmod 555����āA�����Ȃ��Ȃ�
#############################################################################
sub Over1000
{
	my ($GB, $dat) = @_;

	my $b1000 = "���̃X���b�h�͂P�O�O�O�𒴂��܂����B <br> ���������Ȃ��̂ŁA�V�����X���b�h�𗧂ĂĂ��������ł��B�B�B ";
#	my $p1000 = $GB->{PATH} . "1000.txt"	;
	my $r1000 = $GB->{NOWTIME} % 10		;	# �����_��1000.txt
	my $p1000 = $GB->{PATH} . "100" . $r1000 . ".txt"	;
	if(!(-e $p1000))	{$p1000 = $GB->{PATH} . "1000.txt"	;}
	my $lastdat = "";

	if(-s $p1000 && open(PDATA1000,"$p1000"))
	{
		$b1000 = ""		;
		foreach(<PDATA1000>)
		{
			my $bbb = $_	;
			chomp($bbb)	;
			$bbb =~ s/\n//g	;
			$bbb =~ s/\r//g	;
			$b1000 .= $bbb	;
		}
		close(PDATA1000)	;
	}

	$lastdat = "�P�O�O�P<><>Over 1000 Thread<> $b1000 <>\n";

	# ���ɂP�O�O�P�������Ă�������A�����̂���߂�
	if ($GB->{DATLAST}[-1] ne $lastdat)
	{
		# �P�O�O�P�������ݏ���
		if(open(OUT,">>$dat"))
		{
			print OUT $lastdat;
			close(OUT);

			# $GB�̏���
			# dat�̔ԍ����ЂƂ����߂�
			++$GB->{DATNUM};
			# $GB->{DATLAST}���ЂƂ����o��
			shift(@{$GB->{DATLAST}});
			push(@{$GB->{DATLAST}}, $lastdat);
		}
	}

	# dat�������Ȃ�����
	chmod(0555, $dat);

	return 0;
}
#############################################################################
# BBY�ɐV�X���̏���`����
#############################################################################
sub NotifyBBY
{
	my ($GB) = @_;

	my $AHOST;	# BBY�ւ�DNSquery�z�X�g���w��p�ϐ�
	my $DNSbby;	# BBY��DNS�T�[�o�w��p�ϐ�

	if($ENV{'SERVER_NAME'} =~ /bbspink\.com/)
	{# bbspink.com�̏ꍇ
		$DNSbby = $FOX->{DNSSERVER}->{BBYP};
		$AHOST = "$GB->{NEWTHREAD}.$GB->{FORM}->{'bbs'}.$ENV{'SERVER_NAME'}.bby.bbspink.com.";
	}
	else
	{# 2ch�̏ꍇ
		$DNSbby = $FOX->{DNSSERVER}->{BBY};
		$AHOST = "$GB->{NEWTHREAD}.$GB->{FORM}->{'bbs'}.$ENV{'SERVER_NAME'}.bby.2ch.net.";
	}
	if($FOX->{BBY})
	{
		$FOX->{BBY} = &foxDNSquery($AHOST, $DNSbby);
	}

	return 0;
}
#############################################################################
# BBS�ɏ������݂̏���`����
#############################################################################
sub NotifyBBS
{
	my ($GB) = @_;

	my $BYTES = length($GB->{FORM}->{'MESSAGE'});
	my $BHOST = "$GB->{NOWTIME}.$$.$ENV{'REMOTE_ADDR'}.$GB->{NEWTHREAD}.$BYTES.$GB->{FORM}->{'key'}.$GB->{FORM}->{'bbs'}.$ENV{'SERVER_NAME'}.bbs.bbs.2ch.net.";
	if($FOX->{BBS})
	{
		$FOX->{BBS} = &foxDNSquery($BHOST, $FOX->{DNSSERVER}->{BBS});
	}
	#my $aaa = $FOX->{BBS}	;
	#&DispError2($GB,"FOX ��","<font color=green>FOX ��</font> ($aaa)");

	return 0;
}
#############################################################################
# �t�@�C���̃��l�[�����s��
# ����: $src�A$dst
# �߂�l: 0�܂��̓G���[���b�Z�[�W
#############################################################################
sub TryRename
{
	my ($src, $dst) = @_;
	my $status = undef;
	my $count = 1000;

	# rename�����s���Ă݂�
	for (1..$count)
	{
		rename($src, $dst) and return 0;
	}
	# �X�e�[�^�X��ۑ�����
	$status = $!;

	unlink($src);
	return $status;
}
#######################################################################
# subject.txt���X�V����
# ������ĂԂ��Ƃɂ��A@{$GB->{NEWSUB}} ��subject.txt����荞�܂��
# $GB->{SUBLINE} �������ŏ��������
# $GB->{FILENUM} �ɂ͂�����subject.txt�̍s��������悤��
#######################################################################
sub UpdateSubject
{
	my ($GB) = @_;
	my @newsub = ();	# ������ @newsub �̓��[�J���ϐ�(��������)

	#�T�u�W�F�N�g�p�X
	my $subject = $GB->{PATH} . "subject.txt";
	my $rnd = int(rand(99999));
	my $subtemp = $GB->{PATH} . $rnd . $GB->{FORM}->{'time'} . ".tmp";
	my $keyfile = $GB->{FORM}->{'key'} . ".dat";

	#subject.txt��荞�ݗp
	my (@SUBJ1, @SUBJ2);

	#�X���^�C���o�p
	my $dat1 = "";
	my $title = "";

	#subject.txt�����E���ёւ��p
	my ($i, $subtm);

	{
		# slurp mode; �t�@�C���͒P�ꕶ����ɑS���ǂݍ���
		local $/;
		#�T�u�W�F�N�g�t�@�C����ǂݍ���
		open(SUBR, $subject);		#SUBJECT���J��
		$subtm = <SUBR>;		#���e��S�ēǂݍ���
		close(SUBR);			#����
	}

	# $SUBJ2[0] �� $keyfile �̃X���ɂȂ�悤��
	# �Ȃ��ꍇ�� @SUBJ1 �ɑS�������
	if (substr($subtm, 0, length($keyfile) + 2) eq "$keyfile<>") {
		@SUBJ2 = split(/^/m, $subtm);
	}
	elsif (($i = index($subtm, "\n$keyfile<>")) >= 0) {
		@SUBJ1 = split(/^/m, substr($subtm, 0, ++$i));
		@SUBJ2 = split(/^/m, substr($subtm, $i));
	}
	else {
		@SUBJ1 = split(/^/m, $subtm);
	}
	$GB->{FILENUM} = @SUBJ1 + @SUBJ2;

	#$GB->{SUBLINE} ����������
	#dat��1�s�ڂ̗v�f����X���^�C�𓾂�
	$dat1 = $GB->{DAT1};
	#���s�J�b�g
	chomp($dat1);
	#1�ڂ̗v�f�����H����
	$title = (split(/<>/, $dat1))[4];
	#������ŏ���$GB->{SUBLINE}�Ƃ��Ďg�p����
	$GB->{SUBLINE} = "$title ($GB->{DATNUM})\n";

	if($GB->{NEWTHREAD})
	{
		#�V�X���̏ꍇ�A��ԏ�ɂ̂�����
		$subtm = "$keyfile<>$GB->{FORM}->{'subject'} (1)\n";
		# @SUBJ2 �͋�̂͂������O�̂���
		@newsub = ($subtm, @SUBJ1, @SUBJ2);
		++$GB->{FILENUM};
	}
	else
	{
		if($GB->{FORM}->{'mail'} =~ /sage/)
		{
			### sage�̏ꍇ�̏��� ###
			$SUBJ2[0] = "$keyfile<>$GB->{SUBLINE}";
			@newsub = (@SUBJ1, @SUBJ2);
		}
		else
		{
			### �ʏ�̏ꍇ�̏��� ###
			shift @SUBJ2;
			$subtm = "$keyfile<>$GB->{SUBLINE}";
			@newsub = ($subtm, @SUBJ1, @SUBJ2);
		}
	}

	# subject.txt �ւ̎��ۂ̏������ݏ���
	if(@newsub)
	{
		#SUBJECT�ɏ�������
		open(SUBT, ">$subtemp");
		#flock(SUBT, 2);
		&PutLines(*SUBT, @newsub);
		#flock(SUBT,8);
		close(SUBT);
		&TryRename($subtemp, $subject);
	}
	else
	{
		@newsub = (@SUBJ1, @SUBJ2);
	}

	# @{$GB->{NEWSUB}} �ɏ������ʂ���
	@{$GB->{NEWSUB}} = @newsub;

	return 0;
}
#######################################################################
# subback.html���X�V����
# UpdateSubject�̌�ŌĂԂ���
#######################################################################
sub UpdateSubback
{
	my ($GB) = @_;

	my $sub = $GB->{PATH} . "subback.html";

	$GB->{base} = "http://$ENV{'SERVER_NAME'}$ENV{'SCRIPT_NAME'}";
	$GB->{base} =~ s/[^\/]*\.cgi/read\.cgi\/$GB->{FORM}->{'bbs'}\//;

	open(HED,">$sub");
	#flock(HED,2);

	# subback��HTML�w�b�_����1
	my @subbackhead1 = (
	qq|<html lang="ja">|,
	qq|<head>|,
	qq|<title>$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE'}���X���b�h�ꗗ</title>|,
	qq|<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">|,
	qq|<base href="$GB->{base}" target="body">|,
	qq|<script type="text/javascript" src="http://www2.2ch.net/snow/index.js" defer></script>|
	);
	&PutLines(*HED, @subbackhead1);
	my @subbackhead2 = (
	qq|<style type="text/css"><!--\n|,
	qq|a { margin-right: 1em; }|,
	qq|div.floated { border: 1px outset honeydew; float: left; height: 20em; line-height: 1em; margin: 0 0 .5em 0; padding: .5em; }|,
	qq|div.floated, div.block { background-color: honeydew; }|,
	qq|div.floated a, div.block a { display: block; margin-right: 0; text-decoration: none; white-space: nowrap; }|,
	qq|div.floated a:hover, div.block a:hover { background-color: cyan; }|,
	qq|div.floated a:active, div.block a:active { background-color: gold; }|,
	qq|div.right { clear: left; text-align: right; }|,
	qq|div.right a { margin-right: 0; }|,
	qq|div.right a.js { background-color: dimgray; border: 1px outset dimgray; color: palegreen; text-decoration: none; }|,
	qq|\n|,
	qq|--></style>|,
	qq|</head>|,
	qq|<body>|,
	qq|<div><small id="trad">\n|
	);
	&PutLines(*HED, @subbackhead2);

	# subback�̒��g����
	my $i = 0;
	foreach(@{$GB->{NEWSUB}})
	{
		chomp;
		++$i;
		/^(\w+)\.dat<>(.*)/;
		my ($key, $value) = ($1, $2);
		&Put1Line(*HED, "<a href=\"$key/l50\">$i: $value</a>\n");
	}

	# subback�̂�����̕���
	my @subbackfoot = (
	qq|</small></div><div class="right"><small>|,
	qq|<a href="javascript:changeSubbackStyle();" target="_self" class="js">�\\���X�^�C���ؑ�</a>&nbsp;\n|,
	&IsReadHtml($GB) ? qq|<a href="javascript:switchReadJsMode();" target="_self" class="js">read.cgi ���[�h�ؑ�</a>&nbsp;\n| : qq||,
	qq|<a href="../../../$GB->{FORM}->{'bbs'}/kako/"><b>�ߋ����O�q�ɂ͂�����</b></a></small></div>\n|,
	qq|</body>|,
	qq|</html>|
	);
	&PutLines(*HED, @subbackfoot);
	#flock(HED,8);
	close(HED);

	return 0;
}
#######################################################################
# �g�b�v(index.html)�����
# UpdateSubject�̌�ŌĂԂ���
#######################################################################
sub MakeIndex4PC
{
	my ($GB) = @_;

	my $rnd = int(rand(99999));
	my $INDEXtemp = $GB->{PATH} . $rnd . $GB->{FORM}->{'time'} . ".tmps";

	#open(HTM,">$GB->{INDEXFILE}");
	open(HTM,">$INDEXtemp");

	#--------�܂��w�b�_�����
	my @index_header1 = (
	qq|<html lang="ja">|,
	qq|<head>|,
	qq|<meta http-equiv="Content-Type" content="text/html; charset=shift_jis">|,
	#�N�b�L�[���������邽�߂� JavaScript
	qq|<script type="text/javascript" src="http://www2.2ch.net/snow/index.js" defer></script>|,
	);
	&PutLines(*HTM, @index_header1);
	# JavaScript �ł���(�Ƃ肠����)
	if(&IsReadHtml($GB))
	{
		# BE �֘A JavaScript
		my @index_scriptheader = (
		qq|<script type="text/javascript" src="http://www2.2ch.net/snow/be.js" defer></script>|
		);
		&PutLines(*HTM, @index_scriptheader);
	}
	my @index_header2 = (
	qq|<title>$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE'}</title>|,
	qq|<style>body{	margin:0;	padding:0;}</style>|,
	qq|</head>|,
	qq|<body text=$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TEXT_COLOR'} link=$FOX->{$GB->{FORM}->{bbs}}->{'BBS_LINK_COLOR'} alink=$FOX->{$GB->{FORM}->{bbs}}->{'BBS_ALINK_COLOR'} vlink=$FOX->{$GB->{FORM}->{bbs}}->{'BBS_VLINK_COLOR'} background=$FOX->{$GB->{FORM}->{bbs}}->{'BBS_BG_PICTURE'}>|,
	qq|<script type="text/javascript" src="http://www.ff.iij4u.or.jp/~ch2/js/2chtop.js"></script>|
	);
	&PutLines(*HTM, @index_header2);

	#�e�[�}�\���O
	#if($FOX->{$GB->{FORM}->{bbs}}->{BBS_BG_SOUND})
	#{
	#	&Put1Line(*HTM, "<bgsound src=\"$FOX->{$GB->{FORM}->{bbs}}->{BBS_BG_SOUND}\" autostart=\"true\">");
	#}

	#--------�^�C�g���摜
	$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE_LINK'}=~ s/http:\/\/info.2ch.net\/info.html/http:\/\/info.2ch.net\/guide/g;
	if($FOX->{$GB->{FORM}->{bbs}}->{BBS_TITLE_PICTURE})
	{
		&Put1Line(*HTM, "<div align=center>");
		if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE_LINK'})
		{
			&Put1Line(*HTM, "<a href=\"$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE_LINK'}\" border=0>");
		}
		if($FOX->{$GB->{FORM}->{bbs}}->{BBS_TITLE_PICTURE} =~/js/)
		{
			&Put1Line(*HTM, "<script src=$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE_PICTURE'}></script>");
		}
		else
		{
			&Put1Line(*HTM, "<img src=\"$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE_PICTURE'}\" border=0>");
		}
		if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE_LINK'})
		{
			&Put1Line(*HTM, "</a>");
		}
		&Put1Line(*HTM, "</div>");
	}
	else
	{
		&Put1Line(*HTM, "<div align=center>");
		if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE_LINK'})
		{
			&Put1Line(*HTM, "<a href=\"$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE_LINK'}\" border=0>");
		}
		&Put1Line(*HTM, "<font color=\"$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE_COLOR'}\"><h1>$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE'}</h1></font>");
		if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE_LINK'})
		{
			&Put1Line(*HTM, "</a>");
		}
		&Put1Line(*HTM, "</div>");
	}

	#--------�f���^�C�g��
	my @index_title1 = (
	qq|<table border=1 cellspacing=7 cellpadding=3 width=95% bgcolor=$FOX->{$GB->{FORM}->{bbs}}->{"BBS_MAKETHREAD_COLOR"} align=center>|,
	qq|<tr>|,
	qq|<td align=center>|,
	qq|<table border=0 cellpadding=1 width=100%>|,
	qq|<tr>|,
	qq|<td nowrap COLSPAN=2>|,
	qq|<font size=+1><b>$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE'}</b></font><br>|,
	qq|</td>|,
	qq|<td nowrap width=5% align=right valign=top>|,
	&IsReadHtml($GB) ? qq|<a href="javascript:switchReadJsMode();" style="background-color:dimgray;border:1px outset dimgray;color:palegreen;text-decoration:none;">read.cgi ���[�h�ؑ�</a>&nbsp; | : qq||,
	qq|<a href=#menu>��</a>|,
	qq|<a href=#1>��</a>|,
	qq|</td>|,
	qq|</tr>|,
	qq|<tr>|,
	qq|<td colspan=3>|
	);
	&PutLines(*HTM, @index_title1);

	# �uBBx���~�܂��Ă��܂��v�\��
	if(!$FOX->{BBM}) { &Put1Line(*HTM, "<font color=red size=+2>BBM ���~�܂��Ă��܂�</font><br>\n"); }
	if(!$FOX->{BBM2}) { &Put1Line(*HTM, "<font color=red size=+2>BBM2 ���~�܂��Ă��܂�</font><br>\n"); }
	if(!$FOX->{BBQ}) { &Put1Line(*HTM, "<font color=red size=+2>BBQ ���~�܂��Ă��܂�</font><br>\n"); }
	if(!$FOX->{BBX}) { &Put1Line(*HTM, "<font color=red size=+2>BBX ���~�܂��Ă��܂�</font><br>\n"); }
	if(!$FOX->{BBN}) { &Put1Line(*HTM, "<font color=red size=+2>BBN ���~�܂��Ă��܂�</font><br>\n"); }
	if(!$FOX->{BBY}) { &Put1Line(*HTM, "<font color=red size=+2>BBY ���~�܂��Ă��܂�</font><br>\n"); }
	if(!$FOX->{BBS}) { &Put1Line(*HTM, "<font color=red size=+2>BBS ���~�܂��Ă��܂�</font><br>\n"); }
	if(!$FOX->{BBR}) { &Put1Line(*HTM, "<font color=red size=+2>BBR ���~�܂��Ă��܂�</font><br>\n"); }
	if(!$FOX->{BBE}) { &Put1Line(*HTM, "<font color=red size=+2>BBE ���~�܂��Ă��܂�</font><br>\n"); }

	#--------�J�X�^���t���b�V���iflash.txt�j
	my $CUSTOM_FLASH_HTML =  "./flash.txt";
	if(open(READ, $CUSTOM_FLASH_HTML))
	{
		local $/;
		&Put1Line(*HTM, <READ>);
		close(READ);
	}

	#--------�J�X�^���w�b�_(���[�J�����[��)�ihead.txt�j
	my $CUSTOM_HEAD_HTML = $GB->{PATH} . "head.txt";
	if(open(READ, $CUSTOM_HEAD_HTML))
	{
		local $/;
		#&Put1Line(*HTM, "<center><font size=+2><b>���P�����{���B�B�B<a href=\"http://yy12.kakiko.com/emg2ch/\">��</a></b></font></center><p>");
		&Put1Line(*HTM, <READ>);
		close(READ);
	}

	#--------�V�K�X���b�h
	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_PASSWORD_CHECK'} eq "checked")
	{
		my @index_title2 = (
		qq|<br>|,
		qq|</td>|,
		qq|</tr>|,
		qq|<tr>|,
		qq|<td nowrap colspan=5 align=center>|,
		qq|</td>|,
		qq|</tr>|,
		qq|</table>|,
		qq|<b><a href=http://info.2ch.net/before.html>�������ޑO�ɓǂ�ł�</a> �b |,
		qq|<a href=http://info.2ch.net/guide/>�Q�����˂�K�C�h</a>|,
		qq|$FOX->{specialad} \| |,
		qq|<a href=\"http://info.2ch.net/guide/faq.html\">�e�`�p</a></b>|
		);
		&PutLines(*HTM, @index_title2);
	}
	else
	{
		my @index_title2 = (
		qq|<br>|,
		qq|</td>|,
		qq|</tr>|,
		qq|<tr>|,
		qq|<td nowrap align=right>|,
		qq|</td>|,
		qq|</tr>|,
		qq|</table>|,
		qq|<b><a href=http://info.2ch.net/before.html>�������ޑO�ɓǂ�ł�</a> �b |,
		qq|<a href=http://info.2ch.net/guide/>�Q�����˂�K�C�h</a> \| |,
		qq|<a href=\"http://info.2ch.net/guide/faq.html\">�e�`�p</a>|,
		qq|$FOX->{specialad}</b>|
		);
		&PutLines(*HTM, @index_title2);
	}

	#--------������y�[�W�����N
	# pageview.cgi�͔p�~����Ă���
	#use integer;
	#my $lp = $GB->{FILENUM} / $FOX->{$GB->{FORM}->{bbs}}->{"BBS_THREAD_NUMBER"};
	#if($GB->{FILENUM} != $lp * $FOX->{$GB->{FORM}->{bbs}}->{"BBS_THREAD_NUMBER"})
	#{
	#	$lp++;
	#}
	#if($lp > 1)
	#{
	#	&Put1Line(*HTM, "<a href=\"../test/pageview.cgi?page=$lp&bbs=$GB->{FORM}->{'bbs'}\">�Ō�̃y�[�W</a>");
	#}
	#if($GB->{FILENUM} > $FOX->{$GB->{FORM}->{bbs}}->{"BBS_THREAD_NUMBER"})
	#{
	#	&Put1Line(*HTM, "�@<a href=\"../test/pageview.cgi?page=2&bbs=$GB->{FORM}->{'bbs'}\">���̃y�[�W</a>");
	#}
	my @index_title3 = (
	qq|</td>|,
	qq|</tr>|,
	qq|<tr>|,
	qq|<td>|,
	qq|<font size=2>$FOX->{links}</font>|,
	qq|</td>|,
	qq|</tr>|,
	qq|</table><br>|
	);
	&PutLines(*HTM, @index_title3);

	#--------�L����
	my @index_ad = (
	qq|<table border=1 cellspacing=7 cellpadding=3 width=95% bgcolor=$FOX->{$GB->{FORM}->{bbs}}->{'BBS_MAKETHREAD_COLOR'} align=center>|,
	qq|<tr>|,
	qq|<td>|,
	qq|$FOX->{headad}|,
	qq|</tr>|,
	qq|</td>|,
	qq|</table>|,
	qq|$FOX->{putad}|
	);
	&PutLines(*HTM, @index_ad);

	#�X���b�h�f���o���p�Ƀt�@�C�����𒲐�
	my $menumin = $FOX->{$GB->{FORM}->{bbs}}->{"BBS_THREAD_NUMBER"};
	my $menumax = $FOX->{$GB->{FORM}->{bbs}}->{"BBS_MAX_MENU_THREAD"};
	if($GB->{FILENUM} < $FOX->{$GB->{FORM}->{bbs}}->{"BBS_THREAD_NUMBER"})
	{
		$menumin = $GB->{FILENUM};
	}
	if($GB->{FILENUM} < $FOX->{$GB->{FORM}->{bbs}}->{"BBS_MAX_MENU_THREAD"})
	{
		$menumax = $GB->{FILENUM};
	}

	#--------�X���b�h�ꗗ
	my @index_list = (
	qq|<a name="menu"></a>|,
	qq|<table border=1 cellspacing=7 cellpadding=3 width=95% bgcolor="$FOX->{$GB->{FORM}->{bbs}}->{"BBS_MENU_COLOR"}"align=center>|,
	qq|<tr>|,
	qq|<td>|,
	qq|<font size=2>|
	);
	&PutLines(*HTM, @index_list);

	#�X���b�h�ꗗ��f���o��
	# �ŏ���$menumin��
	for(my $SubCount = 1; $SubCount <= $menumin; $SubCount++)
	{
		my $file = @{$GB->{NEWSUB}}[$SubCount-1];
		chomp($file);
		$file =~ /^(\w+)\.dat<>(.*)/;
		my ($key, $value) = ($1, $2);
		# �����ł͖�������html�����Ȃ�(�{���ɕK�v�ɂȂ钼�O�܂ŕۗ�)
		#unless(-e "$GB->{TEMPPATH}$key.html")
		#{
		#	&MakeWorkFile($GB, $key);
		#}
		&Put1Line(*HTM, "<a href=\"../test/read.cgi/$GB->{FORM}->{'bbs'}/$key/l50\" target=\"body\">$SubCount:</a> <a href=\"#$SubCount\">$value</a>�@");
	}
	# ����ȍ~
	for(my $SubCount = $menumin + 1; $SubCount <= $menumax; $SubCount++)
	{
		my $file = @{$GB->{NEWSUB}}[$SubCount-1];
		chomp($file);
		$file =~ /^(\w+)\.dat<>(.*)/;
		my ($key, $value) = ($1, $2);
		&Put1Line(*HTM, "<a href=\"../test/read.cgi/$GB->{FORM}->{'bbs'}/$key/l50\" target=\"body\">$SubCount: $value</a>�@");
	}
	# �X���b�h�ꗗ(subback.html)�ւ̃����N
	&Put1Line(*HTM, "<div align=\"right\"><a href=\"subback.html\"><b>�X���b�h�ꗗ�͂�����</b></a></font></td></tr></table>");

	#--------�L����(��΂���̃X�y�[�X)
	# XXX ���̂� bbs-yakin.cgi �̒��ɂ���
	# ���̃T�u���[�`�����Ńt�@�C���n���h�����uHTM�v����
	# �v���؂茈�ߑł��Ă���̂ŗv����
	# ������͈����œn���悤�ɂ������������Ǝv�� -- 11/22/2005 by ��

	# IPv6.2ch.net��maido3�̃T�[�o�ł͂Ȃ��̂ŁA�L���͏o���Ȃ�
	if($ENV{SERVER_NAME} ne "ipv6.2ch.net")
	{
		&YakinCounterCode($GB->{FORM}->{bbs});
	}

	#--------�X���b�h��f���o��
	my $front = $menumin;
	my $next = 2;
	for(my $ancnum = 1; $ancnum <= $menumin; $ancnum++)
	{
		my $file = @{$GB->{NEWSUB}}[$ancnum-1];
		$file =~ /^(\w+)\.dat/;
		my ($key) = ($1);
		my @log = ();
		my $count = 0;#	�J��Ԃ��J�E���g
		
		# subject.txt�ɂ���̂ɁA�\����html���������ĂȂ�������
		# ����1�񎎂��Ă݂�A�Ƃ����̂��A100�񂮂炢����Ă݂�
		# (����������Ȃ��Ƃ�100�����m�����Aneet4vip�Ō��\���܂�������)
		for ($count = 1; $count <= 100; $count++)
		{
			open(IN, "$GB->{TEMPPATH}$key.html");
			@log = <IN>;
			close(IN);
			if(@log >= 2)
			{
				next;
			}
		}
		# ����ł����߂�������A���傤���Ȃ�����MakeWorkFile���āA
		# �����ǂݒ���
		if($count == 101)
		{
			&MakeWorkFile($GB, $key);
			open(IN, "$GB->{TEMPPATH}$key.html");
			@log = <IN>;
			close(IN);
		}
		# �X���̍ŏ��̂Ƃ���
		my $first = shift(@log);
		$first =~ s/\$ANCOR/$ancnum/g;
		$first =~ s/\$FRONT/$front/g;
		$first =~ s/\$NEXT/$next/g;
		&Put1Line(*HTM, "\n" . $first);
		# �X����html�{��
		&PutLines(*HTM, @log);
		# ������ɂ���������̓t�H�[��
		my @index_surefoot = (
		qq|<dd>|,
		qq|<form method=POST action="../test/bbs.cgi?guid=ON">|,
		qq|<input type=hidden name=bbs value=$GB->{FORM}->{'bbs'}>|,
		qq|<input type=hidden name=key value=$key>|,
		qq|<input type=hidden name=time value=$GB->{NOWTIME}>|,
		qq|<input type=submit value="��������" name="submit">|,
		qq| ���O�F	|,
		qq|<input type=text name=FROM size=19>|,
		qq| E-mail�F|,
		qq|<input type=text name=mail size=19>|,
		qq|<ul>|,
		qq|<textarea rows=5 cols=64 wrap=OFF name=MESSAGE></textarea><br>|,
		qq|<b>|,
		qq|<a href="../test/read.cgi/$GB->{FORM}->{'bbs'}/$key/">�S���ǂ�</a> |,
		qq|<a href="../test/read.cgi/$GB->{FORM}->{'bbs'}/$key/l50">�ŐV50</a> |,
		qq|<a href="../test/read.cgi/$GB->{FORM}->{'bbs'}/$key/-100">1-100</a> |,
		#qq|<a href="http://info.2ch.net/test/tb.cgi?__mode=list&tb_id=http://$ENV{'SERVER_NAME'}/test/read.cgi/$GB->{FORM}->{'bbs'}/$key">�֘A�y�[�W</a> |,
		qq|<a href="#menu">�̃g�b�v</a> <a href="$GB->{PATH}./index.html">�����[�h</a>|,
		qq|</b>|,
		qq|</ul>|,
		qq|</form>|,
		qq|</dl>|,
		qq|</td>|,
		qq|</tr>|,
		qq|</table><br>|
		);
		&PutLines(*HTM, @index_surefoot);
		$front++;
		if($front > $menumin)
		{
			$front = 1;
		}
		$next++;
		if($next > $menumin)
		{
			$next = 1;
		}
	}

	#--------�t�b�^�[�ŕ߂���
	&Put1Line(*HTM, "<center>");
	# pageview.cgi�͔p�~����Ă���
	#if($menumin < $menumax)
	#{
	#	&Put1Line(*HTM, "<a href=\"../test/pageview.cgi?page=2&bbs=$GB->{FORM}->{'bbs'}\"><font size=5><b>���̃y�[�W</b></font></a>");
	#}

	#--------�V�K�X���b�h�쐬�̂Ƃ���
	my @index_newthread1 = (
	qq|<table border=1 cellspacing=7 cellpadding=3 width=95% bgcolor=$FOX->{$GB->{FORM}->{bbs}}->{"BBS_MAKETHREAD_COLOR"} align=center>|,
	qq|<tr>|,
	qq|<td>|,
	qq|<form method=POST action="../test/bbs.cgi?guid=ON">|
	);
	&PutLines(*HTM, @index_newthread1);
	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_PASSWORD_CHECK'} eq "checked")
	{
		my @index_newthread2 = (
		qq|<br><input type=submit value="�V�K�X���b�h�쐬��ʂ�" name=submit>|,
		qq|<input type=hidden name=bbs value=$GB->{FORM}->{'bbs'}>|,
		qq|<input type=hidden name=time value=$GB->{NOWTIME}>|,
		qq|</td>|,
		qq|</tr>|,
		qq|</table>|,
		qq|</form>|,
		qq|</table>|
		);
		&PutLines(*HTM, @index_newthread2);
	}
	else
	{
		my @index_newthread2 = (
		qq|<td nowrap>|,
		qq|�^�C�g���F|,
		qq|<input type=text name=subject size=40>|,
		qq|<input type=submit value="�V�K�X���b�h�쐬" name=submit><br>|,
		qq|���O�F|,
		qq|<input type=text name=FROM size=19>|,
		qq| E-mail�F|,
		qq|<input type=text name=mail size=19><br>|,
		qq|���e�F|,
		qq|<textarea rows=5 cols=60 wrap=OFF name=MESSAGE></textarea>|,
		qq|<input type=hidden name=bbs value=$GB->{FORM}->{'bbs'}>|,
		qq|<input type=hidden name=time value=$GB->{NOWTIME}>|,
		qq|</td>|,
		qq|</tr>|,
		qq|</form>|,
		qq|</table>|
		);
		&PutLines(*HTM, @index_newthread2);
	}

	# �L��(footad)�Ƃ��������J�E���^�[
	# �ǂ̂悤�Ȍ`�̍폜�˗��ł���A�A�A
	# �o�[�W����(�ƍL��)
	my $foot = $FOX->{footad} . "<a href=http://count.2ch.net/?$GB->{FORM}->{'bbs'}><img src=http://count.2ch.net/ct.php/$GB->{FORM}->{'bbs'}  BORDER=0></a><br><b>�ǂ̂悤�Ȍ`�̍폜�˗��ł�����J�����Ă��������܂�</b><br>";
	&Put1Line(*HTM, "<br><br>$foot</center><br>");

	# �Ō�̕���
	&Put1Line(*HTM, "$GB->{version}");
	&Put1Line(*HTM, "<br>" . $FOX->{lastad});

	# �����܂�
	&Put1Line(*HTM, "</body></html>");

	#flock(HTM,8);
	close(HTM);

	&TryRename($INDEXtemp, $GB->{INDEXFILE});

	return 0;
}
#############################################################################
# �������݂܂�����\�����A����I������B
#############################################################################
sub endhtml
{
	my ($GB) = @_	;

	# �X���b�h924�̃G���[�����͂����ł���(�Ō�̍Ō�)
	# �ŋ��L���b�v�ł́A924�ɂ����X�\
	if($GB->{FORM}->{'key'} =~ /^924/ && !$GB->{STRONGCAP})
	{
		&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F���̃X���b�h�ɂ͏������߂܂���B");
	}

	if($GB->{TBACK})	{&TBacksuperEnd;}

	# �͂Ȃ�����N�b�L�[(���e���������ꍇ�̂ݑ���N�b�L�[)�𑗂�
	if(($GB->{COOKIES}{$GB->{PIN1}} || '') ne $GB->{PIN2})
	{
		# �N�b�L�[�̓g���b�N�o�b�N�łȂ�����������
		if(!$GB->{TBACK})
		{
			print "Set-Cookie: $GB->{PIN}; expires=$FOX->{COOKIEEXPIRES}; path=/\n";
		}
	}
	my $nana = "$FOX->{$GB->{FORM}->{bbs}}->{'BBS_NONAME_NAME'}";

	$nana =~ s/(\W)/'%' . unpack('H2', $1)/eg;

	print "Set-Cookie: PREN=$nana; expires=$FOX->{COOKIEEXPIRES}; path=/\n";

	print "Content-type: text/html; charset=shift_jis\n\n";
	#-----------------------------------------------------------------------
if($ENV{'HTTP_USER_AGENT'} =~ /iPhone/)
{
	print <<EOF;
<html lang="ja">
<head>
<title>�������݂܂����B</title>
<meta http-equiv="Content-Type" content="text/html; charset=shift_jis">
<meta name="viewport" content="width=device-width,initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.6,user-scalable=yes" />
</head>
<body>�������݂��I���܂����B(iPhone)<br><br>
�����Ŗ߂��Ă���B<br><br>
<br><br><br><br><br>
<center>
</center>
</body>
</html>
EOF
}
else
{
	print <<EOF;
<html lang="ja">
<head>
<title>�������݂܂����B</title>
<meta http-equiv="Content-Type" content="text/html; charset=shift_jis">
<meta content=5;URL=$GB->{INDEXFILE} http-equiv=refresh>
</head>
<body>�������݂��I���܂����B<br><br>
��ʂ�؂�ւ���܂ł��΂炭���҂��������B<br><br>
<br><br><br><br><br>
<center>
</center>
</body>
</html>
EOF
}

#<img width=160 height=120 src="http://www2.2ch.net/img/Hello-502index.gif" border=1 alt="Hello 502">
	#<br><br>$FOX->{putad}
	#�����܁[��!!
	exit;
}
#############################################################################
#�@�V�K�X���b�h�ʉ��
#############################################################################
sub newbbs
{
	my ($GB) = @_;
	print "Content-type: text/html; charset=shift_jis\n\n";

	my @newbbshtml1 = (
	qq|<html lang="ja">|,
	qq|<head>|,
	qq|<meta http-equiv="Content-Type" content="text/html; charset=x-sjis">|,
	#�N�b�L�[���������邽�߂� JavaScript
	qq|<script type="text/javascript" src="http://www2.2ch.net/snow/index.js" defer></script>|,
	qq|<title>$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE'}</title>|,
	qq|</head>|,
	qq|<body text="$FOX->{$GB->{FORM}->{bbs}}->{"BBS_TEXT_COLOR"}" BGCOLOR="$FOX->{$GB->{FORM}->{bbs}}->{"BBS_BG_COLOR"}" link="$FOX->{$GB->{FORM}->{bbs}}->{"BBS_LINK_COLOR"}" alink="$FOX->{$GB->{FORM}->{bbs}}->{"BBS_ALINK_COLOR"}" vlink="$FOX->{$GB->{FORM}->{bbs}}->{"BBS_VLINK_COLOR"}" background="$FOX->{$GB->{FORM}->{bbs}}->{"BBS_BG_PICTURE"}">|
	);
	print @newbbshtml1;

	#--------�^�C�g���摜
	if($FOX->{$GB->{FORM}->{bbs}}->{BBS_TITLE_PICTURE})
	{
		print "<div align=center>";
		if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE_LINK'})
		{
			print "<a href=\"$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE_LINK'}\" border=0>";
		}
		print "<img src=\"$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE_PICTURE'}\" border=0>";
		if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE_LINK'})
		{
			print "</a>";
		}
		print "</div>";
	}
	else
	{
		print "<div align=center>";
		if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE_LINK'})
		{
			print "<a href=\"$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE_LINK'}\" border=0>";
		}
		print "<font color=\"$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE_COLOR'}\"><h1>$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE'}</h1></font>";
		if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE_LINK'})
		{
			print "</a>";
		}
		print "</div>";
	}

	#--------�f���^�C�g��
	my @newbbshtml2 = (
	qq|<br>|,
	qq|<table border=1 cellspacing=7 cellpadding=3 width=95% bgcolor=$FOX->{$GB->{FORM}->{bbs}}->{"BBS_MAKETHREAD_COLOR"} align=center>|,
	qq|<tr>|,
	qq|<td align="center">|,
	qq|<form method=POST action="../test/bbs.cgi?guid=ON">|,
	qq|<table border="0" cellpadding="1" width="100%">|,
	qq|<tr>|,
	qq|<td nowrap colspan="3">|,
	qq|<font +1><b>$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE'}</b></font><br>|,
	qq|</td>|,
	qq|</tr>|,
	qq|<tr>|,
	qq|<td colspan="4">|
	);
	print @newbbshtml2;

	#--------�J�X�^���w�b�_(���[�J�����[��)�ihead.txt�j
	my $CUSTOM_HEAD_HTML = "$GB->{PATH}head.txt";
	if(open(READ, $CUSTOM_HEAD_HTML))
	{
		local $/;
		print <READ>;
		close(READ);
	}

	#--------�V�K�X���b�h
	my @newbbshtml3 = (
	qq|<br>|,
	qq|</td>|,
	qq|</tr>|,
	qq|<tr>|,
	qq|<td nowrap align="right">|,
	qq|�^�C�g���F|,
	qq|</td>|,
	qq|<td>|,
	qq|<input type="text" name="subject" size="40">|,
	qq|</td>|,
	qq|<td>|,
	qq|<input type=submit value="�V�K�X���b�h�쐬" name="submit">|,
	qq|</td>|,
	qq|</tr>|,
	qq|<tr>|,
	qq|<td nowrap align="right">|,
	qq|���O�F|,
	qq|</td>|,
	qq|<td nowrap colspan="2">|,
	qq|<input type=text name=FROM size=19> E-mail�F|,
	qq|<input type=text name=mail size=19>|,
	qq|</td>|,
	qq|</tr><tr>|,
	qq|<td nowrap align="right" valign="top">|,
	qq|���e�F|,
	qq|</td>|,
	qq|<td colspan="3">|,
	qq|<textarea rows=5 cols=60 wrap=OFF name=MESSAGE></textarea>|,
	qq|<input type=hidden name=bbs value=$GB->{FORM}->{'bbs'}>|,
	qq|<input type=hidden name=time value=$GB->{NOWTIME}>|,
	qq|</td>|,
	qq|</tr>|,
	qq|</table>|,
	qq|<b><a href="http://info.2ch.net/before.html">�������ޑO�ɓǂ�ł�</a> �b <a href="http://info.2ch.net/guide/">�Q�����˂�K�C�h</a>$FOX->{specialad}</b><br><br>|,
	qq|</form>|,
	qq|</td>|,
	qq|</tr>|,
	qq|</table><br>|,
	qq|</body>|,
	qq|</html>|
	);
	print @newbbshtml3;

	# ��ʂ�\��������exit
	exit;
}
#############################################################################
#�@�V�K�X���b�h�u���b�N
#############################################################################
#sub subbbs
#{
#	my ($GB) = @_	;
#
#	my $msg = $GB->{FORM}->{'MESSAGE'};
#	my $sbj = $GB->{FORM}->{'subject'};
#	$msg =~ s/<[Bb][Rr]>/\n/g;
#	$msg =~ s/&/&amp;/g;
#	$msg =~ s/"/&quot;/g;
#	$sbj =~ s/&/&amp;/g;
#	$sbj =~ s/"/&quot;/g;
#
#	print "Content-type: text/html; charset=shift_jis\n\n";
#	print <<EOF;
#<html>
#<head>
#<meta http-equiv="Content-Type" content="text/html; charset=x-sjis">
#<TITLE>$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE'}</TITLE>
#</HEAD><body bgcolor="#FFFFFF">
#<font size=+1 color=#FF0000>�������݊m�F�B</font><br><br>
#�������݂Ɋւ��ėl�X�ȃ��O��񂪋L�^����Ă��܂��B<br>
#�����Ǒ��ɔ�������A���l�ɖ��f�������鏑�����݂͍T���ĉ�����<br>
#	<form method=POST action="../test/subbbs.cgi">
#	�^�C�g���F$GB->{FORM}->{'subject'}
#		<input type="hidden" name="subject" value="$sbj" size="40"><br>
#	���O�F$GB->{FORM}->{'FROM'}
#		<INPUT TYPE=hidden NAME=FROM SIZE=19 value="$GB->{FORM}->{'FROM'}"><br>
#	E-mail �F $GB->{FORM}->{'mail'}
#		<INPUT TYPE=hidden NAME=mail SIZE=19 value="$GB->{FORM}->{'mail'}"><br>
#	���e�F<ul>$GB->{FORM}->{'MESSAGE'}
#		<input type=hidden name=MESSAGE value="$msg"></ul>
#<br>
#<input type=hidden name=bbs value=$GB->{FORM}->{'bbs'}>
#<input type=hidden name=time value=$GB->{NOWTIME}>
#<input type=submit value="�S�ӔC�𕉂����Ƃ��������ď�������" name="submit"><br>
#</form>
#�ύX����ꍇ�͖߂�{�^���Ŗ߂��ď��������ĉ������B<br>
#
#EOF
#	exit;
#}
#############################################################################
#index.html�쐬�p�t�@�C�����쐬
# ����: $GB, �ΏۂƂȂ�dat�̃L�[$key
# $key��$GB->{FORM}->{'key'}�������������ꍇ�AGetDatInfo�œǂ񂾂��̂��g����
#############################################################################
sub MakeWorkFile
{
	my ($GB, $key) = @_;
	my $workfile = $GB->{TEMPPATH} . $key . ".html";
	my (@messx, @content);
	my ($mailto, $time, $brmax, $topnum, $firstlog, $name, $mail, $subject, $message);
	my $datnum = 0;	# ����dat�̍s��
	# �ΏۂƂȂ�dat�ɑ΂��AMakeWorkFile����$GB�̂悤�Ɏg����ϐ�
	# $key��$GB->{FORM}->{'key'}���Ⴄ���Ɏg�p����
	my $TMPGB = {};

$GB->{DEBUG} .= "IN MakeWorkFile($key) file=$workfile<br>";

	# ����������dat�ƃL�[���Ⴄ���ǂ����𒲂ׂ�
	if($GB->{FORM}->{'key'} != $key)
	{
		# �L�[��������ꍇ�A�K�v�� $TMPGB ����������
		# GetDatInfo �̑O�ɁA����炪�Z�b�g����ĂȂ��Ƃ����Ȃ�
		$TMPGB->{NEWTHREAD} = 0;
		$TMPGB->{DATPATH} = $GB->{DATPATH};
		$TMPGB->{FORM}->{bbs} = $GB->{FORM}->{bbs};
		$TMPGB->{DAT1} = "";
		$TMPGB->{DATNUM} = 0;
		$TMPGB->{DATLAST} = ();

		# $TMPGB �� dat �̏���ǂݍ���
		&GetDatInfo($TMPGB, $key);

		# ����Ă����l���Z�b�g����
		$firstlog = $TMPGB->{DAT1};
		$datnum = $TMPGB->{DATNUM};
		@content = @{$TMPGB->{DATLAST}};
	}
	else
	{
		# �L�[�������ꍇ�A���ɂ�����̂��Z�b�g����
		$firstlog = $GB->{DAT1};
		$datnum = $GB->{DATNUM};
		@content = @{$GB->{DATLAST}};
	}

	# ��L�����ɂ��A
	#  $firstlog��dat��>>1�̗v�f
	#  $datnum�ɊY������dat�̍s��
	#  @content�ɊY������dat�̍ŐV���X��
	# ��������

	#���s�J�b�g
	chomp($firstlog);

	#>>1�̗v�f�����H����
	($name,$mail,$time,$message,$subject) = split(/<>/,$firstlog);

$GB->{DEBUG} .= "MakeWorkFile($key) file=$workfile<br>";
	open(SHTM,">$workfile");	#���O�e���|�������J��
#	flock(SHTM,2);

	#�T�u�W�F�N�g�e�[�u��(�X���^�C�̃A���J�[�̂Ƃ���)��f���o��
	my @subjecttable = (
	qq|<table border=1 cellspacing=7 cellpadding=3 width=95% bgcolor="$FOX->{$GB->{FORM}->{bbs}}->{"BBS_THREAD_COLOR"}" align=center>|,
	qq|<tr>|,
	qq|<td>|,
	qq|<dl class="thread">|,
	qq|<a name="\$ANCOR"></a>|,
	qq|<div align="right"><a href ="#menu">��</a>|,
	qq|<a href="#\$FRONT">��</a>|,
	qq|<a href="#\$NEXT">��</a>|,
	qq|</div>|,
	qq|<b>�y\$ANCOR:$datnum�z<font size=5 color="$FOX->{$GB->{FORM}->{bbs}}->{'BBS_SUBJECT_COLOR'}">$subject</font></b>|
	);
	&PutLines(*SHTM, @subjecttable);

	#>>1�̃n�C�p�[�����N�쐬�Ɠf���o��
	#-----------------------------------------------------------------------

	# http:// �����n�C�p�[�����N�ɂ���
	$message = &MakeHyperLink($GB, $message);

	# ���O����mailto:�̃����N����������
	$mailto = &MakeMailto($GB, $mail, $name);

	#BE:�̃����N�����
	#$time =~ s/BE:(\d+)-([^ ]*)/<a href="javascript:be($1);">?$2<\/a>/;
	$time =~ s{BE:(\d+)-(.*)$}{<a href="javascript:be($1);">?$2</a>};

	#>>1��f���o��
	&Put1Line(*SHTM, "<dt>1 ���O�F$mailto $time<dd>$message <br><br><br>");

	#�ŐVBBS_CONTENTS_NUMBER�̃��X�̃n�C�p�[�����N�쐬�Ɠf���o��
	#-----------------------------------------------------------------------

	#���O������A�\���R���e���c���`�F�b�N
	if($datnum > $FOX->{$GB->{FORM}->{bbs}}->{"BBS_CONTENTS_NUMBER"})
	{
		$topnum = $datnum - ($FOX->{$GB->{FORM}->{bbs}}->{"BBS_CONTENTS_NUMBER"} - 1);
	}
	else
	{
		$topnum = 2;
	}

	# �ŐV���X���������
	foreach(@content)
	{
		chomp;	#���s���J�b�g

		#�v�f�����H����
		($name,$mail,$time,$message,$subject) = split(/<>/);

		unless($_)
		{
			$topnum++;
			next;
		}

		# http:// �����n�C�p�[�����N�ɂ���
		$message = &MakeHyperLink($GB, $message);

		# ���O����mailto:�̃����N����������
		$mailto = &MakeMailto($GB, $mail, $name);

		#BE:�̃����N�����
		#$time =~ s/BE:(\d+)-([^ ]*)/<a href="javascript:be($1);">?$2<\/a>/;
		$time =~ s{BE:(\d+)-(.*)$}{<a href="javascript:be($1);">?$2</a>};
		#�f���o��
		&Put1Line(*SHTM, "<dt>$topnum ���O�F$mailto �F$time<dd>");

		#�u�ȗ�����܂����v�̏���
		my @messx = split(/<br>/,$message);	#���b�Z�[�W���s�ŃJ�b�g
		my $messy = @messx;			#�s�����v�Z
		# BBS_LINE_NUMBER��葽���A�ȗ��K�v
		if($messy > $FOX->{$GB->{FORM}->{bbs}}->{"BBS_LINE_NUMBER"})
		{
			my $messz = join('<br>',@messx[0 .. $FOX->{$GB->{FORM}->{bbs}}->{'BBS_LINE_NUMBER'}-1]);
			&Put1Line(*SHTM, "$messz <br>");
			&Put1Line(*SHTM, "<font color=\"$FOX->{$GB->{FORM}->{bbs}}->{'BBS_NAME_COLOR'}\">�i�ȗ�����܂����E�E�S�Ă�ǂނɂ�<a href=\"../test/read.cgi/$GB->{FORM}->{'bbs'}/$key/$topnum\" target=\"_blank\">����</a>�������Ă��������j</font><br>");
		}
		# �ȗ��s�v
		else
		{
			my $messz = join('<br>',@messx[0 .. $messy-1]);
			&Put1Line(*SHTM, "$messz <br>");
		}

		$topnum++;
		# �Ō��<br>���o�͂��Ă����܂�
		&Put1Line(*SHTM, "<br>\n");
	}

	#-----------------------------------------------------------------------

#	flock(SHTM,8);
	close(SHTM);

	# �p�[�~�b�V���������͕s�v
	#chmod(0666,$workfile);
}
#############################################################################
# ���������URI��T���āA�n�C�p�[�����N�ɂ���
# ����: $GB, $message
# �߂�l: ���H���$message
#############################################################################
sub MakeHyperLink
{
	my ($GB, $message) = @_;

	#https/ftp�͉��L�����Ɋ֌W�Ȃ�������
	#https://��ftp://�̏�����Saborin�t���O�������Ă����炳�ڂ�
	if(!$GB->{SABORIN})
	{
		$message =~ s/(https|ftp)\:\/\/([\w|\:\!\#\$\%\=\&\-\^\`\\\|\@\~\[\{\]\}\;\+\*\,\.\?\/]+)/<a href="$1:\/\/$2" target="_blank">$1:\/\/$2<\/a>/g;
	}
	#http�̏ꍇ
	if($message =~ /2ch\.net/ || $message =~ /bbspink\.com/)
	{
	
	#	$message =~ s/http\:\/\/img\.2ch\.net/sssp\:\/\/img\.2ch\.net/g;

		#2ch/bbspink���͒�����
		$message =~ s/http\:\/\/([\w|\:\!\#\$\%\=\&\-\^\`\\\|\@\~\[\{\]\}\;\+\*\,\.\?\/]+)/<a href="http:\/\/$1" target="_blank">http:\/\/$1<\/a>/g;
	}
	elsif($message =~ /maido3\.com/)
	{
		#maido3.com�͒�����
		$message =~ s/http\:\/\/([\w|\:\!\#\$\%\=\&\-\^\`\\\|\@\~\[\{\]\}\;\+\*\,\.\?\/]+)/<a href="http:\/\/$1" target="_blank">http:\/\/$1<\/a>/g;
	}
	else
	{
		#�O�������N
		if($ENV{'SERVER_NAME'} =~ /bbspink\.com/)
		{
			#bbspink��pinktower�o�R
			$message =~ s/http\:\/\/([\w|\:\!\#\$\%\=\&\-\^\`\\\|\@\~\[\{\]\}\;\+\*\,\.\?\/]+)/<a href="http:\/\/pinktower.com\/$1" target="_blank">http:\/\/$1<\/a>/g;
		}
		else
		{
			#2ch��ime.nu�o�R
			$message =~ s/http\:\/\/([\w|\:\!\#\$\%\=\&\-\^\`\\\|\@\~\[\{\]\}\;\+\*\,\.\?\/]+)/<a href="http:\/\/ime.nu\/$1" target="_blank">http:\/\/$1<\/a>/g;
		}
	}

	# sssp�̏���(BE�̃A�C�R��)
	$message =~ s/sssp\:\/\/img\.2ch\.net\/([\w|\:\!\#\$\%\=\&\-\^\`\\\|\@\~\[\{\]\}\;\+\*\,\.\?\/]+)/<img src="http:\/\/img\.2ch\.net\/$1">/g;

	#$message =~ s/sssp/http/g;
			
	return $message;
}
#############################################################################
# ���O�̂Ƃ����mailto:�����N�����
# ����: $GB, $mail: ���[���A�h���X, $name: ���O
# �߂�l: �ł������O���̕�����
#############################################################################
sub MakeMailto
{
	my ($GB, $mail, $name) = @_;
	my $mailto = "";

	#���[�����ɓ��͂�����ꍇ�Amailto:�̃����N�ɂ���
	if($mail ne "")
	{
		$mailto = "<a href=\"mailto:$mail \"><b>$name </b></a>";
	}
	else
	{
		$mailto = "<font color=$FOX->{$GB->{FORM}->{bbs}}->{'BBS_NAME_COLOR'}><b>$name </b></font>";
	}

	return $mailto;
}
#############################################################################
# �X�����ċK���`�F�b�N
# IN: �Ȃ�
# OUT: 0 �X���[ 1 �񐶒�
#############################################################################
sub Check_SURETATE
{
	my ($GB) = @_	;

	#�ȉ��̔͂���[
	if(&KiseiOFF($GB))			{return 0;}
#	if($GB->{FORM}->{'bbs'} eq "campus")	{return 0;}

	# ���̓X���[
		if(!$FOX->{$GB->{FORM}->{bbs}}->{"BBS_BE_TYPE2"} && $GB->{MARU})			{return 0;}

	# ���̓X���[
	if($GB->{CAP})				{return 0;}

	#����p2�͈ȉ��̔X�����ĕs��
	if($GB->{P22CH})
	{
		if($GB->{FORM}->{'bbs'} eq "slot")	{&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F���̔�p2�ł̃X�����Ă͏o���Ȃ��̂��B");}
	}

	# ����D��
	#if($GB->{FORM}->{'bbs'} eq "news" || $GB->{FORM}->{'bbs'} eq "poverty")
	#{
	#	if(!$GB->{P22CH} && $GB->{KABUU} && $GB->{BEpoints} > 3000)	{return 0;}
	#}
	#else
	#{
	#	if(!$GB->{P22CH} && $GB->{KABUU})	{return 0;}
	#}

	# �ȉ��A��L�̗D���[�u���󂯂Ȃ��ꍇ

	# Type2��be�K�{
	if($FOX->{$GB->{FORM}->{bbs}}->{"BBS_BE_TYPE2"})
	{
		if(!$GB->{isBE})
		{
			&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�FBe���O�C�����Ă�������(t)�B<a href=\"http://be.2ch.net/\">be.2ch.net</a>");
		}
	}

#			$GB->{FORM}->{'MESSAGE'} = 'sssp://img.2ch.net/ico/' . $GB->{icon} .' <br>'. $GB->{FORM}->{'MESSAGE'} ;


	# Type2��Be�|�C���g������Ȃ��ƃX�����ĕs��
	if($FOX->{$GB->{FORM}->{bbs}}->{"BBS_BE_TYPE2"})
	{
		# 1000 �|�C���g�ȏ�Ȃ��Ƃ���
		my $pointlimit = 1000;

		# news ���� 6000 �|�C���g
		if($GB->{FORM}->{'bbs'} eq 'news')	{$pointlimit = 18000;}
#		if($GB->{FORM}->{'bbs'} eq "poverty")	{$pointlimit =  3000;}

		if($GB->{BEpoints} < $pointlimit)
		{
			&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�FBe�|�C���g������܂���B($pointlimit)");
		}
	}


	# Type2�̓|�C���g���T�Ώێ҂͖������ɃX�����ĉ\
	#�Ƃ肠�����A�S�ɂ��Ă݂�̊��B
	if($FOX->{$GB->{FORM}->{bbs}}->{"BBS_BE_TYPE2"})
	{
		# news ����
		if($GB->{FORM}->{'bbs'} eq 'news')
		{
			# BE�u�u���b�N���X�g�v�ɂȂ��ꍇ�ɂ̂ݓ��T�𗘗p�\
			if(!&Check_BEBlack($GB))
			{
				if($GB->{BELucky})		{return 0;}
			}
		}
	}

	# �����z�Ȃ��̂̓X�����ĕs��
	my $remo = $GB->{HOST29}	; #�����郊���z
	my $ipip = $ENV{REMOTE_ADDR}	;
	if($remo eq $ipip)	{&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�X�����Ắ����g���Əo���܂���B");}

	# �g�тƌ���p2�ł́A����L�^����
	my $kiroku = "";
#	if($GB->{KEITAI})	{ $kiroku = "$GB->{HOST}($GB->{IDNOTANE})"; }
#	elsif($GB->{KEITAIBROWSER})
#				{ $kiroku = "$GB->{HOST}($GB->{IDNOTANE})"; }
#	elsif($GB->{P22CH})	{ $kiroku = "$GB->{HOST}($GB->{IDNOTANE})"; }
#	else			{ $kiroku = "$GB->{HOST}($GB->{MARU})"; }

	if($GB->{KEITAI})	{ $kiroku = "$GB->{IDNOTANE}"; }
	elsif($GB->{KEITAIBROWSER})
				{ $kiroku = "$GB->{HOST}($GB->{IDNOTANE})"; }
	elsif($GB->{P22CH})	{ $kiroku = "P2-$GB->{IDNOTANE}"; }
	else			{ $kiroku = "$GB->{HOST}"; }

	my $IP_number = 0;

	if($GB->{IPv6})
	{
		use Net::IP;
		my $ip = new Net::IP($ENV{REMOTE_ADDR});
		$IP_number = $ip->intip();
		# ��64bit�ɂ���A�����I�ɂ�48bit( >> 80 )�ł���������
		$IP_number = $IP_number >> 64;
	}
	else
	{
		# IP �A�h���X���琔�����擾(�E�́E)�j���j�� 65025 �ʂ�
#		$IP_number = eval { $ENV{REMOTE_ADDR} =~ s/^(\d+)\.(\d+)/return $1 * $2/e };
#		$IP_number = eval { $ENV{REMOTE_ADDR} =~ s/^(\d+)\.(\d+)/return $2/e };
		$IP_number = eval { $ENV{REMOTE_ADDR} =~ s/^(\d+)\.(\d+)/return ($1 % 4) * 256 + $2/e };
	}

	my $ripfile = "$GB->{WPATH}RIP.cgi";

	# ���X�g�����p�o�b�t�@�݂����Ȃ́B
	my @diff_list = ();
	push @diff_list, sprintf qq|%s,%s,%d\n|, $IP_number, $kiroku, $GB->{FORM}->{key};

	# �Ⴞ��܂ł�bbsd�ɖ₢���킹��
	if(IsSnowmanServer)
	{
		my $cmd = 'chkthr';
		my $rcode = bbsd($GB->{FORM}->{bbs}, $cmd, 'RIP.cgi', $IP_number, $kiroku, 'dummy');
		# �^�C���A�E�g���ǂ����`�F�b�N
		if(&bbsd_TimeoutCheck($GB, $rcode))
		{
			&bbsd_TimeoutError($GB, $cmd);
		}
		# ��������(�󕶎���ȊO)�A����
		if($rcode ne '')
		{
			return 1;
		}
	}
	# �ʏ�T�[�o�ł̓��X�g��ǂ�Ń}�b�`���O����
	else
	{
		# �X�����ċK�����X�g�ǂݍ���
		local *Deny_list;
		open   Deny_list, '<', $ripfile; # $ripfile �̓O���[�o������
		my @Deny = <Deny_list>;
		close Deny_list;
	
		# IP �A�h���X�ŏ���
		# ���X�g���猟���B���݂���� 1 ��Ԃ��Ă΂��΂��B
		foreach (@Deny){
			return 1 if $IP_number == (split /,/)[0];
		}
	
		# �X���[�Ȃ̂ŃX�����ċK�����X�g�ɓo�^
		if (@diff_list) {
			unshift @Deny, @diff_list;
			splice  @Deny, $FOX->{$GB->{FORM}->{bbs}}->{'BBS_THREAD_TATESUGI'};
	
			# �X�����ċK�����X�g�̍X�V
			open  Deny_list, '>', "$ripfile.tmp"; # �ꎞ�t�@�C���ɏ����o��
			print Deny_list @Deny;
			close Deny_list;
			&TryRename("$ripfile.tmp", $ripfile); # �t�@�C���������ɖ߂�
		}
	}

	return 0; # �X���[����
}
#############################################################################
# BE �̏����u���b�N���X�g�ɓo�^����
# ����: �u���b�N���X�g�̃t�@�C�����A�o�^���
# �߂�l: 0: �o�^�����A1: ������������
#############################################################################
sub Record_BEBlack
{
	my ($recordfile, $dmdm) = @_;

	# �Ⴞ��܃T�[�o�ł͉������Ȃ�(�Q�Ǝ��ɓo�^����邽��)
	if(IsSnowmanServer)	{return 0;}

	if(open(REC, ">>$recordfile"))
	{
		print REC $dmdm, "\n";
		close(REC);
	}
	else
	{
		return 1;
	}

	return 0;
}
#############################################################################
# BE �́u�u���b�N���X�g�v���ւ̓o�^�E�`�F�b�N
# �Ⴞ��܂ł́Abbsd ��DB�ɋL�^����
# ����: $GB
# �߂�l: 0: �o�^�Ȃ��A1: �u���b�N���X�g�o�^����
#############################################################################
sub Check_BEBlack
{
	my ($GB) = @_;
	my $dmdm = $GB->{FORM}->{'DMDM'};	# email address
	my $recordfile = "./book/.RIP_BE.cgi";
	my @badbe = ();
	my $match = 0;

	# �|�C���g���T�̎��͋L�^���Ȃ�
	if($GB->{BELucky})		{return 0;}

	# �Ⴞ��܂ł͂Ȃ�������
	# �Ⴞ��܂̎��́A���̉��̃��b�N�A�b�v�ŐV�K�o�^�����
	if(!IsSnowmanServer)
	{
		# �t�@�C�����Ȃ����A�L�^���Ė߂�
		if(!(-e $recordfile))
		{
			&Record_BEBlack($recordfile, $dmdm);
			return 0;
		}
	}

	# �t�@�C�������鎞�A���g���}�b�`���O����
	# �Ⴞ��܂ł�bbsd�ɖ₢���킹��
	if(IsSnowmanServer)
	{
		my $errmsg = "";
		my $statnum = 0;
		my $cmd = 'chkid';
		$errmsg = bbsd_db($GB->{FORM}->{'bbs'}, $cmd, 'beblack', $dmdm, 3600, 1, 1, 'dummy');
		# �^�C���A�E�g���ǂ����`�F�b�N
		# �^�C���A�E�g��������X���[����
		if(&bbsd_TimeoutCheck($GB, $errmsg))
		{
			return 0;
		}

		# ���ʂ�؂�o��
		$statnum = (split(/,/, $errmsg))[0];

		# �o�^����������A�E�g
		if($statnum != 0)	{return 1;}
		# �o�^���Ȃ���΃X���[����
		return 0;
	}
	else
	{
		open(REC, $recordfile);
		@badbe = <REC>;
		close(REC);
		foreach(@badbe)
		{
			chomp;
			if($_ eq $dmdm)
			{
				$match = 1;
				next;
			}
		}
	}

	# �}�b�`�����ꍇ
	if($match)			{return 1;}

	# �}�b�`���Ȃ��ꍇ�A�P�ɋL�^���Ă����܂�
	&Record_BEBlack($recordfile, $dmdm);
	return 0;
}
#############################################################################
# �X�����ăX�s�[�h�`�F�b�N 0: ok 1:�X�s�[�h�ᔽ
#############################################################################
sub Check_Speed
{
	my ($GB) = @_		;

return 0;
#�P�p���Ă݂�

	#�Ⴞ��܂̓X���[(bbsd�ւ�API�g���Ď����ł���Ǝv�����ǁA���͂��Ȃ�)
	if(IsSnowmanServer)		{return 0;}
	# news4vip��news�ȊO�̓X���[
	#if($GB->{FORM}->{'bbs'} ne 'news4vip'
	#&& $GB->{FORM}->{'bbs'} ne 'news')	{return 0;}
	# �Ǘ��l�̎w�߂ɂ��news4vip�̂̂�т���� -- 2005/11/18 by ��
	if($GB->{FORM}->{'bbs'} ne 'news')	{return 0;}
	#���̓X���[
	if($GB->{CAP})				{return 0;}

	#���̓X���[
	if($GB->{MARU})				{return 0;}

	my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($GB->{NOWTIME});
	if($min < 3)	{return 1;}	# �����O���܂ł̓X�����ĕs��

	my $vaio = "./book/.A_B_C.cgi";
	if(!(-e $vaio))			# ���߂ẴX������
	{
		open(YAN1,">>$vaio");print YAN1 "1";close(YAN1);
		return 0;
	}

	my $prmtime = (local $_=stat($vaio)) ? $_->mtime : 0;
	my $keika = $GB->{NOWTIME} - $prmtime	;
	$keika /= 60			;	# ���ɂ���
	# �Ǘ��l�̎w���ɂ��R�����g�A�E�g -- 2005/11/15 by ��
	#if($GB->{FORM}->{'bbs'} ne 'news')
	#{
	#	if($keika < 15)	{return 1;}	# N���Ԃ͂���
	#}
	if($keika < 1)	{return 1;}		# N���Ԃ͂���

	open(YAN1,">>$vaio");print YAN1 "1";close(YAN1);

	return 0; # �X���[����
}
#######################################################################
# �̃X���b�h�������E�l�𒴂��Ă��Ȃ����`�F�b�N����
#######################################################################
sub mumumuThreadNumExceededCheck
{
	my ($GB) = @_;
	my $num = 0;
	my $exceed = 96;	#���̐��𒴂���X�����͋֎~
	my @dir;

	#���̓X���[
	if($GB->{MARU})			{ return 0; }

	#�X���b�h���𐧌��������Ȃ��ꍇ�̓X���[
	if(!&IsThreadLimitIta($GB))	{ return 0; }

	# livejupiter��192�܂�
	if($GB->{FORM}->{'bbs'} eq 'livejupiter') { $exceed = 192; }
	# livevenus��192�܂�
	if($GB->{FORM}->{'bbs'} eq 'livevenus')	{ $exceed = 192; }
	# eq/eqplus��128�܂�
	if($GB->{FORM}->{'bbs'} eq 'eq')	{ $exceed = 128; }
	if($GB->{FORM}->{'bbs'} eq 'eqplus')	{ $exceed = 128; }

	## ������������ ##

	# dat�̐��𒲂ׂ�
	# �Ⴞ��܂ł�bbsd�ɖ₢���킹��
	if (IsSnowmanServer)
	{
		my $cmd = 'getndats';
		$num = bbsd($GB->{FORM}->{'bbs'}, $cmd, 'dummy'); 
		# �^�C���A�E�g���ǂ����`�F�b�N
		if(&bbsd_TimeoutCheck($GB, $num))
		{
			&bbsd_TimeoutError($GB, $cmd);
		}
	}
	else
	{
		# dat�f�B���N�g�����J��(���߂Ȃ�-1)
		if (!opendir(DIR, $GB->{DATPATH}))	{ return -1; }

		# dat�f�B���N�g����ǂݍ��݁A���𒲂ׂ�
		@dir = readdir(DIR);
		closedir(DIR);

		# readdir() �́A"." ".." �����邽�߁A
		# �z��̍ŏI�Y������1���������l��dat�̐��ƂȂ�
		$num = $#dir - 1;
	}

	#���E�l���z���鐔�̃X���b�h����������^
	if ($num > $exceed)	{return 1;}
	else			{return 0;}
}
#############################################################################
# /i/index.html ���쐬���邩�ǂ���
#############################################################################
sub MakeIndex4Keitai296
{
	if($ENV{'SERVER_NAME'} =~ /bbspink\.com/)	{return 1;}
	if($ENV{'SERVER_NAME'} =~ /qb/)			{return 1;}
	if($ENV{'SERVER_NAME'} =~ /dso/)		{return 1;}
	return 0;
}
#############################################################################
# /i/index.html ���쐬����
#############################################################################
sub MakeIndex4Keitai
{
	my ($GB) = @_;

	# qb�n�Adso�Abbspink.com �ȊO�̃T�[�o�ł� /i/index.html �����Ȃ�
	if(!&MakeIndex4Keitai296)	{return 0;}

#	if(
#	   $ENV{'SERVER_NAME'} =~ /idol/ ||
#	   $ENV{'SERVER_NAME'} =~ /pie/ ||
#	   $ENV{'SERVER_NAME'} =~ /sakura01/ ||
#	   $ENV{'SERVER_NAME'} =~ /sakura02/ ||
#	   $ENV{'SERVER_NAME'} =~ /sakura03/)
#	{
#		return MakeIndex4KeitaiUla($GB);
#	}
	################�L������
	my $tag;

	my $adadf = "./docomo_ad.txt"	;
	if($ENV{'SERVER_NAME'} =~ /bbspink\.com/)
	{
		$adadf = "../HOHO-01.txt";
	}

	open(IMAD, $adadf);
	$tag = <IMAD>;
	close(IMAD);

	################�L������
	#i-mode�p�e�L�X�g���J��

	my $imodeindex = $GB->{IMODEPATH} . "index.html";
	my $count=0;
	my $ibase = "http://$ENV{'SERVER_NAME'}$ENV{'SCRIPT_NAME'}";
	$ibase =~ s/read\.cgi/r\.i/;

	$GB->{DEBUG} .= "IN MakeIndex4Keitai ($imodeindex)<br>";

	unless(-e $GB->{IMODEPATH})
	{
		#umask(0);
		mkdir($GB->{IMODEPATH},0777);
	}
	open(SUBW,">$imodeindex");
#	flock(SUBW,2);

	# �w�b�_
	my @imodeindexhead = (
	qq|<html lang="ja">|,
	qq|<head>|,
	qq|<base href=\"$ibase\">|,
	qq|<title>$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE'}</title>|,
	qq|</head><body>|
	);
	&PutLines(*SUBW, @imodeindexhead);

	if($ENV{'SERVER_NAME'} =~ /bbspink/)
	{
		my $UlaUrl = "http://same.ula.cc/test/p.so/$ENV{'SERVER_NAME'}/$GB->{FORM}->{'bbs'}/";
		&Put1Line(*SUBW, "<a href=\"$UlaUrl\"> ������ł������������B</a><br><br>");
		&Put1Line(*SUBW, "<br><br><br><br><br><br><br><br><br><br>");
		&Put1Line(*SUBW, "<br><br><br><br><br><br><br><br><br><br>");
	}
	# �L���ƃ^�C�g��
	my @imodeindexbody = (
	qq|$tag|,
	qq|<hr>$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE'}<hr>|
	);
	&PutLines(*SUBW, @imodeindexbody);

	foreach(@{$GB->{NEWSUB}})
	{
		chomp;
		/^(\w+)\.dat<>(.*)/;
		my ($key, $value) = ($1, $2);
		$count++;
		&Put1Line(*SUBW, "$count: <a href=r.i/$GB->{FORM}->{'bbs'}/$key/i>$value</a><br>");
		if($count == 30) { last; }
	}

	# ����(���̃y�[�W�A�ɑ���)(p.i�������N)
	&Put1Line(*SUBW, "<hr><a href=p.i/$GB->{FORM}->{'bbs'}/30>����</a>");
	# �t�b�^
	&Put1Line(*SUBW, "<hr></body></html>"); #<hr>$IMAD
	
#	flock(SUBW,8);
	close(SUBW);
	#�p�[�~�b�V���������͕s�v
	#chmod(0666, $imodeindex);
}
#############################################################################
# /i/index.html ���쐬����
#############################################################################
sub MakeIndex4KeitaiUla
{
	my ($GB) = @_;

	my $UlaUrl = "http://same.ula.cc/test/p.so/$ENV{'SERVER_NAME'}/$GB->{FORM}->{'bbs'}/";

	#i-mode�p�e�L�X�g���J��

	my $imodeindex = $GB->{IMODEPATH} . "index.html";
	my $count=0;
	my $ibase = "http://$ENV{'SERVER_NAME'}$ENV{'SCRIPT_NAME'}";
	$ibase =~ s/read\.cgi/r\.i/;

	unless(-e $GB->{IMODEPATH})
	{
		#umask(0);
		mkdir($GB->{IMODEPATH},0777);
	}
	open(SUBW,">$imodeindex");
#	flock(SUBW,2);

	# �w�b�_
	my @imodeindexhead = (
	qq|<html lang="ja">|,
	qq|<head>|,
	qq|<base href=\"$ibase\">|,
	qq|<title>$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE'}</title>|,
	qq|</head><body>|
	);
	&PutLines(*SUBW, @imodeindexhead);

	&Put1Line(*SUBW, "<a href=\"$UlaUrl\">�ړ]���܂����B</a></body></html>");

	# �t�b�^
	&Put1Line(*SUBW, "<hr></body></html>"); #<hr>$IMAD
	
#	flock(SUBW,8);
	close(SUBW);
	#�p�[�~�b�V���������͕s�v
	#chmod(0666, $imodeindex);
}
#############################################################################
#
#############################################################################
sub Check_HardPosting
{	#�A���J�L�R

	my ($GB) = @_	;

	#�V�X���̏ꍇ�X���[
	if($GB->{NEWTHREAD})			{return 0;}

	#�ȉ��̔͂���[
	if(&KiseiOFF($GB))			{return 0;}
#	if($GB->{FORM}->{'bbs'} eq "campus")	{return 0;}
	#ex�n�̈ꕔ�͂���[
	if($ENV{'SERVER_NAME'} =~ /ex19/)	{return 0;}
	if($ENV{'SERVER_NAME'} =~ /ex21/)	{return 0;}
	if($ENV{'SERVER_NAME'} =~ /ex22/)	{return 0;}
	if($ENV{'SERVER_NAME'} =~ /news23/)	{return 0;}
	if($ENV{'SERVER_NAME'} =~ /atlanta/)	{return 0;}
	#���̓X���[
	if($GB->{CAP})				{return 0;}
	#���͂���[
	if($GB->{MARU})				{return 0;}
	#����D�҂̓X���[
	if($GB->{KABUU})				{return 0;}

	#BE���O�C�����Ă���ƃX���[(�ɂȂ��Ă邯�ǁA�ǂ����낤)
	#if($GB->{isBE})			{return 0;}
	#����p2�̓X���[
	#if($GB->{P22CH})			{return 0;}

#	if($GB->{FORM}->{bbs} ne 'news' && $GB->{MARU})		{return 0;}

	my $kazu = $FOX->{$GB->{FORM}->{bbs}}->{"timecount"} - $FOX->{$GB->{FORM}->{bbs}}->{"timeclose"};
	my $bun = length($GB->{FORM}->{'MESSAGE'});
	my $mss = substr($GB->{FORM}->{'MESSAGE'}, 0, 16); $mss =~ s/</&lt;/g; $mss =~ s/>/&gt;/g;
#	my $tane = $GB->{HOST4}	;
	my $tane = $ENV{'REMOTE_ADDR'}	;
	if($GB->{MARU})		{$tane = $GB->{MARU};}
	if($GB->{P22CH})	{$tane = $GB->{IDNOTANE};}
	if($GB->{KEITAI})	{$tane = $GB->{IDNOTANE};}
	if($GB->{KEITAIBROWSER}) {$tane = $GB->{IDNOTANE};}

	# �Ⴞ��܂ł́Abbsd�ɖ₢���킹��
	if(IsSnowmanServer)
	{
		my $cmd = 'chktimecount';
		my $messcount = bbsd_db($GB->{FORM}->{bbs}, $cmd, $tane, 'dummy'); 
		# �^�C���A�E�g���ǂ����`�F�b�N
		# �^�C���A�E�g�Ȃ�Atimecout/timeclose�̓X���[
		if(&bbsd_TimeoutCheck($GB, $messcount))
		{
			return 0;
		}
		# �Ђ����������ꍇ�́A�񐔂��Ԃ��ė���
		if($messcount != 0)
		{
			&DispError2($GB, "�d�q�q�n�q�I", "�d�q�q�n�q�F�A�����e�ł����H�H $messcount��");
		}
		else
		{
			return 0;
		}
	}
	# �ʏ�T�[�o�ł́A�����F
	else
	{
		#�A���������݃`�F�b�N
		my (@ao, $siro, @kiiro);
		open(NJY,"$GB->{WPATH}aosirokiiro.cgi");
		@ao = <NJY>;
		@kiiro = @ao;
		close(NJY);
	
		my $aoN = @ao	;
		my $messcount = 0;
		foreach(@ao)
		{
			chomp;
			my ($ridee, $namee, $valuee, $sizee, $mess) = split(/,/);
			my $checkhost = $tane;
			$checkhost =~ s/<.*>//;
			if($valuee =~ /$checkhost/)	{++$messcount;}
		}
		#if($GB->{FORM}->{bbs} eq 'news' && open(AAA,">> ./111.111"))
		#{print AAA "###000###$FOX->{$GB->{FORM}->{bbs}}->{timecount},$FOX->{$GB->{FORM}->{bbs}}->{timeclose},[$messcount],$aoN,$tane,<$GB->{MARU}>\n";close(AAA);}
	
		#if($GB->{MARU})		{$messcount -= 2;}
		if($messcount >= $FOX->{$GB->{FORM}->{bbs}}->{"timeclose"})
		{
			&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�A�����e�ł����H�H $messcount��");
		}
	
		$siro = "$GB->{FORM}->{'key'},$GB->{FORM}->{'time'},$tane,$bun,$messcount\n";
		unshift(@kiiro, $siro);
		@ao = @kiiro[0..$FOX->{$GB->{FORM}->{bbs}}->{'timecount'}-1];
	
		if(open(LAST,">$GB->{WPATH}aosirokiiro.cgi"))
		{
			print LAST @ao;
			close(LAST);
		}
	
		return 0;
	}
}
#######################################################################
# BBM
#######################################################################
sub BBMcheck
{
	my ($GB) = @_;

	if(&KiseiOFF($GB))			{return 0;}

	if(!&GoodKeitai($GB))
	{
		$GB->{BURNEDKEITAI} = 1;
		#�ȉ��̔̓X���[
		if($GB->{FORM}->{'bbs'} eq "accuse")	{return 0;}
#		if($GB->{FORM}->{'bbs'} eq "goki")	{return 0;}
#		if($GB->{FORM}->{'bbs'} eq "campus")	{return 0;}
		#operate�͂���[
#		if($GB->{FORM}->{'bbs'} ne "operate")
#		{
			&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�E�B���X�x��B�B�B<br>$GB->{IDNOTANE} �͂Q�����˂�ɂ͏������Ƃ��������Ă�����Ă��܂��B");
#		}
		#�Ă���}�[�N������(���A���͏�őS���G���[�Ȃ̂łǂ����o�Ȃ�)
		if($GB->{BURNEDKEITAI})
		{
			$GB->{FORM}->{'FROM'} = ' </b>[��.i!]<b> ' . $GB->{FORM}->{'FROM'};
		}
	}
	return 0	;
}
#######################################################################
# �u�ǂ��g�сv���ǂ������ׂ�(BBM�₢���킹��)
#######################################################################
sub GoodKeitai
{
	my ($GB) = @_;
	my $career = "";
	my $newthread = "";
	my $idnotane = "";

	my $AHOST = "";
	my $SPAM = "";

	#�ȉ��̔̓X���[
	if(&KiseiOFF($GB))			{return 0;}
#	if($GB->{FORM}->{'bbs'} eq "campus")	{return 1;}

	# ����BBM���肩�ǂ������A�g�b�v�y�[�W�ł킩��悤��
	$GB->{version} .= " +BBM";

	#�g�шȊO�͂���[
	if(!($GB->{KEITAI} || $GB->{KEITAIBROWSER}))	{return 1;}

	#ID�̎�(�ŗL�ԍ�)��DNS�N�G���p�ɕϊ�
	$idnotane = $GB->{IDNOTANE};
	$idnotane =~ s/\_/\-/g;
	# DoCoMo�ł́u�������t���O���v��t�����Ă���BBM���Ă�
	if(length($idnotane) eq 7 && ($GB->{KEITAI} || $GB->{KEITAIBROWSER}))
	{
		$idnotane = &MakeImodeIDforDNS($idnotane);
	}

	#�g�уL�����A���ƂɕύX
	if   ($GB->{KEITAI} eq 1)	{ $career = "docomo"; }
	elsif($GB->{KEITAI} eq 2)	{ $career = "au"; }
	elsif($GB->{KEITAI} eq 3)	{ $career = "vodafone"; }
	elsif($GB->{KEITAI} eq 5)	{ $career = "emobile"; }
	else				{ $career = "others"; }

	#�V�X���b�h���ǂ����̔���
	if($GB->{FORM}->{'subject'} ne "")	{ $newthread = "b"; }
	else					{ $newthread = "a"; }

#	$AHOST = "$GB->{NOWTIME}.$$.$idnotane.A.B.C.D.X.bbm.2ch.net.";
	$AHOST = "$GB->{NOWTIME}.$$.c.$GB->{FORM}->{'bbs'}.$GB->{FORM}->{'key'}.$newthread.B.C.D.$career.$idnotane.bbm.2ch.net.";

	#BBM�ُ펞�͂���[
	if(!$FOX->{BBM})		{return 1;}
	#BBM�ւ̖₢���킹
	$SPAM = &foxDNSquery2($AHOST);
#$SPAM = "127.0.0.0";
	#�Ă���Ă����A�������݂��߁[
	if($SPAM eq "127.0.0.2")	{return 0;}
	#BBM���~�܂��Ă��܂�����
	elsif($SPAM eq "127.0.0.0")	{ $FOX->{BBM} = 0; }

	#�����܂ŗ������͓̂��ɖ��Ȃ�
	return 1;
}
#############################################################################
#
#############################################################################
sub BBXcheck
{
	my ($GB) = @_	;

	#IsKoukoku���s�t���O�����Z�b�g����Ă��鎞
	#(���ʃT�[�o��LA������)�̓X���[
	if(!$FOX->{ISKOUKOKU})			{return 0;}
	#�ȉ��̔͂���[
	if(&KiseiOFF($GB))			{return 0;}
	if($GB->{FORM}->{'bbs'} eq "sec2chd")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "sec2ch")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "newservant"){return 0;}
	if($GB->{FORM}->{'bbs'} eq "ad")	{return 0;}
#	if($GB->{FORM}->{'bbs'} eq "campus")	{return 0;}
#	if($GB->{FORM}->{'bbs'} eq "news")	{return 0;}
#	if($GB->{FORM}->{'bbs'} eq "news4vip")	{return 0;}

	# IPv6���ł�BBX��(�܂�)�Ȃ�
	if($GB->{IPv6})				{return 0;}

	#IsKoukoku�����s����(�X�L�b�v����)�T�[�o���ǂ����̃`�F�b�N�́A
	#bbs-entry.cgi��mumumuIsIsKoukoku()�ł܂Ƃ߂Ă��悤�ɂ���
	#���Ńg���b�N�o�b�N����Ȃ����̓X���[
#	if($GB->{CAP} && !$GB->{TBACK})		{return 0;}
	#���̓X���[
	#if($GB->{MARU})			{return 0;}
	#�L������?
	my $NG_word = &IsKoukoku($GB)	;
	if($NG_word eq '')			{return 0;}

	# ���ꂼ��̒l�����o�������Ƃ��́A�ȉ��̂悤�Ƀf���t�@�����X����΁E�E�E
	my @NG_word_status = @{$NG_word};

	# ���̂悤�ɂ��ꂼ��ɒl���������܂��B
	# $NG_word_status[0] �ɂ͋K�������� [Shift_JIS]
	# $NG_word_status[1] �ɂ� MD5 �l
	# $NG_word_status[2] �ɂ� �t���O

	# BBR �֑��M�iNG���[�h�ǐՑ��u�H�j @2005/01/22 by �������L����
	# MD5-�Y�����[�h�ɕt����ꂽmd5�l.������t���O.���e�҂�IP�A�h���X.�T�u�X�N���C�o.�X���b�h�ԍ�.��.�I��.bbr.2ch.net.
	# �Ԃ�l�͂���Ȃ�����ǂ�TimeOut�������v�肻��������Net::DNS���g���������悢���ȁH

	my $SubNo = $GB->{IDNOTANE}; # _ �� - �ϊ����Ȃ��Ⴉ���Ȃ̂ŁB
	$SubNo =~ tr/_/-/;

	# docomo�g�тł́u�������t���O�v�����Ă���BBR/BBN���Ă�
	if(length($SubNo) eq 7 && ($GB->{KEITAI} || $GB->{KEITAIBROWSER}))
	{
		$SubNo = &MakeImodeIDforDNS($SubNo);
	}

	my $CHOST =
		sprintf qq|MD5-%s.%d.%s.%s.%d.%s.%s.bbr.2ch.net.|,
		$NG_word_status[1], # MD5�l
		$NG_word_status[2] ? 1 : 0, # ������t���O�B����ۂ��ƃC�����Ȃ̂�
		$ENV{REMOTE_ADDR}, # IP�A�h���X�i�Ђ�����Ԃ��Ȃ��Ă��������Ƃɂ��悤��j
		$SubNo !~ /\./ ? $SubNo : '0', # �T�u�X�N���C�o����Ȃ��݂����Ƃ��ɂ� '0' �ɂ��Ă����B
		$GB->{FORM}->{'key'}, # �X���b�h�ԍ�
		$GB->{FORM}->{'bbs'}, # ���i�f�B���N�g�����j
		$ENV{SERVER_NAME}, # �I��(FQDN)
	;
	if($FOX->{BBR})
	{
		$FOX->{BBR} = &foxDNSquery($CHOST, $FOX->{DNSSERVER}->{BBR});
	}

	# ���̂Ƃ��ɁE�E�E
	if ($NG_word_status[2] == 1) # �t���O�� 1 �̂Ƃ��́u�����ςt���O�v�Ȃ̂ł��̎��̏����B
	{
		&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�����炪�炢�Ă܂���B");
	}

	# DNS�₢���킹����
	my $HHH = "";
	my $AHOST = "";
	if($GB->{KEITAI} || $GB->{KEITAIBROWSER} || $GB->{P22CH})
	{
		# DNS�����ɂ������Ă�����X���[
		if(!$FOX->{BBN})	{return 0;}

		# �g�т܂��͌���p2: bbn.2ch.net
		# �����ɗ���܂łɁA$SubNo�� _ => - �ϊ��ς݂̏�񂪓����Ă���
		# BBM�Ɠ����t�H�[�}�b�g�Ŗ₢���킹�̎�����
		$HHH = "$GB->{NOWTIME}.$$.c.$GB->{FORM}->{'bbs'}.$GB->{FORM}->{'key'}.$GB->{NEWTHREAD}.B.C.D.$GB->{KEITAI}.$SubNo";
		$AHOST = "$HHH.bbn.2ch.net.";
	}
	else
	{
		# DNS�����ɂ������Ă�����X���[
		if(!$FOX->{BBX})	{return 0;}

		# �g�шȊO: bbx.2ch.net
		# ���̂Ƃ���AIR-EDGE PHONE��������
		$HHH = $ENV{REMOTE_ADDR}	;
		$HHH =~ s/(\d+)\.(\d+)\.(\d+)\.(\d+)/$4.$3.$2.$1/;
		$AHOST = "$HHH.bbx.2ch.net.";
	}

	# DNS�₢���핔���́A�g��/PC����
	my $SPAM = &foxDNSquery2($AHOST);
#	my $SPAM = '127.0.0.0';

	# DNS������������A�Ȍ�D����������܂�DNS�₢���킹���~
	if($SPAM eq "127.0.0.0")
	{
		if($GB->{KEITAI} || $GB->{KEITAIBROWSER} || $GB->{P22CH})
		{
			$FOX->{BBN} = 0;
		}
		else
		{
			$FOX->{BBX} = 0;
		}
		return 0;
	}
	# BBX/BBN�o�^����̏ꍇ
	elsif ($SPAM eq "127.0.0.2")
	{
		my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($GB->{NOWTIME});
		$mon ++		;
		my $yakinFile = "../_bg/logs/Rock54-$year-$mon-$mday.txt"	;
		open(YAN1,">>$yakinFile");print YAN1 "$GB->{DATE}\t$ENV{REMOTE_ADDR}\t$GB->{HOST4}\t$GB->{IDNOTANE}\t$NG_word_status[0]\n";close(YAN1);

		#&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F���b�N�͐l�����B");
		&endhtml($GB);
	}
	return 0;
}
#############################################################################
#㩁A㩁A㩁A㩁A㩂�
#���́F
#IsKoukoku(�Ώە�����[Shift_JIS],Rock54�̃t�@�C����)�@����͖����Bsub �Œ�`���B
#�Ԃ茌�Ԃ���[�F
#OK �Ȃ�� �󕶎���(�U)
#NG �Ȃ�� �i�K��������(�^)[Shift_JIS], MD5�l, �t���O�j�̃��X�g�ւ̃��t�@�����X
sub IsKoukoku
{
	my ($GB) = @_;

	my $In_Strings = $GB->{FORM}->{'MESSAGE'}; # �����̂ő��

	#if($ENV{SERVER_NAME} =~ /bbspink.com/)
	#{
		$In_Strings .= $GB->{FORM}->{'mail'}	;
		$In_Strings .= $GB->{FORM}->{'FROM'}	;
		$In_Strings .= $GB->{FORM}->{'subject'}	;
	#}

	my $ccpp = &CoPiPe($GB,$In_Strings)	;#�R�s�y�𔻒肵�悤�ƁA�A�A
	if($ccpp)		{return $ccpp	;}

	# ����Rock54/54M(IsKoukoku)���肩�ǂ������A�g�b�v�y�[�W�ł킩��悤��
	$GB->{version} .= " +Rock54/54M";

	# �ǂݍ��ށB�B�B
	# my @Rock_word = @FOX_Ro54; # �������̖��ʂȂ̂ŏȗ����Ă݂܂����B

	# �ł� NG ���[�h�̃`�F�b�N�B
	foreach my $NG_word_ref (@FOX_Ro54)
	{
		my $NG_word = $NG_word_ref->[0]; # ���t�@�����X������o���B
		if (my $matched = $In_Strings =~ $NG_word ? $& : undef) {
			return [$matched, @$NG_word_ref[1 .. $#$NG_word_ref]];
		} # ���v������NG���[�h�����̓E�o�ƃ��t�@�����X��Ԃ��B
		# �s�� NG ���[�h�������������������Ȃ���΃X�L�b�v
	}
	return '';
}
sub CoPiPe
{
	my ($GB,$mes) = @_	;

#return ''	;

	#�ȉ��̔͂���[
	if($ENV{'SERVER_NAME'} =~ /ex/)			{return '';}
	if($GB->{FORM}->{'bbs'} ne "news")		{return '';}

	my @mm = split(/<br>/,$mes)	;
	$mm[1] =~ s/ |�@//g	;
	$mm[2] =~ s/ |�@//g	;

	if(length($mm[1]) > 6 && $mm[1] eq $mm[2])	{return $mm[1]	;}

#if(length($mes) < 512)		{return '';}

	if($mes =~ /������/)	{return '������';}
	if($mes =~ /������/)	{return '������';}
	if($mes =~ /������/)	{return '������';}
	if($mes =~ /������/)	{return '������';}
	if($mes =~ /������/)	{return '������';}
	if($mes =~ /������/)	{return '������';}
	if($mes =~ /������/)	{return '������';}
	if($mes =~ /������/)	{return '������';}
	if($mes =~ /\|\|\|\|\|/)	{return '|||||';}
	if($mes =~ /�^�_/)	{return '�^�_';}
	if($mes =~ /�i�K�j/)	{return '�i�K�j';}
	if($mes =~ /�c/)	{return '�c';}
	if($mes =~ /�i���j/)	{return '�i���j';}
	if($mes =~ /����/)	{return '����';}
	if($mes =~ /����/)	{return '����';}
	if($mes =~ /iiiiiiiii/)	{return 'iiiiiiiii';}
	if($mes =~ /:::::/)	{return ':::::';}

	my $aa = &IsAA($GB,$mes)		;
	if($aa)	{return 'AA'	;}

	return ''	;
}
sub IsAA
{
	my ($GB,$mes) = @_	;
	#���̓X���[
	if($GB->{CAP})				{return 0;}
	#���̓X���[
	if($GB->{MARU})				{return 0;}

	my $bbb = "�@ �@ �@"		;
	my $nnn = ($mes =~ s/\Q$bbb\E/$bbb/g);
	if($nnn > 1)	{return 1;}

	return 0	;
}
#############################################################################
#
#############################################################################
sub checkProxyList
{
	my ($GB) = @_			;
	my $RADDR = $ENV{'REMOTE_ADDR'}	;

	#�g�т�BBQ�X���[(BBM�ł��)
	if($GB->{KEITAI})			{return 0;}
	if($GB->{KEITAIBROWSER})		{return 0;}

	#�ȉ��̔͂���[
	if(&KiseiOFF($GB))			{return 0;}
	#if($GB->{FORM}->{'bbs'} eq "campus")	{return 0;}

	# ����p2�ł́Ap2-client-ip: ���Q�Ƃ���
	# p2-client-ip: ��foxSetHost�ŁA$GB->{HOST2} �ɓ����Ă���
	if($GB->{P22CH})
	{
		$RADDR = $GB->{HOST2};
	}

	$RADDR =~ /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/	;
	my $query_addr = "$4.$3.$2.$1.niku.2ch.net."	;

	if(!$FOX->{BBQ})			{return 0;}
	my $SPAM = &foxDNSquery2($query_addr)	;
	if($SPAM eq '127.0.0.2')		{return 1;}
	if($SPAM eq "127.0.0.0")		{$FOX->{BBQ} = 0;}
	return 0	;
}
#==================================================
#�@�z�X�g�̔���
#==================================================
sub foxSetHost
{
	my ($GB) = @_	;

	$GB->{KEITAI} = 0		;
	$GB->{KEITAIBROWSER} = 0	;

	# IPv6�ł͐V�݂̊֐����g��
	if($GB->{IPv6})
	{
		$GB->{HOST} = &GetRemoteHostName($ENV{'REMOTE_ADDR'});
		$GB->{HOST29} = $GB->{HOST};
	}
	else
	{
#		$GB->{HOST} = $ENV{'REMOTE_ADDR'};
		$GB->{HOST} = gethostbyaddr(pack('C4',split(/\./, $ENV{'REMOTE_ADDR'})), 2) || $ENV{'REMOTE_ADDR'};
		$GB->{HOST29} = $GB->{HOST}		;
	} 
	# �����ۂ����̔���
	# �Ƃ肠����IPv6�̎��̓X�L�b�v���Ƃ��āA���Ƃōl���悤�A�A�A�B
	if($GB->{IPv6})
	{
		$GB->{HOST2} = '';
	}
	else
	{
		my @prox;
		push(@prox, $ENV{"HTTP_$_"} || '') foreach (qw/X_FORWARDED_FOR FORWARDED VIA/);
		my $prox = join(' ', @prox);
		if ($prox)
		{
			my ($xxx, $yyy) = '';
			$xxx = $& if ($prox =~ /\d+\.\d+\.\d+\.\d+/);
			$yyy = $1 if ($prox =~ /[\s\/]([\w]+\.[\w\.]+):\d/);
			if($xxx)
			{
				$GB->{HOST2} = gethostbyaddr(pack('C4',split(/\./, $xxx)), 2) || $yyy || $xxx;
			}
			else
			{
				$GB->{HOST2} = $yyy || $xxx;
			}
		}
		else
		{
			$GB->{HOST2} = '';
		}
	}

	# AIR-EDGE MEGAPLUS�������ꍇ�AHTTP_CLIENT_IP���`�F�b�N���A
	# �R����Ƃ��ē��삳����
	#if (&mumumuIsIP4MegaPlus($ENV{'REMOTE_ADDR'}))
	#{
	#	my $xxx = $ENV{'HTTP_CLIENT_IP'};
	#	#&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�FMegaPlus");
	#	$GB->{HOST2} = $xxx if ($xxx);
	#}

	# HTTP_CLIENT_IP (= Client_IP:)�������Ă�����A
	# �ꗥ�������݂����f�肷��
	if ($ENV{'HTTP_CLIENT_IP'})
	{
		my $xxx = $ENV{'HTTP_CLIENT_IP'};
		&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�ςȏ�񂪑����ė��܂����B<br>Client_IP: $xxx");
	}

	$GB->{HOST3} = $ENV{'REMOTE_ADDR'};
	$GB->{HOST4} = $GB->{HOST};

	$GB->{HOST} .= "<$GB->{HOST2}>" if ($GB->{HOST2});
	$GB->{HOST5} = $GB->{HOST}			;	#���O�L�^�p(i���[�h�AEZweb�A�{�[�_�t�H���I���C�u�͒[���ŗL��񂠂�)

	$GB->{IDNOTANE}=$ENV{'REMOTE_ADDR'};

	# �g�їp�u���E�U�̏ꍇ�̏���
	&mumumuSetHost4KeitaiBrowser($GB);

	# ����p2
	if(&mumumuIsIP4P22ch($GB->{HOST3}))
	{
		if($ENV{HTTP_USER_AGENT} =~ /p2-user: (\d+)/)
		{
			$GB->{HOST5} .= "($1)";
			$GB->{IDNOTANE} = $1;
			$GB->{P22CH} = 1;
		}
		else
		{
			&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F����p2����̓��e�ł�p2-user�𑗐M����悤�ɂ��Ă��������B");
		}
		# p2-client-ip: ����ڑ��z�X�g�̏��� $GB->{HOST2} �ɓ���
		if($ENV{HTTP_USER_AGENT} =~ /p2-client-ip: (\d+)\.(\d+)\.(\d+)\.(\d+)/)
		{
			$GB->{HOST2} = $1 . "." . $2 . "." . $3 . "." . $4;

			# �����[�g�z�X�g�����L�^����(�K���������悤��)
			#my $p2host;
			#$p2host = gethostbyaddr(pack('C4',split(/\./, $GB->{HOST2})), 2) || $GB->{HOST2};
			#$GB->{HOST5} .= "($p2host)";
		}
		else
		{
			&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F����p2����̓��e�ł�p2-client-ip�𑗐M����悤�ɂ��Ă��������B");
		}
	}
	# i���[�h
	if(&mumumuIsIP4IMode($GB->{HOST3}))
	{
		# i���[�hID�Ɉڍs�A2008/6/1 by mumumu
		#if($ENV{'HTTP_USER_AGENT'} =~ /ser([\w]{11,})/)
		#{
		#	$GB->{HOST5} .= "(" . $ENV{'HTTP_USER_AGENT'} .")";
		#	$GB->{IDNOTANE} = $1;
		#	$GB->{KEITAI} = 1;
		#}
		#else
		#{
		#	&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�[���ŗL���𑗐M���Ă��������B");
		#}
		if($ENV{HTTP_X_DCMGUID} ne '')
		{
			$GB->{HOST5} .= "(" . $ENV{'HTTP_X_DCMGUID'} .")";
			$GB->{IDNOTANE} = $ENV{'HTTP_X_DCMGUID'};
			$GB->{KEITAI} = 1;
		}
		else
		{
			&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�Fi���[�hID������Ɏ擾�ł��܂���ł����B");
		}
	}
	# EZweb
	elsif(&mumumuIsIP4EZWeb($GB->{HOST3}))
	{
		if($ENV{'HTTP_X_UP_SUBNO'} ne '')
		{
			$GB->{HOST5} .= "(" . $ENV{'HTTP_X_UP_SUBNO'} .")";
			$GB->{IDNOTANE} = $ENV{'HTTP_X_UP_SUBNO'};
			$GB->{IDNOTANE} =~ s/\.ezweb\.ne\.jp//;
			$GB->{IDNOTANE} =~ s/\.ido\.ne\.jp//;
			$GB->{KEITAI} = 2;
		}
		else
		{
			&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�[���ŗL���𑗐M���Ȃ��g�ђ[������͓��e�ł��܂���B");
		}
	}
	# �{�[�_�t�H���I���C�u
	elsif(&mumumuIsIP4Vodafone($GB->{HOST3}))
	{
		if($ENV{'HTTP_USER_AGENT'} =~ /SN([\w]+?) /)
		{
			$GB->{HOST5} .= "($1)";
			$GB->{IDNOTANE} = $1;
			$GB->{KEITAI} = 3;
		}
		else
		{
			&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�[���V���A���ԍ��𑗐M���Ȃ�Vodafone����͓��e�ł��܂���B");
		}
	}
	# emobile EMnet
	elsif(&mumumuIsIP4EMnet($GB->{HOST3}))
	{
		# HTTP���N�G�X�g�w�b�_�́uHTTP_X_EM_UID�v���擾���邱�ƂŁA
		# EMnet�Ή��[������ʒm����郆�j�[�N�ȃ��[�UID���m�F�ł��܂��B
		# �t�H�[�}�b�g�́A"u"����n�܂�18Byte�̕�����ɂȂ�܂��B
		#
		# ���[�UID�̓��[�U�̑���ɂ���Ēʒm���~���邱�Ƃ��\�ł��B
		# ���̏ꍇ�A�{�g���w�b�_�͕t������܂���B
		# http://developer.emnet.ne.jp/useragent.html
		if($ENV{HTTP_X_EM_UID} ne '')
		{
			$GB->{HOST5} .= "(" . $ENV{'HTTP_X_EM_UID'} .")";
			$GB->{IDNOTANE} = $ENV{'HTTP_X_EM_UID'};
			# 4 �� ���ۂ� �Ŏg���Ă��邽�� 5 �Ƃ���
			$GB->{KEITAI} = 5;
		}
		else
		{
			&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�Femobile��EMnet�ڑ��ł̓��[�UID��ʒm���Ȃ��Ɠ��e�ł��܂���B");
		}
	}
	$GB->{HOST999} = $GB->{HOST5} . $GB->{HOST2}		;

	# �g�ъe�Ђ̃T�[�o�𐔂��邼
	&countKeitaiServer($GB)					;
}
#######################################################################
# �e��g�їp�u���E�U�̃z�X�g���擾
#######################################################################
sub mumumuSetHost4KeitaiBrowser
{
	my ($GB) = @_;
	my $browser = 0;

	# �g�їp�u���E�U����Ȃ���΂΂��΂�
	$browser = &mumumuIsKeitaiBrowser($GB);
	if(!$browser) {return 0;}

	# $browser = 1: ibisBrowser
	if($browser == 1)
	{
		if(&ProcessibisBrowser($GB))
		{
			&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�g�їp�u���E�U����̏��𐳂����擾�ł��܂���ł����B($browser)");
		}
	}
	# $browser = 2: jig Browser
	elsif($browser == 2)
	{
		if(&ProcessjigBrowser($GB))
		{
			&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�g�їp�u���E�U����̏��𐳂����擾�ł��܂���ł����B($browser)");
		}
	}
	# $browser = 3: SoftBank PC�T�C�g�u���E�U
	elsif($browser == 3)
	{
		if(&ProcesspcsiteBrowser($GB))
		{
			&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�FPC�T�C�g�u���E�U����̓��e�ł̓V���A���ԍ��𑗐M����悤�ɂ��Ă��������B($browser)");
		}
	}
	# $browser = 4: i���[�h�t���u���E�U
	elsif($browser == 4)
	{
		if(&ProcessimodefullBrowser($GB))
		{
			&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�Fi���[�h�t���u���E�U����̓��e�ł�i���[�hID�𑗐M����悤�ɂ��Ă��������B($browser)");
		}
	}
	# $browser = 5: au PC�T�C�g�r���[�A�[
	elsif($browser == 5)
	{
		# PC�T�C�g�r���[�A�[����̐ڑ��͖������ŃG���[�ɂ���
		&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�Fau��PC�T�C�g�r���[�A�[���瓊�e���邱�Ƃ͂ł��܂���B($browser)");
	}

	return 0;
}
#######################################################################
# ibisBrowser(�g�їp�u���E�U�̈��)�̂��߂̃z�X�g���擾
# mumumuSetHost4KeitaiBrowser����Ă΂��
# �߂�l: 0 �擾����
#        -1 �擾���s
#######################################################################
sub ProcessibisBrowser
{
	my ($GB) = @_;

	my $ua = $ENV{'HTTP_USER_AGENT'};
	my $ip = undef;
	my $career = undef;
	my $serial = undef;

	# Mozilla/4.0 (compatible; ibisBrowser; ipIP�A�h���X; ser�[���Œ�ԍ�)
	# ��i���[�hID�Ή��ɂ��ȉ��̂悤�ɕύX
	# Mozilla/4.0 (compatible; ibisBrowser; ipIP�A�h���X; i���[�hID)
	# ��SoftBank�[���̏ꍇ - 2009/3/25 by mumumu
	# Mozilla/4.0 (compatible; ibisBrowser; ipIP�A�h���X; SN�[���V���A���ԍ�)
	# ��Windows Mobile��
	# Mozilla/4.0 (compatible; ibisBrowser; ipIP�A�h���X; IBIS_WM�[���Œ�ԍ�)

	# ibisBrowser �łȂ��ꍇ�͂���
	if($ua !~ /ibisBrowser/)	{ return -1; }

	
	# �g�ё�IP�A�h���X��� ipIP�A�h���X
	# ID
	# ���Ƃ�邩�ǂ���(�Ƃ�Ȃ��Ⴞ��)
	if($ua =~ /ip(\d+)\.(\d+)\.(\d+)\.(\d+)\; (\w+)\)/)
	{
		$ip = $1 . "." . $2 . "." . $3 . "." . $4;
		$serial = $5;
	}
	else
	{
		return -1;
	}

	# IP�A�h���X���g�їp���ǂ������ׂ�
	$career = &IsIP4Mobile($ip);

	# �g�уL�����A�ʂ̌ŗL��񏈗�
	# �����͂�����T�u���[�`����������
	# $career = 1: DoCoMo
	if($career == 1)
	{
		# i���[�hID��7��������Ȃ��Ⴞ��
		if(length($serial) ne 7)
		{
			return -1;
		}
	}
	# $career = 2: au
	elsif($career == 2)
	{
		return -1;
	}
	# $career = 3: SoftBank
	elsif($career == 3)
	{
		# "SN" + 15��������Ȃ��Ƃ��߁AID��SN�̌�̕����̂ݒ��o
		if($serial =~ /SN([\w]{15,})/)
		{
			$serial = $1;
		}
		else
                {
			return -1;
		}
	}
	# ��
	else
	{
		# Windows Mobile��
		# Mozilla/4.0 (compatible; ibisBrowser; ipIP�A�h���X; IBIS_WM�[���Œ�ԍ�)
		if($ua =~ /IBIS_WM([\w]{16,})/)
		{
			$serial = $1;
			$serial = "IBIS_WM" . $1;
		}
		else
		{
			return -1;
		}
	}

	# �����܂ŗ�����$ip��$serial�ɏ�񂪐����������Ă���
	#&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�Fip=$ip, serial=$serial");
	$GB->{HOST5} .= "($serial)";
	$GB->{IDNOTANE} = $serial;
	$GB->{KEITAIBROWSER} = 1;

	return 0;
}
#######################################################################
# jig Browser(�g�їp�u���E�U�̈��)�̂��߂̃z�X�g���擾
# mumumuSetHost4KeitaiBrowser����Ă΂��
# �߂�l: 0 �擾����
#        -1 �擾���s
#######################################################################
sub ProcessjigBrowser
{
	my ($GB) = @_;

	# �g�ё���IP�A�h���X��X-Forwarded-For�w�b�_�[�Œ[���ŗL����
	# X-Subscriber-ID�w�b�_�[�ő��M����悤�ɂ��Ă��܂��B

	my $ip = $ENV{'HTTP_X_FORWARDED_FOR'};
	my $serialseed = $ENV{'HTTP_X_SUBSCRIBER_ID'};
	my $career = undef;
	my $serial = undef;

	# �ƂꂽIP�A�h���X���g�їp����Ȃ��ꍇ�͂���
	$career = &IsIP4Mobile($ip);
	if(!$career)			{ return -1; }

	# �g�уL�����A�ʂ̌ŗL��񏈗�
	# �����͂�����T�u���[�`����������
	# $career = 1: DoCoMo
	if($career == 1)
	{
		# 7����(i���[�hID)���ǂ������ׁA����ȊO�̓G���[
		if(length($serialseed) eq 7)
		{
			$serial = $serialseed;
		}
		else
		{
			return -1;
		}
	}
	# $career = 2: au
	elsif($career == 2)
	{
		$serialseed =~ s/\.ezweb\.ne\.jp//;
		$serial = $serialseed;
	}
	# $career = 3: SoftBank
	elsif($career == 3)
	{
		if($serialseed =~ /SN([\w]{15,})/)
                {
                        $serial = $1;
		}
		else
		{
			return -1;
		}
	}
	# Willcom ��(�Ƃ肠����)���Ή��Ƃ���
	else
	{
		return -1;
	}

	# �����܂ŗ�����$ip��$serial�ɏ�񂪐����������Ă���
	#&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�Fip=$ip, serial=$serial");
	$GB->{HOST5} .= "($serial)";
	$GB->{IDNOTANE} = $serial;
	$GB->{KEITAIBROWSER} = 2;

	return 0;
}
#######################################################################
# pcsiteBrowser(�\�t�g�o���N�g�їp�t���u���E�U)�̂��߂̃z�X�g���擾
# mumumuSetHost4KeitaiBrowser����Ă΂��
# �߂�l: 0 �擾����
#        -1 �擾���s
#######################################################################
sub ProcesspcsiteBrowser
{
	my ($GB) = @_;

	my $ua = $ENV{'HTTP_USER_AGENT'};
	my $serial = undef;

	# Mozilla/4.08 (911T;SoftBank;SN354000000000000) NetFront/3.3

	# SoftBank �łȂ��ꍇ�͂���
	if($ua !~ /SoftBank/)	{ return -1; }
	# NetFront �łȂ��ꍇ�͂���
	if($ua !~ /NetFront/)	{ return -1; }

	# �ŗL���擾����
	# �����͂�����T�u���[�`����������
	if($ua =~ /SN([\w]+?)\)/)
	{
		$serial = $1;
	}
	else
	{
		return -1;
	}

	# �����܂ŗ�����$serial�ɏ�񂪐����������Ă���
	#&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�Fserial=$serial");
	$GB->{HOST5} .= "($serial)";
	$GB->{IDNOTANE} = $serial;
	$GB->{KEITAIBROWSER} = 3;

	return 0;
}
#######################################################################
# imodefullBrowser(�h�R���g�їp�t���u���E�U)�̂��߂̃z�X�g���擾
# mumumuSetHost4KeitaiBrowser����Ă΂��
# �߂�l: 0 �擾����
#        -1 �擾���s
#######################################################################
sub ProcessimodefullBrowser
{
	my ($GB) = @_;

	my $cid = undef;

	if($ENV{HTTP_X_DCMGUID} ne '')
	{
		$cid = $ENV{'HTTP_X_DCMGUID'};
	}
	else
	{
		return -1;
	}

	# �����܂ŗ�����$cid�ɏ�񂪐����������Ă���
	#&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�Fcid=$cid");
	$GB->{HOST5} .= "(" . $cid .")";
	$GB->{IDNOTANE} = $cid;
	$GB->{KEITAIBROWSER} = 4;

	return 0;
}
#######################################################################
#�@�V�K�X���b�h�ƕ��ʂ̏������݂̏��`�F�b�N
#######################################################################
sub foxSetInformation
{
	my ($GB) = @_	;

	my $DATAFILE ="";	#.dat�t�@�C����錾���Ă���

	# �t�H�[���̎��ԏ�񂪂��������ꍇ
	if($GB->{FORM}->{'time'} >= $GB->{NOWTIME})
	{
		&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�u���E�U�𗧂��グ�Ȃ����Ă݂Ă��������B");
	}

	# �V�X���̏ꍇ
	if($GB->{FORM}->{'subject'} ne "")
	{
		# submit���Ȃ��ꍇ�A�X�����Ă���
		if($GB->{FORM}->{'submit'} eq "")
		{
			&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�X���b�h���Ă����ł��B�B�B");
		}

		# �T�u�W�F�N�g������ΐV�K�X���Ȃ̂ŃL�[�����݂ɐݒ�
		$GB->{FORM}->{'key'} = $GB->{NOWTIME}	;
		# �V�X���t���O�𗧂Ă�
		$GB->{NEWTHREAD} = $GB->{NOWTIME}	;

		###################################################
		#�@�V�K�X���u���b�N���������Ă����΂��isubbbs.cgi�j
		###################################################
#		if($GB->{FORM}->{'FROM'} =~/fusianasan/){
#		if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_NEWSUBJECT'} ne "" && $GB->{FORM}->{'submit'} =~ /�V�K/)
#		{
#
#			subbbs($GB);
#		}
		###################################################

		#�V�K�X���b�h�̃L�[�𓾂�(���Ldo�`while�̒u������)
		$GB->{FORM}->{'key'} = &mumumuAllocateThreadKey($GB);
		$DATAFILE = $GB->{DATPATH} . $GB->{FORM}->{'key'} . ".dat";
# ���̃R�[�h���Ɗ��� $DATAFILE �����݂��Ă����ꍇ�A�����Ŗ������[�v�Ɋׂ�
#		do {
#			#�T�u�W�F�N�g������ΐV�K�X���Ȃ̂ŃL�[�����݂ɐݒ�
#			$GB->{FORM}->{'key'} = $GB->{NOWTIME};
#			#.dat�t�@�C���̐ݒ�
#			$DATAFILE = $GB->{DATPATH} . $GB->{FORM}->{'key'} . ".dat";
#		} while ( -e $DATAFILE ) ;
	}
	# ���X�̏ꍇ
	else
	{
		if(defined($GB->{FORM}->{'key'}))
		{
			#�L�[����������Ȃ��ꍇ�΂��΂��I
			if($GB->{FORM}->{'key'} =~ /\W/ || $GB->{FORM}->{'key'} eq "")
			{
				&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�L�[��񂪕s���ł��I");
			}
		}
		else
		{
			if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_PASSWORD_CHECK'} eq "checked")
			{
				# �V�K�X���b�h�ʉ��
				&newbbs($GB);
			}
			else
			{
				#�T�u�W�F�N�g���L�[�����݂��Ȃ��Ȃ�΂��΂�
				&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�T�u�W�F�N�g�����݂��܂���I");
			}
		}
		#.dat�t�@�C���̐ݒ�
		$DATAFILE = $GB->{DATPATH} . $GB->{FORM}->{'key'} . ".dat";
		#.dat�����݂��ĂȂ��������Ȃ��Ȃ�΂��΂�
		# �Ⴞ��܂ł� -w �� -s �̔����bbsd�ɂ܂�����(�����ł͂��Ȃ�)
		if(!IsSnowmanServer)
		{
			unless(-w $DATAFILE)
			{
				&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F���̃X���b�h�ɂ͏������߂܂���B");
			}
			unless( -s $DATAFILE <= 512000)
			{
				&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F���̃X���b�h��512k�𒴂��Ă���̂ŏ����܂���I");
			}
		}
	}
}
#######################################################################
# �V�X���̃X���b�h�L�[�����肷��
#######################################################################
sub mumumuAllocateThreadKey
{
	my ($GB) = @_;
	my $maxtries = 3;	# �X���b�h�����ɂ��������̍Ď��s��
	my $i = 0;
	my $threadkey = $GB->{NOWTIME};
	my $datafile = $GB->{DATPATH} . $threadkey . ".dat";

	# �Ⴞ��܃T�[�o�ł͂��̂܂܎g�p(bbsd�ɂ܂�����)
	if(IsSnowmanServer)
	{
		return $threadkey;
	}

	# �����X���b�h�L�[���Ȃ���Ζ����
	# ���̏ꍇ�͂����ł������傤��
	if ( ! -e $datafile )
	{
		return $threadkey;
	}
	# �����t�@�C�������ɂ������ꍇ
	# live�n����Ȃ��ꍇ�A������Ƃ��񂪂��Ă݂�
	elsif(!$ENV{'SERVER_NAME'} =~ /live/)
	{
		for ($i = 1; $i <= $maxtries; $i++)
		{
			$threadkey++;
			$datafile = $GB->{DATPATH} . $threadkey . ".dat";
			if ( ! -e $datafile )
			{
				# �X���b�h�L�[���X�V
				# $GB->{NOWTIME} ���X�V���邱��
				$GB->{NOWTIME} = $threadkey;
				return $threadkey;
			}
		}
	}
	# �ł�����ς肾�߂��������炲�߂�Ȃ���
	&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F�ʂ̐l���������ɃX���b�h�𗧂Ă悤�Ƃ��Ă��܂��B���߂�Ȃ����B");
}
#############################################################################
#	�X���Ԃ�
#############################################################################
# >100,101,102��������̓_��
sub SureAnc
{
	my ($GB) = @_	;

	#�ȉ��̔͂���[
	if(&KiseiOFF($GB))			{return 0;}
	if($GB->{FORM}->{'bbs'} eq "sec2ch")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "sec2chd")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "saku")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "saku2ch")	{return 0;}
	#���̓X���[
	if($GB->{CAP})				{return 0;}
	#���̓X���[
	if($GB->{MARU})				{return 0;}

	my $nnn = ($GB->{FORM}->{'MESSAGE'} =~ s/(\d)/$1/g);
#&DispError2($GB,"�d�q�q�n�q�I","nnn=$nnn");
	if($nnn < 120)	{return 0;}

#	$nnn = ($GB->{FORM}->{'MESSAGE'} =~ s/([&gt;\d+|-\d+|,\d+])/$1/g);
	$nnn = ($GB->{FORM}->{'MESSAGE'} =~ s/(&gt;\d+)/$1/g);
	if($nnn < 12)	{return 0;}
	$nnn += ($GB->{FORM}->{'MESSAGE'} =~ s/(-\d+)/$1/g);
	$nnn += ($GB->{FORM}->{'MESSAGE'} =~ s/(,\d+)/$1/g);
#&DispError2($GB,"�d�q�q�n�q�I","nnn=$nnn");
	if($nnn > 10)	{&endhtml($GB);	}

	return 0	;
}
# http://��������̓_��
sub SureHttp
{
	my ($GB) = @_	;

	#�ȉ��̔͂���[
	if(&KiseiOFF($GB))			{return 0;}
	if($GB->{FORM}->{'bbs'} eq "sec2ch")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "sec2chd")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "saku")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "saku2ch")	{return 0;}
	#���̓X���[
	if($GB->{CAP})				{return 0;}
	#���̓X���[
	if($GB->{MARU})				{return 0;}

	my $bbb = "\/" ;
	my $nnn = ($GB->{FORM}->{'MESSAGE'} =~ s/\Q$bbb\E/$bbb/g);
	if($nnn < 5){	return ;	}

	$bbb = "ttp\:" ;
	$nnn = ($GB->{FORM}->{'MESSAGE'} =~ s/\Q$bbb\E/$bbb/g);
	if($nnn > 20)	{&endhtml($GB);	}

	return 0	;
}
sub IsAAbbs
{
	my ($GB) = @_	;

	if($GB->{FORM}->{bbs} eq 'aastory')		{return 1;}
	if($GB->{FORM}->{bbs} eq 'aasaloon')		{return 1;}
	if($GB->{FORM}->{bbs} eq 'nida')		{return 1;}
	if($GB->{FORM}->{bbs} eq 'mona')		{return 1;}
	if($GB->{FORM}->{bbs} eq 'kao')			{return 1;}

	if($GB->{FORM}->{bbs} eq 'eroaa')		{return 1;}

	return 0	;
}
# �T����R�̓_��
sub SureUtsu
{
	my ($GB) = @_	;

	#�ȉ��̔͂���[
	if(&KiseiOFF($GB))			{return 0;}
	if($GB->{FORM}->{'bbs'} eq "sec2ch")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "sec2chd")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "saku")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "saku2ch")	{return 0;}
	if(&IsAAbbs($GB))			{return 0;}
	#���̓X���[
	if($GB->{CAP})				{return 0;}
	#���̓X���[
	if($GB->{MARU})				{return 0;}

	if(length($GB->{FORM}->{'MESSAGE'}) < 10)	{return 0;}

	my $bbb = substr($GB->{FORM}->{'MESSAGE'}, 0, 4) ;
	if($bbb =~ /�@/)	{return 0;}
#	if($bbb =~ /[0-9a-zA-Z\:\.\;\+\,]/)	{return 0;}
	if($bbb =~ /[\:\.\;]/)	{return 0;}

	if($bbb eq "�@�Q")	{return 0;}
	if($bbb eq "�@�@")	{return 0;}
	my $nnn = ($GB->{FORM}->{'MESSAGE'} =~ s/\Q$bbb\E/$bbb/g);
	if($nnn > 20){	&endhtml($GB);	}

	return 0	;
}
# >> ����R�̓_��
sub SureTsubushi
{
	my ($GB) = @_	;

	#�ȉ��̔͂���[
	if(&KiseiOFF($GB))			{return 0;}
	if($GB->{FORM}->{'bbs'} eq "saku")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "saku2ch")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "owarai")	{return 0;}
#	if($GB->{FORM}->{'bbs'} eq "campus")	{return 0;}
	#���̓X���[
	if($GB->{CAP})				{return 0;}
	#���̓X���[
	if($GB->{MARU})				{return 0;}

	my $bbb = "&gt;&gt;";
	my $nnn = ($GB->{FORM}->{'MESSAGE'} =~ s/\Q$bbb\E/$bbb/g);
	if($nnn > 10){	&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F>> ���������܂��I");}

	$bbb = "http://";
	$nnn = ($GB->{FORM}->{'MESSAGE'} =~ s/\Q$bbb\E/$bbb/g);
	if($nnn > 15){	&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�Fhttp:// ���������܂��I");}

	$bbb = "https://";
	$nnn = ($GB->{FORM}->{'MESSAGE'} =~ s/\Q$bbb\E/$bbb/g);
	if($nnn > 15){	&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�Fhttps:// ���������܂��I");}

	$bbb = "ftp://";
	$nnn = ($GB->{FORM}->{'MESSAGE'} =~ s/\Q$bbb\E/$bbb/g);
	if($nnn > 15){	&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�Fftp:// ���������܂��I");}

	return 1	;
}
sub OtameshiMaru
{
	my ($GB) = @_	;

	return		;

	my $id = 'summit'	;
	my $pw = 'touya'	;
	if($GB->{FORM}->{'MESSAGE'} =~ /$id/i)	{&endhtml($GB);	}
	if($GB->{FORM}->{'MESSAGE'} =~ /$pw/i)	{&endhtml($GB);	}
	return		;
}
#############################################################################
# bbsd�o�R�ŏ�������(�Ⴞ��ܔ�WriteDatFile)
#############################################################################
sub WriteSnow
{
	my ($GB, $DATALOG) = @_;

	# bbsd�ɏ������݃R�}���h�𑗂�
	my $errmsg = bbsd(
			$GB->{FORM}->{'bbs'},
			$GB->{FORM}->{'key'},
			$GB->{OUTDAT},
			$GB->{version},
			$FOX->{headadfile},
			$FOX->{putadfile},
			&{$FOX->{maido3adfile}}($GB->{FORM}{bbs}),
			$FOX->{lastad},
			"$DATALOG:$GB->{LOGDAT}"
			); 

	# �^�C���A�E�g���ǂ����`�F�b�N
	if(&bbsd_TimeoutCheck($GB, $errmsg))
	{
		#XXX
		return 0;
		&bbsd_TimeoutError($GB, 'WriteSnow');
	}

	# �V�X���̎��͎��ۂ̃X���b�h�L�[������̂ŁA�����ۑ�
	if($GB->{NEWTHREAD})
	{
		#�X���b�h�L�[��������ۑ����Ė߂�
		if($errmsg !~ /\D/)
		{
			$GB->{FORM}->{'key'} = $errmsg;
			return 0;
		}
		#�����łȂ��Ƃ��̓G���[������
	}

	# $errmsg ���󕶎��񂶂�Ȃ��ꍇ�A�G���[����
	if($errmsg)
	{
		$errmsg = +{
			# �����Ȃ��ꍇ
			# 1000���X�z���E512kB�z��
			do{local $! = EDQUOT;} => '���̃X���b�h��1000���X�܂���512k�𒴂��Ă���̂ŏ����܂���I',
			# �X���b�h�X�g�b�v
			do{local $! = EACCES;} => '���̃X���b�h�ɂ͏������߂܂���B',
			# �Ȃ��X���b�h�ɏ������Ƃ���
			do{local $! = ENOENT;} => '�X���b�h������܂���B',
			# bbsd�ł̃X�����ă��g���C�񐔂𒴂���
			do{local $! = EEXIST;} => '�ʂ̐l���������ɃX���b�h�𗧂Ă悤�Ƃ��Ă��܂��B���߂�Ȃ����B'
		}->{$errmsg}
			# ���̑��̃G���[
			|| "�s���ȃG���[���������܂����B<br>(board:$GB->{FORM}{bbs} key:$GB->{FORM}{key} errmsg:$errmsg)<br>���̃��b�Z�[�W���R�s�y���āA�^�p���ŕ񍐂��Ă���������Ƃ��肪�����ł��B";
		&DispError2($GB, '�d�q�q�n�q�I', "�d�q�q�n�q�F$errmsg");
	}

	return 0;
}
#############################################################################
# bbs.cgi ���C�����[�`���A�������火
#############################################################################
sub bbs_main
{
	my ($GB) = @_			;

#&DispError2($GB,"�s���y ��","<font color=green>�s���y ��</font>�@�ށH�ǂ��Ŏ��������̂��ȁH($GB->{FORM}->{bbs})<br>($GB->{FORM}->{get})");
#&DispError2($GB,"FOX ��","<font color=green>FOX ��</font>�@���悢��{��($GB->{FORM}->{bbs})<br>time=$GB->{NOWTIME}<br>mail=$GB->{FORM}->{mail} kihon=$GB->{FORM}->{kihon}");

	require "jcode.pl"		;
	require "bbs-yakin.cgi"		;
	&YakinInit			;

	&foxSetHost($GB)		;	#�@�z�X�g�̔���
	#�������܂ł͊O���Ɠ����Ȃ��Ǝv��

	#if(&IsP2($GB))	{&DispError2($GB,"�d�q�q�n�q�I","p2���f��");}

	# 2006�N5��20���A914�����ً̋}�Ή� by ��
	#if($GB->{FORM}->{'key'} =~ /^914/)
	#{
	#	&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�F���̃X���b�h�ɂ͏������߂܂���B���߂�Ȃ����B");
	#}

	# 2006�N7��23���Abe�����ً̋}�Ή� by ��
	#if($GB->{FORM}->{bbs} eq 'be')
	#{
	#	&DispError2($GB,"�d�q�q�n�q�I","�d�q�q�n�q�Fbe�͌��ݒ������ł��B���߂�Ȃ����B");
	#}

	# IsCentiSec���^�̏ꍇ�A1/100�b�܂ŕ\������
	# &Yamada��$GB->{DATE}���Q�Ƃ��Ă���̂ŁA�����Ŏ��s����K�v������
	if(&IsCentiSec($GB))
	{
		my $csec = sprintf("%02d", int($GB->{NOWMICROTIME} / 10000));
		$GB->{DATE} .= '.' . $csec;
	}

	#&Yamada($GB)	;
	&Saga($GB)	;	#����E�B���X

	#���������灦�͂͂����Ă������\��
	&foxSetInformation($GB)		;	#�@�V�K�X���b�h�ƕ��ʂ̏������݂̏��`�F�b�N

#��ꂽ�̂ł����܂ŁA
#&DispError2($GB,"FOX ��","<font color=green>FOX ��</font>�@��ꂽ�̂ł����܂�($GB->{FORM}->{bbs})<br>time=$GB->{NOWTIME}");

	#�N�b�L�[�̏���(�g���b�N�o�b�N�ł̓X�L�b�v)
	if(!$GB->{TBACK})
	{
		#�N�b�L�[�𔭍s
		#  NAME= �� MAIL= �̃N�b�L�[�� bbs.cgi �ł͂Ȃ��A
		#  JavaScript �o�R�Ŕ��s���邱�Ƃɂ���
		#  JavaScript �� MakeIndex4PC / newbbs �ňȉ��� .js ��ǂݍ���
		#    http://www2.2ch.net/snow/index.js
		#&PutCookie($GB);
		#�N�b�L�[��H�������`�F�b�N
		unless($ENV{'HTTP_COOKIE'} || $GB->{FORM}->{'get'} ne '' || $GB->{FORM}->{kihon} ne 'suriashi')
		{
			#���e�m�F��ʂ��o���āAexit����
			#����: �����o�Ă��铊�e�m�F��ʂ�
			#foxIkinari�ŏo�Ă��āA�����ł͂Ȃ�
			&ToukouKakunin($GB);
			exit;
		}
		#&DispError2($GB,"root ��","�N�b�L�[������ HTTP_COOKIE: $ENV{'HTTP_COOKIE'}");
	}

#==================================================
#�@���̃`�F�b�N�ƏC��
#==================================================

	# IsKoukoku�����s���邩�ǂ���
	# ����$FOX->{ISKOUKOKU} = 0�Ȃ�ă`�F�b�N���Ȃ�
	if($FOX->{ISKOUKOKU})
	{
		if(!&mumumuIsIsKoukoku($GB)) { $FOX->{ISKOUKOKU} = 0; }
	}

	#subject.txt/subback.html�̎��s�����ڂ邩�ǂ���
	if(&Saborin($GB))
	{
		$GB->{SABORIN} = 1;
	}

	#���̏���
	&ProcessMaru($GB);

	##############################################
	#�j���[���̕⊮
	$GB->{FORM}->{'FROM'} =~ s/^ //g;
	$GB->{FORM}->{'FROM'} =~ s/^�@//g;

	&NanashiReplace4vip($GB);
	##############################################

	#���O���E���[�����̋֎~��(�u�폜�v�u�Ǘ��v�u�R��v�Ȃ�)�̏���
	&NGNameReplace($GB);

	#�n���h���i�g���b�v�j�̏���
	#&jcode::tr(\$GB->{FORM}->{'FROM'}, '��', '#');
	#if($GB->{FORM}->{'FROM'} =~ /([^#]*)#(.+)/)
	if(defined $GB->{TRIPKEY})
	{
		&ProcessTrip($GB, $GB->{FORM}{FROM}, $GB->{TRIPKEY});
		# ���ꂽ�g���b�v���ǂ����`�F�b�N
		&BadTripCheck($GB);
	}

	#�n���h���i�L���b�v�j�̏���
	&jcode::tr(\$GB->{FORM}->{'mail'}, '��', '#');
	if($GB->{FORM}->{'mail'} =~ /([^#]*)#(.+)/)
	{
		&ProcessCap($GB, $1, $2);
	}

	#�L���b�v����Ȃ����Aneet4vip/neet4pink�̓��ꏈ��
	if(!$GB->{CAP})
	{
		if($GB->{FORM}->{'bbs'} =~ /neet/)
		{
			# neet�n�͋���������
			$GB->{FORM}->{'FROM'} = $FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_NONAME_NAME'};
			# neet4pink�̓g���b�v�L��
			if($GB->{FORM}->{'bbs'} =~ /neet4pink/)
			{
				# �g���b�v�����񂪂���ꍇ
				if($GB->{TRIPSTRING} ne "")
				{
					$GB->{FORM}->{'FROM'} .= "</b> ��$GB->{TRIPSTRING} <b>";
				}
			}
		}
	}

	# ���O���̓`�F�b�N�A�������⊮�Ə����Aheaven4vip�̖������u������
	&ProcessNanashi($GB);

	# tasukeruyo�̏���
	if($GB->{FORM}->{'FROM'} =~ /tasukeruyo/)
	{
		# operate/operate2 �� dso �T�[�o�ł̂ݗL��
		# ipv6 �ł��L���ɂ��Ă݂�
		if(	$GB->{FORM}->{'bbs'} eq 'ihou' ||
			$GB->{FORM}->{'bbs'} =~ "operate" ||
			$GB->{FORM}->{'bbs'} =~ "ipv6" ||
			$ENV{'SERVER_NAME'} =~ /dso/)
		{
			&Tasukeruyo($GB);
		}
	}

	# fusianasan�̏���
	if($GB->{FORM}->{'FROM'} =~ /fusianasan/)
	{
		&Fusianasan($GB);
	}

	# �n�k�֘A�̌����ǉ�
	&EQfromWhere($GB);

	#���j�R�[�h�ϊ�
	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_UNICODE'} eq "change")
	{
		$GB->{FORM}->{'MESSAGE'} =~ s/\&\#[0-9;]*/�H/gi;
	}

	#����D�� ������ ��
	if($GB->{KABUU})
	{
		if($GB->{FORM}->{'FROM'} =~ s/������ ��/������ ��/)
		{
			$GB->{FORM}->{'FROM'} =~ s/������ ��//	;
			$GB->{FORM}->{'FROM'} .= "������ ��"	;
		}
	}

#&DispError2($GB,"FOX ��","<font color=green>FOX ��</font>�@���낢��`�F�b�N����@<br>FROM=$GB->{FORM}->{'FROM'}<br>MESSAGE=[$GB->{FORM}->{'MESSAGE'}]<br>mail=$GB->{FORM}->{'mail'}<br>");

#==================================================
#�@�G���[���X�|���X�i���ʂ̃G���[�͂܂Ƃ߂Ă΂��΂��j
#==================================================

	#�t�H�[�����̃`�F�b�N(���ɕςȕ����A���Ԃ��ǂ߂Ȃ�)
	&FormInfoCheck($GB);

	#referer�`�F�b�N(�u���E�U�ςł����)
	if(!$GB->{TBACK} && ($GB->{FORM}->{'submit'} ne "��������" || $ENV{'HTTP_USER_AGENT'} =~ /Mozilla/))
	{
		&BraHen($GB);
	}

#==================================================
#�@�t�B�[���h�T�C�Y�̔���
#==================================================

	# �X���^�C�A���O�A���A�h�A�{���̒����`�F�b�N
	&FieldSizeCheck($GB);

	# �{���̍s���ƒ�������s�̃`�F�b�N
	&FieldLineCheck($GB);

	# >> ����R�̓_����
#	&SureTsubushi($GB)	;
#	&SureUtsu($GB)		;	# �T����R�̓_��
#	&SureHttp($GB)		;	# http:����R�̓_��
#	&SureAnc($GB)		;	# >100����R�̓_��
	#���������R��h�~
	&OtameshiMaru($GB)	;
	#�p���
	&NoJapanese($GB)	;
	
#==================================================
#�@�ʂ̓��ꏈ��
#==================================================

	# �ʂ̓��ꏈ��
	&ItabetsuSpecial($GB);

#&DispError2($GB,"FOX ��","<font color=green>FOX ��</font>�@��������40%�i��ł݂�@<br>($GB->{HOST})<br>$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE'}<br>");

#==================================================
#�@���ތn�e�폈��
#==================================================

	&GeroTrap($GB)		;

	&checkPragma($GB)	;

	&checkProxyAtAll($GB)	;	#���J�v���N�V�K��

	&checkDenyList($GB)	;	#�A�N�փ��X�g(proxy999.cgi)���Ȃ߂܂킷

	&vip931($GB)		;	#VIP�L��

	&bybySaru($GB)		;	#�o�C�o�C���邳��

	&antiHosyu($GB)		;	#�����ێ�c�[������

	&BBMcheck($GB)		;	#BBM (�g�ыK��)

	&BBXcheck($GB)		;	#Rock54/Rock54M (�L���������}��)

	&ToolGekitai0($GB)	;	#Samba24 (�V�A�����e�K��)

	&GooMorningKeitai($GB)	;	#BBM2 �g�тł̋K��݂�

#&DispError2($GB,"FOX ��","<font color=green>FOX ��</font>�@���ނ���Ȃ������@<br>($GB->{HOST})<br>$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE'}<br>");

#&DispError2($GB,"FOX ��","<font color=green>FOX ��</font>�@��������50%�i��ł݂�@<br>($GB->{HOST},$GB->{HOST999},$GB->{IDNOTANE})<br>$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE'}<br>$GB->{MARU}<br>");

#==================================================
#�@�X�����Đ������A���J�L�R
#==================================================

	# �V�X���̏ꍇ�A�X�����ă`�F�b�N
	if($GB->{FORM}->{'subject'} ne "")
	{
		#�j���[��saku�ł́��Ă��`�F�b�N
		&VipQ2MaruyakiCheck($GB)	;
		#�e��X�����ă`�F�b�N���܂Ƃ߂Ď��{
		&SuretateTotalCheck($GB)	;
	}

	# timecount/timeclose(�A�����e�ł����H x��)�̏���
	&Check_HardPosting($GB);

#==================================================
#�@�g���b�N�o�b�N
#==================================================

	#�g���b�N�o�b�N����
	&foxTrackBack($GB)		;

#==================================================
#�@VIP�N�I���e�B
#==================================================

	#�����̕\��
	&ReplKabuka($GB)		;

	#VIP�N�I���e�B(���݂����Ƃ����N�ʂƂ�IQ�Ƃ��D�Ƃ�)
	&ReplOmikuji($GB)		;
	&ReplOtoshidama($GB)		;
	&ReplIQ($GB)			;
	&ReplShip($GB)			;

	#VIP�N�I���e�B2.0
	&VipQ2($GB)			;	#!vip2:command:

#==================================================
#�@���X�|���X�A���J�[�i�{���j
#==================================================

	# ���X�A���J�[�̏��� (>>���X�ԍ� >>���X�ԍ�-���X�ԍ�)
	&ResAnchor($GB);

#==================================================
#�@�t�@�C������i�c�`�s�t�@�C���X�V�j
#==================================================

	# BE���ǂ���
	if($GB->{isBE})
	{
		# �|�C���g�ɉ������ABE�p�̕�������쐬����
		# $GB->{xBE} �Ɋi�[�����
		&MakeBEString($GB);
	}
	else
	{
		# BE����Ȃ��ꍇ
		$GB->{xBE} = "";
	}

	# �g���b�N�o�b�N�̏ꍇ�A���O���͌Œ�
	if($GB->{TBACK})	{$GB->{FORM}->{'FROM'} = "�g���b�N�o�b�N ��";}

	# ID�̂Ƃ���ɕ\�����镶����ƁA���@��̈������
	# $GB->{xID} �� $GB->{LOGDAT} �Ɋi�[�����
	&MakeIdStringAndLogdat($GB);

	# 1���j�b�g����dat�����
	# $GB->{OUTDAT} �Ɋi�[�����
	&MakeOutdat($GB);

	# ���̃t�@�C����(�t���p�X)
	my $DATALOG = $GB->{LOGPATH} . $GB->{FORM}->{'key'} . ".cgi";

	# dat�̃t�@�C����(�t���p�X)
	my $DATAFILE = $GB->{DATPATH} . $GB->{FORM}->{'key'} . ".dat";

#==================================================
#�@dat�������݁Adat�f�[�^�ǂݍ��݁A1000��������
#==================================================

	if(IsSnowmanServer)
	{
		# ���O�̃f�B���N�g�����Ȃ���΍쐬
		unless(IsSnowmanServer == BBSD->{REMOTE} || -e $GB->{LOGPATH})
		{
			#umask(0);
			mkdir($GB->{LOGPATH},0777);
		}
		# �ŋ��L���b�v�ł́A924�ɂ����X�\
		if($GB->{FORM}->{'key'} =~ /^924/ && !$GB->{STRONGCAP})
		{
			#�X���b�h924 = �������߂Ȃ��X���b�h
			&Update924($GB, $DATAFILE);
		}
		else
		{
			# �������ݏ���
			&WriteSnow($GB, $DATALOG);
		}
	}
	else
	{
		# �ʏ�̏���(�Ⴞ��܂���Ȃ��ꍇ)
		# �ŋ��L���b�v�ł́A924�ɂ����X�\
		if($GB->{FORM}->{'key'} =~ /^924/ && !$GB->{STRONGCAP})
		{
			#�X���b�h924 = �������߂Ȃ��X���b�h
			&Update924($GB, $DATAFILE);
		}
		else
		{
			# dat�t�@�C����������
			&WriteDatFile($GB, $DATAFILE, $GB->{OUTDAT}, 0);
			# ���O�̃f�B���N�g�����Ȃ���΍쐬
			unless(-e $GB->{LOGPATH})
			{
				#umask(0);
				mkdir($GB->{LOGPATH},0777);
			}
			# ���O�t�@�C����������
			&WriteDatFile($GB, $DATALOG, $GB->{LOGDAT}, 1);
		}

		# <�`���V�̗�>
		# dat�ɒǋL����O��dat�̏�����肵���ق����A������
		# �����悤�ȋC������B�Ⴆ�΁A�����̂��A������Ă���
		# �������݂������Ȃ��Ƃ��A���������������ł��邾�낤���A
		# 1000�����̏������y�ɂȂ�悤�ȋC������B
		#
		# ���������ւ̉e�����ł����Ǝv���邵�A���낢���
		# ����p���l������̂ŁA���͂Ƃ肠�����A�������Ă����B
		# 11/11/2005 by ��
		# </�`���V�̗�>

		# dat�̏�����肵�A$GB�ɃZ�b�g���Ă���
		# ������͌��/html/�̉������(MakeWorkFile)�̂Ɏg��
		# $GB->{DATNUM}, $GB->{DAT1}, $GB->{DATLAST}
		&GetDatInfo($GB, $GB->{FORM}->{'key'});

		#&DispError2($GB,"root ��","���X��: $GB->{DATNUM} <br>1�̓��e: $GB->{DAT1} <br>DATLAST�̓�: $GB->{DATLAST}[0]");

		# 1000�����̏���������
		if($GB->{DATNUM} > 999)
		{
			&Over1000($GB, $DATAFILE);
			# 1050�����ً}�X�g�b�p�[
			if($GB->{DATNUM} > 1049)
			{
				&EmergOver1000($GB, $DATAFILE);
				# 1100�����ً}�X�g�b�p�[(�Ō�̎�i)
				if($GB->{DATNUM} > 1099)
				{
					&EmergOver1000Final($GB, $DATAFILE);
				}
			}
		}
		#VIP�N�H���e�B�ł̃X���X�g
		if($GB->{VIPQ2STOP})
		{
			chmod(0555, $DATAFILE);
		}
	}

#==================================================
# bby.2ch.net �ɒʒm�B�V�X���b�h���������B
#==================================================

	if($GB->{NEWTHREAD})
	{
		&NotifyBBY($GB);
	}

#==================================================
# bbs.2ch.net �ɒʒm�B�������ݏ��
#==================================================

	&NotifyBBS($GB);

$GB->{DEBUG} .= "��������60%�i��ł݂�<br>";
#&DispError2($GB,"FOX ��","<font color=green>FOX ��</font>�@��������60%�i��ł݂�@<br>dat�ւ̒ǋL���I�����Ƃ���<br>($GB->{HOST},$GB->{HOST999},$GB->{IDNOTANE})<br>$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE'}<br>$GB->{MARU}<br>");

#==================================================
#�@�t�@�C������isubject.txt & subback.html�j
#==================================================

	# �Ⴞ��܃T�[�o�ł́A�ȍ~�̃t�@�C�������͂��Ȃ�(bbsd�����s)
	if(IsSnowmanServer)
	{
		&endhtml($GB);
	}

	# subject.txt���X�V����
	# ������ @{$GB->{NEWSUB}} �ɃT�u�W�F�N�g�������Ă���
	# $GB->{SUBLINE} �������ŏ��������
	# $GB->{FILENUM} �ɂ͂�����subject.txt�̍s��������悤��
	&UpdateSubject($GB);

	#&DispError2($GB,"root ��","newsub�̓�: ${$GB->{NEWSUB}}[0]");

	# html/ �̉������
	&MakeWorkFile($GB, $GB->{FORM}->{'key'});

	#subback.html���X�V����
	#Saborin�t���O�������Ă����炳�ڂ�
	if(!$GB->{SABORIN})
	{
		&UpdateSubback($GB);
	}

#==================================================
#�@�{�g�s�l�k�f������ (index.html)
#==================================================

	#�g�їp��index�����(/i/index.html)
	#saku/saku2ch�ł��A�g�їp�� index.html �͍��
	if(!$GB->{SABORIN})
	{
		&MakeIndex4Keitai($GB);
	}

	#Saborin�t���O�������Ă��� or
	# saku/saku2ch�ł� index.html �̍X�V�����ڂ� (sakud�ł͍��̂Œ���)
	if(!$GB->{SABORIN} && !($GB->{FORM}->{'bbs'} eq "saku" || $GB->{FORM}->{'bbs'} eq "saku2ch"))
	{
		&MakeIndex4PC($GB);
	}

	$GB->{DEBUG}  .= "�����ɔ��ŗ~������bbs.cgi�͎v���Ă���=$GB->{INDEXFILE}<br>";
	#&DispError2($GB,"FOX ��","<font color=green>FOX ��</font>�@�Ō�ǂ��Ȃ��Ă��?�@<br><br>");

	# ��ԍŌ�̂Ƃ���̏���
	&endhtml($GB);

#&DispError2($GB,"FOX ��","<font color=green>FOX ��</font>�@�������ɍŌ�܂Ői��ł݂�@<br>dat�ւ̒ǋL���I�����Ƃ���<br>($GB->{HOST},$GB->{HOST999},$GB->{IDNOTANE})<br>$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE'}<br>$GB->{MARU}<br>");
}
sub KiseiOFF
{
	my ($GB) = @_			;
#	if($GB->{FORM}->{bbs} eq 'ghard')	{return 1;}
#	if($ENV{'SERVER_NAME'} =~ /bbspink/)	{return 1;}
	return 0	;
}
#############################################################################
# ���C�����[�`���I���B�����l�ł����B
#############################################################################
1;
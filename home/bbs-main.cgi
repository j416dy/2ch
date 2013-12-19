use strict 'vars';
use File::stat;
use POSIX qw(:errno_h strftime);
use BBSD;

# 古いのは old に入れたぞー by や
# 了解です by む

# 070320  携帯と携帯用ブラウザ(ibis/jig)では変なホスト名規制なし by む
# 070425  jigブラウザのCIDRブロック追加 by む
# 070719  Willcom/EZweb/iモードのCIDRブロック追加 by む
# 070903  WillcomのCIDRブロック追加 by む
# 071009  Y!ケータイのCIDRブロック追加・変更 by む
# 071110  jigブラウザのCIDRブロック追加 by む
# 071114  jigブラウザのCIDRブロック追加 by む
# 071208  管理人の作業部分を整形(内容は変更せず)
#         ibisBrowserゲートウェイ用新IPアドレスを登録
#         WillcomのCIDRブロック追加
#         「関連ページ」のリンクを非表示に by む
# 071209  ibisBrowser(Windows Mobile版)に対応 by む
# 071211  beのアイコン周り。 by ひ
# 080209  ibisBrowserゲートウェイ用新IPアドレスを登録 by む
# 080214  c-othersがcに統合されたことに伴う改修 by む
#         EZwebのアドレスレンジが増えたことに対応 by む
# 080216  公式P2の先が串だったらねぎまをつける by む
# 080218  tiger2514(なまずの棲家)のarea47表示を「地底」に設定 by む
# 080219  headline/BBYのDNSを新サーバに移行 by む
# 080221  stats/BBSのDNSを新サーバに移行 by む
# 080227  WillcomのCIDRブロック追加 by む
# 080301  foxDNSqueryをブロックしない$res->bgsendに変更 by む
# 080313  rock54/BBRのDNSを新サーバに移行 by む
# 080314  BBY/BBS/BBRのDNSサーバIPアドレスをinitFOXで定義 by む
# 080429  SoftBankのPCサイトブラウザに対応(jig, ibisと同じ処理) by む
# 080601  DoCoMoのiモードIDに本格対応 by む
# 080601a iモードIDへの対応リファイン(BBM/BBR/BBN) by む
# 080602  iモードフルブラウザからの書き込みに対応  by む
# 080603  ibis/jigブラウザのiモードID対応化に対応 by む
# 080618  WillcomのCIDRブロック追加 by む
# 080711  公式p2のIPアドレス追加 by む
# 080714  126.240.0.0/12 だったらiPhoneからの書き込みとする(ShikibetsuMark) by む
# 080714a 上記判断の後、UA経由を復活(ShikibetsuMark) by む
# 080718  iモード、EZwebのCIDRブロック追加 by む
# 080723  ヘッダーをいぢってみる by ひ
# 080727  IPv6に対応、BBQとBBX、foxSetHostの串っぽい判定部分はとりあえずスキップ by む
# 080727a IPv6スレ立て規制の判定を /48 で行う、IPv6時のIDを 48 + 16 + 64 bit で生成 by む
# 080728  IPv6時のIDを 上48 + 上64 + 下64 bit で生成 by む
# 080728a IPv6時のIDを 上48 + 上64 + 全128bit で生成 by む
# 080728b IPv6スレ立て規制の判定を /64 に戻してみる by む
# 080729  GetRemoteHostName: 一つ目の PTR レコードを見つけたら処理を打ち切る by む
# 080807  ula.cc/u.la/s2ch.net から書けなくなった問題を修正 by む
# 080906  musicnews も板別キャップに by む
# 080911  schipholの板別キャップ廃止 by む
# 080913  板別キャップかどうかはIsItabetsuCapで判定 by む
# 080913  newsのポイントを10000以上に変更 by ひ
# 080930  povertyのポイントは3000以上に変更 by や
# 081001  WillcomのCIDRブロック追加 by む
# 090112  ibisBrowserからdocomo携帯の時は7桁のIDじゃないとだめ(バグ取り) by む
# 090225  jigブラウザのCIDRブロック追加 by む
# 090324  ibisBrowser(SoftBank版)に対応 by む
# 090330  マイクロ秒の取得を syscall から Time::HiRes に変更 by む
# 090401  jigブラウザのCIDRブロック追加 by む
# 090426  EZwebのCIDRブロックを最新版に変更(追加と削除) by む
# 090605  jigブラウザのCIDRブロック追加・削除 by む
# 090619  トリップ新方式導入 by Sun
# 090731  emobile EMnetに対応、携帯扱いに。BBM2の対応は別途必要 by む
# 090781  emobile EMnetもBBM2に対応 by む
# 081220  iモードのCIDRブロック追加 by む
# 100105  Set-Cookie 有効期間の変更 by Sun
# 100219  EZwebのCIDRブロックを最新版に変更(追加) by む
# 100320  jigブラウザのCIDRブロック追加 by む
# 100402  stats.2ch.net (a.ns.bbs.2ch.net) のIPアドレス変更に対応 by む
# 100410  iPhone(panda)のCIDRブロック追加 by む
# 100414  headline.2ch.net (a.ns.bby.2ch.net) のIPアドレス変更に対応 by む
# 100420  Y!ケータイのCIDRブロック削除、PCサイトブラウザのCIDRブロック変更 by む
# 100516  なまずの棲家をtiger2514からbanana3104に変更 by む
# 100517  公式p2のIPアドレス一部変更 by む
# 100526  jigブラウザのCIDRブロック追加 by む
# 100531  live28デビューに対応、板あたりのスレッド数制限を live23/live24 と同じに by む
# 100601  live28ではSaborin有効 by む
# 100602  板あたりのスレッド数限界値の判定を板別に移行 by む
# 100603  スレッド数限界値を設定する板の判定をサブルーチン化 by む
# 100606  Saborinの更新判定をPIDによるものからrand()によるものに変更 by む
# 100617  hayabusaサーバは1/100秒まで表示 by む
# 100619  live*サーバの1/100秒表示解除 by む
# 100724  auのPCサイトビューアーのIPアドレスレンジからの投稿はエラーにする by む
# 100914  orz.2ch.ioからの投稿を許可 by garnet
# 100918  EZwebのCIDRブロックを最新版に変更(追加) by む
# 101005  jigブラウザのCIDRブロックを最新版に変更(追加・削除) by む
# 101014  WillcomのCIDRブロックを最新版に変更(追加・削除) by む
# 101028  jigブラウザのCIDRブロックを最新版に変更(追加) by む

#############################################################################
#	BE のICONを表示する　sssp://
#############################################################################
sub dispIconSssp
{
	my ($GB) = @_;

	if($GB->{icon} eq '')	{return 0;}

	if($GB->{NINNIN})	{return 0;}	#株優ステルスでoff

#	if(!$GB->{NEWTHREAD})	{return 0;}	#スレ立て時以外はoff

	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_OVERSEA_PROXY'} eq "checked")	{return 1;}

#	if($GB->{FORM}->{'bbs'} eq "operate2")	{return 1;}
	if($GB->{FORM}->{'bbs'} eq "news")	{return 1;}
	if($GB->{FORM}->{'bbs'} eq "poverty")	{return 1;}
	if($GB->{FORM}->{'bbs'} eq "news4vip")	{return 1;}

	return 0	;
}
#############################################################################
#	携帯各社のサーバを数えるぞ
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

	my $remo = $GB->{HOST29}	; #いわゆるリモホ
	my $ipip = $ENV{REMOTE_ADDR}	;
	$fff .= "$ipip.txt"		;

	if(open(LX,">> $fff")){print LX "$remo\t\t\t\t\t\t\t\t\n";close(LX);}

	return 1	;
}
#############################################################################
# docomo携帯のiモードIDから、DNS問い合わせ用文字列を作成する
# 入力: iモードID文字列
# 戻り値: DNS問い合わせ用文字列
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
# マルチバイト(日本語等)が書けない板　英語板
#############################################################################
sub NoJapanese
{
	my ($GB) = @_	;

	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_4WORLD'} eq "checked")
	{
		my $a = $GB->{FORM}->{'MESSAGE'} . $GB->{FORM}->{'mail'} . $GB->{FORM}->{'FROM'} . $GB->{FORM}->{'subject'}	;
		if($a =~ /[^a-zA-Z0-9\.\, #_<>\(\)\?\/\&\;\!\:\=\'\+\-\*\~\%\@\"\[\]\+]/)	{&DispError2($GB,"ＥＲＲＯＲ！","日本語は受け付けていません");	}
	}
#	return	0	;

	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_4WORLD'} eq "kanji")
	{
		my $a = $GB->{FORM}->{'MESSAGE'}	;
#		$a =~ s/[\x88-\x9F\xE0-\xFF][\x9F-\xFF]//g	;
		$a =~ s/[\x88-\x9F\xE0-\xFF][\x80-\xFF]//g	;
		$a =~ s/<br>//g				;
		$a =~ s/ //g				;
		$a =~ s/　//g				;
		if($a ne '')	{&DispError2($GB,"ＥＲＲＯＲ！","漢字しか受け付けていません");	}
	}
	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_4WORLD'} eq "hira")
	{
		my $a = $GB->{FORM}->{'MESSAGE'}	;
		$a =~ s/[\x82][\x9E-\xFF]//g	;
		$a =~ s/<br>//g				;
		$a =~ s/ //g				;
		$a =~ s/　//g				;
		if($a ne '')	{&DispError2($GB,"ＥＲＲＯＲ！","ひらがなしか受け付けていません");	}
	}
	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_4WORLD'} eq "kata")
	{
		my $a = $GB->{FORM}->{'MESSAGE'}	;
		$a =~ s/&gt;&gt;[0-9\-,]+//g		;	# >>23とか
		$a =~ s/[\x81][\x48-\x49]//g		;	# ？　と　！
		$a =~ s/[\x81][\x5B-\x5C]//g		;	# ー　と　―
		$a =~ s/[\x83][\x40-\x9F]//g		;
		$a =~ s/<br>//g				;
		$a =~ s/ //g				;
		$a =~ s/　//g				;
		if($a ne '')	{&DispError2($GB,"ＥＲＲＯＲ！","カタカナしか受け付けていません");	}
	}
	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_4WORLD'} eq "senji")
	{
		my $a = $GB->{FORM}->{'MESSAGE'} . $GB->{FORM}->{'subject'}	;
		$a =~ s/&gt;&gt;[0-9\-,]+//g		;	# >>23とか
		$a =~ s/!vip2:stop://g			;	# !vip2:stop:!vip2:heal:
		$a =~ s/!vip2:heal://g			;	# !vip2:stop:
		$a =~ s/(\x81[\x40-\xFF]|\x83[\x40-\x9F]|[\x88-\x9F][\x40-\xFF]|[\xE0-\xFF][\x40-\xFF])+//g; #(いろいろ記号|カタカナ|漢字aA|漢字bB)+
#		$a =~ s/http:\/\/[a-zA-Z0-9.,_\/]+//g	;	#URL 旧　↓新
		$a =~ s/h?ttps?:\/\/[a-zA-Z0-9.,_\/+-]+//g;	# +- ダケ追加。h 抜キト 
		$a =~ s/<br>//g				;
		$a =~ s/ //g				;
		$a =~ s/　//g				;
		if($a ne '')	{&DispError2($GB,"ＥＲＲＯＲ！","漢字とカタカナしか受け付けていません");	}
	}

#$GB->{FORM}->{'MESSAGE'} .= "<hr>$FOX->{$GB->{FORM}->{bbs}}->{'BBS_RAWIP_CHECK'} // PREN=$GB->{COOKIES}{PREN}";

	return	0	;
}
#############################################################################
# 保守ツール対策  by や http://web1.nazca.co.jp/despair/hosyu/
#############################################################################
sub antiHosyu
{
	my ($GB) = @_			;
	if($GB->{FORM}->{'FROM'} =~ /◆2d\.AlKjN5I/)
	{
		&DispError2($GB,"ＥＲＲＯＲ！","ktkr");
	}
	return 0	;
}
#############################################################################
# 携帯での規約見せ　携帯DBの実験 by や
#############################################################################
sub useBBM2
{
	my ($GB) = @_			;

#return 0	;

	if($GB->{KEITAI})	{return 1;}	#携帯
#	if($GB->{P22CH})	{return 1;}	#P2

	return 0	;
}
sub GooMorningKeitai
{
	my ($GB) = @_			;

	#BBM異常時はするー
	if(!$FOX->{BBM2})	{return 0;}

	if(!&useBBM2($GB))	{return 0;}

	my $au = &NotifyUlaBbmPOST($GB)	;
	if($au eq 'ZZZ:700')	{return 0;}
	if($au eq 'ZZZ:701')	{&DispError3($GB,"ＥＲＲＯＲ！","はじめまして。<BR>701[$au]");}
	if($au eq 'ZZZ:702')	{&DispError3($GB,"ＥＲＲＯＲ！","あら、久しぶり。<BR>702[$au]");}
	if($au eq 'ZZZ:703')	{&DispError3($GB,"ＥＲＲＯＲ！","こんばんわ。<BR>703[$au]");}
	if($au eq 'ZZZ:704')	{&DispError3($GB,"ＥＲＲＯＲ！","かまた。<BR>704[$au]");}
	if($au eq 'ZZZ:705')	{&DispError3($GB,"ＥＲＲＯＲ！","ぴんぽん。<BR>705[$au]");}
	if($au =~ /ZZZ:710/)	{&DispError3($GB,"ＥＲＲＯＲ！","■ もちつけ2.0。<BR>710[$au]");}
	&DispError3($GB,"ＥＲＲＯＲ！","ただいま調整中。<BR>?[$au]");
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

	# エラーチェック
	if ($response->is_error)
	{
		return "通信エラー";
	}
	chomp($db_content);
	return $db_content;
}
#############################################################################
#　伝説の機能 2.0
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
	$GB->{FORM}->{'MESSAGE'} .= "MP$pay使って回復の呪文を唱えた!<font color=blue>★ミ</font> $MP回復した。<br>";

	if(open(STP,">> $fff"))
	{
		print STP "$GB->{FORM}->{'DMDM'}\t$GB->{FORM}->{'MDMD'}\t$IP\t-$MP\n";
		close(STP)	;
	}
	my $dn = @dmg + 1	;

#	my $td = $MP * $dn	;
	my $td = $alldamege - $MP	;

	$GB->{FORM}->{'MESSAGE'} .= "このスレは$dn回目に回復の呪文を受けた ($td/$MX)<br>";

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

	$GB->{NINNIN} = 0		;		#sakuの時はbe表示

	$GB->{FORM}->{'MESSAGE'} .= "<br>---<br>";
	if($GB->{BEpoints} < 8000)	{$GB->{FORM}->{'MESSAGE'} .= "見習い戦士のふつうの攻撃<br>";}
	elsif($GB->{BEelite} eq 'BRZ'){$GB->{FORM}->{'MESSAGE'} .= "プチヒーローのちょっとした攻撃 <br>"; $PLUSATK = 5;}
	elsif($GB->{BEelite} eq 'PLT'){$GB->{FORM}->{'MESSAGE'} .= "まほうつかいたんのつよめの攻撃 <br>"; $PLUSATK = 10;}
	elsif($GB->{BEelite} eq 'DIA'){$GB->{FORM}->{'MESSAGE'} .= "グランドプリーストのかなりの攻撃 <br>"; $PLUSATK = 15;}
	elsif($GB->{BEelite} eq 'SOL'){$GB->{FORM}->{'MESSAGE'} .= "真の勇者のさすがの攻撃 <br>"; $PLUSATK = 20;}

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
			$GB->{FORM}->{'MESSAGE'} .= "すかった。<br>";
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
			$GB->{FORM}->{'MESSAGE'} .= "すかった２。<br>";
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

	$GB->{FORM}->{'MESSAGE'} .= "MP$mpmp使ってへっぽこの呪文を唱えた。<font color=red>★ミ</font> （スレのダメージ $alldamege） <br>";

	if(open(STP,">> $fff"))
	{
		print STP "$GB->{FORM}->{'DMDM'}\t$GB->{FORM}->{'MDMD'}\t$IP\t$MP\n";
		close(STP)	;
	}
	my $dn = @dmg + 1	;

#	my $td = $MP * $dn	;
	my $td = $alldamege + $MP	;

	$GB->{FORM}->{'MESSAGE'} .= "このスレは$dn回目のダメージを受けた ($td/$MX)<br>";
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
		$GB->{FORM}->{'MESSAGE'} .= "こうかは ばつぐんだ!! さらにこのスレは$dn回目のダメージを受けた ($td/$MX)<br>";
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
		$GB->{FORM}->{'MESSAGE'} .= "ぼうそうがはじまった!! さらにこのスレは$dn回目のダメージを受けた ($td/$MX)<br>";
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
			$GB->{FORM}->{'MESSAGE'} .= "追加攻撃!! さらにこのスレは$dn回目のダメージを受けた ($td/$MX)<br>";
		}		
	}

	if($td >= $MX)
	{
		&VipQ2Saku($GB,$GB->{FORM}->{bbs},$GB->{FORM}->{key})	;
		$GB->{FORM}->{'MESSAGE'} .= "このスレは・・・<br><br>停止しました。<br>";
		$GB->{VIPQ2STOP} = 1	;	#スレスト
	}

	return 1;
}
sub gotoBobon
{
	my ($GB,$log,$ipip,$mes) = @_	;

	if($ipip =~ /[^0-9\.]/)	{return 0;}
#携帯
#</b>団体役員(関東)<b><><>2008/09/29(月) 17:04:10.76 xN47qM/8O<>泣きそう<>うんこたれた
#<>wb35proxy04.ezweb.ne.jp(05001018144926_mi.ezweb.ne.jp)<>59.135.38.174<> (2dec14b8c0e2be97b74d845f3be5ced0 hardkitayo@yahoo.co.jp)<>KDDI-SH31 UP.Browser/6.2.0.10.3.5 (GUI) MMP/2.0 
#P2
#</b>四十代(埼玉県)<b><><>2008/09/29(月) 16:28:58.51 UZXBNes+P<>【news】ニュース速報運用情報13<>パス変更によるsaku回避すると“まずは”IPさらされるから、気をつけろ！
#<>cw43.razil.jp(462143)219.182.232.16<>210.135.98.43<> (85c00438802bac3606f3a3edbd96bbe9 iressa01@yahoo.co.jp)<>Monazilla/1.00 (P2/p2.2ch.net; p2-client-ip: 
	$log =~ /\((\S+)\)[0-9\.]*<>[0-9\.]+<>/	;
	my $yaki = $1	;

	my $rhost = gethostbyaddr(pack('c4',split(/\./, $ipip)), 2) || $ipip;
	if($rhost =~ /docomo.ne.jp$/)	{return "焼いてもらってちょ docomo[$yaki]";}
	if($rhost =~ /ezweb.ne.jp$/)	{return "焼いてもらってちょ AU[$yaki]";}
	if($rhost =~ /jp-\w.ne.jp$/)	{return "焼いてもらってちょ softbank[$yaki]";}
	if($rhost =~ /vodafone.ne.jp$/)	{return "焼いてもらってちょ softbank[$yaki]";}
	if($rhost =~ /\.razil.jp$/)	{return "焼いてもらってちょ P2[$yaki]";}
	if($rhost =~ /\.maido3.com$/)	{return "これは焼けない1";}
	if($rhost =~ /\.ibis.ne.jp$/)	{return "ibisはまだ対応していないのだ";}
	if($rhost =~ /\.jig.jp$/)	{return "jigはまだ対応していないのだ";}


	my $bburl = "http://qb6.2ch.net/test/asokin/kiri.cgi?ox=$ipip&key=$mes&cow=274";
	my $ua = LWP::UserAgent->new();
	$ua->agent('Mozilla/5.0 FOX(2ch.se)');
	$ua->timeout(3);
	my $request = HTTP::Request->new('GET', $bburl);
	my $response = $ua->request($request) ;#ここで GET 処理

	return "わっ";
}
sub VipQ2Saku
{
	my ($GB,$bbs,$key) = @_	;

#$GB->{FORM}->{'MESSAGE'} .= "VipQ2Saku<br>";
	my $logdat = "../../test/ggg/" . $bbs . "dat/" . $key . ".cgi";
	if(!open(LXX,"$logdat"))	{return 0;}
#$GB->{FORM}->{'MESSAGE'} .= "ログ発見<br>";
	my @lxx = <LXX>	;
	close(LXX)	;

	my $gxx = $lxx[0]	;
#(0a9a9eea0582eb7fad96dcbb0333de29 yakin@80.kg)<>
	$gxx =~ / \(([0-9a-z]+) (\S+)\)<>/;
	my $gx1 = $1	;
	my $gx2 = $2	;

	if($gx1 && $gx2)
	{
		my $sp = 300		;		# 基本値
		$sp += int(rand(800))	;		# ランダム加算
		if($GB->{KABUU})	{$sp *= 5;}	# 株主優待加算

		if(&wasteBEx($GB,$gx2,$gx1,$sp))
		{
			$GB->{FORM}->{'MESSAGE'} .= "<font size=+1 face=\"Arial\" color=red><b>$sp</b></font> sakuった<br>";
		}
		else
		{#パスワード変更で逃げたりポイント足りないときはボボン送り
			my $bxx = $lxx[0]		;
			$bxx =~ /<>([0-9\.]+)<>/	;
			my $ipip = $1			;
			my $rr = &gotoBobon($GB,$bxx,$ipip,"vip2:saku:($bbs)")	;
			$GB->{FORM}->{'MESSAGE'} .= "<font color=red>（￣ー￣）ニヤリッ</font> ($rr)<br>";
		}
	}
#●かな?
#$GB->{FORM}->{'MESSAGE'} .= "●かな?<br>";
	my $mxx = $lxx[0]	;
#ちょろ ★<><>2007/12/24(月) 03:47:54.75 5vawQ6AY0<>すれたて<>
#●の一時停止のテスト<>KD125055017119.ppp-bb.dion.ne.jp[tjuTdvdhyupQ06ao]<>125.55.17.119<>tjuTdvdhyupQ06ao ( )<>Monazilla/1.00 (JaneView/0.1.12.1)
#[tjuTdvdhyupQ06ao]

	my ($d1,$d2,$d3,$d4,$d5,$d6,$d7,$d8,$d9) = split(/<>/,$mxx)	;
	$d6 =~ /\[([a-zA-Z0-9]+)\]/;
	my $mx1 = $1	;
	my $mx2 = $1	;
#&DispError2($GB,"ＥＲＲＯＲ！","d6=[$mx1][$d6][$mxx]");
#&DispError2($GB,"ＥＲＲＯＲ！","d6=[$mx1][$d6]");
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
$GB->{FORM}->{'MESSAGE'} .= "<br><font color=red>この●はしばらくの間スレ立てできなくなりました。</font><br><br>";
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
			&DispError2($GB,"ＥＲＲＯＲ！","この●はしばらくの間スレ立てできません。[あと$ato秒](saku担当)");
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
	my $response = $ua->request($request) ;#ここで GET 処理
	my $response_body = $response->content();#GETの結果はここに入っている

	my $db_content = $response->content();

	my ($user_points, $xxx) = split(/ /, $db_content);

	if($xxx eq '')
	{
		$GB->{FORM}->{'MESSAGE'} .= "ログインしてないです。<br>";
		return 0		;
	}
	my $BEpoints = $user_points	;
	my $BExxx    = $xxx		;
	if($BEpoints < $mp)
	{
		$GB->{FORM}->{'MESSAGE'} .= "MPが足りません。($mp/$BEpoints)";
		return 0		;
	}
	my $uiui = &rulaPayCost($DMDM,$MDMD,$BExxx,$mp);
	if($uiui eq '通信エラー')
	{
		&DispError2($GB,"ＥＲＲＯＲ！","beサーバが・・・");
	}
	if($uiui =~ /insufficient points/)
	{
		$GB->{FORM}->{'MESSAGE'} .= '急ぎ杉ですよ。。。<br>';
		return 0		;
	}
	return 1;
}
#########################################
#	BE ポイント消費
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
	my $response = $ua->request($request) 		;#ここで GET 処理
	my $response_code = $response->code()		;#結果はここに入っている
	my $response_body = $response->content()	;#GETの結果はここに入っている

	# エラーチェック
	if ($response->is_error)
	{
		return "通信エラー";
	}

	return $response_body	;
}
#############################################################################
#	リモホ -> 都道府県名
#############################################################################
sub area47
{
	my ($GB) = @_;

	my @kenmei = ()	;

	@kenmei = (
'樺太','北海道','青森県','岩手県','宮城県','秋田県','山形県','福島県','茨城県','栃木県',
'群馬県','埼玉県','千葉県','東京都','神奈川県','新潟県','富山県','石川県','福井県','山梨県',
'長野県','岐阜県','静岡県','愛知県','三重県','滋賀県','京都府','大阪府','兵庫県','奈良県',
'和歌山県','鳥取県','島根県','岡山県','広島県','山口県','徳島県','香川県','愛媛県','高知県',
'福岡県','佐賀県','長崎県','熊本県','大分県','宮崎県','鹿児島県','沖縄県','台湾','不明なsoftbank',
'東北地方','関東地方','中部地方','関西地方','四国地方','中国地方','九州地方','西日本','東日本','CATV-infoweb',
'空','糸','62','63','64','dion軍','田舎おでん','catv?','長屋','チベット自治区',
'北陸地方','山陰地方','中国四国','73','74','75','76','スリランカ','広西チワン族自治区','内モンゴル自治区',
'USA','カナダ','82','83','84','85','86','87','伊勢','地底',
'チリ')	;

if($GB->{FORM}->{bbs} eq 'news12345')
{
	@kenmei = (
'横浜','福岡県','香川県','群馬県','宮城県','沖縄県','宮崎県','佐賀県','茨城県','高知県',
'岡山県','大阪府','秋田県','埼玉県','愛知県','新潟県','大分県','鹿児島県','静岡県','長崎県',
'長野県','愛媛県','鳥取県','神奈川県','三重県','兵庫県','京都府','東京都','滋賀県','奈良県',
'和歌山県','島根県','熊本県','山形県','石川県','富山県','徳島県','千葉県','福井県','岐阜県',
'福島県','北海道','山梨県','山口県','岩手県','広島県','栃木県','青森県','台湾','会津',
'関東地方','中部地方','関西地方','四国地方','中国地方','九州地方','西日本','東日本','東北地方','CATV-infoweb',
'空','糸','62','63','64','久留米','田舎おでん','讃岐','長屋','巣鴨',
'北陸地方','山陰地方','中国四国','73','74','75','76','スリランカ','ネブラスカ州','コネチカット州',
'USA','カナダ','82','83','84','85','86','87','88','地底',
'チリ')	;
}
if($GB->{FORM}->{bbs} eq 'campus')
{
	@kenmei = (
'横浜','福岡県','香川県','群馬県','宮城県','沖縄県','宮崎県','佐賀県','茨城県','高知県',
'岡山県','大阪府','秋田県','埼玉県','愛知県','新潟県','大分県','鹿児島県','静岡県','長崎県',
'長野県','愛媛県','鳥取県','神奈川県','三重県','兵庫県','京都府','東京都','滋賀県','奈良県',
'和歌山県','島根県','熊本県','山形県','石川県','富山県','徳島県','千葉県','福井県','岐阜県',
'福島県','北海道','山梨県','山口県','岩手県','広島県','栃木県','青森県','台湾','会津',
'関東地方','中部地方','関西地方','四国地方','中国地方','九州地方','西日本','東日本','東北地方','CATV-infoweb',
'空','糸','62','63','64','久留米','田舎おでん','讃岐','長屋','巣鴨',
'北陸地方','山陰地方','中国四国','73','74','75','76','77','ネブラスカ州','コネチカット州',
'USA','カナダ','82','83','84','85','86','87','88','地底',
'チリ')	;
}
if($GB->{FORM}->{bbs} eq 'newsnewsnews')
{
	@kenmei = (
'石油','もこりん','りんご','わんこそば','ささかまぼこ','きりたんぽ','さくらんぼ','もも','なっとう','ぎょうざ',
'こんにゃく','しまむら','らっかせい','もんじゃ','しうまい','おにぎり','ぶり','かぶらずし','らっきょう','ほうとう',
'聖火リレー','あゆ','はんぺん','味噌カツ','あかふく','鮒寿司','おたべ','たこやき','おいしい水','しか',
'うめぼし','なし','どろえび','きびだんご','もみじ饅頭','ふく','すだち','うどん','みかん','かつお',
'あら','とうふ','ちゃんぽん','馬刺し','カボス','そのまんま','黒酢','泡盛','ばなな','キムチ',
'黄河','長江','珠河','淮河','松花江','海河','銭塘江','平湖','春暁','ウイグル族',
'わたあめ','蜘蛛','62','63','64','笑','田舎おでん','プーアル茶','大酒','湖北省',
'回族','チワン族','ミャオ族','73','74','75','76','77','遼寧省','甘粛省',
'USA','カナダ','82','83','84','85','86','87','88','地底',
'酢豚')	;
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
	my $remo = $GB->{HOST29}; #いわゆるリモホ

#return "うはは";

	#P2の時はルックアップ
	if($GB->{P22CH})
	{
		my $p2r = "";
		#return "アイダホ州";X-P2-Mobile-Serial-BBM
		if($ENV{HTTP_USER_AGENT} =~ /p2-client-ip: (\d+\.\d+\.\d+\.\d+)/)
		{
			$p2r = $1;

			# リモートホスト名を記録する(規制が効くように)
			$remo = gethostbyaddr(pack('C4',split(/\./, $p2r)), 2) || $p2r;
		}
		else
		{
			&DispError2($GB,"ＥＲＲＯＲ！","進入禁止");
		}
		##携帯固有番号取得
		if(&mumumuIsIP4EZWeb($p2r))
		{
			my $ser = $ENV{HTTP_X_P2_MOBILE_SERIAL_BBM}	;
#if(open(LX,">> HOST29.000")){print LX "(P2:AU)$remo($ser)\n";close(LX);}
if($ser eq ''){&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：端末固有情報を送信してください。");}
		}
		elsif(&mumumuIsIP4IMode($p2r))
		{
			my $ser = $ENV{HTTP_X_P2_MOBILE_SERIAL_BBM}	;
#if(open(LX,">> HOST29.000")){print LX "(P2:Docomo)$remo($ser)\n";close(LX);}
if($ser eq ''){&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：端末固有情報を送信してください。");}
		}
		elsif(&mumumuIsIP4Vodafone($p2r))
		{
			my $ser = $ENV{HTTP_X_P2_MOBILE_SERIAL_BBM}	;
#if(open(LX,">> HOST29.000")){print LX "(P2:SB)$remo($ser)\n";close(LX);}
if($ser eq ''){&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：端末固有情報を送信してください。");}
		}
	}

	if($remo =~ /\.go\.jp$/)		{return "伊勢";}
	if($remo =~ /\.tw$/)			{return "台";}
	if($remo =~ /\.cn$/)			{return "中";}
	if($remo =~ /\.kr$/)			{return "韓";}
	if($remo =~ /\.kp$/)			{return "朝";}
	if($remo =~ /\.de$/)			{return "独";}
	if($remo =~ /\.us$/)			{return "米";}
	if($remo =~ /\.fr$/)			{return "仏";}
	if($remo =~ /\.uk$/)			{return "英";}
	if($remo =~ /\.is$/)			{return "アイスランド";}
	if($remo =~ /\.au$/)			{return "豪";}
	if($remo =~ /\.ca$/)			{return "加";}
	if($remo =~ /\.br$/)			{return "ブラジル";}
	if($remo =~ /\d+\.\d+\.\d+\.\d+$/)	{return "アラビア";}

	# SB
	if($remo =~ /jp-.\.ne\.jp/)
	{
		#Jフォン東日本
		if($remo =~ /jp-d\.ne\.jp/){return "北海道";}
		if($remo =~ /jp-h\.ne\.jp/){return "東北・新潟";}
		if($remo =~ /jp-t\.ne\.jp/){return "関東・甲信越";}
		#Jフォン西日本
		if($remo =~ /jp-k\.ne\.jp/){return "関西";}
		if($remo =~ /jp-r\.ne\.jp/){return "北陸";}
		if($remo =~ /jp-s\.ne\.jp/){return "四国";}
		if($remo =~ /jp-n\.ne\.jp/){return "中国";}
		if($remo =~ /jp-q\.ne\.jp/){return "九州・沖縄";}
		#Ｊフォン東海 jp-c.ne.jp
		if($remo =~ /jp-c\.ne\.jp/){return "東海";}
		return 77;
	}
	# AU
	if($remo =~ /\.ezweb\.ne\.jp/)
	{
		if($GB->{IDNOTANE} =~ /^0500101/)	{return "関東";}
		if($GB->{IDNOTANE} =~ /^0500103/)	{return "東海";}
		if($GB->{IDNOTANE} =~ /^0500401/)	{return "関東・甲信越";}
		if($GB->{IDNOTANE} =~ /^0500403/)	{return "東海";}
		if($GB->{IDNOTANE} =~ /^0500405/)	{return "-長野";}
		if($GB->{IDNOTANE} =~ /^050/)	{return "東海・関東";}
		if($GB->{IDNOTANE} =~ /^0700/)	{return "関西・北陸";}
		if($GB->{IDNOTANE} =~ /^0701/)	{return "九州";}
		if($GB->{IDNOTANE} =~ /^07022/)	{return "山陽";}
		if($GB->{IDNOTANE} =~ /^0702/)	{return "中国・四国";}
		if($GB->{IDNOTANE} =~ /^0703/)	{return "新潟・東北";}
		if($GB->{IDNOTANE} =~ /^0704/)	{return "北陸地方";}
		if($GB->{IDNOTANE} =~ /^0705/)	{return "北海道";}
		if($GB->{IDNOTANE} =~ /^0706/)	{return "四国";}
		if($GB->{IDNOTANE} =~ /^0707/)	{return "九州・沖縄";}
		if($GB->{IDNOTANE} =~ /^070/)	{return "au-関東以外";}
#if(open(LX,">> HOST29.000")){print LX "(AU)$remo($GB->{IDNOTANE})\n";close(LX);}
		return 78;
	}
	if($remo =~ /proxy(\d+)\.docomo\.ne\.jp/)
	{
		my $ppp = $1			;
		return 79			;
	}
	#携帯はスルー
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

	# namazuplus用(89 = 地底)
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

	#●はスルー
	if($GB->{MARU})			{return 65;}

#if(open(LX,">> HOST29.000")){print LX "(xxx)$remo($ken) = $r\n";close(LX);}
#&DispError2($GB,"ＥＲＲＯＲ！","「dion.ne.jp」はかけないのだ!!<br><a href=\"http://qb5.2ch.net/test/read.cgi/operate/1175759037/l5n\">ここで</a>fusianasanして県名報告してネ");

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

	if($ken =~ /^61-27-/)		{return 1;}	#北海道
	if($ken =~ /^61-25-140-/)	{return 8;}	#茨城
	if($ken =~ /^61-26-231-/)	{return 8;}	#茨城
	if($ken =~ /^59-171-144-/)	{return 10;}	#群馬
	if($ken =~ /^61-24-20-/)	{return 10;}	#群馬
	if($ken =~ /^59-171-106-/)	{return 11;}	#埼玉
	if($ken =~ /^61-21-248-/)	{return 11;}	#埼玉
	if($ken =~ /^61-21-253-/)	{return 11;}	#埼玉
	if($ken =~ /^61-23-223-/)	{return 11;}	#埼玉
	if($ken =~ /^203-165-84-/)	{return 11;}	#埼玉
	if($ken =~ /^203-165-244-/)	{return 11;}	#埼玉
	if($ken =~ /^210-20-165-/)	{return 11;}	#埼玉
	if($ken =~ /^210-20-196-/)	{return 11;}	#埼玉
	if($ken =~ /^61-23-72-/)	{return 12;}	#千葉
	if($ken =~ /^61-23-94-/)	{return 12;}	#千葉
	if($ken =~ /^61-24-24-/)	{return 12;}	#千葉
	if($ken =~ /^203-165-164-/)	{return 12;}	#千葉
	if($ken =~ /^210-194-64-/)	{return 12;}	#千葉
	if($ken =~ /^210-194-66-/)	{return 12;}	#千葉
	if($ken =~ /^59-171-201-/)	{return 13;}	#東京
	if($ken =~ /^60-62-121-/)	{return 13;}	#東京
	if($ken =~ /^61-23-157-/)	{return 13;}	#東京
	if($ken =~ /^61-23-171-/)	{return 13;}	#東京
	if($ken =~ /^61-24-32-/)	{return 13;}	#東京
	if($ken =~ /^61-26-3-/)		{return 13;}	#東京
	if($ken =~ /^61-26-36-/)	{return 13;}	#東京
	if($ken =~ /^61-26-50-/)	{return 13;}	#東京
	if($ken =~ /^61-26-232-/)	{return 13;}	#東京
	if($ken =~ /^124-144-94-/)	{return 13;}	#東京
	if($ken =~ /^125-14-111-/)	{return 13;}	#東京
	if($ken =~ /^125-14-81-/)	{return 13;}	#東京
	if($ken =~ /^125-14-240-/)	{return 13;}	#東京
	if($ken =~ /^203-165-104-/)	{return 13;}	#東京
	if($ken =~ /^203-165-204-/)	{return 13;}	#東京
	if($ken =~ /^203-165-232-/)	{return 13;}	#東京
	if($ken =~ /^210-20-66-/)	{return 13;}	#東京
	if($ken =~ /^210-194-120-/)	{return 13;}	#東京
	if($ken =~ /^210-194-152-/)	{return 13;}	#東京
	if($ken =~ /^203-165-96-/)	{return 13;}	#東京
	if($ken =~ /^61-21-73-/)	{return 14;}	#神奈川
	if($ken =~ /^59-171-234-/)	{return 14;}	#神奈川
	if($ken =~ /^61-24-194-/)	{return 14;}	#神奈川
	if($ken =~ /^61-24-194-/)	{return 14;}	#神奈川
	if($ken =~ /^61-26-205-/)	{return 14;}	#神奈川
	if($ken =~ /^61-26-246-/)	{return 14;}	#神奈川
	if($ken =~ /^61-26-253-/)	{return 14;}	#神奈川
	if($ken =~ /^124-144-103-/)	{return 14;}	#神奈川
	if($ken =~ /^125-14-212-/)	{return 14;}	#神奈川
	if($ken =~ /^124-144-137-/)	{return 14;}	#神奈川
	if($ken =~ /^210-20-154-/)	{return 14;}	#神奈川
	if($ken =~ /^210-194-19-/)	{return 14;}	#神奈川
	if($ken =~ /^210-194-62-/)	{return 14;}	#神奈川
	if($ken =~ /^210-194-184-/)	{return 14;}	#神奈川
	if($ken =~ /^210-194-240-/)	{return 14;}	#神奈川
	if($ken =~ /^60-62-34-/)	{return 15;}	#新潟
	if($ken =~ /^125-15-201-/)	{return 25;}	#滋賀
#	if($ken =~ /^61-27-136-/)	{return 31;}	#鳥取
	if($ken =~ /^60-62-47-/)	{return 31;}	#鳥取
	if($ken =~ /^61-22-30-/)	{return 35;}	#山口
	if($ken =~ /^61-22-45-/)	{return 35;}	#山口
	if($ken =~ /^61-22-39-/)	{return 40;}	#福岡
	if($ken =~ /^61-22-235-/)	{return 40;}	#福岡
	if($ken =~ /^61-26-232-/)	{return 40;}	#福岡

#	if(open(LX,">> HOST29.000")){print LX "(home)$remo($ken)\n";close(LX);}
#&DispError2($GB,"ＥＲＲＯＲ！","「home.ne.jp」はかけないのだ!!<br><a href=\"http://qb5.2ch.net/test/read.cgi/operate/1173710224/l5n\">ここで</a>fusianasanして県名報告してネ");
	return 69;
}
sub area47sb
{
	my ($remo,$ken) = @_;

	if($ken eq '126068')	{return 1;}	#北海道
	if($ken eq '218127')	{return 1;}	#北海道
	if($ken eq '219041')	{return 1;}	#北海道
	if($ken eq '219168')	{return 1;}	#北海道
	if($ken eq '219181')	{return 1;}	#北海道
	if($ken eq '221023')	{return 1;}	#北海道
	if($ken eq '221030')	{return 1;}	#北海道
	if($ken eq '221032')	{return 1;}	#北海道
	if($ken eq '221036')	{return 1;}	#北海道
	if($ken eq '221046')	{return 1;}	#北海道
	if($ken eq '221062')	{return 1;}	#北海道
	if($ken eq '221029')	{return 2;}	#青森
	if($ken eq '221054')	{return 2;}	#青森
	if($ken eq '219053')	{return 3;}	#岩手
	if($ken eq '219173')	{return 3;}	#岩手
	if($ken eq '221033')	{return 3;}	#岩手
	if($ken eq '221039')	{return 3;}	#岩手
	if($ken eq '221053')	{return 3;}	#岩手
	if($ken eq '221054')	{return 3;}	#岩手
	if($ken eq '126098')	{return 4;}	#宮城
	if($ken eq '218112')	{return 4;}	#宮城
	if($ken eq '219057')	{return 4;}	#宮城・秋田
	if($ken eq '219171')	{return 4;}	#宮城
	if($ken eq '219208')	{return 4;}	#宮城
	if($ken eq '221020')	{return 4;}	#宮城
	if($ken eq '221026')	{return 4;}	#宮城
	if($ken eq '221105')	{return 4;}	#秋田
	if($ken eq '221058')	{return 5;}	#宮城
	if($ken eq '219051')	{return 7;}	#福島・宮城
	if($ken eq '219057')	{return 7;}	#福島
	if($ken eq '219172')	{return 7;}	#福島
	if($ken eq '221044')	{return 7;}	#福島
	if($ken eq '060100')	{return 8;}	#茨城
	if($ken eq '218137')	{return 8;}	#茨城
	if($ken eq '219006')	{return 8;}	#茨城
	if($ken eq '220005')	{return 8;}	#茨城
	if($ken eq '220006')	{return 8;}	#茨城
	if($ken eq '221040')	{return 8;}	#茨城
	if($ken eq '221043')	{return 8;}	#茨城
	if($ken eq '060091')	{return 9;}	#栃木
	if($ken eq '126096')	{return 9;}	#栃木
	if($ken eq '219055')	{return 9;}	#栃木
	if($ken eq '219056')	{return 9;}	#栃木
	if($ken eq '219192')	{return 9;}	#栃木
	if($ken eq '220004')	{return 9;}	#栃木
	if($ken eq '221027')	{return 9;}	#栃木
	if($ken eq '221031')	{return 9;}	#栃木
	if($ken eq '220003')	{return 11;}	#群馬
	if($ken eq '220007')	{return 11;}	#群馬
	if($ken eq '060086')	{return 11;}	#埼玉
	if($ken eq '218128')	{return 11;}	#埼玉
	if($ken eq '218118')	{return 11;}	#埼玉
	if($ken eq '218119')	{return 11;}	#埼玉
	if($ken eq '218177')	{return 11;}	#埼玉
	if($ken eq '219012')	{return 11;}	#埼玉
	if($ken eq '219013')	{return 11;}	#埼玉
	if($ken eq '219014')	{return 11;}	#埼玉
	if($ken eq '219058')	{return 11;}	#埼玉・群馬
	if($ken eq '219181')	{return 11;}	#埼玉
	if($ken eq '219182')	{return 11;}	#埼玉
	if($ken eq '219183')	{return 11;}	#埼玉
	if($ken eq '219193')	{return 11;}	#埼玉
	if($ken eq '219194')	{return 11;}	#埼玉
	if($ken eq '219199')	{return 11;}	#埼玉
	if($ken eq '219201')	{return 11;}	#埼玉
	if($ken eq '219214')	{return 11;}	#埼玉
	if($ken eq '219200')	{return 11;}	#埼玉
	if($ken eq '221018')	{return 11;}	#埼玉
	if($ken eq '220001')	{return 11;}	#埼玉
	if($ken eq '060088')	{return 12;}	#千葉
	if($ken eq '060089')	{return 12;}	#千葉
	if($ken eq '060101')	{return 12;}	#千葉
	if($ken eq '126064')	{return 12;}	#千葉
	if($ken eq '126112')	{return 12;}	#千葉
	if($ken eq '218135')	{return 12;}	#千葉
	if($ken eq '218178')	{return 12;}	#千葉
	if($ken eq '218180')	{return 12;}	#千葉
	if($ken eq '219010')	{return 12;}	#千葉
	if($ken eq '219011')	{return 12;}	#千葉
	if($ken eq '219016')	{return 12;}	#千葉
	if($ken eq '219174')	{return 12;}	#千葉
	if($ken eq '219176')	{return 12;}	#千葉
	if($ken eq '219189')	{return 12;}	#千葉
	if($ken eq '219190')	{return 12;}	#千葉
	if($ken eq '219191')	{return 12;}	#千葉
	if($ken eq '221022')	{return 12;}	#千葉
	if($ken eq '221025')	{return 12;}	#千葉
	if($ken eq '221038')	{return 12;}	#千葉
	if($ken eq '221056')	{return 12;}	#千葉
	if($ken eq '060076')	{return 13;}	#東京
	if($ken eq '060081')	{return 13;}	#東京
	if($ken eq '060085')	{return 13;}	#東京
	if($ken eq '126065')	{return 13;}	#東京
	if($ken eq '126080')	{return 13;}	#東京
	if($ken eq '218130')	{return 13;}	#東京
	if($ken eq '218132')	{return 13;}	#東京
	if($ken eq '218133')	{return 13;}	#東京
	if($ken eq '218134')	{return 13;}	#東京
	if($ken eq '218138')	{return 13;}	#東京
	if($ken eq '218176')	{return 13;}	#東京
	if($ken eq '219000')	{return 13;}	#東京
	if($ken eq '219001')	{return 13;}	#東京
	if($ken eq '219002')	{return 13;}	#東京
	if($ken eq '219003')	{return 13;}	#東京
	if($ken eq '219004')	{return 13;}	#東京
	if($ken eq '219005')	{return 13;}	#東京
	if($ken eq '219007')	{return 13;}	#東京
	if($ken eq '219008')	{return 13;}	#東京
	if($ken eq '219009')	{return 13;}	#東京
	if($ken eq '219011')	{return 13;}	#東京
	if($ken eq '219015')	{return 13;}	#東京
	if($ken eq '219018')	{return 13;}	#東京
	if($ken eq '219017')	{return 13;}	#東京
	if($ken eq '219019')	{return 13;}	#東京
	if($ken eq '219036')	{return 13;}	#東京
	if($ken eq '219037')	{return 13;}	#東京
	if($ken eq '219169')	{return 13;}	#東京
	if($ken eq '219176')	{return 13;}	#東京
	if($ken eq '219184')	{return 13;}	#東京
	if($ken eq '219185')	{return 13;}	#東京
	if($ken eq '219186')	{return 13;}	#東京
	if($ken eq '219187')	{return 13;}	#東京
	if($ken eq '219188')	{return 13;}	#東京
	if($ken eq '219195')	{return 13;}	#東京
	if($ken eq '219196')	{return 13;}	#東京
	if($ken eq '219197')	{return 13;}	#東京
	if($ken eq '219198')	{return 13;}	#東京
	if($ken eq '219215')	{return 13;}	#東京
	if($ken eq '219218')	{return 13;}	#東京
	if($ken eq '221016')	{return 13;}	#東京
	if($ken eq '221021')	{return 13;}	#東京
	if($ken eq '221028')	{return 13;}	#東京
	if($ken eq '221034')	{return 13;}	#東京
	if($ken eq '221041')	{return 13;}	#東京
	if($ken eq '221106')	{return 13;}	#東京
	if($ken eq '221108')	{return 13;}	#東京
	if($ken eq '060082')	{return 14;}	#神奈川
	if($ken eq '060083')	{return 14;}	#神奈川
	if($ken eq '126067')	{return 14;}	#神奈川
	if($ken eq '219204')	{return 14;}	#神奈川
	if($ken eq '218139')	{return 14;}	#神奈川
	if($ken eq '218140')	{return 14;}	#神奈川
	if($ken eq '218141')	{return 14;}	#神奈川
	if($ken eq '218144')	{return 14;}	#神奈川
	if($ken eq '219035')	{return 14;}	#神奈川
	if($ken eq '219038')	{return 14;}	#神奈川
	if($ken eq '219039')	{return 14;}	#神奈川
	if($ken eq '219042')	{return 14;}	#神奈川
	if($ken eq '219043')	{return 14;}	#神奈川
	if($ken eq '219044')	{return 14;}	#神奈川
	if($ken eq '219045')	{return 14;}	#神奈川
	if($ken eq '219046')	{return 14;}	#神奈川
	if($ken eq '219052')	{return 14;}	#神奈川
	if($ken eq '219175')	{return 14;}	#神奈川
	if($ken eq '219177')	{return 14;}	#神奈川
	if($ken eq '219178')	{return 14;}	#神奈川
	if($ken eq '219179')	{return 14;}	#神奈川
	if($ken eq '219180')	{return 14;}	#神奈川
	if($ken eq '219202')	{return 14;}	#神奈川
	if($ken eq '219205')	{return 14;}	#神奈川
	if($ken eq '219206')	{return 13;}	#神奈川・東京
	if($ken eq '219207')	{return 14;}	#神奈川
	if($ken eq '221017')	{return 14;}	#神奈川
	if($ken eq '221019')	{return 14;}	#神奈川
	if($ken eq '221037')	{return 14;}	#神奈川
	if($ken eq '219040')	{return 15;}	#新潟
	if($ken eq '219058')	{return 15;}	#新潟
	if($ken eq '220008')	{return 15;}	#新潟
	if($ken eq '221052')	{return 15;}	#新潟
	if($ken eq '221060')	{return 15;}	#新潟
	if($ken eq '220021')	{return 16;}	#富山
	if($ken eq '220052')	{return 16;}	#富山
	if($ken eq '219213')	{return 17;}	#石川
	if($ken eq '221071')	{return 17;}	#石川
	if($ken eq '221081')	{return 17;}	#石川
	if($ken eq '221093')	{return 17;}	#石川
	if($ken eq '221095')	{return 17;}	#石川
	if($ken eq '219061')	{return 18;}	#福井
	if($ken eq '220024')	{return 18;}	#福井
	if($ken eq '220010')	{return 19;}	#山梨・静岡
	if($ken eq '220009')	{return 20;}	#長野
	if($ken eq '126069')	{return 22;}	#静岡
	if($ken eq '218131')	{return 22;}	#静岡
	if($ken eq '218143')	{return 22;}	#静岡
	if($ken eq '219047')	{return 22;}	#静岡
	if($ken eq '219048')	{return 22;}	#静岡
	if($ken eq '220023')	{return 22;}	#静岡・岐阜
	if($ken eq '220000')	{return 22;}	#静岡
	if($ken eq '220002')	{return 22;}	#静岡
	if($ken eq '221024')	{return 22;}	#静岡・三重
	if($ken eq '060096')	{return 23;}	#岐阜
	if($ken eq '220031')	{return 23;}	#岐阜
	if($ken eq '221035')	{return 23;}	#岐阜
	if($ken eq '221045')	{return 23;}	#岐阜
	if($ken eq '218122')	{return 23;}	#愛知
	if($ken eq '218142')	{return 23;}	#愛知
	if($ken eq '218179')	{return 23;}	#愛知
	if($ken eq '219032')	{return 23;}	#愛知
	if($ken eq '219033')	{return 23;}	#愛知
	if($ken eq '219049')	{return 23;}	#愛知
	if($ken eq '219050')	{return 23;}	#愛知・三重
	if($ken eq '219170')	{return 23;}	#愛知
	if($ken eq '219203')	{return 23;}	#愛知
	if($ken eq '219209')	{return 23;}	#愛知
	if($ken eq '219210')	{return 23;}	#愛知
	if($ken eq '220028')	{return 23;}	#愛知
	if($ken eq '220029')	{return 23;}	#愛知
	if($ken eq '220002')	{return 23;}	#愛知
	if($ken eq '220030')	{return 23;}	#愛知
	if($ken eq '221057')	{return 23;}	#愛知
	if($ken eq '221059')	{return 23;}	#愛知
	if($ken eq '221107')	{return 23;}	#愛知
	if($ken eq '219054')	{return 24;}	#三重
	if($ken eq '220026')	{return 24;}	#三重
	if($ken eq '220027')	{return 24;}	#三重・愛知
	if($ken eq '218129')	{return 25;}	#滋賀
	if($ken eq '220051')	{return 25;}	#滋賀
	if($ken eq '221075')	{return 25;}	#滋賀
	if($ken eq '218121')	{return 26;}	#京都
	if($ken eq '218123')	{return 26;}	#京都
	if($ken eq '219025')	{return 26;}	#京都
	if($ken eq '219029')	{return 26;}	#京都
	if($ken eq '219030')	{return 26;}	#京都・滋賀
	if($ken eq '219092')	{return 26;}	#京都
	if($ken eq '220041')	{return 26;}	#京都
	if($ken eq '220037')	{return 26;}	#京都
	if($ken eq '220046')	{return 26;}	#京都
	if($ken eq '220047')	{return 26;}	#京都
	if($ken eq '221055')	{return 26;}	#京都
	if($ken eq '2210920')	{return 26;}	#京都
	if($ken eq '060105')	{return 27;}	#大阪
	if($ken eq '218121')	{return 27;}	#大阪
	if($ken eq '218126')	{return 27;}	#大阪
	if($ken eq '218129')	{return 27;}	#大阪
	if($ken eq '218136')	{return 27;}	#大阪
	if($ken eq '218181')	{return 27;}	#大阪
	if($ken eq '218182')	{return 27;}	#大阪
	if($ken eq '219020')	{return 27;}	#大阪
	if($ken eq '219021')	{return 27;}	#大阪
	if($ken eq '219023')	{return 27;}	#大阪
	if($ken eq '219024')	{return 27;}	#大阪
	if($ken eq '219062')	{return 27;}	#大阪
	if($ken eq '220011')	{return 27;}	#大阪
	if($ken eq '220012')	{return 27;}	#大阪
	if($ken eq '220013')	{return 27;}	#大阪
	if($ken eq '220018')	{return 27;}	#大阪
	if($ken eq '220032')	{return 27;}	#大阪
	if($ken eq '220033')	{return 27;}	#大阪
	if($ken eq '220034')	{return 27;}	#大阪
	if($ken eq '220035')	{return 27;}	#大阪
	if($ken eq '220036')	{return 27;}	#大阪
	if($ken eq '220038')	{return 27;}	#大阪
	if($ken eq '220042')	{return 27;}	#大阪
	if($ken eq '060110')	{return 28;}	#兵庫
	if($ken eq '218124')	{return 28;}	#兵庫
	if($ken eq '218125')	{return 28;}	#兵庫
	if($ken eq '218154')	{return 28;}	#兵庫
	if($ken eq '219022')	{return 28;}	#兵庫
	if($ken eq '219026')	{return 28;}	#兵庫
	if($ken eq '219027')	{return 28;}	#兵庫
	if($ken eq '220014')	{return 28;}	#兵庫
	if($ken eq '220015')	{return 28;}	#兵庫
	if($ken eq '220016')	{return 28;}	#兵庫
	if($ken eq '220017')	{return 28;}	#兵庫
	if($ken eq '220039')	{return 28;}	#兵庫
	if($ken eq '220040')	{return 28;}	#兵庫
	if($ken eq '220044')	{return 28;}	#兵庫
	if($ken eq '221064')	{return 28;}	#兵庫
	if($ken eq '221092')	{return 28;}	#兵庫
	if($ken eq '218183')	{return 29;}	#奈良・京都
	if($ken eq '126070')	{return 29;}	#奈良
	if($ken eq '220043')	{return 29;}	#奈良
	if($ken eq '221072')	{return 29;}	#奈良
	if($ken eq '220050')	{return 30;}	#和歌山
	if($ken eq '060120')	{return 31;}	#鳥取
	if($ken eq '221079')	{return 32;}	#島根
	if($ken eq '060118')	{return 33;}	#岡山
	if($ken eq '126087')	{return 33;}	#岡山
	if($ken eq '218115')	{return 33;}	#岡山
	if($ken eq '219063')	{return 33;}	#岡山
	if($ken eq '220056')	{return 33;}	#岡山
	if($ken eq '221084')	{return 33;}	#岡山・広島
	if($ken eq '221094')	{return 33;}	#岡山・広島
	if($ken eq '221097')	{return 33;}	#岡山
	if($ken eq '221100')	{return 33;}	#岡山
	if($ken eq '060116')	{return 34;}	#広島
	if($ken eq '218120')	{return 34;}	#広島
	if($ken eq '219060')	{return 34;}	#広島・鳥取
	if($ken eq '220019')	{return 34;}	#広島
	if($ken eq '220020')	{return 34;}	#広島
	if($ken eq '220025')	{return 34;}	#広島
	if($ken eq '220053')	{return 34;}	#広島
	if($ken eq '219034')	{return 35;}	#山口
	if($ken eq '221063')	{return 35;}	#山口
	if($ken eq '221085')	{return 35;}	#山口
	if($ken eq '221086')	{return 36;}	#徳島
	if($ken eq '219028')	{return 37;}	#香川
	if($ken eq '219211')	{return 37;}	#香川
	if($ken eq '220045')	{return 37;}	#香川
	if($ken eq '221080')	{return 37;}	#香川
	if($ken eq '221096')	{return 37;}	#香川
	if($ken eq '221076')	{return 38;}	#愛媛
	if($ken eq '220048')	{return 38;}	#愛媛
	if($ken eq '221089')	{return 39;}	#高知
	if($ken eq '126071')	{return 40;}	#福岡
	if($ken eq '126071')	{return 40;}	#福岡
	if($ken eq '060122')	{return 40;}	#福岡
	if($ken eq '218114')	{return 40;}	#福岡
	if($ken eq '218116')	{return 40;}	#福岡
	if($ken eq '218117')	{return 40;}	#福岡
	if($ken eq '219212')	{return 40;}	#福岡
	if($ken eq '220054')	{return 40;}	#福岡
	if($ken eq '220058')	{return 40;}	#福岡
	if($ken eq '220059')	{return 40;}	#福岡
	if($ken eq '220060')	{return 40;}	#福岡
	if($ken eq '220061')	{return 40;}	#福岡
	if($ken eq '221098')	{return 40;}	#福岡
	if($ken eq '221078')	{return 40;}	#福岡
	if($ken eq '221098')	{return 40;}	#福岡
	if($ken eq '221101')	{return 40;}	#福岡
	if($ken eq '220020')	{return 41;}	#佐賀・福岡
	if($ken eq '221067')	{return 41;}	#佐賀
	if($ken eq '220055')	{return 42;}	#長崎
	if($ken eq '221083')	{return 43;}	#熊本
	if($ken eq '221088')	{return 43;}	#熊本
	if($ken eq '220022')	{return 43;}	#熊本
	if($ken eq '060125')	{return 44;}	#大分
	if($ken eq '218113')	{return 44;}	#大分
	if($ken eq '220062')	{return 44;}	#大分
	if($ken eq '221077')	{return 45;}	#宮崎
	if($ken eq '220063')	{return 46;}	#鹿児島
	if($ken eq '221065')	{return 46;}	#鹿児島
	if($ken eq '221074')	{return 46;}	#鹿児島
	if($ken eq '221082')	{return 46;}	#鹿児島
	if($ken eq '221087')	{return 46;}	#鹿児島
	if($ken eq '221091')	{return 46;}	#鹿児島
	if($ken eq '219031')	{return 47;}	#沖縄
	if($ken eq '220057')	{return 47;}	#沖縄
	if($ken eq '220049')	{return 42;}	#中国四国(高知)

#&DispError2($GB,"ＥＲＲＯＲ！","「不明なsoftbank」はかけないのだ!!<br><a href=\"http://qb5.2ch.net/test/read.cgi/operate/1173710224/\">ここで</a>fusianasanして県名報告してネ");

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


	if($remo =~ /oyma(\d+|\d+n\d+)\.catv.ppp.infoweb.ne.jp$/)	{return 9;}	#栃木県(09)
	if($remo =~ /fnbs(\d+|\d+n\d+)\.catv.ppp.infoweb.ne.jp$/)	{return 12;}	#千葉県(12)
	if($remo =~ /nkno(\d+|\d+n\d+)\.catv.ppp.infoweb.ne.jp$/)	{return 13;}	#東京都(13)
	if($remo =~ /ohta(\d+|\d+n\d+)\.catv.ppp.infoweb.ne.jp$/)	{return 13;}	#
	if($remo =~ /ktsk(\d+|\d+n\d+)\.catv.ppp.infoweb.ne.jp$/)	{return 13;}	#
	if($remo =~ /hcou(\d+|\d+n\d+)\.catv.ppp.infoweb.ne.jp$/)	{return 13;}	#
	if($remo =~ /tkbn(\d+|\d+n\d+)\.catv.ppp.infoweb.ne.jp$/)	{return 13;}	#
	if($remo =~ /odwr(\d+|\d+n\d+)\.catv.ppp.infoweb.ne.jp$/)	{return 14;}	#神奈川県(14)
	if($remo =~ /youx(\d+|\d+n\d+)\.catv.ppp.infoweb.ne.jp$/)	{return 21;}	#岐阜県(21)
	if($remo =~ /ymgt(\d+|\d+n\d+)\.catv.ppp.infoweb.ne.jp$/)	{return 21;}	#岐阜県(21)
	if($remo =~ /hmmt(\d+|\d+n\d+)\.catv.ppp.infoweb.ne.jp$/)	{return 22;}	#静岡県(22)
	if($remo =~ /aksi(\d+|\d+n\d+)\.catv.ppp.infoweb.ne.jp$/)	{return 28;}	#兵庫県(28)
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

	#京都府
	if($remo =~ /zaq3d2e6[89a-f]..\.zaq.ne.jp/)	{return 26;}
	if($remo =~ /zaq3dc06[c-f]..\.zaq.ne.jp/)	{return 26;}
	if($remo =~ /zaqd37c8[0-5]..\.zaq.ne.jp/)	{return 26;}
	if($remo =~ /zaqd37c8[67]..\.zaq.ne.jp/)	{return 26;}
	if($remo =~ /zaqd37cc[0-9a-c]..\.zaq.ne.jp/)	{return 26;}
	if($remo =~ /zaqd37cc[d-f]..\.zaq.ne.jp/)	{return 26;}
	if($remo =~ /zaqd38730..\.zaq.ne.jp/)		{return 26;}
	if($remo =~ /zaqd3873[1-7]..\.zaq.ne.jp/)	{return 26;}

	#兵庫県
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

	#滋賀県
	if($remo =~ /zaqd378b[4-7]..\.zaq.ne.jp/)	{return 25;}	#残りはすべて大阪府
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

	if($ken eq 'AH1')	{return 60;}	# 空
	if($ken eq 'TEP')	{return 51;}	# 関東地方
	if($ken eq 'CEP')	{return 52;}	# 中部地方
	if($ken eq 'EAO')	{return 57;}	# 西日本
	if($ken eq 'EAT')	{return 58;}	# 東日本
	if($ken eq 'SAP')	{return 1;}	# 北海道
	if($ken eq 'SOD')	{return 1;}	# 北海道
	if($ken eq 'OKI')	{return 2;}	# 青森
	if($ken eq 'MRN')	{return 3;}	# 岩手
	if($ken eq 'AOB')	{return 4;}	# 宮城
	if($ken eq 'NKD')	{return 5;}	# 秋田
	if($ken eq 'IMZ')	{return 6;}	# 山形
	if($ken eq 'HNZ')	{return 7;}	# 福島
	if($ken eq 'FKH')	{return 7;}	# 福島
	if($ken eq 'AKA')	{return 8;}	# 茨城
	if($ken eq 'HRD')	{return 9;}	# 栃木
	if($ken eq 'KKR')	{return 10;}	# 群馬
	if($ken eq 'SKN')	{return 11;}	# 埼玉
	if($ken eq 'FNA')	{return 12;}	# 千葉
	if($ken eq 'OFS')	{return 13;}	# 東京
	if($ken eq 'HDO')	{return 14;}	# 神奈川
	if($ken eq 'NGN')	{return 15;}	# 新潟
	if($ken eq 'TYN')	{return 16;}	# 富山
	if($ken eq 'KNZ')	{return 17;}	# 石川
	if($ken eq 'KNN')	{return 17;}	# 石川
	if($ken eq 'FKN')	{return 18;}	# 福井
	if($ken eq 'KFN')	{return 19;}	# 山梨
	if($ken eq 'SYD')	{return 20;}	# 長野
	if($ken eq 'GFN')	{return 21;}	# 岐阜
	if($ken eq 'SDD')	{return 22;}	# 静岡
	if($ken eq 'SSJ')	{return 23;}	# 愛知
	if($ken eq 'YKM')	{return 24;}	# 三重
	if($ken eq 'OTU')	{return 25;}	# 滋賀
	if($ken eq 'KYN')	{return 26;}	# 京都
	if($ken eq 'KYO')	{return 26;}	# 京都
	if($ken eq 'NWT')	{return 27;}	# 大阪
	if($ken eq 'OSA')	{return 27;}	# 大阪
	if($ken eq 'KBM')	{return 28;}	# 兵庫
	if($ken eq 'DAJ')	{return 29;}	# 奈良
	if($ken eq 'WKN')	{return 30;}	# 和歌山
	if($ken eq 'TTN')	{return 31;}	# 鳥取
	if($ken eq 'SMN')	{return 32;}	# 島根
	if($ken eq 'IMM')	{return 33;}	# 岡山
	if($ken eq 'NIH')	{return 34;}	# 広島
	if($ken eq 'YGN')	{return 35;}	# 山口
	if($ken eq 'TKN')	{return 36;}	# 徳島
	if($ken eq 'TMN')	{return 37;}	# 香川
	if($ken eq 'TKH')	{return 37;}	# 香川
	if($ken eq 'MYN')	{return 38;}	# 愛媛
	if($ken eq 'KCN')	{return 39;}	# 高知
	if($ken eq 'FKC')	{return 40;}	# 福岡
	if($ken eq 'TGS')	{return 41;}	# 佐賀
	if($ken eq 'SCO')	{return 42;}	# 長崎
	if($ken eq 'OBY')	{return 43;}	# 熊本
	if($ken eq 'OMC')	{return 44;}	# 大分
	if($ken eq 'MZN')	{return 45;}	# 宮崎
	if($ken eq 'KMI')	{return 46;}	# 鹿児島
	if($ken eq 'YRM')	{return 47;}	# 沖縄
	if($ken eq 'ATU')	{return 61;}	# ダイアルアップ
	if($ken eq 'TYO')	{return 61;}	# ダイアルアップ
	if($ken eq 'CBC')	{return 61;}	# ダイアルアップ
	if($ken eq 'TBT')	{return 61;}	# ダイアルアップ
	if($ken eq 'KAJ')	{return 61;}	# ダイアルアップ
	if($ken eq 'PAX')	{return 61;}	# ダイアルアップ
	if($ken eq 'RIF')	{return 61;}	# ダイアルアップ
	if($ken eq 'NIG')	{return 61;}	# ダイアルアップ

#	if(open(LX,">> HOST29.000")){print LX "(odn)$remo($ken)\n";close(LX);}
&DispError2($GB,"ＥＲＲＯＲ！","「おでん」はかけないのだ!!<br><a href=\"http://qb5.2ch.net/test/read.cgi/operate/1173710224/\">ここで</a>fusianasanして県名報告してネ");

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
	if($remo =~ /\.bbiq\.jp$/)	#bbiq.jp 九州地方
	{
		if($remo =~ /hakata03/)	{return 41;}
		return 40;
	}

if($remo =~ /\.ccnw\.ne\.jp$/)		{return 23;}	#.*.ccnw.ne.jp$ 中部ケーブルネットワーク（愛知・岐阜）
if($remo =~ /\.katch\.ne\.jp$/)		{return 23;}	#.*.katch.ne.jp$ KATCH-NET（愛知）
if($remo =~ /\.enat\.org$/)		{return 21;}	#.*.enat.org$ City.Ena'T.Org（岐阜県恵那市）
if($remo =~ /\.thn\.ne\.jp$/)		{return 22;}	#.*.thn.ne.jp$ THN CATVインターネットサービス（静岡）
if($remo =~ /\.kitanet\.ne\.jp$/)	{return 13;}	#.*.kitanet.ne.jp$ 北ネットインターネットサービス（東京都北区）
if($remo =~ /\.hot-cha\.tv$/)		{return 35;}	#.*.hot-cha.tv$ ほっちゃテレビ（山口県長門市）
if($remo =~ /\.across\.or\.jp$/)	{return 22;}	#.*.across.or.jp$ ドリームウェーブ静岡（静岡）
if($remo =~ /\.cty-net\.ne\.jp$/)	{return 24;}	#.*.cty-net.ne.jp$ シー・ティー・ワイ インターネット接続サービス（三重）
if($remo =~ /\.miyazaki-catv\.ne\.jp$/)	{return 45;}	#.*.miyazaki-catv.ne.jp$ MCN 宮崎ケーブルテレビ（宮崎）
if($remo =~ /\.tac-net\.ne\.jp$/)	{return 23;}	#.*.tac-net.ne.jp$ 知多半島ケーブルネットワーク（愛知）
if($remo =~ /\.orihime\.ne\.jp$/)	{return 23;}	#.*.orihime.ne.jp$ おりひめねっと（愛知県一宮市）
if($remo =~ /\.starcat\.ne\.jp$/)	{return 23;}	#.*.starcat.ne.jp$ Starcatインターネット（愛知県名古屋市）
if($remo =~ /\.nmt\.ne\.jp$/)		{return 36;}	#.*.nmt.ne.jp$ NMTネット（徳島）
if($remo =~ /\.tcn-catv\.ne\.jp$/)	{return 13;}	#.*.tcn-catv.ne.jp$ 東京ケーブルネットワーク（東京）
if($remo =~ /\.kcv\.ne\.jp$/)		{return 33;}	#.*.kcv.ne.jp$ ゆめネットワーク（岡山）
if($remo =~ /\.csf\.ne\.jp$/)		{return 40;}	#.*.csf.ne.jp$ ケーブルステーション福岡（福岡）
if($remo =~ /\.cts-net\.ne\.jp$/)	{return 44;}	#.*.cts-net.ne.jp$ CTSインターネットサービス（大分）
if($remo =~ /\.scn-net\.ne\.jp$/)	{return 14;}	#.*.scn-net.ne.jp$ 湘南ケーブルネットワーク（神奈川）
if($remo =~ /\.amigo\d?\.ne\.jp$/)	{return 24;}	#.*.amigo2.ne.jp$ アミーゴインターネットサービス（三重）
if($remo =~ /\.catvy\.ne\.jp$/)		{return 6;}	#.*.catvy.ne.jp$ ケーブルテレビ山形（山形）
if($remo =~ /\.ztv\.ne\.jp$/)		{return 24;}	#.*.ztv.ne.jp$ Z-LAN（三重）
if($remo =~ /\.actv\.ne\.jp$/)		{return 2;}	#.*.actv.ne.jp$ 青森ケーブルテレビ（青森）
if($remo =~ /\.hicat\.ne\.jp$/)		{return 34;}	#.*.hicat.ne.jp$ 広島シティケーブルテレビ HICAT（広島）
if($remo =~ /\.kcn\.ne\.jp$/)		{return 53;}	#.*.kcn.ne.jp$ KCN-Net Service（近畿）
if($remo =~ /\.itscom\.jp$/)		{return 13;}	#.*.itscom.jp$ イッツ・コミュニケーションズ株式会社（東京・神奈川）
if($remo =~ /\.246\.ne\.jp$/)		{return 13;}	#.*.246.ne.jp$ イッツ・コミュニケーションズ株式会社（東京・神奈川）
if($remo =~ /\.aikis\.or\.jp$/)		{return 30;}	#.*.aikis.or.jp$ あいあい紀州ネット（和歌山）
if($remo =~ /\.coara\.or\.jp$/)		{return 40;}	#.*.coara.or.jp$ ニューCOARA（大分・福岡）
if($remo =~ /\.kumin\.ne\.jp$/)		{return 40;}	#.*.kumin.ne.jp$ くーみんブロードバンド（福岡）
if($remo =~ /\.gujo-tv\.ne\.jp$/)	{return 21;}	#.*.gujo-tv.ne.jp$ 郡上広域連合（岐阜）
if($remo =~ /\.hcvnet.jp$/)		{return 31;}	#.*.hcvnet.jp$ 株式会社　コンピュータ・サービス（鳥取）
if($remo =~ /\.spacelan\.ne\.jp$/)	{return 17;}	#.*.spacelan.ne.jp$ 金沢ケーブルテレビネット（石川）
if($remo =~ /\.ayu\.ne\.jp$/)		{return 14;}	#.*.ayu.ne.jp$ 厚木伊勢原ケーブルネットワーク（神奈川）
if($remo =~ /\.cna\.ne\.jp$/)		{return 5;}	#.*.cna.ne.jp$ 秋田ケーブルテレビ（秋田）
if($remo =~ /\.catvnet\.ne\.jp$/)	{return 54;}	#.*.catvnet.ne.jp$ CATVネットワークサービス（四国）
if($remo =~ /\.m-net\.ne\.jp$/)		{return 13;}	#.*.m-net.ne.jp$ My TV（東京）
if($remo =~ /\.ncv\.ne\.jp$/)		{return 1;}	#.*.ncv.ne.jp$ NCV（北海道函館市）
if($remo =~ /\.adachi\.ne\.jp$/)	{return 13;}	#.*.adachi.ne.jp$ ケーブルテレビ足立（東京）
if($remo =~ /\.wac2\.net$/)		{return 28;}	#.*.wac2.net$ わくわくネットワーク（兵庫）
if($remo =~ /\.net3-tv\.net$/)		{return 16;}	#.*.net3-tv.net$ Net3 Internet（富山）
if($remo =~ /\.lcv\.ne\.jp$/)		{return 20;}	#.*.lcv.ne.jp$ LCV-Net（長野）
if($remo =~ /\.tontonme\.ne\.jp$/)	{return 47;}	#.*.tontonme.ne.jp$ とんとんみ～（沖縄）
if($remo =~ /\.denkosekka\.ne\.jp$/)	{return 51;}	#.*.denkosekka.ne.jp$ 電光石火（平成電電）
if($remo =~ /\.mecha\.ne\.jp$/)		{return 24;}	#.*.mecha.ne.jp$ MeCha（ケーブルネット鈴鹿）
if($remo =~ /\.oninet\.ne\.jp$/)	{return 33;}	#.*.oninet.ne.jp$ oniネット（岡山）
if($remo =~ /\.rmc\.ne\.jp$/)		{return 25;}	#.*.rmc.ne.jp$ Rmcネットワーク（滋賀）
if($remo =~ /\.mco\.ne\.jp$/)		{return 47;}	#.*.mco.ne.jp$ ちゃんぷるネット（沖縄）
if($remo =~ /\.aitai\.ne\.jp$/)		{return 23;}	#.*.aitai.ne.jp$ Aitai net（愛知・岐阜）
if($remo =~ /\.ocv\.ne\.jp$/)		{return 51;}	#.*.ocv.ne.jp$ 小田急ケーブルテレビジョン

if($remo =~ /\.nns\.ne\.jp$/)		{return 19;}	#*.nns.ne.jp$ 日本ネットワークサービス（山梨）
if($remo =~ /\.cablenet\.ne\.jp$/)	{return 11;}	#.*.cablenet.ne.jp$ ケーブルネット埼玉
if($remo =~ /\.milare-tv\.ne\.jp$/)	{return 16;}	#.*.milare-tv.ne.jp$ みらーれTV（富山）
if($remo =~ /\.mni\.ne\.jp$/)		{return 4;}	#.*.mni.ne.jp$ ケーブルテレビ キャベツ(宮城)
if($remo =~ /\.gallery\.ne\.jp$/)	{return 39;}	#.*.gallery.ne.jp$ インターネットGallery（高知）
if($remo =~ /\.cans\.ne\.jp$/)		{return 26;}	#.*.cans.ne.jp$ ケーブルネットワークそのべ（京都）
if($remo =~ /\.ict\.ne\.jp$/)		{return 24;}	#.*.ict.ne.jp$ 伊賀上野ケーブルテレビ（三重）
if($remo =~ /\.ctk\.ne\.jp$/)		{return 21;}	#.*.ctk.ne.jp$ ケーブルテレビ可児（岐阜）
if($remo =~ /\.ucatv\.ne\.jp$/)		{return 9;}	#.*.ucatv.ne.jp$ 宇都宮ケーブルテレビ（栃木）
if($remo =~ /\.cncm\.ne\.jp$/)		{return 42;}	#.*.cncm.ne.jp$ 長崎ケーブルメディア（長崎）
if($remo =~ /\.itakita\.net$/)		{return 5;}	#.*.itakita.net$ 秋田県IT基盤協会
if($remo =~ /\.ogaki-tv\.ne\.jp$/)	{return 21;}	#.*.ogaki-tv.ne.jp$ 大垣ケーブルテレビ（岐阜）
if($remo =~ /\.t-net\.ne\.jp$/)		{return 13;}	#.*.t-net.ne.jp$ 多摩ケーブルネットワーク（東京）
if($remo =~ /\.fureai-ch\.ne\.jp$/)	{return 34;}	#.*.fureai-ch.ne.jp$ ふれあいチャンネル（広島）
if($remo =~ /\.synapse\.ne\.jp$/)	{return 46;}	#.*.synapse.ne.jp$ シナプス（鹿児島）
if($remo =~ /\.dokidoki\.ne\.jp$/)	{return 38;}	#.*.dokidoki.ne.jp$ マジカルサイト・インターネットサービス（愛媛）
if($remo =~ /\.shizuokanet\.ne\.jp$/)	{return 22;}	#.*.shizuokanet.ne.jp$ 静岡インターネット（静岡）
if($remo =~ /\.kyoto-inet\.or\.jp$/)	{return 26;}	#.*.kyoto-inet.or.jp$ 京都アイネットBB（京都）
if($remo =~ /\.wainet\.ne\.jp$/)	{return 45;}	#.*.wainet.ne.jp$ わいWaiネット（宮崎）
if($remo =~ /\.kcn-tv\.ne\.jp$/)	{return 43;}	#.*.kcn-tv.ne.jp$ 熊本ケーブルネットワーク（熊本）
if($remo =~ /\.d-b\.ne\.jp$/)		{return 44;}	#.*.d-b.ne.jp$ 大分合同新聞インターネット（大分）
if($remo =~ /\.parkcity\.ne\.jp$/)	{return 13;}	#.*.parkcity.ne.jp$ 武蔵野三鷹ケーブルテレビ（東京）
if($remo =~ /\.nirai\.ne\.jp$/)		{return 47;}	#.*.nirai.ne.jp$ 沖縄ケーブルネットワーク（沖縄）
if($remo =~ /\.cosmos\.ne\.jp$/)	{return 47;}	#.*.cosmos.ne.jp$ COSMOS NET COMMUNICATIONS（沖縄）
if($remo =~ /\.kct\.ne\.jp$/)		{return 33;}	#.*.kct.ne.jp$ 倉敷ケーブルテレビ（岡山）
if($remo =~ /\.me-h\.ne\.jp$/)		{return 1;}	#.*.me-h.ne.jp$ ME北海道ネットワークサービス（北海道）
if($remo =~ /\.asagaotv\.ne\.jp$/)	{return 17;}	#.*.asagaotv.ne.jp$ あさがおテレビ（石川）
if($remo =~ /\.medias\.ne\.jp$/)	{return 23;}	#.*.medias.ne.jp$ 知多メディアスネットワーク
if($remo =~ /\.octv\.ne\.jp$/)		{return 1;}	#.*.octv.ne.jp$ 帯広シティーケーブル（北海道）
if($remo =~ /\.wbs\.ne\.jp$/)		{return 22;}	#.*.wbs.ne.jp$ Web静岡
if($remo =~ /\.commufa\.jp$/)		{return 52;}	#.*.commufa.jp$ コミュファ（中部電力）
if($remo =~ /\.sni\.ne\.jp$/)		{return 41;}	#.*.sni.ne.jp$ 佐賀新聞・長崎新聞インターネット（佐賀・長崎）
if($remo =~ /\.netwave\.or\.jp$/)	{return 54;}	#.*.netwave.or.jp$ Netwaveインターネットサービス（四国）
if($remo =~ /\.mopera\.ne\.jp$/)	{return 60;}	#.*.mopera.ne.jp$ モペラ（FOMAの接続サービス？）
if($remo =~ /\.koalanet\.ne\.jp$/)	{return 12;}	#.*.koalanet.ne.jp$ コアラテレビ（千葉）
if($remo =~ /\.clovernet\.ne\.jp$/)	{return 23;}	#.*.clovernet.ne.jp$ クローバーネット（愛知）
if($remo =~ /\.hottv\.ne\.jp$/)		{return 25;}	#.*.hottv.ne.jp$ 近江八幡ケーブルネットワーク株式会社（滋賀県近江八幡市）
if($remo =~ /\.tvk\.ne\.jp$/)		{return 17;}	#.*.tvk.ne.jp$ テレビ小松（石川）
if($remo =~ /\.tcn\.ne\.jp$/)		{return 36;}	#.*.tcn.ne.jp$ 徳島ケーブルネットワーク（徳島）
if($remo =~ /\.ccv\.ne\.jp$/)		{return 34;}	#.*.ccv.ne.jp$ ふれあいチャンネル（広島）
if($remo =~ /\.cnc\.jp$/)		{return 12;}	#.*.cnc.jp$ 株式会社ケーブルネットワーク千葉
if($remo =~ /\.e-catv\.ne\.jp$/)	{return 38;}	#.*.e-catv.ne.jp$ 愛媛CATV（愛媛）
if($remo =~ /\.wind\.ne\.jp$/)		{return 10;}	#.*.wind.ne.jp$ 群馬インターネット（群馬）
if($remo =~ /\.hit-5\.net$/)		{return 32;}	#.*.hit-5.net$ 雲州わがとこテレビ（島根）
if($remo =~ /\.yukiguni\.net$/)		{return 15;}	#.*.yukiguni.net$ ゆきぐにネット（新潟）
if($remo =~ /\.kct\.ad\.jp$/)		{return 33;}	#.*.kct.ad.jp$ 株式会社倉敷ケーブルテレビ（岡山）
if($remo =~ /\.ictnet\.ne\.jp$/)	{return 3;}	#.*.ictnet.ne.jp$ 岩手ケーブルテレビジョン（岩手）
if($remo =~ /\.chikamatsu\.ne\.jp$/)	{return 13;}	#.*.chikamatsu.ne.jp$ PS/PLAZA 地下松（東京都千代田区）
if($remo =~ /\.miracle\.ne\.jp$/)	{return 55;}	#.*.miracle.ne.jp$ San-inNet（山陰地方）
if($remo =~ /\.avis\.ne\.jp$/)		{return 71;}	#.*.avis.ne.jp$ アヴィス（長野）
if($remo =~ /\.fcv\.ne\.jp$/)		{return 30;}	#.*.fcv.ne.jp$ 福岡ケーブルビジョン
if($remo =~ /\.inacatv\.ne\.jp$/)	{return 20;}	#.*.inacatv.ne.jp$ 伊那ケーブルテレビジョン
if($remo =~ /\.incl\.ne\.jp$/)		{return 70;}	#.*.incl.ne.jp$ インクル（北陸地方）
if($remo =~ /\.c-able\.ne\.jp$/)	{return 35;}	#.*.c-able.ne.jp$ 山口ケーブルビジョン（山口）
if($remo =~ /\.tees\.ne\.jp$/)		{return 23;}	#.*.tees.ne.jp$ 豊橋ケーブルネットワーク（愛知県豊橋市・田原市）

if($remo =~ /\.cty8\.com$/)		{return 16;}	#.*.cty8.com$ ケーブルテレビ八尾（富山）
if($remo =~ /\.bc9\.ne\.jp$/)		{return 9;}	#.*.bc9.ne.jp$ 鹿沼ケーブルテレビ（栃木鹿沼市）
if($remo =~ /\.cc9\.ne\.jp$/)		{return 9;}	#.*.cc9.ne.jp$ 栃木ケーブルテレビ（栃木・群馬）
if($remo =~ /\.cnh\.ne\.jp$/)		{return 16;}	#.*.cnh.ne.jp$ 氷見・羽咋ケーブルネット（富山県氷見市・羽咋市）
if($remo =~ /\.catvmics\.ne\.jp$/)	{return 23;}	#.*.catvmics.ne.jp$ ミクスネットワーク（愛知県岡崎市）
if($remo =~ /\.cts\.ne\.jp$/)		{return 13;}	#.*.cts.ne.jp$ ケーブルテレビ品川（東京都品川区）
if($remo =~ /\.tcat\.ne\.jp$/)		{return 11;}	#.*.tcat.ne.jp$ テプコケーブルテレビ（埼玉）
if($remo =~ /\.tcnet\.ne\.jp$/)		{return 16;}	#.*.tcnet.ne.jp$ 高岡ケーブルネットワーク（富山県高岡市・福岡町）
if($remo =~ /\.winknet\.ne\.jp$/)	{return 28;}	#.*.winknet.ne.jp$ 姫路ケーブルテレビ（兵庫県姫路市）
if($remo =~ /\.usennet\.ne\.jp$/)	{return 25;}	#.*.usennet.ne.jp$ 守山有線放送（滋賀県守山市）
if($remo =~ /\.ictv\.ne\.jp$/)		{return 11;}	#.*.ictv.ne.jp$ 入間ケーブルテレビ（埼玉県入間市）
if($remo =~ /\.otv\.ne\.jp$/)		{return 10;}	#.*.otv.ne.jp$ 群馬ケーブルメディア（群馬県太田市・桐生市）
if($remo =~ /\.sdx\.ne\.jp$/)		{return 11;}	#.*.sdx.ne.jp$ 埼玉データエクスチェンジサービス（埼玉）
if($remo =~ /\.tcv\.jp$/)		{return 13;}	#.*.tcv.jp$ 東京ケーブルビジョン
if($remo =~ /\.h555\.net$/)		{return 28;}	#.*.h555.net$ h555.net（兵庫県）
if($remo =~ /\.lan-do\.ne\.jp$/)	{return 1;}	#.*.lan-do.ne.jp$ 旭川ケーブルテレビ ポテト（北海道旭川市）
if($remo =~ /\.bbbn\.jp$/)		{return 34;}	#.*.bbbn.jp$ BBBN（広島県）
if($remo =~ /\.ctb\.ne\.jp$/)		{return 44;}	#.*.ctb.ne.jp$ CTBメディア（大分）
if($remo =~ /\.intsurf\.ne\.jp$/)	{return 24;}	#.*.intsurf.ne.jp$ イントサーフ（三重県桑名市・東員町）
if($remo =~ /\.cvk\.ne\.jp$/)		{return 19;}	#.*.cvk.ne.jp$ 峡西ＣＡＴＶ（山梨県南アルプス市）
if($remo =~ /\.omn\.ne\.jp$/)		{return 6;}	#.*.omn.ne.jp$ ニコニコケーブルテレビジョン（山形）
if($remo =~ /\.kcv-net\.ne\.jp$/)	{return 11;}	#.*.kcv-net.ne.jp$ 川越ケーブルテレビ（埼玉県川越市）
if($remo =~ /\.accsnet\.ne\.jp$/)	{return 8;}	#.*.accsnet.ne.jp$ ACCSnet（茨城県つくば市）
if($remo =~ /\.tst\.ne\.jp$/)		{return 16;}	#.*.tst.ne.jp$ となみ衛星通信テレビ（富山県小矢部市・南砺市・砺波市）
if($remo =~ /\.ctt\.ne\.jp$/)		{return 16;}	#.*.ctt.ne.jp$ ケーブルテレビ富山（富山県富山市・舟橋村）
if($remo =~ /\.fctv\.ne\.jp$/)		{return 18;}	#.*.fctv.ne.jp$ 福井ケーブルテレビ（福井）
if($remo =~ /\.izu\.co\.jp$/)		{return 22;}	#.*.izu.co.jp$ 伊豆急ケーブルネットワーク（静岡県東部）
if($remo =~ /\.icnet\.ne\.jp$/)		{return 12;}	#.*.icnet.ne.jp$ いちかわケーブルネットワーク（千葉県市川市）
if($remo =~ /\.kyoto-inetbb\.jp$/)	{return 26;}	#.*.kyoto-inetbb.jp$ 京都アイネットBB（京都）
if($remo =~ /\.cc22\.ne\.jp$/)		{return 34;}	#.*.cc22.ne.jp$ ふれあいチャンネル（広島市）
if($remo =~ /\.catv296\.ne\.jp$/)	{return 12;}	#.*.catv296.ne.jp$ ケーブルネット296（千葉）
if($remo =~ /\.ueda\.ne\.jp$/)		{return 20;}	#.*.ueda.ne.jp$ 上田ケーブルビジョン（長野）
if($remo =~ /\.toshima\.ne\.jp$/)	{return 13;}	#.*.toshima.ne.jp$ 豊島ケーブルネットワーク（東京都豊島区）
if($remo =~ /\.ii-okinawa\.ne\.jp$/)	{return 47;}	#.*.ii-okinawa.ne.jp$ ii-okinawa（沖縄）
if($remo =~ /\.biwa\.ne\.jp$/)		{return 25;}	#.*.biwa.ne.jp$ BIWALOBE（滋賀）
if($remo =~ /\.tvkumagaya\.ne\.jp$/)	{return 11;}	#.*.tvkumagaya.ne.jp$ 熊谷ケーブルテレビ（埼玉県熊谷市）
if($remo =~ /\.mable\.ne\.jp$/)		{return 32;}	#.*.mable.ne.jp$ 山陰ケーブルビジョン（島根県松江市）
if($remo =~ /\.tamatele\.ne\.jp$/)	{return 33;}	#.*.tamatele.ne.jp$ 玉島テレビ（岡山県倉敷市）
if($remo =~ /\.ccnet-ai\.ne\.jp$/)	{return 23;}	#.*.ccnet-ai.ne.jp$ CCNet豊川局（愛知県豊川市）
if($remo =~ /\.infoaomori\.ne\.jp$/)	{return 2;}	#.*.infoaomori.ne.jp$ 7-dj.com（青森）
if($remo =~ /\.7-dj\.ne\.jp$/)		{return 2;}	#.*.infoaomori.ne.jp$ 7-dj.com（青森）

if($remo =~ /\.btvm\.ne\.jp$/)		{return 46;}	#.*.btvm.ne.jp$ BTVケーブルテレビジョン（鹿児島）
if($remo =~ /\.kbn\.ne\.jp$/)		{return 37;}	#.*.kbn.ne.jp$ 香川テレビ放送網（香川）
if($remo =~ /\.rcn\.ne\.jp$/)		{return 18;}	#.*.rcn.ne.jp$ menet（福井）
if($remo =~ /\.hearts\.ne\.jp$/)	{return 38;}	#.*.hearts.ne.jp$ HEART NET（愛媛）
if($remo =~ /\.yct\.ne\.jp$/)		{return 33;}	#.*.yct.ne.jp$ 矢掛放送（岡山県小田郡矢掛町）
if($remo =~ /\.c3-net\.ne\.jp$/)	{return 14;}	#.*.c3-net.ne.jp$ JCN港南（神奈川県横浜市）
if($remo =~ /\.ginga-net\.ne\.jp$/)	{return 3;}	#.*.ginga-net.ne.jp$ 北上ケーブルテレビ（岩手県北上市）
if($remo =~ /\.icn-net\.ne\.jp$/)	{return 3;}	#.*.icn-net.ne.jp$ 一関ケーブルネットワーク（岩手県一関市）
if($remo =~ /\.canet\.ne\.jp$/)		{return 16;}	#.*.canet.ne.jp$ 射水ケーブルテレビ（富山県射水市・高岡市）
if($remo =~ /\.kamakuranet\.ne\.jp$/)	{return 14;}	#.*.kamakuranet.ne.jp$ 鎌倉ケーブルテレビ（神奈川県鎌倉市）
if($remo =~ /\.s-cnet\.ne\.jp$/)	{return 22;}	#.*.s-cnet.ne.jp$ ドリームウェーブ静岡（静岡県静岡市）
if($remo =~ /\.c-marinet\.ne\.jp$/)	{return 4;}	#.*.c-marinet.ne.jp$ 塩釜ケーブルテレビ（宮城県塩釜市・多賀城市・利府町・七ヶ浜町）
if($remo =~ /\.himawarinet\.ne\.jp$/)	{return 42;}	#.*.himawarinet.ne.jp$ ひまわりてれび（長崎）
if($remo =~ /\.ccsnet\.ne\.jp$/)	{return 35;}	#.*.ccsnet.ne.jp$ シティーケーブル周南（山口県周南市）
if($remo =~ /\.sakura-catv\.ne\.jp$/)	{return 13;}	#.*.sakura-catv.ne.jp$ さくらケーブルテレビ（東京都墨田区）
if($remo =~ /\.hinocatv\.ne\.jp$/)	{return 13;}	#.*.hinocatv.ne.jp$ 日野ケーブルテレビ（東京都）
if($remo =~ /\.watv\.ne\.jp$/)		{return 9;}	#.*.watv.ne.jp$ わたらせテレビ（栃木県足利市）
if($remo =~ /\.mctv\.ne\.jp$/)		{return 24;}	#.*.mctv.ne.jp$ MCTV松阪ケーブルテレビ（三重県松阪市）
if($remo =~ /\.tmtv\.ne\.jp$/)		{return 14;}	#.*.tmtv.ne.jp$ ケーブルネットつづきの森（横浜市都筑区）
if($remo =~ /\.ttv\.ne\.jp$/)		{return 13;}	#.*.ttv.ne.jp$ 多摩テレビ（東京都八王子市・町田市・多摩市・稲城市）
if($remo =~ /\.sopia\.or\.jp$/)		{return 8;}	#.*.sopia.or.jp$ ソピアフォンス株式会社（茨城県鹿嶋市）
if($remo =~ /\.nice-tv\.jp$/)		{return 16;}	#.*.nice-tv.jp$ NICE TV（富山県魚津市）
if($remo =~ /\.iwamicatv\.jp$/)		{return 32;}	#.*.iwamicatv.jp$ 石見ケーブルビジョン（島根県浜田市・江津市）
if($remo =~ /\.cac-net\.ne\.jp$/)	{return 23;}	#.*.cac-net.ne.jp$ CATV愛知（愛知県半田市）

if($remo =~ /\.inforyoma\.or\.jp$/)	{return 39;}	#inforyoma.or.jp 高知
if($remo =~ /\.joetsu\.ne\.jp$/)	{return 15;}	#joetsu.ne.jp 新潟
if($remo =~ /\.cable-net\.ne\.jp$/)	{return 25;}	#cable-net.ne.jp 滋賀
if($remo =~ /\.icc\.ne\.jp$/)		{return 14;}	#icc.ne.jp 神奈川
if($remo =~ /\.bai\.ne\.jp$/)		{return 28;}	#bai.ne.jp 兵庫
if($remo =~ /\.people-i\.ne\.jp$/)	{return 41;}	#people-i.ne.jp 佐賀
if($remo =~ /\.fruits\.ne\.jp$/)	{return 19;}	#fruits.ne.jp 山梨
if($remo =~ /\.viplt\.ne\.jp$/)		{return 70;}	#viplt.ne.jp 北陸
if($remo =~ /\.taku\.ne\.jp$/)		{return 41;}	#taku.ne.jp 佐賀
if($remo =~ /\.htv-net\.ne\.jp$/)	{return 2;}	#htv-netne.jp 青森
if($remo =~ /\.gol\.ne\.jp$/)		{return 68;}	#'gol.ne.jp'
if($remo =~ /\.kinet-tv\.ne\.jp$/)	{return 26;}	#'kinet-tv.ne.jp'京都
if($remo =~ /\.cyberbb\.ne\.jp$/)	{return 68;}	#'cyberbb.ne.jp'
if($remo =~ /\.tribe\.ne\.jp$/)		{return 68;}	#'tribe.ne.jp'
if($remo =~ /\.janis\.or\.jp$/)		{return 20;}	#janis.or.jp（長野）
if($remo =~ /\.valley\.ne\.jp$/)	{return 20;}	#valley.ne.jp（長野）
if($remo =~ /\.tnc\.ne\.jp$/)		{return 22;}	#tnc.ne.jp　静岡
if($remo =~ /\.tokai\.or\.jp$/)		{return 22;}	#tokai.or.jp　静岡
if($remo =~ /\.chukai\.ne\.jp$/)	{return 31;}	#chukai.ne.jp　鳥取
if($remo =~ /\.nasicnet\.ne\.jp$/)	{return 27;}	#nasicnet.ne.jp　大阪
if($remo =~ /\.namikata\.ne\.jp$/)	{return 38;}	#namikata.ne.jp　愛媛
if($remo =~ /\.bunbun\.ne\.jp$/)	{return 41;}	#bunbun.ne.jp 佐賀
if($remo =~ /\.harenet\.ne\.jp$/)	{return 33;}	#harenet.ne.jp 岡山
if($remo =~ /\.yomogi\.or\.jp$/)	{return 9;}	#yomogi.or.jp 栃木
if($remo =~ /\.ttn\.ne\.jp$/)		{return 18;}	#ttn.ne.jp 福井
if($remo =~ /\.rosenet\.ne\.jp$/)	{return 13;}	#rosenet.ne.jp 東京
if($remo =~ /\.ctktv\.ne\.jp$/)		{return 14;}	#ctktv.ne.jp 神奈川
if($remo =~ /\.gctv\.ne\.jp$/)		{return 23;}	#gctv.ne.jp 名古屋
if($remo =~ /\.kamon\.ne\.jp$/)		{return 34;}	#kamon.ne.jp 広島
if($remo =~ /\.canvas\.ne\.jp$/)	{return 68;}	#canvas.ne.jp 長屋
if($remo =~ /\.i-chubu\.ne\.jp$/)	{return 52;}	#i-chubu.ne.jp 中部
if($remo =~ /\.oct-net\.ne\.jp$/)	{return 44;}	#oct-net.ne.jp 大分
if($remo =~ /\.megax\.ne\.jp$/)		{return 56;}	#megax.ne.jp 九州
if($remo =~ /\.icntv\.ne\.jp$/)		{return 12;}	#icntv.ne.jp 千葉
if($remo =~ /\.cyberhome\.ne\.jp$/)	{return 68;}	#cyberhome.ne.jp 長屋
if($remo =~ /\.pcsitebrowser\.ne\.jp$/)	{return 60;}	#pcsitebrowser.ne.jp 空
if($remo =~ /\.nava21\.ne\.jp$/)	{return 24;}	#nava21.ne.jp 三重
if($remo =~ /\.catv-mic\.ne\.jp$/)	{return 3;}	#catv-mic.ne.jp 岩手
if($remo =~ /\.edit\.ne\.jp$/)		{return 13;}	#edit.ne.jp 東京
if($remo =~ /\.mto\.ne\.jp$/)		{return 33;}	#mto.ne.jp 岡山
if($remo =~ /\.seaple\.ne\.jp$/)	{return 12;}	#seaple.ne.jp 千葉
if($remo =~ /\.firstserver\.ne\.jp$/)	{return 27;}	#firstserver.ne.jp 大阪

if($remo =~ /\.anc-tv\.ne\.jp$/)	{return 20;}	#.anc-tv.ne.jp 長野県　20
if($remo =~ /\.attmil\.ne\.jp$/)	{return 68;}	#.attmil.ne.jp 
if($remo =~ /\.attnet\.ne\.jp$/)	{return 68;}	#.attnet.ne.jp 
if($remo =~ /\.bias\.ne\.jp$/)		{return 68;}	#.bias.ne.jp ホスティングサービス？
if($remo =~ /\.bb-west\.ne\.jp$/)	{return 57;}	#.bb-west.ne.jp 関西 中部 九州
if($remo =~ /\.cableone\.ne\.jp$/)	{return 68;}	#.cableone.ne.jp 佐賀県 41
if($remo =~ /\.dsnw\.ne\.jp$/)		{return 41;}	#.dsnw.ne.jp 全国区　都道府県別可能か？
if($remo =~ /\.eagle-net\.ne\.jp$/)	{return 17;}	#.eagle-net.ne.jp 石川県　17
if($remo =~ /\.eastcom\.ne\.jp$/)	{return 12;}	#.eastcom.ne.jp 千葉県　12
if($remo =~ /\.icn-tv\.ne\.jp$/)	{return 35;}	#.icn-tv.ne.jp 山口県 35
if($remo =~ /\.em-net\.ne\.jp$/)	{return 68;}	#.em-net.ne.jp 全国区
if($remo =~ /\.hachigamenet\.ne\.jp$/)	{return 41;}	#.hachigamenet.ne.jp 佐賀県
if($remo =~ /\.hagakure\.ne\.jp$/)	{return 41;}	#.hagakure.ne.jp 佐賀県
if($remo =~ /\.hal\.ne\.jp$/)		{return 68;}	#.hal.ne.jp 全国区
if($remo =~ /\.i-younet\.ne\.jp$/)	{return 22;}	#.i-younet.ne.jp 静岡県
if($remo =~ /\.ip-link\.ne\.jp$/)	{return 51;}	#.ip-link.ne.jp 関東地方
if($remo =~ /\.iprevolution\.ne\.jp$/)	{return 68;}	#.iprevolution.ne.jp 全国区
if($remo =~ /\.ium\.ne\.jp$/)		{return 13;}	#.ium.ne.jp 串っぽい(東京)
if($remo =~ /\.ktv\.ne\.jp$/)		{return 10;}	#.ktv.ne.jp 群馬県
if($remo =~ /\.matsumoto\.ne\.jp$/)	{return 20;}	#.matsumoto.ne.jp 長野県
if($remo =~ /\.nsk\.ne\.jp$/)		{return 71;}	#.nsk.ne.jp 富山、福井、石川
if($remo =~ /\.pikara\.ne\.jp$/)	{return 14;}	#.pikara.ne.jp 四国
if($remo =~ /\.raidway\.ne\.jp$/)	{return 68;}	#.raidway.ne.jp 神奈川
if($remo =~ /\.rnac\.ne\.jp$/)		{return 5;}	#.rnac.ne.jp 秋田・岩手
if($remo =~ /\.rurbannet\.ne\.jp$/)	{return 12;}	#.rurbannet.ne.jp 千葉
if($remo =~ /\.sensyu\.ne\.jp$/)	{return 27;}	#.sensyu.ne.jp 大阪
if($remo =~ /\.speednet\.ne\.jp$/)	{return 68;}	#.speednet.ne.jp 東京
if($remo =~ /\.tctv\.ne\.jp$/)		{return 13;}	#.tctv.ne.jp 東京
if($remo =~ /\.ttmy\.ne\.jp$/)		{return 14;}	#.ttmy.ne.jp 神奈川
if($remo =~ /\.tvm\.ne\.jp$/)		{return 20;}	#.tvm.ne.jp 長野
if($remo =~ /\.urban\.ne\.jp$/)		{return 68;}	#.urban.ne.jp 
if($remo =~ /\.goennet\.ne\.jp$/)	{return 32;}	#.goennet.ne.jp 島根
if($remo =~ /\.ictweb\.ne\.jp$/)	{return 47;}	#.ictweb.ne.jp 沖縄

if($remo =~ /\.tns\.ne\.jp$/)		{return 68;}	#.tns.ne.jp トヨタ自動車関連　全国区
if($remo =~ /\.warabi\.ne\.jp$/)	{return 11;}	#.warabi.ne.jp 埼玉
if($remo =~ /\.stnet\.ne\.jp$/)		{return 68;}	#.stnet.ne.jp 全国　(フレッツ)
if($remo =~ /\.bmobile\.ne\.jp$/)	{return 60;}	#.bmobile.ne.jp 全国　(PHS)
if($remo =~ /\.meon\.ne\.jp$/)		{return 55;}	#.meon.ne.jp 山口 岡山県・鳥取県
if($remo =~ /\.hinanet\.ne\.jp$/)	{return 6;}	#.hinanet.ne.jp 山形
if($remo =~ /\.nima-cho\.ne\.jp$/)	{return 32;}	#.nima-cho.ne.jp 島根
if($remo =~ /\.nus\.ne\.jp$/)		{return 19;}	#.nus.ne.jp 山梨
if($remo =~ /\.tv-naruto\.ne\.jp$/)	{return 36;}	#.tv-naruto.ne.jp 徳島
if($remo =~ /\.access-internet\.ne\.jp$/)	{return 60;}	#.access-internet.ne.jp ソフトバンクモバイルのサービス
if($remo =~ /\.cat-v\.ne\.jp$/)		{return 4;}	#.cat-v.ne.jp 宮城
if($remo =~ /\.mct\.ne\.jp$/)		{return 46;}	#.mct.ne.jp 鹿児島
if($remo =~ /\.iam\.ne\.jp$/)		{return 68;}	#.iam.ne.jp 
if($remo =~ /\.arena\.ne\.jp$/)		{return 68;}	#.arena.ne.jp 

if($remo =~ /\.comcast\.net$/)		{return 80;}	#.comcast.net 米国
if($remo =~ /\.cilas\.net$/)		{return 68;}	#.cilas.net 全国マンション
if($remo =~ /\.fiberbit\.net$/)		{return 68;}	#.fiberbit.net 全国
if($remo =~ /\.hawaiiantel\.net$/)	{return 80;}	#.hawaiiantel.net アメリカ ハワイ
if($remo =~ /\.hinet\.net$/)		{return 68;}	#.hinet.net 台湾
if($remo =~ /\.imouto\.net$/)		{return 48;}	#.imouto.net 全国
if($remo =~ /\.isao\.net$/)		{return 68;}	#.isao.net 地域別可能？
if($remo =~ /\.mediatti\.net$/)		{return 68;}	#.mediatti.net catv　全国
if($remo =~ /\.solteria\.net$/)		{return 68;}	#.solteria.net IP-VPNサービス　ソフトバンクテレコム系
if($remo =~ /\.zero-isp\.net$/i)	{return 68;}	#.zero-isp.net 全国・地域特定不能

if($remo =~ /\.ibara\.ne\.jp$/)		{return 33;}	#.ibara.ne.jp 岡山
if($remo =~ /\.rak-rak\.ne\.jp$/)	{return 52;}	#.rak-rak.ne.jp 中部地方
if($remo =~ /\.cypress\.ne\.jp$/)	{return 30;}	#.cypress.ne.jp 和歌山
if($remo =~ /\.seiryu\.ne\.jp$/)	{return 21;}	#.seiryu.ne.jp 岐阜県
if($remo =~ /\.wings\.ne\.jp$/)		{return 68;}	#.wings.ne.jp 全国
if($remo =~ /\.jyaken\.ne\.jp$/)	{return 34;}	#.jyaken.ne.jp 広島
if($remo =~ /\.bb4u\.ne\.jp$/)		{return 68;}	#.bb4u.ne.jp 全国　マンション
if($remo =~ /\.n-cube\.ne\.jp$/)	{return 68;}	#.n-cube.ne.jp 全国
if($remo =~ /\.ont\.ne\.jp$/)		{return 5;}	#.ont.ne.jp 秋田県
if($remo =~ /\.awaikeda\.ne\.jp$/)	{return 36;}	#.awaikeda.net 徳島
if($remo =~ /\.ccjnet\.ne\.jp$/)	{return 34;}	#.ccjnet.ne.jp 広島
if($remo =~ /\.hotspot\.ne\.jp$/)	{return 60;}	#.hotspot.ne.jp ホットスポット
if($remo =~ /\.brew\.ne\.jp$/)		{return 60;}	#.brew.ne.jp ezwebのフルブラウザ

if($remo =~ /\.openmobile\.ne\.jp$/)	{return 68;}	#.openmobile.ne.jp(全国)ソフトバンクモバイル？
if($remo =~ /\.jet\.ne\.jp$/)		{return 58;}	#.jet.ne.jp(東日本)
if($remo =~ /\.icv\.ne\.jp$/)		{return 32;}	#.icv.ne.jp(島根)
if($remo =~ /\.kagacable\.ne\.jp$/)	{return 17;}	#.kagacable.ne.jp(石川)
if($remo =~ /\.icv-net\.ne\.jp$/)	{return 42;}	#.icv-net.ne.jp(長崎)
if($remo =~ /\.izumo\.ne\.jp$/)		{return 32;}	#.izumo.ne.jp(島根)
if($remo =~ /\.ch-you\.ne\.jp$/)	{return 20;}	#.ch-you.ne.jp(長野)
if($remo =~ /\.hotcn\.ne\.jp$/)		{return 1;}	#.hotcn.ne.jp(北海道)
if($remo =~ /\.nct\.ne\.jp$/)		{return 7;}	#.nct.ne.jp(福島)
if($remo =~ /\.otc\.ne\.jp$/)		{return 47;}	#.otc.ne.jp(沖縄)

if($remo =~ /\.shawcable\.net$/)	{return 81;}	#.shawcable.net(カナダ)
if($remo =~ /\.verizon\.net$/)		{return 80;}	#.verizon.net(アメリカ)
if($remo =~ /\.i-products\.net$/)	{return 68;}	#.i-products.net(全国)ibisBrowser?
if($remo =~ /\.awaikeda\.net$/)		{return 36;}	#.awaikeda.net(徳島)
if($remo =~ /\.bitcat\.net$/)		{return 51;}	#.bitcat.net(bitcatは三井不動産マンション向けサービス→ライブドアに吸収合併で東京・神奈川・埼玉かなと思います)
if($remo =~ /\.Level3\.net$/)		{return 80;}	#.Level3.net(アメリカ)
if($remo =~ /\.edu$/)			{return 80;}	#.edu(アメリカ)

if($remo =~ /\.awacco\.ne\.jp$/)	{return 36;}	#.awacco.ne.jp(徳島)
if($remo =~ /\.ccnetmie\.ne\.jp$/)	{return 24;}	#.ccnetmie.ne.jp(三重)
if($remo =~ /\.ciaotv\.ne\.jp$/)	{return 24;}	#.ciaotv.ne.jp(三重)
if($remo =~ /\.firnet\.ne\.jp$/)	{return 43;}	#.firnet.ne.jp(熊本)
if($remo =~ /\.fnj\.ne\.jp$/)		{return 68;}	#.fnj.ne.jp(全国)
if($remo =~ /\.haginet\.ne\.jp$/)	{return 35;}	#.haginet.ne.jp(山口)
if($remo =~ /\.i-berry\.ne\.jp$/)	{return 9;}	#.i-berry.ne.jp(栃木)
if($remo =~ /\.i-yume\.ne\.jp$/)	{return 32;}	#.i-yume.ne.jp(島根)
if($remo =~ /\.icknet\.ne\.jp$/)	{return 38;}	#.icknet.ne.jp(愛媛)
if($remo =~ /\.infoeddy\.ne\.jp$/)	{return 57;}	#.infoeddy.ne.jp(西日本)

if($remo =~ /\.jctv\.ne\.jp$/)		{return 36;}	#.jctv.ne.jp　徳島
if($remo =~ /\.jway\.ne\.jp$/)		{return 8;}	#.jway.ne.jp　茨城
if($remo =~ /\.kcb-net\.ne\.jp$/)	{return 39;}	#.kcb-net.ne.jp　高知
if($remo =~ /\.kctvnet\.ne\.jp$/)	{return 1;}	#.kctvnet.ne.jp　北海道
if($remo =~ /\.kkm\.ne\.jp$/)		{return 32;}	#.kkm.ne.jp　島根
if($remo =~ /\.nkoutokuji\.ne\.jp$/)	{return 46;}	#.koutokuji.ne.jp　鹿児島
if($remo =~ /\.kyt-net\.ne\.jp$/)	{return 26;}	#.kyt-net.ne.jp　京都
if($remo =~ /\.kvision\.ne\.jp$/)	{return 35;}	#.kvision.ne.jp　山口
if($remo =~ /\.maotv\.ne\.jp$/)		{return 22;}	#.maotv.ne.jp　静岡
if($remo =~ /\.mcbnet\.ne\.jp$/)	{return 37;}	#.mcbnet.ne.jp　香川

if($remo =~ /\.nanmoku\.ne\.jp$/)	{return 10;} #.nanmoku.ne.jp(群馬)
if($remo =~ /\.nct9\.ne\.jp$/)		{return 15;} #.nct9.ne.jp(新潟)
if($remo =~ /\.netfour\.ne\.jp$/)	{return 41;} #.netfour.ne.jp(佐賀)
if($remo =~ /\.nkansai\.ne\.jp$/)	{return 57;} #.nkansai.ne.jp(西日本)
if($remo =~ /\.octp-net\.ne\.jp$/)	{return 42;} #.octp-net.ne.jp(長崎)
if($remo =~ /\.okuizumo\.ne\.jp$/)	{return 32;} #.okuizumo.ne.jp(島根)
if($remo =~ /\.pcm\.ne\.jp$/)		{return 25;} #.pcm.ne.jp(滋賀)
if($remo =~ /\.qtnet\.ne\.jp$/)		{return 56;} #.qtnet.ne.jp(九州地方)
if($remo =~ /\.ryucom\.ne\.jp$/)	{return 47;} #.ryucom.ne.jp(沖縄)
if($remo =~ /\.sakura\.ne\.jp$/)	{return 68;} #.sakura.ne.jp(レンタルサーバ)

if($remo =~ /\.sanuki\.ne\.jp$/)	{return 37;}	#.sanuki.ne.jp(香川)
if($remo =~ /\.scatv\.ne\.jp$/)		{return 39;}	#.scatv.ne.jp(高知)
if($remo =~ /\.shiojiri\.ne\.jp$/)	{return 20;}	#.shiojiri.ne.jp(長野)
if($remo =~ /\.snowman\.ne\.jp$/)	{return 1;}	#.snowman.ne.jp(北海道)
if($remo =~ /\.sub\.ne\.jp$/)		{return 68;}	#.sub.ne.jp(全国)dti法人向け
if($remo =~ /\.tvt\.ne\.jp$/)		{return 33;}	#.tvt.ne.jp(岡山)
if($remo =~ /\.webone\.ne\.jp$/)	{return 1;}	#.webone.ne.jp(北海道)
if($remo =~ /\.yappo\.ne\.jp$/)		{return 68;}	#.yappo.ne.jp(全国)ケータイゲートウェイサービスbydocomo
if($remo =~ /\.leo-net\.jp$/)		{return 67;}	#.leo-net.jp
if($remo =~ /\.bb-niigata\.jp$/)	{return 15;}	#.bb-niigata.jp(新潟)

if($remo =~ /\.lbdsl\.net$/)		{return 80;} #.lbdsl.net　アメリカ
if($remo =~ /\.cox\.net$/)		{return 80;} #.cox.net　アメリカ
if($remo =~ /\.vrtc\.net$/)		{return 21;} #.vrtc.net　岐阜県恵那市岩村町
if($remo =~ /\.pacbell\.net$/)		{return 80;} #.pacbell.net　アメリカ
if($remo =~ /\.iowatelecom\.net$/)	{return 80;} #.iowatelecom.net　アメリカ
if($remo =~ /\.ms246\.net$/)		{return 13;} #.ms246.net　東京・神奈川
if($remo =~ /\.gujocity\.net$/)		{return 21;} #.gujocity.net　岐阜県郡上八幡
if($remo =~ /\.gru\.net$/)		{return 80;} #.gru.net　アメリカ
if($remo =~ /\.ovh\.net$/)		{return 80;} #.ovh.net　フランス
if($remo =~ /\.axelmark\.net$/)		{return 68;} #.axelmark.net　sv0134.dc01.axel

if($remo =~ /\.bitcat\.net$/)		{return 68;} #.bitcat.net(全国マンション？)
if($remo =~ /\.dsl\.net$/)		{return 80;} #.dsl.net(アメリカ)
if($remo =~ /\.e-awa\.net$/)		{return 36;} #.e-awa.net(徳島)
if($remo =~ /\.e-nt\.net$/)		{return 80;} #.e-nt.net(アメリカ)
if($remo =~ /\.proxad\.net$/)		{return 80;} #.proxad.net(フランス)
if($remo =~ /\.arcor-ip\.net$/)		{return 80;} #.arcor-ip.net(ドイツ)
if($remo =~ /\.fastres\.net$/)		{return 80;} #.fastres.net(イタリア)
if($remo =~ /\.t-dialin\.net$/)		{return 80;} #.t-dialin.net(ドイツ)
if($remo =~ /\.nameservices\.net$/)	{return 80;} #.nameservices.net(アメリカ)
if($remo =~ /\.sbcglobal\.net$/)	{return 80;} #.sbcglobal.net(アメリカ)
if($remo =~ /\.fctv-net\.net$/)		{return 42;} #.fctv-net.jp(長崎)
if($remo =~ /\.kwins\.net$/)		{return 60;} #.kwins.net(モバイル)
if($remo =~ /\.ycix\.net$/)		{return 19;} #.ycix.net(山梨)

if($remo =~ /\.nasicnet\.com$/)		{return 68;} #.nasicnet.com(全国マンション)
if($remo =~ /\.xiando\.com$/)		{return 68;} #.xiando.com(海外セイシェル)
if($remo =~ /\.george24\.com$/)		{return 68;} #.george24.com(全国マンション)
if($remo =~ /\.kaga-tv\.com$/)		{return 17;} #.kaga-tv.com(石川)

if($remo =~ /\.takamori\.ne\.jp$/)	{return 20;} #.takamori.ne.jp(長野)
if($remo =~ /\.hctv\.ne\.jp$/)		{return 11;} #.hctv.ne.jp(埼玉)
if($remo =~ /\.dcn\.ne\.jp$/)		{return 51;} #.dcn.ne.jp(関東地方)
if($remo =~ /\.icn\.ne\.jp$/)		{return 15;} #.icn.ne.jp(新潟)
if($remo =~ /\.au-net\.ne\.jp$/)	{return 68;} #.au-net.ne.jp(全国)
if($remo =~ /\.knc\.ne\.jp$/)		{return 1;}  #.knc.ne.jp(北海道)
if($remo =~ /\.coralnet\.or\.jp$/)	{return 70;} #.coralnet.or.jp(北陸)
if($remo =~ /\.mitene\.or\.jp$/)	{return 68;} #.mitene.or.jp(全国)
if($remo =~ /\.din\.or\.jp$/)		{return 68;} #.din.or.jp(全国)

if($remo =~ /\.zoot\.jp$/)		{return 68;} #.zoot.jp　全国
if($remo =~ /\.gmo-access\.jp$/)	{return 68;} #.gmo-access.jp　全国
if($remo =~ /\.dsn\.jp$/)		{return 68;} #.dsn.jp 全国
if($remo =~ /\.withe\.ne\.jp$/)		{return 68;} #.withe.ne.jp マンション
if($remo =~ /\.supercsi\.jp$/)		{return 72;} #.supercsi.jp　中国地方？(四国も)
if($remo =~ /\.banban\.jp$/)		{return 28;} #.banban.jp(兵庫)
if($remo =~ /\.viplt\.ne\.jp$/)		{return 71;} #.viplt.ne.jp 北陸中心だけどフレッツの範囲は西日本

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
#'50東北地方','51関東地方','52中部地方','53関西地方','54四国地方','55中国地方','56九州地方','57西日本','58東日本','',

	my $ken = ''; #←このブロックで定義されてない
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
#	スレつぶし撃退(バイバイさるさん)
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

	#★はスルー
	if($GB->{CAP})					{return 0;}
	#●はスルー
#	if($GB->{MARU})					{return 0;}
	#株主優待はスルー
	if($GB->{KABUU})				{return 0;}
	if($GB->{KABUUP})				{return 0;}

	my $kaimadeOK = 10	; #M回までok
	my $kaiChu = 18		; #N回中　ただし毎時クリアされます。

	my $host = $ENV{'REMOTE_ADDR'}			;	#IP
	if($GB->{P22CH})	{$host = $GB->{HOST2}	;}	#IP from p2
	$host =~ /(\d+)\.(\d+)\.(\d+)\.(\d+)/;
	$host = "$1.$2.$3"	;
	if($GB->{KEITAI})	{$host = $GB->{IDNOTANE};}	#携帯固有番号

	my $remo = $GB->{HOST29}; #いわゆるリモホ
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

	# 雪だるまはするー
	if($ENV{SERVER_NAME} =~ /^live2[34]\./)	{return 0;}

	# live系はするー
#	if($ENV{'SERVER_NAME'} !~ /live/)	{return 0;}
#	if($ENV{'SERVER_NAME'} !~ /ex15/)	{return 0;}
#	if($ENV{'SERVER_NAME'} !~ /ex16/)	{return 0;}

	my ($saruPath, @saruList, %kai);
	if(IsSnowmanServer)
	{
		# 引っかかった場合のみその回数 (それ以外 0) が返る
		# age は毎時一斉クリアの挙動にすべく調整
		$kai{$host} = bbsd($GB->{FORM}{bbs}, 'chkthrtimecount', $GB->{FORM}{key}, $GB->{NOWTIME} % 3600, $kaiChu, $kaimadeOK + 1, $host, 'nolog');
		# タイムアウト等エラーの場合はスキップ
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
		&DispError2($GB,"ＥＲＲＯＲ！","やはり貴方は投稿しすぎです。バイバイさるさん。<BR>合言葉=好きな車は？");
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
# 名無しの処理(地震関連板)
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
# 名無しの処理(vipランダム)
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
	#●はスルー
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

#	my $off = (($mon*31 + $mday)*24 + $hhh)	;	#　毎時変更
	my $off =  ($mon*31 + $mday)		;	#　毎日変更
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
#		$a47 = "$yy才";
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
		$omikuji3 =~ s/\(\S+\)/<\/b>\(チリ\)<b>/;
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
		$omikuji3 =~ s/\(\S+\)/\(チリ\)/;
	}
}	

	$GB->{FORM}->{'FROM'} = "$fusi$kab <\/b>$omikuji3<b>"	;

#	$GB->{FORM}->{'FROM'} = "$GB->{FORM}->{'FROM'}<\/b>$omikuji3<b>"	;
#	$GB->{FORM}->{'FROM'} = "<\/b>$FOX_774[$sss]<b>"	;
	undef $GB->{TRIPKEY};
	return 1;
}
#############################################################################
# vip臭い
#############################################################################
sub vip931
{
	my ($GB) = @_	;

#	return 0	;

	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_VIP931'} ne "checked")	{return 0;}

#my $eee = $GB->{FORM}->{bbs} . "+" . $FOX->{$GB->{FORM}->{bbs}}->{'BBS_VIP931'};
#&DispError2($GB,"ＥＲＲＯＲ！","checked $eee");

	#携帯はスルー
	if($GB->{KEITAI})			{return 0;}
	if($GB->{KEITAIBROWSER})		{return 0;}
	# 携帯・味ぽんはするー
	if(&IsIP4Mobile($ENV{REMOTE_ADDR}))	{return 0;}
	#★はスルー
	if($GB->{CAP})				{return 0;}
	#●はスルー
	if($GB->{MARU})				{return 0;}
	#公式p2はスルー
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

	# 情報取得エラーなら臭くないことにする
	if ($response->is_error)		{return 0;}

	$response_body =~ /VIP931\[([0-9]+)\]/;

#&DispError2($GB,"ＥＲＲＯＲ！","vip臭いです($1,$response_code)<br><br><a target=\"_blank\" href=\"http://cook81.2ch.net/\">詳しい解説</a>");

	$GB->{V931} = $1	;

	if($GB->{V931} ne "0")
	{
		# 特定の板ではvipperマークをつけて許可
		if($GB->{FORM}->{'bbs'} eq "operate2" ||
		   $GB->{FORM}->{'bbs'} eq "sec2chd")
		{
			$GB->{FORM}->{'FROM'} = ' </b>[　＾ω＾]<b> ' . $GB->{FORM}->{'FROM'};
			return 0;
		}
		# それ以外
		&DispError2($GB,"ＥＲＲＯＲ！","犬臭いです($1,$response_code)<br><br><a target=\"_blank\" href=\"http://cook81.2ch.net/\">詳しい解説</a>");
	}

	return 0	;
}
#############################################################################
# P2かどうか
#############################################################################
sub IsP2
{
	my ($GB) = @_	;

	#公式p2はスルー
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
# 佐賀ウィルス対策
#############################################################################
##### Mozilla/4.0 (compatible; ICS) 
sub Saga
{
	my ($GB) = @_			;

	if($ENV{'HTTP_USER_AGENT'} =~ /Mozilla\/4\.0 \(compatible; ICS\)/)
	{
		&DispError2($GB,"FOX ★","<font color=green>FOX ★　佐賀ウィルス</font><br><br>調整中。。。");
	}
	return 0;
}
#############################################################################
# 山田ウィルス対策
#############################################################################
##### Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)
sub Yamada
{
	my ($GB) = @_			;

	#if($ENV{'HTTP_USER_AGENT'} !~ /Mozilla\/4\.0/){return 0;}

	my $mss = substr($GB->{FORM}->{'MESSAGE'}, 0, 30);
	# $mss =~ s/</&lt;/g; $mss =~ s/>/&gt;/g;

	#if($ENV{'SERVER_NAME'} =~ /tmp4/ && $GB->{FORM}->{'MESSAGE'} =~ /しとるの/)
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
	#if($ENV{'SERVER_NAME'} =~ /tmp4/ && $GB->{FORM}->{'MESSAGE'} =~ /しとるの/)
	{#cookie
	#if(open(ABCD,">>./yamada.txt")){print ABCD "$ENV{'HTTP_COOKIE'}\n";close(ABCD);}
	#if(open(ABCD,">>./yamada.txt")){print ABCD "[$ENV{HTTP_ACCEPT_LANGUAGE}]\n";close(ABCD);}
	if(open(ABCD,">>./yamada.txt")){print ABCD "[$ENV{'HTTP_USER_AGENT'}]\n";close(ABCD);}
	}
	{
	my $mss = substr($GB->{FORM}->{'MESSAGE'}, 0, 30); $mss =~ s/</&lt;/g; $mss =~ s/>/&gt;/g;
	my $outdat = "$GB->{FORM}->{'FROM'}<>$GB->{FORM}->{'mail'}<>$GB->{DATE}<>$mss<>$GB->{FORM}->{'subject'}<>$GB->{HOST999}<>$ENV{'REMOTE_ADDR'}<><>$ENV{'HTTP_USER_AGENT'}";
	#日付と時間をげとする
	my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($GB->{NOWTIME});
	my $fff = sprintf("../_service/Yamada%04d%02d%02d.txt",$year+1900,$mon+1,$mday)	;
	open(OUT2, ">>$fff");
	print OUT2 "$outdat\n";
	close(OUT2);
	}
&DispError2($GB,"FOX ★","<font color=green>FOX ★　山田ウィルス</font><br><br>調整中。。。");
}
}
#############################################################################
# クッキー発行
#############################################################################
sub PutCookie
{
	my ($GB) = @_;

	#有効期限をつくる
	my $exp = 24 * 60 * 60;
	$exp *= 30;	#有効日数を乗じる
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
# 投稿確認画面
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

	#確認画面を出す
	print "Content-type: text/html; charset=shift_jis\n\n";
	print <<EOF;
<html lang="ja">
<head>
<title>投稿確認</title>
<meta http-equiv="Content-Type" content="text/html; charset=shift_jis">
<meta name="viewport" content="width=device-width,initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.6,user-scalable=yes" />
</head>
<body bgcolor="#FFFFFF">
<font size=+1 color=#FF0000><b>書きこみ確認</b></font><ul><br><br>
<b>$GB->{FORM}->{'subject'} </b><br>名前： $GB->{FORM}->{'FROM'}<br>E-mail： $GB->{FORM}->{'mail'}<br>内容：<br>
$GB->{FORM}->{'MESSAGE'}<br><br>$ENV{HTTP_USER_AGENT}<br><br></ul><b>
投稿確認(2)<br>
・投稿された内容はコピー、保存、引用、転載等される場合があります。<br>
・投稿に関して発生する責任は全て投稿者に帰します。<br></b>
<form method=POST action="../test/bbs.cgi?guid=ON"><input type=hidden name="subject" value="$sbj">
<input type=hidden name=FROM  value="$GB->{FORM}->{'FROM'}">
<input type=hidden name=mail  value="$GB->{FORM}->{'mail'}">
<input type=hidden name=get value="1$mdc">
<input type=hidden name=MESSAGE value="$msg">
<br><input type=hidden name=bbs value=$GB->{FORM}->{'bbs'}>
<input type=hidden name=time value=$GB->{NOWTIME}>
<input type=hidden name=key value=$GB->{FORM}->{'key'}>
<input type=submit value="全責任を負うことを承諾して書き込む" name="submit"><br></form>
変更する場合は戻るボタンで戻って書き直して下さい。<font size=-1>(cookieを設定するとこの画面はでなくなります。)</font><br></body></html>
EOF

	return 0;
}
#############################################################################
# ●の処理
# セッションIDを得てHOST999に保存し、●ログインフラグを立てる
# p2+●は「よっしゃこーい」にする
#############################################################################
sub ProcessMaru
{
	my ($GB) = @_;

	#●のセッションIDを得る
	$GB->{MARU} = &IsMonazilla($GB->{FORM}->{sid});

	#p2+●=p2
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


	#セッションIDが期限切れなら再ログインを促して終了
	if($GB->{MARU} eq "1")
	{
		&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：再度ログインしてね。。。");
	}

	#HOST999に●の情報を入れる
	if($GB->{MARU})	
	{
		$GB->{HOST999} .= "[$GB->{MARU}]";
		# 公式p2以外のp2+●は「よっしゃこーい」
		if(!$GB->{P22CH})
		{
			if($ENV{HTTP_USER_AGENT} =~ /p2\-client\-ip\:/)
			{
				&DispError2($GB,"ＥＲＲＯＲ！","よっしゃこーい");
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
# 文字列1から文字列2を取り払う
# 引数: 文字列1, 文字列2, フラグ
# 戻り値: 処理後の文字列
#
# usuusubonbon のような形も対応
# フラグが1の時にはあらかじめ文字列1の8ビット目をマスクしたうえで比較処理
#############################################################################
sub StripStr
{
	my ($str1, $str2, $flag) = @_;

	my $savestr = $str1;	# 8ビット目をカットする前の文字列を保存しておく

	# フラグが立ってたら、8ビット目をカット
	# 一時的にカットをオフ by む
	#if($flag)
	#{
	#	$str1 =~ tr/\x80-\xFF/\x00-\x7F/;
	#}

	# 文字列がなければばいばい
	if($str1 !~ $str2)	{ return $savestr; }

	# 文字列が存在しなくなるまで変換を繰り返して、、、
	while($str1 =~ $str2)
	{
		$str1 =~ s/$str2//g;
	}

	# 処理結果を返す
	return $str1;
}
########################################################################
# 名前欄とメール欄の禁止ワードの処理
########################################################################
sub NGNameReplace
{
	my ($GB) = @_;

	# NGワード
	$GB->{FORM}->{'FROM'} =~ s/mail/ /g;
	$GB->{FORM}->{'FROM'} =~ s/MAIL/ /g;
	$GB->{FORM}->{'FROM'} =~ s/管理/”管理”/g;
	$GB->{FORM}->{'FROM'} =~ s/管直/”管直”/g;
	$GB->{FORM}->{'FROM'} =~ s/菅直/”菅直”/g;
	$GB->{FORM}->{'FROM'} =~ s/削除/”削除”/g;
	$GB->{FORM}->{'FROM'} =~ s/復帰/”復帰”/g;
	$GB->{FORM}->{'FROM'} =~ s/sakujyo/”sakujyo”/g;
	$GB->{FORM}->{'FROM'} =~ s/★/☆/g;
	$GB->{FORM}->{'FROM'} =~ s/◆/◇/g;
	$GB->{FORM}->{'FROM'} =~ s/山崎渉/fusianasan/g;
	# BadTripCheck を新設したので不要 by む
	#$GB->{FORM}->{'FROM'} = &StripStr($GB->{FORM}->{'FROM'}, "usubon", 1);

	$GB->{FORM}->{'mail'} =~ s/削除/”削除”/g;
	$GB->{FORM}->{'mail'} =~ s/sakujyo/”sakujyo”/g;
	$GB->{FORM}->{'mail'} =~ s/★/☆/g;
	$GB->{FORM}->{'mail'} =~ s/◆/◇/g;

	$GB->{FORM}->{'MESSAGE'}=~ s/sssp:/http:/g;;

	if(!$GB->{MARU})
	{
		$GB->{FORM}->{'FROM'} =~ s/●/○/g;
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
# トリップの処理
# $GB->{TRIPSTRING} に処理結果が入る
########################################################################
sub ProcessTrip
{
	my ($GB, $main_message, $handle_pass) = @_;

	length $handle_pass > 1024
		and &DispError2($GB,'ＥＲＲＯＲ！','ＥＲＲＯＲ：トリップキー長杉！');

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
				# 将来の拡張用
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
	$GB->{FORM}->{'FROM'} = "$main_message </b>◆$GB->{TRIPSTRING} <b>";

	return 0;
}
########################################################################
# 呪われたトリップのチェック
# $GB->{TRIPSTRING} が呪われている場合、エラー
########################################################################
sub BadTripCheck
{
	my ($GB) = @_;
	our %BadTripList;
	BEGIN {
		# 呪われたトリップが増えたら、ここを編集する
		%BadTripList = map +($_ => 1), (
			"3SHRUNYAXA"
		);
	}

	if($BadTripList{$GB->{TRIPSTRING}})
	{
		&DispError2($GB, "ＥＲＲＯＲ！", "ＥＲＲＯＲ：トリップが呪われています。");
	}
	return 0;
}
########################################################################
# キャップの処理
########################################################################
sub ProcessCap
{
	my ($GB, $mail_message, $handle_pass) = @_;

	# 板ごとキャップフラグ
	my $bflag = 0;
	# キャップあぶり出しフラグ
	my $tflag = 0;
	# キャップハンドル名
	my $handle = "";

	# 板別キャップかな?
	if(&IsItabetsuCap($GB))
	{
		$bflag = 1;
	}
	# plus/newsの新スレはあぶり出し
	if($GB->{NEWTHREAD} ne 0 && ($GB->{FORM}->{'bbs'} =~ /plus$/ || $GB->{FORM}->{'bbs'} eq 'news'))
	{
		$tflag = 1;
	}
	# キャップあるかな?
	$handle = &FindCap($GB, $handle_pass, $bflag, $tflag);
	if($handle ne "")
	{
		# キャップがあったら、まずキャップフラグを立てる
		$GB->{CAP} = 1;

		# 次にキャップの種別をチェックする
		if($handle =~ /★$/)
		{
			# ★つきハンドル(強力キャップ)
			$GB->{STRONGCAP} = 1;
			$handle =~ s/★.*//;
		}
		elsif($handle =~ /☆$/)
		{
			# ☆つきハンドル(☆キャップ)
			# 現在では通常キャップと区別なし
			$GB->{WHITECAP} = 1;
			$handle =~ s/☆.*//;
		}

		# 名前入れていたら 名前＠ハンドル ★
		# 名前なしの時は ハンドル ★
		if($GB->{FORM}->{'FROM'})
		{
			$GB->{FORM}->{'FROM'} = "$GB->{FORM}->{'FROM'}＠$handle ★";
		}
		else
		{
			$GB->{FORM}->{'FROM'} = "$handle ★";
		}
	}
	# メール欄の補完 (#より前の文字列)
	$GB->{FORM}->{'mail'} = $mail_message;

	#&DispError2($GB,"root ★","キャップフラグ:$GB->{CAP} ☆フラグ:$GB->{WHITECAP} ★フラグ:$GB->{STRONGCAP}");

	return 0;
}
########################################################################
# キャップがあるかどうか調べ、あったらそのキャップ名を返す
# 引数: $GB, キャップパス, フラグ1, フラグ2
#       フラグ1が真の場合、板別キャップの処理を行う
#       フラグ2が真の場合、キャップあぶりだしの処理を行う
# 戻り値: キャップハンドル名 または ""(該当なしの場合)
########################################################################
sub FindCap
{
	my ($GB, $pass, $bflag, $tflag) = @_;
	my $board = $GB->{FORM}->{'bbs'};
	my $handle_file = "../handle/";
	my $handle_name = "";

	$pass =~ s/[\.\/]//gi;
	$pass .= ".cgi";

	#bflagが真の時は、板別キャップの処理
	if($bflag)
	{
		$handle_file .= $board . "/";
	}
	$handle_file .= $pass;

	# ファイルがあるか調べる
	if(-e $handle_file)
	{
		#tflagが真の時は、キャップのあぶりだし処理
		if($tflag)
		{
			# Perl 5.7.2 以降の utime は undef でおｋ
			my $now = $^V lt v5.7.2 ? time : undef;
			# なんだかうまく動かないのでとりあえず元に戻した by む
			# my $now = time;

			# 雪だるまでは、bbsdにあぶりだし処理を依頼
			if(IsSnowmanServer == BBSD->{REMOTE})
			{
				# bbsd の touch では undef の代わりに 0
				my $cmd = 'touch';
				my $errmsg = bbsd($handle_file, $cmd, $now || 0, 'dummy'); 
				# タイムアウトかどうかチェック
				if(&bbsd_TimeoutCheck($GB, $errmsg))
				{
					&bbsd_TimeoutError($GB, $cmd);
				}
			}
			else
			{
				# undef は変数でなく直接記述でないとダメ
				utime $now || undef, $now || undef, $handle_file;
			}
		}
		#ファイルを開いて中身(ハンドル名)を得る
		open(HANDLE, $handle_file);
		$handle_name = <HANDLE>;
		close(HANDLE);
		chomp($handle_name);
	}
	return $handle_name;
}

########################################################################
# 名無しの処理(heaven4vipでやっているBEポイントによる可変名無し処理)
########################################################################
sub NanashiReplace4Heaven
{
	my ($GB) = @_;

	if($GB->{BEpoints} > 999)	{$GB->{FORM}->{'FROM'} = "<font color=#9933CC>綾小路</font>"	;}
	elsif($GB->{BEpoints} > 499)	{$GB->{FORM}->{'FROM'} = "<font color=#9966CC>嵯峨</font>"	;}
	elsif($GB->{BEpoints} > 99)	{$GB->{FORM}->{'FROM'} = "<font color=#9999CC>小田</font>"	;}
	elsif($GB->{BEpoints} > 29)	{$GB->{FORM}->{'FROM'} = "<span style=\"background-color: #6600cc; color: #ffffff; padding-left: 4px; padding-right: 4px;\">記者</span>"	;}
	elsif($GB->{BEpoints} eq 20)	{$GB->{FORM}->{'FROM'} = "<font color=#99CCCC>お初</font>"	;}
	elsif($GB->{BEpoints} eq 10)	{$GB->{FORM}->{'FROM'} = "<font color=#99CCCC>与作</font>"	;}
	elsif($GB->{BEpoints} > 9)	{$GB->{FORM}->{'FROM'} = "<font color=#99CCCC>山田</font>"	;}
	elsif($GB->{BEpoints} > 1)	{$GB->{FORM}->{'FROM'} = "<font color=#99FFCC>佐藤</font>"	;}

	return 0;
}
#############################################################################
# 名前入力チェック、名無し補完と処理、heaven4vipの名無し置換処理
#############################################################################
sub ProcessNanashi
{
	my ($GB) = @_;

	# 名前入力チェック
	if($FOX->{$GB->{FORM}->{bbs}}->{'NANASHI_CHECK'})
	{
		unless($GB->{FORM}->{'FROM'})
		{
			&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：名前いれてちょ。。。");
		}
	}

	# 名無しの補完と処理
	unless($GB->{FORM}->{'FROM'})
	{
		if(!$GB->{KEITAI} && $FOX->{$GB->{FORM}->{bbs}}->{'BBS_RAWIP_CHECK'} eq "checked" && $GB->{COOKIES}{PREN} ne '')
		{	# 以前に書き込んだ板の名無しさん
#$GB->{FORM}->{'MESSAGE'} .= "<hr>PREN=$GB->{COOKIES}{PREN} // $FOX->{$GB->{FORM}->{bbs}}->{'BBS_NONAME_NAME'}";

			my $prep = $GB->{COOKIES}{PREN}	;

#use URI::Escape;
#$prep = uri_escape($prep);
			$prep =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;

			if($prep =~ /[<>\t\n\#\&]/)	{&endhtml($GB);}
			if(length($prep) > 48)	{&endhtml($GB);}


			# NGワード
			$prep =~ s/mail/ /g;
			$prep =~ s/MAIL/ /g;
			$prep =~ s/管理/”管理”/g;
			$prep =~ s/管直/”管直”/g;
			$prep =~ s/菅直/”菅直”/g;
			$prep =~ s/削除/”削除”/g;
			$prep =~ s/復帰/”復帰”/g;
			$prep =~ s/sakujyo/”sakujyo”/g;
			$prep =~ s/★/☆/g;
			$prep =~ s/◆/◇/g;
			$prep =~ s/山崎渉/fusianasan/g;

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
# tasukeruyoの処理
########################################################################
sub Tasukeruyo
{
	my ($GB) = @_;

	if(length($GB->{FORM}->{'MESSAGE'}) == 0){
		&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：本文がありません！");
	}

	my $user_agent = $ENV{'HTTP_USER_AGENT'};
	# $user_agent =~ s/"/&quot;/g;
	$user_agent =~ s/</&lt;/g;
	$user_agent =~ s/>/&gt;/g;
	$user_agent =~ tr/\t/ /;
	# [\x00\n\r] ⊂ [[:cntrl:]]
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
# fusianasanの処理
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
# フォーム情報のチェック(板名に変な文字、時間が読めない)
##############################################################################
sub FormInfoCheck
{
	my ($GB) = @_;

	#ＢＢＳ名に不正な文字があった場合もばいばい
	if($GB->{FORM}->{'bbs'} =~ /[^a-zA-Z0-9]/)
	{
		&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：ＢＢＳ名が不正です！");
	}
	#時間が読み込めなかったらばいばい
	unless($GB->{FORM}->{'time'})
	{
		&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：フォーム情報が不正です！");
	}

	return 0;
}
########################################################################
# リファラのチェック(ブラウザ変ですよん)
########################################################################
sub BraHen
{
	my ($GB) = @_;

	# 携帯・味ぽんはするー
	if(&IsIP4Mobile($ENV{REMOTE_ADDR}))	{return 0;}
	#★はスルー
	if($GB->{CAP})				{return 0;}
	#●はスルー
	if($GB->{MARU})				{return 0;}

	# UAがないのはブラ変
	#if(!$ENV{'HTTP_USER_AGENT'})
	#{
	#	&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：ブラウザ変ですよん。(ua)$ENV{'HTTP_REFERER'}");
	#}
#	if($ENV{'HTTP_USER_AGENT'} =~ /gikoNavi\/beta50/)
	if($ENV{'HTTP_USER_AGENT'} =~ /gikoNavi\/beta50\/1\.50\.2\.606/)
	{
		&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：ブラウザ変ですよん-2。(ua)$ENV{'HTTP_REFERER'}");
	}

	# *.ula.cc はスルー
	if($ENV{'HTTP_REFERER'} =~ /^http:\/\/\w+\.u\.la\//)	{return 0;}
	if($ENV{'HTTP_REFERER'} =~ /^http:\/\/\w+\.ula\.cc\//)	{return 0;}

	# orz.2ch.io はスルー
	if($ENV{'HTTP_REFERER'} =~ /^http:\/\/orz\.2ch\.io\//)	{return 0;}

	if($ENV{'HTTP_REFERER'} !~ /^http:\/\/$ENV{'HTTP_HOST'}\//)
	{
		#cをフルブラウザから使用した場合に対応
		if($ENV{'HTTP_REFERER'} !~ /^http:\/\/c\.2ch\.net\//)
		{
			&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：ブラウザ変ですよん。(referer1)$ENV{'HTTP_REFERER'}");
		}
	}
	if($ENV{'HTTP_HOST'} ne $ENV{'SERVER_NAME'})
	{
		&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：ブラウザ変ですよん(host)。$ENV{'HTTP_REFERER'}");
	}

	return 0;
}
########################################################################
# スレタイ、名前、メアド、本文の長さチェック
########################################################################
sub FieldSizeCheck
{
	my ($GB) = @_;

	#強い★はスルー
	if($GB->{STRONGCAP})			{return 0;}

	if(length($GB->{FORM}->{'subject'}) > $FOX->{$GB->{FORM}->{bbs}}->{"BBS_SUBJECT_COUNT"})
	{
		&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：サブジェクトが長すぎます！");
	}
	if(length($GB->{FORM}->{'FROM'}) > $FOX->{$GB->{FORM}->{bbs}}->{"BBS_NAME_COUNT"})
	{
		&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：名前が長すぎます！");
	}
	if(length($GB->{FORM}->{'mail'}) > $FOX->{$GB->{FORM}->{bbs}}->{"BBS_MAIL_COUNT"})
	{
		&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：メールアドレスが長すぎます！");
	}
	if(length($GB->{FORM}->{'MESSAGE'}) > $FOX->{$GB->{FORM}->{bbs}}->{"BBS_MESSAGE_COUNT"})
	{
		&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：本文が長すぎます！==$FOX->{$GB->{FORM}->{bbs}}->{BBS_MESSAGE_COUNT}==");
	}
	if(length($GB->{FORM}->{'MESSAGE'}) == 0)
	{
		&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：本文がありません！");
	}

	return 0;
}
########################################################################
# 本文の行数と長すぎる行のチェック
########################################################################
sub FieldLineCheck
{
	my ($GB) = @_;

	#強い★はスルー
	if($GB->{STRONGCAP})			{return 0;}

	#行数＆行長さ制限
	my @msg = split(/<br>/, $GB->{FORM}->{'MESSAGE'});
	my $cnt = @msg;
	if($cnt > ($FOX->{$GB->{FORM}->{bbs}}->{'BBS_LINE_NUMBER'} * 2))
	{
		&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：改行が多すぎます！");
	}
	foreach(@msg)
	{
		#$cnt = tr/[\041-\177]//;
		if(length > 256)
		{
			&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：長すぎる行があります！");
		}
	}

	return 0;
}
##############################################################################
# 板別の特殊処理(sec2chでは一般書き込み禁止とかplusでは★だけスレ立て可能とか)
##############################################################################
sub ItabetsuSpecial
{
	my ($GB) = @_;

	#規制情報板は一般書き込み禁止
	if($GB->{FORM}->{'bbs'} eq "sec2ch")
	{
		if(!$GB->{STRONGCAP})
		{
			&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：規制情報板は一般書き込み禁止です");
		}
	}

	#●板はログインのみ
	if($GB->{FORM}->{'bbs'} =~ /maru$/)
	{
		if(!$GB->{MARU})
		{
			&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：●板は●がないとかけないです。");
		}
	}

	#キャップ専用ニュース板ではキャップ持ちのみ書き込み可能
	if($GB->{FORM}->{'bbs'} =~ /plus$/ && $GB->{FORM}->{'subject'} ne "")
	{
		if($GB->{FORM}->{'bbs'} =~ /liveplus/)
		{
			;# 実験中。。。 plus でもちょっとだけ★無しでも、、、
		}
		elsif(!$GB->{CAP})
		{
			&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：この掲示板は★付きの記者さんのみスレッドが立てられます");
		}
	}

	# saku/saku2ch/sakudは通常のスレ立て禁止
	if($GB->{FORM}->{'bbs'} eq "saku" || $GB->{FORM}->{'bbs'} eq "saku2ch" || $GB->{FORM}->{'bbs'} eq "sakud")
	{
		if (!$GB->{CAP})
		{
			if($GB->{FORM}->{'subject'} ne "" && $GB->{FORM}->{'bbs'} ne "sakud")
			{
				&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：ここはスレッド立て禁止です！！");
			}
		}
	}

	#Be板はログインのみ
	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_BE_ID'})
	{ 
		if(!$GB->{CAP})
		{
			if($GB->{FORM}->{'DMDM'} eq '')
			{
				&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：<a href=\"http://be.2ch.net/\">be.2ch.net</a>でログインしてないと書けません。");
			}
		}
	}

	#IPv6板はIPv6接続だけ(将来はBeのようにSETTING.TXTがよさげ)
	if($GB->{FORM}->{'bbs'} eq "ipv6")
	{
		# キャップでは書ける
		if(!$GB->{CAP})
		{
			if(!$GB->{IPv6})
			{
				&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：IPv6で接続していないと書けません。");
			}
		}
	}

	return 0;
}
#############################################################################
# 各種スレ立てチェックをまとめて行う
#############################################################################
sub SuretateTotalCheck
{
	my ($GB) = @_;

	# のんびり規制
	my $violation = &Check_Speed($GB);
	if($violation)
	{
		&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：のんびり行きましょ。<br>この板スレッド立ち杉。");
	}
	# 新スレ立て規制
	my $tatetate = &Check_SURETATE($GB);
	if($tatetate ne 0)
	{
		&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：新このホストでは、しばらくスレッドが立てられません。<br>またの機会にどうぞ。。。<br><br><a href=http://info.2ch.net/wiki/index.php?BELucky>スレ立て規制回避</a><br><br>$GB->{FORM}->{'FROM'} ($tatetate)");
	}
	# ●スレ立てリミッター
	# 停止 by FOX
	# news 以外再有効化 by む 2006/8/3
	# 停止 by FOX 逆だと思う news だけだめなのだ 2007/4/8
	# news は厳しく
#	if($GB->{FORM}->{'bbs'} eq 'news')
	{
		if($GB->{MARU})
		{
			# ●での単位時間あたりのスレ立て数を調べ、
			# 同じ●で規定数以上だったら、スレ立てはお断りする
	
			my $tcount = $FOX->{KUROMARUTCOUNT};# デフォルト値(6)
	
			#以下のサーバ・板では少なくする
#			if($GB->{FORM}->{bbs} eq 'news')	{ $tcount = 3; }
			if(&mumumuKuromaruSuretateCount($GB, $tcount))
			{
				&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：●でスレッド立て過ぎです。またにしてください。");
			}
		}
	}
	# ごめんなさいリミッター
	if (&mumumuThreadNumExceededCheck($GB))
	{
		#スレッドが多すぎる場合、スレ立てをお断りする
		&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：この板は今スレッド大杉です。ごめんなさい。");
	}

	# ここまで来たらスルー
	return 0;
}
#############################################################################
# レスアンカーをリンクにする
#############################################################################
sub ResAnchor
{
	my ($GB) = @_;

	# >>nnn
	$GB->{FORM}->{'MESSAGE'} =~ s/&gt;&gt;([0-9]+)(?![-\d])/<a href="..\/test\/read.cgi\/$GB->{FORM}->{'bbs'}\/$GB->{FORM}->{'key'}\/$1" target="_blank">&gt;&gt;$1<\/a>/g;
	# >>nnn-nnn
	$GB->{FORM}->{'MESSAGE'} =~ s/&gt;&gt;([0-9]+)\-([0-9]+)/<a href="..\/test\/read.cgi\/$GB->{FORM}->{'bbs'}\/$GB->{FORM}->{'key'}\/$1-$2" target="_blank">&gt;&gt;$1-$2<\/a>/g;

	# 処理の結果1.2倍を超えたらだめ(キャップはスルー)
	if(!$GB->{CAP})
	{
		if(length($GB->{FORM}->{'MESSAGE'}) > ($FOX->{$GB->{FORM}->{bbs}}->{"BBS_MESSAGE_COUNT"} * 1.2)){
			&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：本文が長すぎます！");
		}
	}

	return 0;
}
#############################################################################
# BE用の文字列を作成する
# これを呼ぶことにより、$GB->{xBE} が準備される
#############################################################################
sub MakeBEString
{
	my ($GB) = @_;


	my $user_status = $GB->{BEelite};
	my $user_points_mark = '';
	my $xxx         = $GB->{BExxx}	;

	my $ppp         = $GB->{BEpoints};

	# BEランクに応じた # マークの対応を作る
	#if($user_status    eq "SOL")	{ $user_points_mark = 'S<font color=red>★</font>'; }
	if($user_status    eq "SOL")	{ $user_points_mark = 'S★'; }
	elsif($user_status eq "DIA")	{ $user_points_mark = $user_status; }
	elsif($user_status eq "PLT")	{ $user_points_mark = $user_status; }
	elsif($user_status eq "BRZ")	{ $user_points_mark = $user_status; }
	else				{ $user_points_mark = $user_status; }


	if($user_points_mark ne '')
	{
		$GB->{xBE} = " BE:$xxx-$user_points_mark($ppp)";
	}

	# 「ポイント特典」の表示
	if($FOX->{$GB->{FORM}->{bbs}}->{"BBS_BE_TYPE2"} && $GB->{NEWTHREAD})
	{
		# news poverty だけ
		if($GB->{FORM}->{'bbs'} eq 'news' || $GB->{FORM}->{'bbs'} eq 'poverty')
		{
			if($GB->{BELucky})
			{
				$GB->{xBE} .= " ポイント特典";
			}
		}
	}

	# heaven4vipは特別処理(BE出さない)
	if($GB->{FORM}->{bbs} eq 'heaven4vip')	{$GB->{xBE} = "";}

	#スレ立て時はステルスしない、be見えちゃう
	if($GB->{NEWTHREAD} && $GB->{FORM}->{bbs} eq 'news')
	{
		$GB->{NINNIN} = 0	;
	}
	#株主優待プチ
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
# PC/携帯/味ぽん/p2/携帯用ブラウザ 識別マークの処理
# 戻り値: 識別マーク "" "0" "O" "o" "P" "Q"
########################################################################
sub ShikibetsuMark
{
	my ($GB) = @_;

	# BBS_SLIP=checked ではない場合はなし
	if(!$FOX->{$GB->{FORM}->{'bbs'}}->{BBS_SLIP})	{ return ""; }

	# 実験　iPhone
	# iPhone 3G経由、IPアドレスで判断
	if(&IsIP4iPhone($ENV{'REMOTE_ADDR'}))		{ return "i"; }
	# iPhone Wifi経由、とりあえずUAで判断、偽装されるのは今のところ仕方なし
	if($ENV{'HTTP_USER_AGENT'} =~ /iPhone/)		{ return "I"; }

	# 実験　Docomo の$ENV{HTTP_X_DCMGUID}
#	if($GB->{KEITAI} eq 1)
#	{
#		if($ENV{HTTP_X_DCMGUID})
#		{
#			return "I";
#		}
#		return "i";
#	}

	# 携帯は O
	if($GB->{KEITAI})		{ return "O"; }
	# 公式p2は P
	if($GB->{P22CH})		{ return "P"; }
	# AIR-EDGE PHONEセンター経由の味ぽんは o
	if(&mumumuIsAjipon($ENV{'REMOTE_ADDR'}))
					{ return "o"; }
	# 携帯用ブラウザは Q
	if($GB->{KEITAIBROWSER})	{ return "Q"; }

	# 上記のいずれでもないものは 0
	return "0";
}
#############################################################################
# IDのところに表示する文字列と、芋掘りの芋の種を作成する
# IDのところに表示する文字列は $GB->{xID} に格納され、
# 芋掘りの芋は $GB->{LOGDAT} に格納される
#############################################################################
sub MakeIdStringAndLogdat
{
	my ($GB) = @_;

	#IDを生成する
	my $idcrypt = undef;

	#IPv6では「上48」と「上64」と「全128」から生成した24桁のID
	if ($GB->{IPv6})
	{
		use Net::IP;
		my $ip = new Net::IP($ENV{REMOTE_ADDR});
		my $ip_number = $ip->intip();
		# 上48bit
		my $ip_number_h = $ip_number >> 80;
		# 上64bit
		my $ip_number_m = $ip_number >> 64;

		my $idcrypt_h = &foxGetMD5id(
			$GB->{FORM}->{'bbs'},				#bbs
			$GB->{MD5DATE},					#日付
			$FOX->{$GB->{FORM}->{'bbs'}}->{MD5NUMBER},	#
			$ip_number_h					#
		)	;
		my $idcrypt_m = &foxGetMD5id(
			$GB->{FORM}->{'bbs'},				#bbs
			$GB->{MD5DATE},					#日付
			$FOX->{$GB->{FORM}->{'bbs'}}->{MD5NUMBER},	#
			$ip_number_m					#
		)	;
		my $idcrypt_f = &foxGetMD5id(
			$GB->{FORM}->{'bbs'},				#bbs
			$GB->{MD5DATE},					#日付
			$FOX->{$GB->{FORM}->{'bbs'}}->{MD5NUMBER},	#
			$ip_number					#
		)	;
		$idcrypt = $idcrypt_h . '_' . $idcrypt_m . '_' . $idcrypt_f;
	}
	else
	{
		$idcrypt = &foxGetMD5id(
			$GB->{FORM}->{'bbs'},				#bbs
			$GB->{MD5DATE},					#日付
			$FOX->{$GB->{FORM}->{'bbs'}}->{MD5NUMBER},	#
			$GB->{IDNOTANE}					#
		)	;
	}

	#siberiaで表示するIPアドレス
	my $ipipip = $ENV{REMOTE_ADDR};	#$GB->{HOST29};
	#識別マークを得る (O o P Q 0)
	my $baribari = &ShikibetsuMark($GB);

	#ID用文字列を作る
	# siberiaは発信元IPアドレスを表示
#	if($GB->{FORM}->{'bbs'} eq "siberia")
	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_DISP_IP'} eq "siberia")
	{
		$GB->{xID} = "発信元:$ipipip $baribari";
	}
	elsif($FOX->{$GB->{FORM}->{bbs}}->{'BBS_DISP_IP'} eq "sakhalin")
	{
		$GB->{xID} = "発信元:$ipipip $baribari";
		if($GB->{P22CH})	{$GB->{xID} = "発信元:$ipipip ($GB->{IDNOTANE}) $baribari";}
		if($GB->{KEITAI})	{$GB->{xID} = "発信元:$ipipip ($GB->{IDNOTANE}) $baribari";}
		if($GB->{CAP})		{$GB->{xID} = "発信元:??? $baribari";}
	}
	# IDなしの板
	elsif($FOX->{$GB->{FORM}->{bbs}}->{'BBS_NO_ID'} eq "checked")
	{
		$GB->{xID} = "$baribari";
	}
	# キャップでトラックバックじゃない場合はID:???
	elsif($GB->{CAP} && !$GB->{TBACK})
	{
		$GB->{xID} = "ID:???$baribari";
	}
	# 強制IDの板
	elsif($FOX->{$GB->{FORM}->{bbs}}->{'BBS_FORCE_ID'} eq "checked")
	{
		$GB->{xID} = "ID:$idcrypt$baribari";
	}
	# 任意IDの板はメール欄が空じゃない時はID:???
	elsif($GB->{FORM}->{'mail'} ne "")
	{
		$GB->{xID} = "ID:???$baribari";
	}
	# 任意IDの板でメール欄が空
	else
	{
		$GB->{xID} = "ID:$idcrypt$baribari";
	}

	# BE_TYPE2の板では、★でない●餅の新スレ時には●マークがつく
	if($FOX->{$GB->{FORM}->{bbs}}->{"BBS_BE_TYPE2"} && $GB->{NEWTHREAD})
	{
		if($GB->{MARU} && !$GB->{CAP})
		{
			$GB->{xID} .= "●";
		}
	}

	# 株の処理
	if($GB->{FORM}->{'mail'} =~ /\!stock/)
	{
		my $ksu = &foxGetKabusu($GB,$GB->{FORM}->{'bbs'})	;
		if($ksu > 0)
		{
			$GB->{FORM}->{'mail'} =~ s/\!stock//	;
			my $kbkb = "株";
			if   ($ksu >= 300)	{$kbkb="神";}
			elsif($ksu >= 119)	{$kbkb="桜";}
			elsif($ksu >= 109)	{$kbkb="梅";}
			elsif($ksu >= 99)	{$kbkb="白";}
			elsif($ksu >= 90)	{$kbkb="卒";}
			elsif($ksu >= 88)	{$kbkb="米";}
			elsif($ksu >= 80)	{$kbkb="傘";}
			elsif($ksu >= 77)	{$kbkb="喜";}
			elsif($ksu >= 60)	{$kbkb="還";}
			elsif($ksu >= 40)	{$kbkb="妹";}
			elsif($ksu >= 20)	{$kbkb="愛";}
			$GB->{xID} = " <a href=\"http://2ch.se/\">$kbkb</a> " . $GB->{xID};
		}
	}

	#if(IsP2($GB))
	#{
	#	$GB->{xID} .= ' P2@';
	#	if($GB->{MARU})
	#	{
	#		$GB->{xID} .= "●$GB->{MARU}";
	#	}
	#	$GB->{xID} .= " $ENV{REMOTE_ADDR}($GB->{HOST})";
	#}

	# vip 臭いのテスト&デバッグ
#	my $v931 = "(" . $GB->{V931} . ")";
#	$GB->{xID} .= $v931;
	# 芋掘り用の芋作り
	&MakeLogdat($GB, $idcrypt, $baribari);


#$GB->{xID} .= " DISP_IP=[$FOX->{$GB->{FORM}->{bbs}}->{'BBS_DISP_IP'}]";
	return 0;
}
#############################################################################
# 1ユニット分のログファイル(芋掘りの芋)を作る
# IDと識別マークが必要なので、MakeIdStringAndLogdat から呼ばれることになる
# 芋掘りの芋は $GB->{LOGDAT} に格納される
#############################################################################
sub MakeLogdat
{
	my ($GB, $idcrypt, $baribari) = @_;

	# 芋掘りの芋に入れる、メッセージの頭30バイトを抽出
	my $mss = substr($GB->{FORM}->{'MESSAGE'}, 0, 30);
	$mss =~ s/</&lt;/g; $mss =~ s/>/&gt;/g;

	# 1ユニット分のログファイル(芋掘りの芋)を作る
	my $CID = ""	;
	if($ENV{HTTP_X_DCMGUID})	{$CID = "■■■($ENV{HTTP_X_DCMGUID})■■■";}


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
# 1ユニット分のdatを作る
#############################################################################
sub MakeOutdat
{
	my ($GB) = @_;
	my $hoshos = "";
#	my $message = $GB->{FORM}->{'MESSAGE'};

#			$message =~ s/sssp\:\/\/img\.2ch\.net\/([\w|\:\!\#\$\%\=\&\-\^\`\\\|\@\~\[\{\]\}\;\+\*\,\.\?\/]+)/<img src="http:\/\/img\.2ch\.net\/$1">/g;

	if(&dispIconSssp($GB))	{$GB->{FORM}->{'MESSAGE'} = 'sssp://img.2ch.net/ico/' . $GB->{icon} .' <br> '. $GB->{FORM}->{'MESSAGE'} ;}


	# 1ユニット分のdatを作る
	$GB->{OUTDAT} = "$GB->{FORM}->{'FROM'}<>$GB->{FORM}->{'mail'}<>$GB->{DATE} $GB->{xID}$GB->{xBE}<> $GB->{FORM}->{'MESSAGE'} <>$GB->{FORM}->{'subject'}";

	# saku/saku2ch/sakudは特殊処理(HOST: ホスト名表示、ID・BE表示なし)
	if($GB->{FORM}->{'bbs'} eq "saku" || $GB->{FORM}->{'bbs'} eq "saku2ch" || $GB->{FORM}->{'bbs'} eq "sakud")
	{
		if (!$GB->{CAP})
		{
			$hoshos = $GB->{HOST};
			# 携帯では固有番号も表示する
			if($GB->{KEITAI})
			{
				$hoshos = "$GB->{IDNOTANE} $GB->{HOST}";
			}
			if($GB->{KEITAIBROWSER})
			{
				$hoshos = "$GB->{IDNOTANE} $GB->{HOST}";
			}
			# 公式p2ではユーザ番号と p2-client-ip: の情報も表示する
			# foxSetHostで、$GB->{HOST2} に入っている
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
# スレッド924の日付更新処理(だけ)を行う
# 入力: 924スレッドのdatフルパス名
#############################################################################
sub Update924
{
	my ($GB, $DATAFILE) = @_;
	# Perl 5.7.2 以降の utime は undef でおｋ
	my $now = $^V lt v5.7.2 ? time : undef;

	# 雪だるまではbbsdにageのコマンドを送る
	if(IsSnowmanServer == BBSD->{REMOTE} || IsSnowmanServer && $GB->{FORM}{mail} !~ /sage/)
	{
		# sageならtouchだけ
		if($GB->{FORM}->{'mail'} =~ /sage/)
		{
			# bbsd の touch では undef の代わりに 0
			my $cmd = 'touch';
			my $errmsg = bbsd($DATAFILE, $cmd, $now || 0, 'dummy'); 
			# タイムアウトかどうかチェック
			if(&bbsd_TimeoutCheck($GB, $errmsg))
			{
				&bbsd_TimeoutError($GB, $cmd);
			}
		}
		# ageたい場合、ageるコマンドを送る
		else
		{
			my $cmd = 'raise';
			my $errmsg = bbsd($GB->{FORM}->{'bbs'}, $cmd, $GB->{FORM}->{'key'}, 'dummy'); 
			# タイムアウトかどうかチェック
			if(&bbsd_TimeoutCheck($GB, $errmsg))
			{
				&bbsd_TimeoutError($GB, $cmd);
			}
		}
	}
	else
	{
		# datファイルへの追記を行わず、touchだけを実施
		# undef は変数でなく直接記述でないとダメ
		utime $now || undef, $now || undef, $DATAFILE;
		# パーミッション調整は不要
		#chmod(0666, $DATAFILE);
	}

	return 0;
}
#############################################################################
# datファイルを1行分追加で書き込む
# 入力: $GB、ファイル名、データ1行分(改行コードなし)、フラグ
#       フラグ 0: dat処理、1:ログ処理
#############################################################################
sub WriteDatFile
{
	my ($GB, $filename, $filedata, $flag) = @_;
	use Fcntl; 

	# datの処理の場合、新スレとレスで場合分け
	if (!$flag)
	{
		# 新スレの場合、datがあったらエラー
		if($GB->{NEWTHREAD})
		{
			sysopen(OUT, $filename, O_WRONLY|O_CREAT|O_EXCL, 0666)
			or &DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：板飛びそうなので、またの機会にどうぞ。。。");
		}
		# レスの場合、datに追記できなかったらエラー
		else
		{
			sysopen(OUT, $filename, O_WRONLY|O_APPEND, 0666)
			or &DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：レスしようとしたらdatに書けませんでした。今dat落ちしちゃったかもです。");
		}
	}
	else
	# ログの場合、常に追加モード
	{
		sysopen(OUT, $filename, O_WRONLY|O_APPEND|O_CREAT, 0666)
		or &DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：ログファイルに書けませんでした。");
	}
	print OUT "$filedata\n";
	close(OUT);
	# 前半でumaskしてsysopenで指定しているので、パーミッション調整は不要
	#chmod(0666, $filename);

	return 0;
}
########################################################################
#
########################################################################
#ゲロトラップ防止ここから↓
sub GeroTrap
{
	my ($GB) = @_	;

	#以下の板はするー
	if(&KiseiOFF($GB))			{return 0;}
#	if($GB->{FORM}->{'bbs'} eq "campus")	{return 0;}
	#TBACKはするー
	if($GB->{TBACK})			{return 0;}
	#以下の板はするー
#	if($GB->{FORM}->{'bbs'} eq "siberia")	{return 0;}
	# 携帯・味ぽんはするー
	if(&IsIP4Mobile($ENV{REMOTE_ADDR}))	{return 0;}
	# iPhoneはするー
	if($ENV{'HTTP_USER_AGENT'} =~ /iPhone/)	{return 0;}
	#★はスルー
	if($GB->{CAP})				{return 0;}
	#●はスルー
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
		&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：あなた騙されてますよ？");
	}
	if($ENV{'HTTP_REFERER'} eq '')
	{
		&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：リファラぐらい送ってください");
	}
	return 0;
}
#↑ここまで
#############################################################################
# 携帯かそうでないかをチェックする
# 0: 携帯/AIR-EDGEの味ぽん以外、1: iモード、2: EZweb、3: ボーダフォン!ライブ
# 4: AIR-EDGE PHONEセンター経由の味ぽん
# 5: emobile EMnet
#############################################################################
sub IsIP4Mobile
{
	my ($raddr) = @_;

	# iモード
	if(&mumumuIsIP4IMode($raddr))		{ return 1; }
	# EZweb
	elsif(&mumumuIsIP4EZWeb($raddr))	{ return 2; }
	# Vodafone!ライブ
	elsif(&mumumuIsIP4Vodafone($raddr))	{ return 3; }
	# AIR-EDGE PHONEセンター経由の味ぽん
	elsif(&mumumuIsAjipon($raddr))		{ return 4; }
	# emobile EMnet
	elsif(&mumumuIsIP4EMnet($raddr))	{ return 5; }
	# 上記のどれでもない
	else					{ return 0; }
}
#############################################################################
# iPhoneのIPアドレスかどうかチェックする
#############################################################################
sub IsIP4iPhone
{
	my ($raddr) = @_;

	# CIDRリストに該当があるかどうかチェックする
	return $FOX->{IPHONECIDR}->find($raddr);
}
#############################################################################
# iモードセンタのIPアドレスかどうかチェックする
#############################################################################
sub mumumuIsIP4IMode
{
	my ($raddr) = @_;

	# CIDRリストに該当があるかどうかチェックする
	return $FOX->{IMODECIDR}->find($raddr);
}
#############################################################################
# EZサーバのIPアドレスかどうかチェックする
#############################################################################
sub mumumuIsIP4EZWeb
{
	my ($raddr) = @_;

	# CIDRリストに該当があるかどうかチェックする
	return $FOX->{EZWEBCIDR}->find($raddr);
}
#############################################################################
# ボーダフォンライブ！サーバのIPアドレスかどうかチェックする
#############################################################################
sub mumumuIsIP4Vodafone
{
	my ($raddr) = @_;

	# CIDRリストに該当があるかどうかチェックする
	return $FOX->{SOFTBANKCIDR}->find($raddr);
}
#############################################################################
# emobile EMnetのIPアドレスかどうかチェックする
#############################################################################
sub mumumuIsIP4EMnet
{
	my ($raddr) = @_;

	# CIDRリストに該当があるかどうかチェックする
	return $FOX->{EMNETCIDR}->find($raddr);
}
#############################################################################
# AIR-EDGE PHONEセンターのIPアドレスかどうかチェックする
#############################################################################
sub mumumuIsIP4AirEdgePhone
{
	my ($raddr) = @_;

	# CIDRリストに該当があるかどうかチェックする
	return $FOX->{AIREDGECIDR}->find($raddr);
}
#############################################################################
# AIR-EDGE MEGAPLUSのIPアドレスかどうかチェックする
#############################################################################
sub mumumuIsIP4MegaPlus
{
	my ($raddr) = @_;

	# CIDRリストに該当があるかどうかチェックする
	return $FOX->{MEGAPLUSCIDR}->find($raddr);
}
#############################################################################
# AIR-EDGE PHONEセンター経由の味ぽんかどうか調べる
# AIR-EDGE PHONEセンターからの接続でリファラがない場合にのみ真
#############################################################################
sub mumumuIsAjipon
{
	my ($raddr) = @_;

	if(&mumumuIsIP4AirEdgePhone($raddr) &&
	   $ENV{'HTTP_REFERER'} eq '')	{return 1;}
	else				{return 0;}
}
#############################################################################
# 公式p2のIPアドレスかどうかチェックする
#############################################################################
sub mumumuIsIP4P22ch
{
	my ($raddr) = @_;
	our @P22chIPAddrs;
	BEGIN {
		# IPアドレスに変化があったら、ここを編集する
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
# 相手が携帯用ブラウザかどうかチェックする
# 0: 携帯用ブラウザじゃない
# 1: ibisBrowser
# 2: jig Browser
# 3: SoftBank PCサイトブラウザ
# 4: docomo フルブラウザ
# 5: au PCサイトビューアー
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

	# 削ジェンヌさんからの指令により、newservantだけこのチェックをしない
	if($GB->{FORM}->{'bbs'} ne "newservant")
	{
		# SoftBank PCサイトブラウザ
		if(&mumumuIsIP4pcsiteBrowser($raddr))	{return 3;}
	}

	# docomoフルブラウザ
	if(&mumumuIsIP4imodefullBrowser($raddr))	{return 4;}

	# au PCサイトビューアー
	if(&mumumuIsIP4pcsiteViewer($raddr))	{return 5;}

	# 上記のどれでもない
	return 0;
}
#############################################################################
# ibisBrowser (one of 携帯用フルブラウザ)のIPアドレスかどうかチェックする
#############################################################################
sub mumumuIsIP4ibisBrowser
{
	my ($raddr) = @_;

	# CIDRリストに該当があるかどうかチェックする
	return $FOX->{IBISBROWSERCIDR}->find($raddr);
}
#############################################################################
# jigBrowser (one of 携帯用フルブラウザ)のIPアドレスかどうかチェックする
#############################################################################
sub mumumuIsIP4jigBrowser
{
	my ($raddr) = @_;

	# CIDRリストに該当があるかどうかチェックする
	return $FOX->{JIGBROWSERCIDR}->find($raddr);
}
#############################################################################
# PCサイトブラウザ (ソフトバンク携帯フルブラウザ)のIPアドレスかどうか
#############################################################################
sub mumumuIsIP4pcsiteBrowser
{
	my ($raddr) = @_;

	# CIDRリストに該当があるかどうかチェックする
	return $FOX->{PCSITEBROWSERCIDR}->find($raddr);
}
#############################################################################
# フルブラウザ (ドコモ携帯フルブラウザ)のIPアドレスかどうか
#############################################################################
sub mumumuIsIP4imodefullBrowser
{
	my ($raddr) = @_;

	# CIDRリストに該当があるかどうかチェックする
	return $FOX->{IMODEFULLBROWSERCIDR}->find($raddr);
}
#############################################################################
# PCサイトビューアー (au携帯フルブラウザ)のIPアドレスかどうか
#############################################################################
sub mumumuIsIP4pcsiteViewer
{
	my ($raddr) = @_;

	# CIDRリストに該当があるかどうかチェックする
	return $FOX->{PCSITEVIEWERCIDR}->find($raddr);
}
#############################################################################
#
#############################################################################
sub checkPragma
{
	my ($GB) = @_	;
	#以下の板はするー
	if(&KiseiOFF($GB))			{return 0;}
	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_4WORLD'} eq "checked")	{return 0;}

	#携帯はスルー
	if($GB->{KEITAI})			{return 0;}
	if($GB->{KEITAIBROWSER})		{return 0;}
	#AIR-EDGE PHONEセンターからの接続はスルー
	if(&mumumuIsIP4AirEdgePhone($ENV{'REMOTE_ADDR'}))	{return 0;}
	#newsはスルー
	if($GB->{FORM}->{'bbs'} eq "news")	{return 0;}
	#operate/sec2chdはスルー
	if($GB->{FORM}->{'bbs'} eq "operate")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "sec2chd")	{return 0;}
	#★はスルー
	if($GB->{CAP})				{return 0;}
	#●はスルー
	if($GB->{MARU})				{return 0;}
	#mac はスルー
	if($ENV{HTTP_USER_AGENT} =~ /PDA/)		{return 0;}
	if($ENV{HTTP_USER_AGENT} =~ /Mac/)		{return 0;}
	if($ENV{HTTP_USER_AGENT} =~ /^Monazilla\/1/)	{return 0;}
	if($ENV{HTTP_ACCEPT_LANGUAGE} =~ /ja/)		{return 0;}
	#NetFrontは Pragma: を吐いて来ない
	if($ENV{HTTP_USER_AGENT} =~ /NetFront/)		{return 0;}

	if($ENV{HTTP_PRAGMA})
	{
		&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：ブラウザ変ですよん。$ENV{'HTTP_REFERER'}");
	}
}
#############################################################################
#
#############################################################################
sub ToolGekitai0
{
	my ($GB) = @_	;
	my $span = $FOX->{$GB->{FORM}->{'bbs'}}->{SAMBA24}	;

	#以下の板はスルー
	if(&KiseiOFF($GB))			{return 0;}
#	if($GB->{FORM}->{'bbs'} eq "campus")	{return 0;}

	if(&IsIP4Mobile($ENV{REMOTE_ADDR}))
				{$span += $FOX->{SambaOffset_KEITAI}	;}
	if($GB->{P22CH})	{$span += $FOX->{SambaOffset_P22CH}	;}

	$GB->{version} .= " +Samba24="		;
	$GB->{version} .= $FOX->{$GB->{FORM}->{'bbs'}}->{SAMBA24};

	#★でトラックバックじゃない時はスルー
	if($GB->{CAP} && !$GB->{TBACK})		{return 0;}
	#●はスルー => ●は専用のsamba
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
	my $remo = $GB->{HOST29}	; #いわゆるリモホ
	my $ita  = $GB->{FORM}->{bbs}	;

#	&DispError2($GB,"ＥＲＲＯＲ！","海外ドメイン規制($ita)。");

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

#	&DispError2($GB,"ＥＲＲＯＲ！","海外ドメイン規制($remo)。");
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
		if($remo =~ /$dxx/i)	{&DispError2($GB,"ＥＲＲＯＲ！","海外ドメイン規制($dom)。<a href=\"http://2ch.tora3.net/\">２ちゃんねるビューア</a>を使うと書き込めます。");}
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

	#以下の板はスルー
	if(&KiseiOFF($GB))			{return 0;}
	if($GB->{FORM}->{'bbs'} eq "pinknanmin"){return 0;}
	if($GB->{FORM}->{'bbs'} eq "servant")	{return 0;}
#	if($GB->{FORM}->{'bbs'} eq "campus")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "trafficinfo" && $GB->{KEITAI})	{return 0;}

	#★はスルー
	if($GB->{CAP})				{return 0;}

	#●の判定
	if($GB->{MARU})
	{
		my @PIP = @FOX_K998	;
		#●規制リストチェック
		foreach(@PIP)
		{
			chomp		;
			if(/^\#/)	{next;}
			if(eval { $GB->{MARU} =~ /$_/; })
			{
				# operate2/sec2chdでは●のIDをエラー表示する
				if($GB->{FORM}->{'bbs'} eq "operate2" ||
				   $GB->{FORM}->{'bbs'} eq "housekeeping" ||
				   $GB->{FORM}->{'bbs'} eq "sec2chd")
				{
#					return 0;
					&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：アクセス規制中です！！(●=$GB->{MARU})");
				}
				else
				{
					&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：アクセス規制中です！！(●)");
				}
			}
		}
		#規制リストに載っていない●はスルー
		return 0;
	}

	#p2規制
	if($ENV{'REMOTE_ADDR'} =~ /^61\.165\./)		{&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：アクセス規制中です！！(9)");}
	if($ENV{'REMOTE_ADDR'} =~ /^202\.181\.96\./)	{&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：アクセス規制中です！！(9)");}
	if($ENV{'REMOTE_ADDR'} =~ /^202\.222\.16\./)	{&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：アクセス規制中です！！(9)");}
	if($ENV{'REMOTE_ADDR'} =~ /^21\.240\./)		{&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：アクセス規制中です！！(9)");}
	if($ENV{'REMOTE_ADDR'} =~ /^69\.56\./)		{&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：アクセス規制中です！！(9)");}
	if($ENV{'REMOTE_ADDR'} =~ /^211\.8\.35\./)	{&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：アクセス規制中です！！(9)");}

	#削除系の板は●チェック後はスルー
	if($GB->{FORM}->{'bbs'} eq "saku")	{return 0;}
#	if($GB->{FORM}->{'bbs'} eq "sakud")	{return 0;}
#	if($GB->{FORM}->{'bbs'} eq "saku2ch")	{return 0;}
	#一部の板はスルー
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
		&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：今は書けません。");
	}

	#携帯以外はリモホの文字列をチェック
	if(!($GB->{KEITAI} || $GB->{KEITAIBROWSER}))
	{
		if($GB->{HOST999} =~ /proxy/)	{&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：変なホスト規制中！！　変なホストです。");}
		if($GB->{HOST999} =~ /cache/)	{&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：変なホスト規制中！！　変なホストです。");}
		if($GB->{HOST999} =~ /^tor\./)	{&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：変なホスト規制中！！　変なホストです。");}
		if($GB->{HOST999} =~ /^tor\d+\./)	{&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：変なホスト規制中！！　変なホストです。");}
#		if($GB->{HOST999} =~ /^gw/)	{&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：変なホスト規制中！！　変なホストです。");}
	}
	#海外ドメイン規制
	&CheckDomain($GB)		;

	#書き込み拒否リストで判定
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
#&DispError2($GB,"ＥＲＲＯＲ！","BBS = [$1]");
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
$GB->{DEBUG} .= "リストで判定 ($_) <br>";
		# 大文字小文字区別するので注意
		if(eval { $GB->{HOST999} =~ /$_/; })
		{# リストにあった
			# 拒否られマークをつけるフラグ
			my $deniedmark = 0;

			# accuse/operate/sec2chd で fusianasan してて
			# 新スレではない場合は、、、
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
			# 拒否られマークをつけたうえで書き込みを許可する
			if($deniedmark)
			{
				# [―{}@{}@{}-] と一緒に出る時は
				# 串を持っているようにする
				if($GB->{BURNEDPROXY})
				{
					$GB->{FORM}->{'FROM'} = ' </b>ヾ[´・ω・｀]－<b> ' . $GB->{FORM}->{'FROM'};
				}
				else
				{
					$GB->{FORM}->{'FROM'} = ' </b>[´・ω・｀]<b> ' . $GB->{FORM}->{'FROM'};
				}
				return 1;
			}
			else
			{
				# 上記のもの以外はエラー
				&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：アクセス規制中です！！($_)<br><a href=\"http://qb5.2ch.net/sec2chd/\">ここで告知されています。</a>");
			}
		}
	}
#&DispError2($GB,"FOX ★","<font color=green>FOX ★</font>　どよ<br>");
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
	{#スレ立て時は●でもチェック
		if($ENV{'SERVER_NAME'} =~ /qb/)
		{#qb系
			return 0;
		}
		else
		{#qb系以外
			return 1;	#●でスルー復活してみる
		}
	}
	else
	{#レス時は●でするー
		return 1;
	}
	return 0	;
}
sub checkProxyAtAll
{
	my ($GB) = @_	;

	# news4vipでもBBQ有効(イオナズン対策)
	#if($ENV{'SERVER_NAME'} =~ /bbspink/)	{return 0;}
	#if($GB->{FORM}->{'bbs'} eq "news4vip")	{return 0;}
	#if($GB->{FORM}->{'bbs'} eq "news")	{return 0;}
	#if($GB->{FORM}->{'bbs'} eq "campus")	{return 0;}

	# IPv6環境ではBBQは(まだ)なし
	if($GB->{IPv6})				{return 0;}

	# BBQありをversionに追加
	$GB->{version} .= " +<a href=\"http://bbq.uso800.net/\">BBQ</a>";

	# BBQ に聞いてみる
	$GB->{BURNEDPROXY} = &checkProxyList($GB)		;

	# 公式p2ではProxyの時は全板ねぎまつきでBBQスルー
	# http://qb5.2ch.net/test/read.cgi/operate/1202007319/757-768
	if($GB->{P22CH} && $GB->{BURNEDPROXY})
	{
		$GB->{FORM}->{'FROM'} = ' </b>[―{}@{}@{}-]<b> ' . $GB->{FORM}->{'FROM'};
		return 0;
	}

	# 特定の板ではねぎまをつける
	if($GB->{FORM}->{'bbs'} eq "operate2" && $GB->{BURNEDPROXY}) {$GB->{FORM}->{'FROM'} = ' </b>[―{}@{}@{}-]<b> ' . $GB->{FORM}->{'FROM'};}
	if($GB->{FORM}->{'bbs'} eq "operate" && $GB->{BURNEDPROXY}) {$GB->{FORM}->{'FROM'} = ' </b>[―{}@{}@{}-]<b> ' . $GB->{FORM}->{'FROM'};}
	if($GB->{FORM}->{'bbs'} eq "sec2chd" && $GB->{BURNEDPROXY}) {$GB->{FORM}->{'FROM'} = ' </b>[―{}@{}@{}-]<b> ' . $GB->{FORM}->{'FROM'};}
	if($GB->{FORM}->{'bbs'} eq "goki" && $GB->{BURNEDPROXY}) {$GB->{FORM}->{'FROM'} = ' </b>[―{}@{}@{}-]<b> ' . $GB->{FORM}->{'FROM'};}

	#以下の板はするー
	if($GB->{FORM}->{'bbs'} eq "siberia" && !$GB->{NEWTHREAD})
	{
		my $bFile = "../$GB->{FORM}->{'bbs'}/BBQ/index.html";
		if(!(-e $bFile))	{return 0;}
	}
	#★でトラックバックじゃない時はスルー
	if($GB->{CAP} && !$GB->{TBACK})			{return 0;}

	#●はスルー
	#撤退　2010/5/5
	#if(&foxMARUsuru($GB) && !$GB->{NEWTHREAD})	{return 0;}

	# ありえないホスト
	#携帯以外はリモホの文字列をチェック
	if(!($GB->{KEITAI} || $GB->{KEITAIBROWSER}))
	{
		if($GB->{HOST4} =~ /^ns\d?\.|mail|www|^ftp|^smtp|^news/ || $GB->{HOST2} =~ /^ns\d?\.|mail|www|^ftp|^smtp|^news/)
		{
			&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：変なホスト規制中！！　変なホストです。");
		}
	}

	#operate2/operate/sec2chd で fusianasan はするー
	if($GB->{FORM}->{'bbs'} eq "operate2" && $GB->{FORM}->{'FROM'} =~ /$GB->{HOST}/ && $GB->{FORM}->{'subject'} eq "") {return 0;}
# 串利用の埋め立て荒らし発生のため、
# 一時的に operate の [―{}@{}@{}-] スルーをストップ -- 2006/3/17 by む
#	if($GB->{FORM}->{'bbs'} eq "operate" && $GB->{FORM}->{'FROM'} =~ /$GB->{HOST}/ && $GB->{FORM}->{'subject'} eq "") {return 0;}
#	if($GB->{FORM}->{'bbs'} eq "sec2chd" && $GB->{FORM}->{'FROM'} =~ /$GB->{HOST}/ && $GB->{FORM}->{'subject'} eq "") {return 0;}
	if($GB->{FORM}->{'bbs'} eq "goki" && $GB->{FORM}->{'FROM'} =~ /$GB->{HOST}/ && $GB->{FORM}->{'subject'} eq "") {return 0;}
	#一般的な処理
	if($GB->{BURNEDPROXY} eq 1)
	{
		&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：公開ＰＲＯＸＹからの投稿は受け付けていません！！(1)");
	}
}
############################################################################
# vipクオリティの各種処理ルーチン群
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
	$GB->{FORM}->{'FROM'} =~ s/(\!IQ)/ <\/b>【IQ$iq】<b> /;

	my $bill = $iq * 10 + int(rand(10000))	;
	if($bill < 1000000)	{$bill =~ s/(\d)(\d\d\d)(?!\d)/$1,$2/g;}
	else			{$bill =~ s/(\d)(\d\d\d)(\d\d\d)(?!\d)/$1,$2,$3/g;}

	$GB->{FORM}->{'FROM'} =~ s/(\!bill)/ <\/b>本日の利用料 $bill円<b> /;


	my @omikuji = ('うす','するめ','かめ','もぐら','おっぱい','ばいきん','でぶ','じゅうえん',
			'ぽち','みらーまん','たにし','てっちゃん','おじさん','よだれ','やぎ','ひめ',

			'ハチベエ','モーちゃん','ケニア','ジャンボ','豚','汗かき','コブラ','ポニー',
			'おさげ','まっちょ','カビ','よっしー','ぶりぶり','バケツ','げりべん','二重顎',
			'しもふり','はにわ','まんげつ','ゴリさん','殿下','マカロニ','リーダー','竜ちゃん',
			'寺門','よしこちゃん','ふーせん','委員長','たこ','金歯','ふけ','うし',

			'インド人','栽培マン','あざらし','めがね','ぶーちゃん','ねぐせ','出っ歯','ガリ',
			'ヤキソバン','しょっちゃん','ゾウリムシ','神いわゆるゴッド','ハカセ','モーチャン','空気','ハエ');
	my $omikuji2 = $nm % 64	;
	my $omikuji3 = $omikuji[$omikuji2];
	$GB->{FORM}->{'FROM'} =~ s/(\!kote)/ <\/b>【$omikuji3】<b> /;

	$omikuji2 = int(rand(scalar @omikuji));
	$omikuji3 = $omikuji[$omikuji2];
	if(rand(800) < 1)	{$omikuji3 = "神";}
	if(rand(4000) < 1)	{$omikuji3 = "女神";}
	$GB->{FORM}->{'FROM'} =~ s/(\!sute)/ <\/b>《$omikuji3》<b> /;

	my @kz;
	my @k0 = ('平民','生き物係','黒板係','給食係','掃除係','掲示係','整理係','体育係','音楽係','ベルマーク係','ベルマーク係','保健係','ストーブ係')	;
	my @k1 = ('平民','黒板係','給食係','掃除係','生き物係','整理係','体育係','音楽係','掲示係','ベルマーク係','保健係','ストーブ係','ベルマーク係')	;
	my @k2 = ('平民','給食係','掃除係','生き物係','黒板係','体育係','音楽係','掲示係','整理係','保健係','ストーブ係','ベルマーク係','ベルマーク係')	;
	my @k3 = ('平民','掃除係','生き物係','黒板係','給食係','音楽係','掲示係','整理係','体育係','ストーブ係','ベルマーク係','ベルマーク係','保健係')	;
	my @k4 = ('平民','掲示係','整理係','体育係','音楽係','ベルマーク係','ベルマーク係','保健係','ストーブ係','生き物係','黒板係','給食係','掃除係')	;
	my @k5 = ('平民','整理係','体育係','音楽係','掲示係','ベルマーク係','保健係','ストーブ係','ベルマーク係','生き物係','黒板係','給食係','掃除係')	;
	my @k6 = ('平民','体育係','音楽係','掲示係','整理係','保健係','ストーブ係','ベルマーク係','ベルマーク係','生き物係','黒板係','給食係','掃除係')	;
	my @k7 = ('平民','音楽係','掲示係','整理係','体育係','ストーブ係','ベルマーク係','ベルマーク係','保健係','掃除係','生き物係','黒板係','給食係')	;
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
#本文
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
		return "Attack $1 ---> Success. <font color=red>撃沈!!</font>"	;
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
	my $ships = "<font color=green face=\"Arial\"><b>current ships</b></font>($nnn) $path軍<br>";
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

	if($iq < 150)	{return '<font color=green>知能が低くて建造できませんでした。</font>' . "($name)";};
	if(length($name) >16)	{return '<font color=green>船名が長すぎます。</font>' . "($name)";};

	my $folder = "$path"	;
	if(-e "$folder/$name.ship")	{return '<font color=green>同名の船が既に存在します。</font>' . "($name)";};
	my @ds = ()		;
	if(opendir(DIR, $folder))
	{
		@ds = grep(!/^\./ && -f "$folder/$_", readdir(DIR));
		closedir DIR	;
	}
	my $nnn = @ds		;
	if($nnn >= 5)
	{
		return '<font color=green>これ以上建造できません。</font>' . "($name)"	;
	}
	if($name =~ /\d/)
	{
		return '<font color=green>数字が使えなくなりました。</font>' . "($name)"	;
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
	my @m0 = ('ニート','奴隷','召使','羊飼い','乳母','執事','修道士','靴磨き','盗賊','貧民','皿洗い','丁稚',
		'奴隷','奴隷','釣り師','影武者','足軽','スパイ','右大臣','伍長','パシリ','童貞','童貞','童貞',
		'奴隷','奴隷','飛脚','木こり','道化師','マギー','鍋奉行','番頭','男爵','門番','奥女中','部屋方',
		'奴隷','奴隷','スリ師','あきんど','忍び','妖怪','精霊','妖精','魔獣','親方','管理人','吟遊詩人',
		'奴隷','奴隷','奴隷','奴隷','奴隷','奴隷','奴隷','奴隷','奴隷','奴隷','悪魔',
		'奴隷','奴隷','奴隷','奴隷','奴隷','奴隷','奴隷','奴隷','奴隷','奴隷',
		'奴隷','奴隷','大工','床屋','背後霊','鍛冶屋','仕立屋','詐欺師','美人局','遊女','悪代官','風見鶏',
		'奴隷','奴隷','親分','子分','ゴト師','ギャンブラー','マフィア','ギャング','長老','助っ人','不良','ヤンキー',
		'奴隷','奴隷','元ヤン','ヤンママ','下手人','小僧','坊主','運び屋','蛇使い','1,000円亭主','ナース','DQN',
		'レスラー','<font color=tomato>スーパーハカー</font>','リーマン','駄菓子屋','痴漢','ストーカー','探偵','ドワーフ','役人','ヒッキー',
		'窓際社員','人造人間',
#'','','','','','','','',
		'奴隷','奴隷','メイド')	;
#		'','','','','','','','','','',
	my $omikuji2 = int(rand(scalar @m0));
	my $omikuji3 = $m0[$omikuji2];
	if(rand(200) < 1)	{$omikuji3 = "狐";}
	if(rand(400) < 1)	{$omikuji3 = "AV監督";}

	return $omikuji3	;
}
sub GetMibunBe
{
	my @m0 = ('僧侶','大臣','公爵','ナイト','戦士','魔法使い','天使',
			'武士','忍','くのいち','先生','教授','理事','常務','専務',
			'大佐','本部長','査察官','ドクター','婦長','委員長','頭取','機長',
#'','','','','','','','',
#'','','','','','','','',
		'王様','王様','王様')	;
	my $omikuji2 = int(rand(scalar @m0));
	my $omikuji3 = $m0[$omikuji2];
#	if(rand(200) < 1)	{$omikuji3 = "狐";}
#	if(rand(400) < 1)	{$omikuji3 = "AV監督";}

	return $omikuji3	;
}
sub GetJinsei
{
	my @m0 = (
		'恋','同棲','浮気','離婚','抜け駆け','駆け落ち','失踪','引越し',
		'留学','海外留学','1,000万馬券当てる','宝くじ買う','片思い','やせる','入院','歌手デビュー',
		'受験','出産','第３子誕生','ついに逝く','逮捕','入院','太る','太る',
		'バンドやる','おれおれに引っかかる','財布落とす','自転車盗まれる','うんこ踏む','うんこたれる','絵を描く','また落選',
		'自己破産','ぼこられる','家建てる','空き巣にやられる','また一人','自殺','2ch中毒','ひきこもる',
		'家出する','太る','太る','太る','太る','太る','太る','太る',
#		'太る','太る','太る','太る','太る','太る','太る','太る',
#'','','','','','','','',
		'結婚','リストラ','就職')	;
	my $omikuji2 = int(rand(scalar @m0));
	my $omikuji3 = $m0[$omikuji2];
	if(rand(200) < 1)	{$omikuji3 = "金鉱発見";}
	if(rand(400) < 1)	{$omikuji3 = "グラミー賞受賞";}

	return $omikuji3	;
}
sub GetAnimal
{
	my @m0 = ('きりんさん','ぞうさん','山口','狐','猫','犬',
		'むささび','ハルキゲニア','マンモス','とど','あざらし','河豚','河馬','海豚',
		'ウィルス','妖怪','エイリアン','E.T','ヤンキー','おばさん','セイウチ','くじら',
		'ワニ','チンパンジー','なまけもの','まんとひひ','おらうーたん','りすさん','亀','しろくま',
		'ツチノコ','ブタ','ブタ','ブタ','ブタ','ブタ','ブタ','ブタ',
		'ぶた','豚','ブタ')	;
	my $omikuji2 = int(rand(scalar @m0));
	my $omikuji3 = $m0[$omikuji2];
	if(rand(200) < 1)	{$omikuji3 = "デブ";}
#	if(rand(400) < 1)	{$omikuji3 = "AV監督";}

	return $omikuji3	;
}
sub GetFood
{
	my @m0 = ('キャベツ','天丼','カツどん','うな重','オムライス','納豆','タツタサンド',
		'ししゃも','しじみ','さとうきび','苺','みみず','金時','お寿司','そば',
		'かに','イカ納豆','さしみ','きりたんぽ','いずし','ステーキ','マック','フレンチフライ',
		'うまい棒','パン','パン','パン','パン','パン','パン','パン',
		'カレーパン','すいとん','きのこ','冷凍マグロ','パン','パン','パン','パン',
#'','','','','','','','',
		'うどん','らーめん','わかめ')	;
	my $omikuji2 = int(rand(scalar @m0));
	my $omikuji3 = $m0[$omikuji2];
	if(rand(200) < 1)	{$omikuji3 = "ピザ";}
#	if(rand(400) < 1)	{$omikuji3 = "AV監督";}

	return $omikuji3	;
}
sub GetDrink
{
	my @m0 = ('味噌汁','ペプシ',
		'酒','バーボン','スコッチ','焼酎','泡盛','テキーラ','牛乳','母乳',
		'ワイン','葡萄酒','ブランデー','はみん','紅茶','缶コーヒー','ビール','マルガリータ',
#'','','','','','','','',
		'天然水','雨','海水')	;
	my $omikuji2 = int(rand(scalar @m0));
	my $omikuji3 = $m0[$omikuji2];

	return $omikuji3	;
}
sub GetWhere
{
	my @m0 = (
		'あそこ','隠れ家','大奥','階段','美濃','尾張','摂津','近場','クルーザー','ボート',
		'岐阜','和歌山','佐賀','長崎','京都','奈良','新潟','岩手','秋田','茨城',
		'イギリス','フランス','ドイツ','オランダ','スペイン','デンマーク','フィンランド','中国','韓国','北朝鮮',
		'大阪','さいたま','田舎','都会','番屋','居酒屋','料亭','カフェ','プール','近所',
		'ベット','牛舎','馬屋','厠','ベランダ','おしいれ','玄関','屋上','地下室','エレベーター',
		'カザフスタン','モロッコ','台所')	;
#		'','','','','','','','','','',
	my $omikuji2 = int(rand(scalar @m0));
	my $omikuji3 = $m0[$omikuji2];
	if(rand(200) < 1)	{$omikuji3 = '天竺';}
	if(rand(400) < 1)	{$omikuji3 = 'ソープ';}

	return $omikuji3	;
}
sub GetDo
{
	my @m0 = (
		'ジャンプ','ブーン','爆発','うｐ','実験','頭突き','変身','逆立ち','体当たり',
		'どろどろ','子作り','セックス','昇天','抱擁','観察','手術','整形','夜這い','夜逃げ',
		'ぐりぐり','下痢','タッチ','キス','メイクラブ','メイクミラクル','貯金','勉強','じゃんけん','不倫',
		'ぎしぎし','あんあん','ちろちろ','ぺろぺろ','べろべろ','にんにん','くんくん','ぐんぐん','たんとん','にょろにょろ',
		'うんこ','もみもみ','正座')	;
#		'','','','','','','','','','',
	my $omikuji2 = int(rand(scalar @m0));
	my $omikuji3 = $m0[$omikuji2];
	if(rand(200) < 1)	{$omikuji3 = "切腹";}
	if(rand(400) < 1)	{$omikuji3 = "初体験";}

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
		$GB->{FORM}->{'FROM'} =~ s/\!kab\:[a-zA-Z0-9]+/ <\/b>【$GB->{MEIGARA}:$GB->{KABUSU}】<b> /;
	}
	elsif($GB->{FORM}->{'FROM'} =~ /\!kab\%/)
	{
		$GB->{FORM}->{'FROM'} =~ s/(\!kab\%)/ <\/b>株主【$GB->{ZENKABU}】<b> /;
	}
	else
	{
		$GB->{FORM}->{'FROM'} =~ s/(\!kab)/ <\/b>株価【$GB->{KABUKA}】<b> /;
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
	my @omikuji = ("大吉","大吉","大吉","大吉","大吉","吉","中吉","小吉","末吉","凶","大凶","ぴょん吉","だん吉","豚");
	my $omikuji2 = int(rand(scalar @omikuji));
	my $omikuji3 = $omikuji[$omikuji2];
	if(rand(800) < 1)	{$omikuji3 = "神";}
	if(rand(10000) < 1)	{$omikuji3 = "女神";}
	$GB->{FORM}->{'FROM'} =~ s/(\!omikuji)/ <\/b>【$omikuji3】<b> /;
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
	my $omikuji3 = "$omikuji2円";
	$GB->{FORM}->{'FROM'} =~ s/(\!dama)/ <\/b>【$omikuji3】<b> /;
	return 0;
}
#############################################################################
# 処理中のdatの情報を$GBにセットする
# 入力: $GB, ターゲットとなるdatの$key
# $GB->{DATNUM}, $GB->{DAT1}, $GB->{DATLAST}[N]
#############################################################################
sub GetDatInfo
{
	my ($GB, $key) = @_;
	my $datfile = $GB->{DATPATH} . $key . ".dat";
	my $datlastnum = $FOX->{$GB->{FORM}->{bbs}}->{"BBS_CONTENTS_NUMBER"};

	if($GB->{NEWTHREAD})
	{
		# 新スレの場合
		$GB->{DAT1} = $GB->{OUTDAT};
		$GB->{DATNUM} = 1;
		@{$GB->{DATLAST}} = ();
	}
	else
	{
		# レスの場合
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
# 最終緊急堤防
# 入力、$GB, datファイル名
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
	&DispError2($GB,"ＥＲＲＯＲ！", "ＥＲＲＯＲ：このスレッドには書き込めません。最後の手段!!");

	return 0;
}
#############################################################################
# 緊急堤防
# 入力、$GB, datファイル名
#############################################################################
sub EmergOver1000
{
	my ($GB, $dat) = @_;

	chmod(0555, $dat);
	&DispError2($GB,"ＥＲＲＯＲ！", "ＥＲＲＯＲ：このスレッドには書き込めません。緊急緊急緊急!!");

	return 0;
}
#############################################################################
# 1000超えの処理をする
# 入力、$GB, datファイル名
# ここでdatはchmod 555されて、書けなくなる
#############################################################################
sub Over1000
{
	my ($GB, $dat) = @_;

	my $b1000 = "このスレッドは１０００を超えました。 <br> もう書けないので、新しいスレッドを立ててくださいです。。。 ";
#	my $p1000 = $GB->{PATH} . "1000.txt"	;
	my $r1000 = $GB->{NOWTIME} % 10		;	# ランダム1000.txt
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

	$lastdat = "１００１<><>Over 1000 Thread<> $b1000 <>\n";

	# 既に１００１が書いてあったら、書くのをやめる
	if ($GB->{DATLAST}[-1] ne $lastdat)
	{
		# １００１書き込み処理
		if(open(OUT,">>$dat"))
		{
			print OUT $lastdat;
			close(OUT);

			# $GBの処理
			# datの番号をひとつすすめる
			++$GB->{DATNUM};
			# $GB->{DATLAST}をひとつ押し出す
			shift(@{$GB->{DATLAST}});
			push(@{$GB->{DATLAST}}, $lastdat);
		}
	}

	# datを書けなくする
	chmod(0555, $dat);

	return 0;
}
#############################################################################
# BBYに新スレの情報を伝える
#############################################################################
sub NotifyBBY
{
	my ($GB) = @_;

	my $AHOST;	# BBYへのDNSqueryホスト名指定用変数
	my $DNSbby;	# BBYのDNSサーバ指定用変数

	if($ENV{'SERVER_NAME'} =~ /bbspink\.com/)
	{# bbspink.comの場合
		$DNSbby = $FOX->{DNSSERVER}->{BBYP};
		$AHOST = "$GB->{NEWTHREAD}.$GB->{FORM}->{'bbs'}.$ENV{'SERVER_NAME'}.bby.bbspink.com.";
	}
	else
	{# 2chの場合
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
# BBSに書き込みの情報を伝える
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
	#&DispError2($GB,"FOX ★","<font color=green>FOX ★</font> ($aaa)");

	return 0;
}
#############################################################################
# ファイルのリネームを行う
# 入力: $src、$dst
# 戻り値: 0またはエラーメッセージ
#############################################################################
sub TryRename
{
	my ($src, $dst) = @_;
	my $status = undef;
	my $count = 1000;

	# renameを試行してみる
	for (1..$count)
	{
		rename($src, $dst) and return 0;
	}
	# ステータスを保存する
	$status = $!;

	unlink($src);
	return $status;
}
#######################################################################
# subject.txtを更新する
# これを呼ぶことにより、@{$GB->{NEWSUB}} にsubject.txtが取り込まれる
# $GB->{SUBLINE} もここで準備される
# $GB->{FILENUM} にはここでsubject.txtの行数が入るようだ
#######################################################################
sub UpdateSubject
{
	my ($GB) = @_;
	my @newsub = ();	# ここの @newsub はローカル変数(封じ込め)

	#サブジェクトパス
	my $subject = $GB->{PATH} . "subject.txt";
	my $rnd = int(rand(99999));
	my $subtemp = $GB->{PATH} . $rnd . $GB->{FORM}->{'time'} . ".tmp";
	my $keyfile = $GB->{FORM}->{'key'} . ".dat";

	#subject.txt取り込み用
	my (@SUBJ1, @SUBJ2);

	#スレタイ抽出用
	my $dat1 = "";
	my $title = "";

	#subject.txt生成・並び替え用
	my ($i, $subtm);

	{
		# slurp mode; ファイルは単一文字列に全部読み込み
		local $/;
		#サブジェクトファイルを読み込む
		open(SUBR, $subject);		#SUBJECTを開く
		$subtm = <SUBR>;		#内容を全て読み込む
		close(SUBR);			#閉じる
	}

	# $SUBJ2[0] が $keyfile のスレになるように
	# ない場合は @SUBJ1 に全部入れる
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

	#$GB->{SUBLINE} を準備する
	#datの1行目の要素からスレタイを得る
	$dat1 = $GB->{DAT1};
	#改行カット
	chomp($dat1);
	#1つ目の要素を加工する
	$title = (split(/<>/, $dat1))[4];
	#それを最初の$GB->{SUBLINE}として使用する
	$GB->{SUBLINE} = "$title ($GB->{DATNUM})\n";

	if($GB->{NEWTHREAD})
	{
		#新スレの場合、一番上にのっける
		$subtm = "$keyfile<>$GB->{FORM}->{'subject'} (1)\n";
		# @SUBJ2 は空のはずだが念のため
		@newsub = ($subtm, @SUBJ1, @SUBJ2);
		++$GB->{FILENUM};
	}
	else
	{
		if($GB->{FORM}->{'mail'} =~ /sage/)
		{
			### sageの場合の処理 ###
			$SUBJ2[0] = "$keyfile<>$GB->{SUBLINE}";
			@newsub = (@SUBJ1, @SUBJ2);
		}
		else
		{
			### 通常の場合の処理 ###
			shift @SUBJ2;
			$subtm = "$keyfile<>$GB->{SUBLINE}";
			@newsub = ($subtm, @SUBJ1, @SUBJ2);
		}
	}

	# subject.txt への実際の書き込み処理
	if(@newsub)
	{
		#SUBJECTに書き込む
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

	# @{$GB->{NEWSUB}} に処理結果を代入
	@{$GB->{NEWSUB}} = @newsub;

	return 0;
}
#######################################################################
# subback.htmlを更新する
# UpdateSubjectの後で呼ぶこと
#######################################################################
sub UpdateSubback
{
	my ($GB) = @_;

	my $sub = $GB->{PATH} . "subback.html";

	$GB->{base} = "http://$ENV{'SERVER_NAME'}$ENV{'SCRIPT_NAME'}";
	$GB->{base} =~ s/[^\/]*\.cgi/read\.cgi\/$GB->{FORM}->{'bbs'}\//;

	open(HED,">$sub");
	#flock(HED,2);

	# subbackのHTMLヘッダ部分1
	my @subbackhead1 = (
	qq|<html lang="ja">|,
	qq|<head>|,
	qq|<title>$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE'}＠スレッド一覧</title>|,
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

	# subbackの中身部分
	my $i = 0;
	foreach(@{$GB->{NEWSUB}})
	{
		chomp;
		++$i;
		/^(\w+)\.dat<>(.*)/;
		my ($key, $value) = ($1, $2);
		&Put1Line(*HED, "<a href=\"$key/l50\">$i: $value</a>\n");
	}

	# subbackのおしりの部分
	my @subbackfoot = (
	qq|</small></div><div class="right"><small>|,
	qq|<a href="javascript:changeSubbackStyle();" target="_self" class="js">表\示スタイル切替</a>&nbsp;\n|,
	&IsReadHtml($GB) ? qq|<a href="javascript:switchReadJsMode();" target="_self" class="js">read.cgi モード切替</a>&nbsp;\n| : qq||,
	qq|<a href="../../../$GB->{FORM}->{'bbs'}/kako/"><b>過去ログ倉庫はこちら</b></a></small></div>\n|,
	qq|</body>|,
	qq|</html>|
	);
	&PutLines(*HED, @subbackfoot);
	#flock(HED,8);
	close(HED);

	return 0;
}
#######################################################################
# 板トップ(index.html)を作る
# UpdateSubjectの後で呼ぶこと
#######################################################################
sub MakeIndex4PC
{
	my ($GB) = @_;

	my $rnd = int(rand(99999));
	my $INDEXtemp = $GB->{PATH} . $rnd . $GB->{FORM}->{'time'} . ".tmps";

	#open(HTM,">$GB->{INDEXFILE}");
	open(HTM,">$INDEXtemp");

	#--------まずヘッダだよん
	my @index_header1 = (
	qq|<html lang="ja">|,
	qq|<head>|,
	qq|<meta http-equiv="Content-Type" content="text/html; charset=shift_jis">|,
	#クッキーを処理するための JavaScript
	qq|<script type="text/javascript" src="http://www2.2ch.net/snow/index.js" defer></script>|,
	);
	&PutLines(*HTM, @index_header1);
	# JavaScript 版だけ(とりあえず)
	if(&IsReadHtml($GB))
	{
		# BE 関連 JavaScript
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

	#テーマソング
	#if($FOX->{$GB->{FORM}->{bbs}}->{BBS_BG_SOUND})
	#{
	#	&Put1Line(*HTM, "<bgsound src=\"$FOX->{$GB->{FORM}->{bbs}}->{BBS_BG_SOUND}\" autostart=\"true\">");
	#}

	#--------タイトル画像
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

	#--------掲示板タイトル
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
	&IsReadHtml($GB) ? qq|<a href="javascript:switchReadJsMode();" style="background-color:dimgray;border:1px outset dimgray;color:palegreen;text-decoration:none;">read.cgi モード切替</a>&nbsp; | : qq||,
	qq|<a href=#menu>■</a>|,
	qq|<a href=#1>▼</a>|,
	qq|</td>|,
	qq|</tr>|,
	qq|<tr>|,
	qq|<td colspan=3>|
	);
	&PutLines(*HTM, @index_title1);

	# 「BBxが止まっています」表示
	if(!$FOX->{BBM}) { &Put1Line(*HTM, "<font color=red size=+2>BBM が止まっています</font><br>\n"); }
	if(!$FOX->{BBM2}) { &Put1Line(*HTM, "<font color=red size=+2>BBM2 が止まっています</font><br>\n"); }
	if(!$FOX->{BBQ}) { &Put1Line(*HTM, "<font color=red size=+2>BBQ が止まっています</font><br>\n"); }
	if(!$FOX->{BBX}) { &Put1Line(*HTM, "<font color=red size=+2>BBX が止まっています</font><br>\n"); }
	if(!$FOX->{BBN}) { &Put1Line(*HTM, "<font color=red size=+2>BBN が止まっています</font><br>\n"); }
	if(!$FOX->{BBY}) { &Put1Line(*HTM, "<font color=red size=+2>BBY が止まっています</font><br>\n"); }
	if(!$FOX->{BBS}) { &Put1Line(*HTM, "<font color=red size=+2>BBS が止まっています</font><br>\n"); }
	if(!$FOX->{BBR}) { &Put1Line(*HTM, "<font color=red size=+2>BBR が止まっています</font><br>\n"); }
	if(!$FOX->{BBE}) { &Put1Line(*HTM, "<font color=red size=+2>BBE が止まっています</font><br>\n"); }

	#--------カスタムフラッシュ（flash.txt）
	my $CUSTOM_FLASH_HTML =  "./flash.txt";
	if(open(READ, $CUSTOM_FLASH_HTML))
	{
		local $/;
		&Put1Line(*HTM, <READ>);
		close(READ);
	}

	#--------カスタムヘッダ(ローカルルール)（head.txt）
	my $CUSTOM_HEAD_HTML = $GB->{PATH} . "head.txt";
	if(open(READ, $CUSTOM_HEAD_HTML))
	{
		local $/;
		#&Put1Line(*HTM, "<center><font size=+2><b>避難訓練実施中。。。<a href=\"http://yy12.kakiko.com/emg2ch/\">避難所</a></b></font></center><p>");
		&Put1Line(*HTM, <READ>);
		close(READ);
	}

	#--------新規スレッド
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
		qq|<b><a href=http://info.2ch.net/before.html>書き込む前に読んでね</a> ｜ |,
		qq|<a href=http://info.2ch.net/guide/>２ちゃんねるガイド</a>|,
		qq|$FOX->{specialad} \| |,
		qq|<a href=\"http://info.2ch.net/guide/faq.html\">ＦＡＱ</a></b>|
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
		qq|<b><a href=http://info.2ch.net/before.html>書き込む前に読んでね</a> ｜ |,
		qq|<a href=http://info.2ch.net/guide/>２ちゃんねるガイド</a> \| |,
		qq|<a href=\"http://info.2ch.net/guide/faq.html\">ＦＡＱ</a>|,
		qq|$FOX->{specialad}</b>|
		);
		&PutLines(*HTM, @index_title2);
	}

	#--------説明やページリンク
	# pageview.cgiは廃止されている
	#use integer;
	#my $lp = $GB->{FILENUM} / $FOX->{$GB->{FORM}->{bbs}}->{"BBS_THREAD_NUMBER"};
	#if($GB->{FILENUM} != $lp * $FOX->{$GB->{FORM}->{bbs}}->{"BBS_THREAD_NUMBER"})
	#{
	#	$lp++;
	#}
	#if($lp > 1)
	#{
	#	&Put1Line(*HTM, "<a href=\"../test/pageview.cgi?page=$lp&bbs=$GB->{FORM}->{'bbs'}\">最後のページ</a>");
	#}
	#if($GB->{FILENUM} > $FOX->{$GB->{FORM}->{bbs}}->{"BBS_THREAD_NUMBER"})
	#{
	#	&Put1Line(*HTM, "　<a href=\"../test/pageview.cgi?page=2&bbs=$GB->{FORM}->{'bbs'}\">次のページ</a>");
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

	#--------広告欄
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

	#スレッド吐き出し用にファイル数を調整
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

	#--------スレッド一覧
	my @index_list = (
	qq|<a name="menu"></a>|,
	qq|<table border=1 cellspacing=7 cellpadding=3 width=95% bgcolor="$FOX->{$GB->{FORM}->{bbs}}->{"BBS_MENU_COLOR"}"align=center>|,
	qq|<tr>|,
	qq|<td>|,
	qq|<font size=2>|
	);
	&PutLines(*HTM, @index_list);

	#スレッド一覧を吐き出す
	# 最初の$menumin個分
	for(my $SubCount = 1; $SubCount <= $menumin; $SubCount++)
	{
		my $file = @{$GB->{NEWSUB}}[$SubCount-1];
		chomp($file);
		$file =~ /^(\w+)\.dat<>(.*)/;
		my ($key, $value) = ($1, $2);
		# ここでは無理してhtmlを作らない(本当に必要になる直前まで保留)
		#unless(-e "$GB->{TEMPPATH}$key.html")
		#{
		#	&MakeWorkFile($GB, $key);
		#}
		&Put1Line(*HTM, "<a href=\"../test/read.cgi/$GB->{FORM}->{'bbs'}/$key/l50\" target=\"body\">$SubCount:</a> <a href=\"#$SubCount\">$value</a>　");
	}
	# それ以降
	for(my $SubCount = $menumin + 1; $SubCount <= $menumax; $SubCount++)
	{
		my $file = @{$GB->{NEWSUB}}[$SubCount-1];
		chomp($file);
		$file =~ /^(\w+)\.dat<>(.*)/;
		my ($key, $value) = ($1, $2);
		&Put1Line(*HTM, "<a href=\"../test/read.cgi/$GB->{FORM}->{'bbs'}/$key/l50\" target=\"body\">$SubCount: $value</a>　");
	}
	# スレッド一覧(subback.html)へのリンク
	&Put1Line(*HTM, "<div align=\"right\"><a href=\"subback.html\"><b>スレッド一覧はこちら</b></a></font></td></tr></table>");

	#--------広告欄(夜勤さんのスペース)
	# XXX 実体は bbs-yakin.cgi の中にある
	# このサブルーチン中でファイルハンドルを「HTM」だと
	# 思い切り決め打っているので要注意
	# いずれは引数で渡すようにした方がいいと思う -- 11/22/2005 by む

	# IPv6.2ch.netはmaido3のサーバではないので、広告は出さない
	if($ENV{SERVER_NAME} ne "ipv6.2ch.net")
	{
		&YakinCounterCode($GB->{FORM}->{bbs});
	}

	#--------スレッドを吐き出す
	my $front = $menumin;
	my $next = 2;
	for(my $ancnum = 1; $ancnum <= $menumin; $ancnum++)
	{
		my $file = @{$GB->{NEWSUB}}[$ancnum-1];
		$file =~ /^(\w+)\.dat/;
		my ($key) = ($1);
		my @log = ();
		my $count = 0;#	繰り返しカウント
		
		# subject.txtにあるのに、十分にhtmlが成長してなかったら
		# もう1回試してみる、というのを、100回ぐらいやってみる
		# (いいかげんなことは100も承知だが、neet4vipで結構うまくいった)
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
		# それでもだめだったら、しょうがないからMakeWorkFileして、
		# それを読み直す
		if($count == 101)
		{
			&MakeWorkFile($GB, $key);
			open(IN, "$GB->{TEMPPATH}$key.html");
			@log = <IN>;
			close(IN);
		}
		# スレの最初のところ
		my $first = shift(@log);
		$first =~ s/\$ANCOR/$ancnum/g;
		$first =~ s/\$FRONT/$front/g;
		$first =~ s/\$NEXT/$next/g;
		&Put1Line(*HTM, "\n" . $first);
		# スレのhtml本体
		&PutLines(*HTM, @log);
		# おしりにくっつける入力フォーム
		my @index_surefoot = (
		qq|<dd>|,
		qq|<form method=POST action="../test/bbs.cgi?guid=ON">|,
		qq|<input type=hidden name=bbs value=$GB->{FORM}->{'bbs'}>|,
		qq|<input type=hidden name=key value=$key>|,
		qq|<input type=hidden name=time value=$GB->{NOWTIME}>|,
		qq|<input type=submit value="書き込む" name="submit">|,
		qq| 名前：	|,
		qq|<input type=text name=FROM size=19>|,
		qq| E-mail：|,
		qq|<input type=text name=mail size=19>|,
		qq|<ul>|,
		qq|<textarea rows=5 cols=64 wrap=OFF name=MESSAGE></textarea><br>|,
		qq|<b>|,
		qq|<a href="../test/read.cgi/$GB->{FORM}->{'bbs'}/$key/">全部読む</a> |,
		qq|<a href="../test/read.cgi/$GB->{FORM}->{'bbs'}/$key/l50">最新50</a> |,
		qq|<a href="../test/read.cgi/$GB->{FORM}->{'bbs'}/$key/-100">1-100</a> |,
		#qq|<a href="http://info.2ch.net/test/tb.cgi?__mode=list&tb_id=http://$ENV{'SERVER_NAME'}/test/read.cgi/$GB->{FORM}->{'bbs'}/$key">関連ページ</a> |,
		qq|<a href="#menu">板のトップ</a> <a href="$GB->{PATH}./index.html">リロード</a>|,
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

	#--------フッターで閉めるよん
	&Put1Line(*HTM, "<center>");
	# pageview.cgiは廃止されている
	#if($menumin < $menumax)
	#{
	#	&Put1Line(*HTM, "<a href=\"../test/pageview.cgi?page=2&bbs=$GB->{FORM}->{'bbs'}\"><font size=5><b>次のページ</b></font></a>");
	#}

	#--------新規スレッド作成のところ
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
		qq|<br><input type=submit value="新規スレッド作成画面へ" name=submit>|,
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
		qq|タイトル：|,
		qq|<input type=text name=subject size=40>|,
		qq|<input type=submit value="新規スレッド作成" name=submit><br>|,
		qq|名前：|,
		qq|<input type=text name=FROM size=19>|,
		qq| E-mail：|,
		qq|<input type=text name=mail size=19><br>|,
		qq|内容：|,
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

	# 広告(footad)とちゃっかりカウンター
	# どのような形の削除依頼であれ、、、
	# バージョン(と広告)
	my $foot = $FOX->{footad} . "<a href=http://count.2ch.net/?$GB->{FORM}->{'bbs'}><img src=http://count.2ch.net/ct.php/$GB->{FORM}->{'bbs'}  BORDER=0></a><br><b>どのような形の削除依頼であれ公開させていただきます</b><br>";
	&Put1Line(*HTM, "<br><br>$foot</center><br>");

	# 最後の部分
	&Put1Line(*HTM, "$GB->{version}");
	&Put1Line(*HTM, "<br>" . $FOX->{lastad});

	# おしまい
	&Put1Line(*HTM, "</body></html>");

	#flock(HTM,8);
	close(HTM);

	&TryRename($INDEXtemp, $GB->{INDEXFILE});

	return 0;
}
#############################################################################
# 書き込みましたを表示し、正常終了する。
#############################################################################
sub endhtml
{
	my ($GB) = @_	;

	# スレッド924のエラー処理はここでする(最後の最後)
	# 最強キャップでは、924にもレス可能
	if($GB->{FORM}->{'key'} =~ /^924/ && !$GB->{STRONGCAP})
	{
		&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：このスレッドには書き込めません。");
	}

	if($GB->{TBACK})	{&TBacksuperEnd;}

	# はなもげらクッキー(投稿完了した場合のみ送るクッキー)を送る
	if(($GB->{COOKIES}{$GB->{PIN1}} || '') ne $GB->{PIN2})
	{
		# クッキーはトラックバックでない時だけ送る
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
<title>書きこみました。</title>
<meta http-equiv="Content-Type" content="text/html; charset=shift_jis">
<meta name="viewport" content="width=device-width,initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.6,user-scalable=yes" />
</head>
<body>書きこみが終わりました。(iPhone)<br><br>
自分で戻ってちょ。<br><br>
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
<title>書きこみました。</title>
<meta http-equiv="Content-Type" content="text/html; charset=shift_jis">
<meta content=5;URL=$GB->{INDEXFILE} http-equiv=refresh>
</head>
<body>書きこみが終わりました。<br><br>
画面を切り替えるまでしばらくお待ち下さい。<br><br>
<br><br><br><br><br>
<center>
</center>
</body>
</html>
EOF
}

#<img width=160 height=120 src="http://www2.2ch.net/img/Hello-502index.gif" border=1 alt="Hello 502">
	#<br><br>$FOX->{putad}
	#おしまーい!!
	exit;
}
#############################################################################
#　新規スレッド別画面
#############################################################################
sub newbbs
{
	my ($GB) = @_;
	print "Content-type: text/html; charset=shift_jis\n\n";

	my @newbbshtml1 = (
	qq|<html lang="ja">|,
	qq|<head>|,
	qq|<meta http-equiv="Content-Type" content="text/html; charset=x-sjis">|,
	#クッキーを処理するための JavaScript
	qq|<script type="text/javascript" src="http://www2.2ch.net/snow/index.js" defer></script>|,
	qq|<title>$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE'}</title>|,
	qq|</head>|,
	qq|<body text="$FOX->{$GB->{FORM}->{bbs}}->{"BBS_TEXT_COLOR"}" BGCOLOR="$FOX->{$GB->{FORM}->{bbs}}->{"BBS_BG_COLOR"}" link="$FOX->{$GB->{FORM}->{bbs}}->{"BBS_LINK_COLOR"}" alink="$FOX->{$GB->{FORM}->{bbs}}->{"BBS_ALINK_COLOR"}" vlink="$FOX->{$GB->{FORM}->{bbs}}->{"BBS_VLINK_COLOR"}" background="$FOX->{$GB->{FORM}->{bbs}}->{"BBS_BG_PICTURE"}">|
	);
	print @newbbshtml1;

	#--------タイトル画像
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

	#--------掲示板タイトル
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

	#--------カスタムヘッダ(ローカルルール)（head.txt）
	my $CUSTOM_HEAD_HTML = "$GB->{PATH}head.txt";
	if(open(READ, $CUSTOM_HEAD_HTML))
	{
		local $/;
		print <READ>;
		close(READ);
	}

	#--------新規スレッド
	my @newbbshtml3 = (
	qq|<br>|,
	qq|</td>|,
	qq|</tr>|,
	qq|<tr>|,
	qq|<td nowrap align="right">|,
	qq|タイトル：|,
	qq|</td>|,
	qq|<td>|,
	qq|<input type="text" name="subject" size="40">|,
	qq|</td>|,
	qq|<td>|,
	qq|<input type=submit value="新規スレッド作成" name="submit">|,
	qq|</td>|,
	qq|</tr>|,
	qq|<tr>|,
	qq|<td nowrap align="right">|,
	qq|名前：|,
	qq|</td>|,
	qq|<td nowrap colspan="2">|,
	qq|<input type=text name=FROM size=19> E-mail：|,
	qq|<input type=text name=mail size=19>|,
	qq|</td>|,
	qq|</tr><tr>|,
	qq|<td nowrap align="right" valign="top">|,
	qq|内容：|,
	qq|</td>|,
	qq|<td colspan="3">|,
	qq|<textarea rows=5 cols=60 wrap=OFF name=MESSAGE></textarea>|,
	qq|<input type=hidden name=bbs value=$GB->{FORM}->{'bbs'}>|,
	qq|<input type=hidden name=time value=$GB->{NOWTIME}>|,
	qq|</td>|,
	qq|</tr>|,
	qq|</table>|,
	qq|<b><a href="http://info.2ch.net/before.html">書き込む前に読んでね</a> ｜ <a href="http://info.2ch.net/guide/">２ちゃんねるガイド</a>$FOX->{specialad}</b><br><br>|,
	qq|</form>|,
	qq|</td>|,
	qq|</tr>|,
	qq|</table><br>|,
	qq|</body>|,
	qq|</html>|
	);
	print @newbbshtml3;

	# 画面を表示したらexit
	exit;
}
#############################################################################
#　新規スレッドブロック
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
#<font size=+1 color=#FF0000>書き込み確認。</font><br><br>
#書き込みに関して様々なログ情報が記録されています。<br>
#公序良俗に反したり、他人に迷惑をかける書き込みは控えて下さい<br>
#	<form method=POST action="../test/subbbs.cgi">
#	タイトル：$GB->{FORM}->{'subject'}
#		<input type="hidden" name="subject" value="$sbj" size="40"><br>
#	名前：$GB->{FORM}->{'FROM'}
#		<INPUT TYPE=hidden NAME=FROM SIZE=19 value="$GB->{FORM}->{'FROM'}"><br>
#	E-mail ： $GB->{FORM}->{'mail'}
#		<INPUT TYPE=hidden NAME=mail SIZE=19 value="$GB->{FORM}->{'mail'}"><br>
#	内容：<ul>$GB->{FORM}->{'MESSAGE'}
#		<input type=hidden name=MESSAGE value="$msg"></ul>
#<br>
#<input type=hidden name=bbs value=$GB->{FORM}->{'bbs'}>
#<input type=hidden name=time value=$GB->{NOWTIME}>
#<input type=submit value="全責任を負うことを承諾して書き込む" name="submit"><br>
#</form>
#変更する場合は戻るボタンで戻って書き直して下さい。<br>
#
#EOF
#	exit;
#}
#############################################################################
#index.html作成用ファイルを作成
# 引数: $GB, 対象となるdatのキー$key
# $keyと$GB->{FORM}->{'key'}が同じだった場合、GetDatInfoで読んだものを使い回す
#############################################################################
sub MakeWorkFile
{
	my ($GB, $key) = @_;
	my $workfile = $GB->{TEMPPATH} . $key . ".html";
	my (@messx, @content);
	my ($mailto, $time, $brmax, $topnum, $firstlog, $name, $mail, $subject, $message);
	my $datnum = 0;	# そのdatの行数
	# 対象となるdatに対し、MakeWorkFile内で$GBのように使える変数
	# $keyと$GB->{FORM}->{'key'}が違う時に使用する
	my $TMPGB = {};

$GB->{DEBUG} .= "IN MakeWorkFile($key) file=$workfile<br>";

	# 今処理中のdatとキーが違うかどうかを調べる
	if($GB->{FORM}->{'key'} != $key)
	{
		# キーが違った場合、必要な $TMPGB を準備する
		# GetDatInfo の前に、これらがセットされてないといけない
		$TMPGB->{NEWTHREAD} = 0;
		$TMPGB->{DATPATH} = $GB->{DATPATH};
		$TMPGB->{FORM}->{bbs} = $GB->{FORM}->{bbs};
		$TMPGB->{DAT1} = "";
		$TMPGB->{DATNUM} = 0;
		$TMPGB->{DATLAST} = ();

		# $TMPGB に dat の情報を読み込む
		&GetDatInfo($TMPGB, $key);

		# 取ってきた値をセットする
		$firstlog = $TMPGB->{DAT1};
		$datnum = $TMPGB->{DATNUM};
		@content = @{$TMPGB->{DATLAST}};
	}
	else
	{
		# キーが同じ場合、既にあるものをセットする
		$firstlog = $GB->{DAT1};
		$datnum = $GB->{DATNUM};
		@content = @{$GB->{DATLAST}};
	}

	# 上記処理により、
	#  $firstlogにdatの>>1の要素
	#  $datnumに該当するdatの行数
	#  @contentに該当するdatの最新レス数
	# が得られる

	#改行カット
	chomp($firstlog);

	#>>1の要素を加工する
	($name,$mail,$time,$message,$subject) = split(/<>/,$firstlog);

$GB->{DEBUG} .= "MakeWorkFile($key) file=$workfile<br>";
	open(SHTM,">$workfile");	#ログテンポラリを開く
#	flock(SHTM,2);

	#サブジェクトテーブル(スレタイのアンカーのところ)を吐き出す
	my @subjecttable = (
	qq|<table border=1 cellspacing=7 cellpadding=3 width=95% bgcolor="$FOX->{$GB->{FORM}->{bbs}}->{"BBS_THREAD_COLOR"}" align=center>|,
	qq|<tr>|,
	qq|<td>|,
	qq|<dl class="thread">|,
	qq|<a name="\$ANCOR"></a>|,
	qq|<div align="right"><a href ="#menu">■</a>|,
	qq|<a href="#\$FRONT">▲</a>|,
	qq|<a href="#\$NEXT">▼</a>|,
	qq|</div>|,
	qq|<b>【\$ANCOR:$datnum】<font size=5 color="$FOX->{$GB->{FORM}->{bbs}}->{'BBS_SUBJECT_COLOR'}">$subject</font></b>|
	);
	&PutLines(*SHTM, @subjecttable);

	#>>1のハイパーリンク作成と吐き出し
	#-----------------------------------------------------------------------

	# http:// 等をハイパーリンクにする
	$message = &MakeHyperLink($GB, $message);

	# 名前欄のmailto:のリンクを処理する
	$mailto = &MakeMailto($GB, $mail, $name);

	#BE:のリンクを作る
	#$time =~ s/BE:(\d+)-([^ ]*)/<a href="javascript:be($1);">?$2<\/a>/;
	$time =~ s{BE:(\d+)-(.*)$}{<a href="javascript:be($1);">?$2</a>};

	#>>1を吐き出す
	&Put1Line(*SHTM, "<dt>1 名前：$mailto $time<dd>$message <br><br><br>");

	#最新BBS_CONTENTS_NUMBER個のレスのハイパーリンク作成と吐き出し
	#-----------------------------------------------------------------------

	#ログ数から、表示コンテンツをチェック
	if($datnum > $FOX->{$GB->{FORM}->{bbs}}->{"BBS_CONTENTS_NUMBER"})
	{
		$topnum = $datnum - ($FOX->{$GB->{FORM}->{bbs}}->{"BBS_CONTENTS_NUMBER"} - 1);
	}
	else
	{
		$topnum = 2;
	}

	# 最新レスを一つずつ処理
	foreach(@content)
	{
		chomp;	#改行をカット

		#要素を加工する
		($name,$mail,$time,$message,$subject) = split(/<>/);

		unless($_)
		{
			$topnum++;
			next;
		}

		# http:// 等をハイパーリンクにする
		$message = &MakeHyperLink($GB, $message);

		# 名前欄のmailto:のリンクを処理する
		$mailto = &MakeMailto($GB, $mail, $name);

		#BE:のリンクを作る
		#$time =~ s/BE:(\d+)-([^ ]*)/<a href="javascript:be($1);">?$2<\/a>/;
		$time =~ s{BE:(\d+)-(.*)$}{<a href="javascript:be($1);">?$2</a>};
		#吐き出す
		&Put1Line(*SHTM, "<dt>$topnum 名前：$mailto ：$time<dd>");

		#「省略されました」の処理
		my @messx = split(/<br>/,$message);	#メッセージを行でカット
		my $messy = @messx;			#行数を計算
		# BBS_LINE_NUMBERより多い、省略必要
		if($messy > $FOX->{$GB->{FORM}->{bbs}}->{"BBS_LINE_NUMBER"})
		{
			my $messz = join('<br>',@messx[0 .. $FOX->{$GB->{FORM}->{bbs}}->{'BBS_LINE_NUMBER'}-1]);
			&Put1Line(*SHTM, "$messz <br>");
			&Put1Line(*SHTM, "<font color=\"$FOX->{$GB->{FORM}->{bbs}}->{'BBS_NAME_COLOR'}\">（省略されました・・全てを読むには<a href=\"../test/read.cgi/$GB->{FORM}->{'bbs'}/$key/$topnum\" target=\"_blank\">ここ</a>を押してください）</font><br>");
		}
		# 省略不要
		else
		{
			my $messz = join('<br>',@messx[0 .. $messy-1]);
			&Put1Line(*SHTM, "$messz <br>");
		}

		$topnum++;
		# 最後に<br>を出力しておしまい
		&Put1Line(*SHTM, "<br>\n");
	}

	#-----------------------------------------------------------------------

#	flock(SHTM,8);
	close(SHTM);

	# パーミッション調整は不要
	#chmod(0666,$workfile);
}
#############################################################################
# 文字列内のURIを探して、ハイパーリンクにする
# 入力: $GB, $message
# 戻り値: 加工後の$message
#############################################################################
sub MakeHyperLink
{
	my ($GB, $message) = @_;

	#https/ftpは下記処理に関係なく直リン
	#https://とftp://の処理はSaborinフラグが立っていたらさぼる
	if(!$GB->{SABORIN})
	{
		$message =~ s/(https|ftp)\:\/\/([\w|\:\!\#\$\%\=\&\-\^\`\\\|\@\~\[\{\]\}\;\+\*\,\.\?\/]+)/<a href="$1:\/\/$2" target="_blank">$1:\/\/$2<\/a>/g;
	}
	#httpの場合
	if($message =~ /2ch\.net/ || $message =~ /bbspink\.com/)
	{
	
	#	$message =~ s/http\:\/\/img\.2ch\.net/sssp\:\/\/img\.2ch\.net/g;

		#2ch/bbspink内は直リン
		$message =~ s/http\:\/\/([\w|\:\!\#\$\%\=\&\-\^\`\\\|\@\~\[\{\]\}\;\+\*\,\.\?\/]+)/<a href="http:\/\/$1" target="_blank">http:\/\/$1<\/a>/g;
	}
	elsif($message =~ /maido3\.com/)
	{
		#maido3.comは直リン
		$message =~ s/http\:\/\/([\w|\:\!\#\$\%\=\&\-\^\`\\\|\@\~\[\{\]\}\;\+\*\,\.\?\/]+)/<a href="http:\/\/$1" target="_blank">http:\/\/$1<\/a>/g;
	}
	else
	{
		#外部リンク
		if($ENV{'SERVER_NAME'} =~ /bbspink\.com/)
		{
			#bbspinkはpinktower経由
			$message =~ s/http\:\/\/([\w|\:\!\#\$\%\=\&\-\^\`\\\|\@\~\[\{\]\}\;\+\*\,\.\?\/]+)/<a href="http:\/\/pinktower.com\/$1" target="_blank">http:\/\/$1<\/a>/g;
		}
		else
		{
			#2chはime.nu経由
			$message =~ s/http\:\/\/([\w|\:\!\#\$\%\=\&\-\^\`\\\|\@\~\[\{\]\}\;\+\*\,\.\?\/]+)/<a href="http:\/\/ime.nu\/$1" target="_blank">http:\/\/$1<\/a>/g;
		}
	}

	# ssspの処理(BEのアイコン)
	$message =~ s/sssp\:\/\/img\.2ch\.net\/([\w|\:\!\#\$\%\=\&\-\^\`\\\|\@\~\[\{\]\}\;\+\*\,\.\?\/]+)/<img src="http:\/\/img\.2ch\.net\/$1">/g;

	#$message =~ s/sssp/http/g;
			
	return $message;
}
#############################################################################
# 名前のところのmailto:リンクを作る
# 入力: $GB, $mail: メールアドレス, $name: 名前
# 戻り値: できた名前欄の文字列
#############################################################################
sub MakeMailto
{
	my ($GB, $mail, $name) = @_;
	my $mailto = "";

	#メール欄に入力がある場合、mailto:のリンクにする
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
# スレ立て規制チェック
# IN: なし
# OUT: 0 スルー 1 寄生虫
#############################################################################
sub Check_SURETATE
{
	my ($GB) = @_	;

	#以下の板はするー
	if(&KiseiOFF($GB))			{return 0;}
#	if($GB->{FORM}->{'bbs'} eq "campus")	{return 0;}

	# ●はスルー
		if(!$FOX->{$GB->{FORM}->{bbs}}->{"BBS_BE_TYPE2"} && $GB->{MARU})			{return 0;}

	# ★はスルー
	if($GB->{CAP})				{return 0;}

	#公式p2は以下の板スレ立て不可
	if($GB->{P22CH})
	{
		if($GB->{FORM}->{'bbs'} eq "slot")	{&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：この板はp2でのスレ立ては出来ないのだ。");}
	}

	# 株主優待
	#if($GB->{FORM}->{'bbs'} eq "news" || $GB->{FORM}->{'bbs'} eq "poverty")
	#{
	#	if(!$GB->{P22CH} && $GB->{KABUU} && $GB->{BEpoints} > 3000)	{return 0;}
	#}
	#else
	#{
	#	if(!$GB->{P22CH} && $GB->{KABUU})	{return 0;}
	#}

	# 以下、上記の優遇措置を受けない場合

	# Type2はbe必須
	if($FOX->{$GB->{FORM}->{bbs}}->{"BBS_BE_TYPE2"})
	{
		if(!$GB->{isBE})
		{
			&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：Beログインしてください(t)。<a href=\"http://be.2ch.net/\">be.2ch.net</a>");
		}
	}

#			$GB->{FORM}->{'MESSAGE'} = 'sssp://img.2ch.net/ico/' . $GB->{icon} .' <br>'. $GB->{FORM}->{'MESSAGE'} ;


	# Type2はBeポイントが足りないとスレ立て不可
	if($FOX->{$GB->{FORM}->{bbs}}->{"BBS_BE_TYPE2"})
	{
		# 1000 ポイント以上ないとだめ
		my $pointlimit = 1000;

		# news だけ 6000 ポイント
		if($GB->{FORM}->{'bbs'} eq 'news')	{$pointlimit = 18000;}
#		if($GB->{FORM}->{'bbs'} eq "poverty")	{$pointlimit =  3000;}

		if($GB->{BEpoints} < $pointlimit)
		{
			&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：Beポイントが足りません。($pointlimit)");
		}
	}


	# Type2はポイント特典対象者は無条件にスレ立て可能
	#とりあえず、全板にしてみるの巻。
	if($FOX->{$GB->{FORM}->{bbs}}->{"BBS_BE_TYPE2"})
	{
		# news だけ
		if($GB->{FORM}->{'bbs'} eq 'news')
		{
			# BE「ブラックリスト」にない場合にのみ特典を利用可能
			if(!&Check_BEBlack($GB))
			{
				if($GB->{BELucky})		{return 0;}
			}
		}
	}

	# リモホないのはスレ立て不可
	my $remo = $GB->{HOST29}	; #いわゆるリモホ
	my $ipip = $ENV{REMOTE_ADDR}	;
	if($remo eq $ipip)	{&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：スレ立ては●を使うと出来ますよ。");}

	# 携帯と公式p2では、種を記録する
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
		# 上64bitにする、将来的には48bit( >> 80 )でもいいかも
		$IP_number = $IP_number >> 64;
	}
	else
	{
		# IP アドレスから数字を取得(・∀・)ニヤニヤ 65025 通り
#		$IP_number = eval { $ENV{REMOTE_ADDR} =~ s/^(\d+)\.(\d+)/return $1 * $2/e };
#		$IP_number = eval { $ENV{REMOTE_ADDR} =~ s/^(\d+)\.(\d+)/return $2/e };
		$IP_number = eval { $ENV{REMOTE_ADDR} =~ s/^(\d+)\.(\d+)/return ($1 % 4) * 256 + $2/e };
	}

	my $ripfile = "$GB->{WPATH}RIP.cgi";

	# リスト豆乳用バッファみたいなの。
	my @diff_list = ();
	push @diff_list, sprintf qq|%s,%s,%d\n|, $IP_number, $kiroku, $GB->{FORM}->{key};

	# 雪だるまではbbsdに問い合わせる
	if(IsSnowmanServer)
	{
		my $cmd = 'chkthr';
		my $rcode = bbsd($GB->{FORM}->{bbs}, $cmd, 'RIP.cgi', $IP_number, $kiroku, 'dummy');
		# タイムアウトかどうかチェック
		if(&bbsd_TimeoutCheck($GB, $rcode))
		{
			&bbsd_TimeoutError($GB, $cmd);
		}
		# あったら(空文字列以外)、だめ
		if($rcode ne '')
		{
			return 1;
		}
	}
	# 通常サーバではリストを読んでマッチングする
	else
	{
		# スレ立て規制リスト読み込み
		local *Deny_list;
		open   Deny_list, '<', $ripfile; # $ripfile はグローバル扱い
		my @Deny = <Deny_list>;
		close Deny_list;
	
		# IP アドレスで処理
		# リストから検索。存在すれば 1 を返してばいばい。
		foreach (@Deny){
			return 1 if $IP_number == (split /,/)[0];
		}
	
		# スルーなのでスレ立て規制リストに登録
		if (@diff_list) {
			unshift @Deny, @diff_list;
			splice  @Deny, $FOX->{$GB->{FORM}->{bbs}}->{'BBS_THREAD_TATESUGI'};
	
			# スレ立て規制リストの更新
			open  Deny_list, '>', "$ripfile.tmp"; # 一時ファイルに書き出し
			print Deny_list @Deny;
			close Deny_list;
			&TryRename("$ripfile.tmp", $ripfile); # ファイル名を元に戻す
		}
	}

	return 0; # スルー判定
}
#############################################################################
# BE の情報をブラックリストに登録する
# 引数: ブラックリストのファイル名、登録情報
# 戻り値: 0: 登録完了、1: 何かおかしい
#############################################################################
sub Record_BEBlack
{
	my ($recordfile, $dmdm) = @_;

	# 雪だるまサーバでは何もしない(参照時に登録されるため)
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
# BE の「ブラックリスト」情報への登録・チェック
# 雪だるまでは、bbsd のDBに記録する
# 引数: $GB
# 戻り値: 0: 登録なし、1: ブラックリスト登録あり
#############################################################################
sub Check_BEBlack
{
	my ($GB) = @_;
	my $dmdm = $GB->{FORM}->{'DMDM'};	# email address
	my $recordfile = "./book/.RIP_BE.cgi";
	my @badbe = ();
	my $match = 0;

	# ポイント特典の時は記録しない
	if($GB->{BELucky})		{return 0;}

	# 雪だるまではない時だけ
	# 雪だるまの時は、この下のルックアップで新規登録される
	if(!IsSnowmanServer)
	{
		# ファイルがない時、記録して戻り
		if(!(-e $recordfile))
		{
			&Record_BEBlack($recordfile, $dmdm);
			return 0;
		}
	}

	# ファイルがある時、中身をマッチングする
	# 雪だるまではbbsdに問い合わせる
	if(IsSnowmanServer)
	{
		my $errmsg = "";
		my $statnum = 0;
		my $cmd = 'chkid';
		$errmsg = bbsd_db($GB->{FORM}->{'bbs'}, $cmd, 'beblack', $dmdm, 3600, 1, 1, 'dummy');
		# タイムアウトかどうかチェック
		# タイムアウトだったらスルー扱い
		if(&bbsd_TimeoutCheck($GB, $errmsg))
		{
			return 0;
		}

		# 結果を切り出し
		$statnum = (split(/,/, $errmsg))[0];

		# 登録があったらアウト
		if($statnum != 0)	{return 1;}
		# 登録がなければスルー判定
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

	# マッチした場合
	if($match)			{return 1;}

	# マッチしない場合、単に記録しておしまい
	&Record_BEBlack($recordfile, $dmdm);
	return 0;
}
#############################################################################
# スレ立てスピードチェック 0: ok 1:スピード違反
#############################################################################
sub Check_Speed
{
	my ($GB) = @_		;

return 0;
#撤廃してみた

	#雪だるまはスルー(bbsdへのAPI使って実装できると思うけど、今はしない)
	if(IsSnowmanServer)		{return 0;}
	# news4vipとnews以外はスルー
	#if($GB->{FORM}->{'bbs'} ne 'news4vip'
	#&& $GB->{FORM}->{'bbs'} ne 'news')	{return 0;}
	# 管理人の指令によりnews4vipののんびり解除 -- 2005/11/18 by む
	if($GB->{FORM}->{'bbs'} ne 'news')	{return 0;}
	#★はスルー
	if($GB->{CAP})				{return 0;}

	#●はスルー
	if($GB->{MARU})				{return 0;}

	my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($GB->{NOWTIME});
	if($min < 3)	{return 1;}	# 毎時三分まではスレ立て不可

	my $vaio = "./book/.A_B_C.cgi";
	if(!(-e $vaio))			# 初めてのスレ立て
	{
		open(YAN1,">>$vaio");print YAN1 "1";close(YAN1);
		return 0;
	}

	my $prmtime = (local $_=stat($vaio)) ? $_->mtime : 0;
	my $keika = $GB->{NOWTIME} - $prmtime	;
	$keika /= 60			;	# 分にする
	# 管理人の指示によりコメントアウト -- 2005/11/15 by む
	#if($GB->{FORM}->{'bbs'} ne 'news')
	#{
	#	if($keika < 15)	{return 1;}	# N分間はだめ
	#}
	if($keika < 1)	{return 1;}		# N分間はだめ

	open(YAN1,">>$vaio");print YAN1 "1";close(YAN1);

	return 0; # スルー判定
}
#######################################################################
# 板のスレッド数が限界値を超えていないかチェックする
#######################################################################
sub mumumuThreadNumExceededCheck
{
	my ($GB) = @_;
	my $num = 0;
	my $exceed = 96;	#この数を超えるスレ数は禁止
	my @dir;

	#●はスルー
	if($GB->{MARU})			{ return 0; }

	#スレッド数を制限する板じゃない場合はスルー
	if(!&IsThreadLimitIta($GB))	{ return 0; }

	# livejupiterは192まで
	if($GB->{FORM}->{'bbs'} eq 'livejupiter') { $exceed = 192; }
	# livevenusは192まで
	if($GB->{FORM}->{'bbs'} eq 'livevenus')	{ $exceed = 192; }
	# eq/eqplusは128まで
	if($GB->{FORM}->{'bbs'} eq 'eq')	{ $exceed = 128; }
	if($GB->{FORM}->{'bbs'} eq 'eqplus')	{ $exceed = 128; }

	## 処理ここから ##

	# datの数を調べる
	# 雪だるまではbbsdに問い合わせる
	if (IsSnowmanServer)
	{
		my $cmd = 'getndats';
		$num = bbsd($GB->{FORM}->{'bbs'}, $cmd, 'dummy'); 
		# タイムアウトかどうかチェック
		if(&bbsd_TimeoutCheck($GB, $num))
		{
			&bbsd_TimeoutError($GB, $cmd);
		}
	}
	else
	{
		# datディレクトリを開く(だめなら-1)
		if (!opendir(DIR, $GB->{DATPATH}))	{ return -1; }

		# datディレクトリを読み込み、数を調べる
		@dir = readdir(DIR);
		closedir(DIR);

		# readdir() は、"." ".." も入るため、
		# 配列の最終添字から1を引いた値がdatの数となる
		$num = $#dir - 1;
	}

	#限界値を越える数のスレッドがあったら真
	if ($num > $exceed)	{return 1;}
	else			{return 0;}
}
#############################################################################
# /i/index.html を作成するかどうか
#############################################################################
sub MakeIndex4Keitai296
{
	if($ENV{'SERVER_NAME'} =~ /bbspink\.com/)	{return 1;}
	if($ENV{'SERVER_NAME'} =~ /qb/)			{return 1;}
	if($ENV{'SERVER_NAME'} =~ /dso/)		{return 1;}
	return 0;
}
#############################################################################
# /i/index.html を作成する
#############################################################################
sub MakeIndex4Keitai
{
	my ($GB) = @_;

	# qb系、dso、bbspink.com 以外のサーバでは /i/index.html を作らない
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
	################広告準備
	my $tag;

	my $adadf = "./docomo_ad.txt"	;
	if($ENV{'SERVER_NAME'} =~ /bbspink\.com/)
	{
		$adadf = "../HOHO-01.txt";
	}

	open(IMAD, $adadf);
	$tag = <IMAD>;
	close(IMAD);

	################広告準備
	#i-mode用テキストを開く

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

	# ヘッダ
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
		&Put1Line(*SUBW, "<a href=\"$UlaUrl\"> こちらでご覧ください。</a><br><br>");
		&Put1Line(*SUBW, "<br><br><br><br><br><br><br><br><br><br>");
		&Put1Line(*SUBW, "<br><br><br><br><br><br><br><br><br><br>");
	}
	# 広告とタイトル
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

	# 続き(次のページ、に相当)(p.iをリンク)
	&Put1Line(*SUBW, "<hr><a href=p.i/$GB->{FORM}->{'bbs'}/30>続き</a>");
	# フッタ
	&Put1Line(*SUBW, "<hr></body></html>"); #<hr>$IMAD
	
#	flock(SUBW,8);
	close(SUBW);
	#パーミッション調整は不要
	#chmod(0666, $imodeindex);
}
#############################################################################
# /i/index.html を作成する
#############################################################################
sub MakeIndex4KeitaiUla
{
	my ($GB) = @_;

	my $UlaUrl = "http://same.ula.cc/test/p.so/$ENV{'SERVER_NAME'}/$GB->{FORM}->{'bbs'}/";

	#i-mode用テキストを開く

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

	# ヘッダ
	my @imodeindexhead = (
	qq|<html lang="ja">|,
	qq|<head>|,
	qq|<base href=\"$ibase\">|,
	qq|<title>$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE'}</title>|,
	qq|</head><body>|
	);
	&PutLines(*SUBW, @imodeindexhead);

	&Put1Line(*SUBW, "<a href=\"$UlaUrl\">移転しました。</a></body></html>");

	# フッタ
	&Put1Line(*SUBW, "<hr></body></html>"); #<hr>$IMAD
	
#	flock(SUBW,8);
	close(SUBW);
	#パーミッション調整は不要
	#chmod(0666, $imodeindex);
}
#############################################################################
#
#############################################################################
sub Check_HardPosting
{	#連続カキコ

	my ($GB) = @_	;

	#新スレの場合スルー
	if($GB->{NEWTHREAD})			{return 0;}

	#以下の板はするー
	if(&KiseiOFF($GB))			{return 0;}
#	if($GB->{FORM}->{'bbs'} eq "campus")	{return 0;}
	#ex系の一部はするー
	if($ENV{'SERVER_NAME'} =~ /ex19/)	{return 0;}
	if($ENV{'SERVER_NAME'} =~ /ex21/)	{return 0;}
	if($ENV{'SERVER_NAME'} =~ /ex22/)	{return 0;}
	if($ENV{'SERVER_NAME'} =~ /news23/)	{return 0;}
	if($ENV{'SERVER_NAME'} =~ /atlanta/)	{return 0;}
	#★はスルー
	if($GB->{CAP})				{return 0;}
	#●はするー
	if($GB->{MARU})				{return 0;}
	#株主優待はスルー
	if($GB->{KABUU})				{return 0;}

	#BEログインしているとスルー(になってるけど、どうだろう)
	#if($GB->{isBE})			{return 0;}
	#公式p2はスルー
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

	# 雪だるまでは、bbsdに問い合わせる
	if(IsSnowmanServer)
	{
		my $cmd = 'chktimecount';
		my $messcount = bbsd_db($GB->{FORM}->{bbs}, $cmd, $tane, 'dummy'); 
		# タイムアウトかどうかチェック
		# タイムアウトなら、timecout/timecloseはスルー
		if(&bbsd_TimeoutCheck($GB, $messcount))
		{
			return 0;
		}
		# ひっかかった場合は、回数が返って来る
		if($messcount != 0)
		{
			&DispError2($GB, "ＥＲＲＯＲ！", "ＥＲＲＯＲ：連続投稿ですか？？ $messcount回");
		}
		else
		{
			return 0;
		}
	}
	# 通常サーバでは、青白黄色
	else
	{
		#連続書き込みチェック
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
			&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：連続投稿ですか？？ $messcount回");
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
		#以下の板はスルー
		if($GB->{FORM}->{'bbs'} eq "accuse")	{return 0;}
#		if($GB->{FORM}->{'bbs'} eq "goki")	{return 0;}
#		if($GB->{FORM}->{'bbs'} eq "campus")	{return 0;}
		#operateはするー
#		if($GB->{FORM}->{'bbs'} ne "operate")
#		{
			&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：ウィルス警報。。。<br>$GB->{IDNOTANE} は２ちゃんねるには書くことを遠慮してもらっています。");
#		}
		#焼かれマークをつける(が、今は上で全部エラーなのでどうせ出ない)
		if($GB->{BURNEDKEITAI})
		{
			$GB->{FORM}->{'FROM'} = ' </b>[†.i!]<b> ' . $GB->{FORM}->{'FROM'};
		}
	}
	return 0	;
}
#######################################################################
# 「良い携帯」かどうか調べる(BBM問い合わせ部)
#######################################################################
sub GoodKeitai
{
	my ($GB) = @_;
	my $career = "";
	my $newthread = "";
	my $idnotane = "";

	my $AHOST = "";
	my $SPAM = "";

	#以下の板はスルー
	if(&KiseiOFF($GB))			{return 0;}
#	if($GB->{FORM}->{'bbs'} eq "campus")	{return 1;}

	# 現在BBMありかどうかが、トップページでわかるように
	$GB->{version} .= " +BBM";

	#携帯以外はするー
	if(!($GB->{KEITAI} || $GB->{KEITAIBROWSER}))	{return 1;}

	#IDの種(固有番号)をDNSクエリ用に変換
	$idnotane = $GB->{IDNOTANE};
	$idnotane =~ s/\_/\-/g;
	# DoCoMoでは「小文字フラグ情報」を付加してからBBMを呼ぶ
	if(length($idnotane) eq 7 && ($GB->{KEITAI} || $GB->{KEITAIBROWSER}))
	{
		$idnotane = &MakeImodeIDforDNS($idnotane);
	}

	#携帯キャリアごとに変更
	if   ($GB->{KEITAI} eq 1)	{ $career = "docomo"; }
	elsif($GB->{KEITAI} eq 2)	{ $career = "au"; }
	elsif($GB->{KEITAI} eq 3)	{ $career = "vodafone"; }
	elsif($GB->{KEITAI} eq 5)	{ $career = "emobile"; }
	else				{ $career = "others"; }

	#新スレッドかどうかの判定
	if($GB->{FORM}->{'subject'} ne "")	{ $newthread = "b"; }
	else					{ $newthread = "a"; }

#	$AHOST = "$GB->{NOWTIME}.$$.$idnotane.A.B.C.D.X.bbm.2ch.net.";
	$AHOST = "$GB->{NOWTIME}.$$.c.$GB->{FORM}->{'bbs'}.$GB->{FORM}->{'key'}.$newthread.B.C.D.$career.$idnotane.bbm.2ch.net.";

	#BBM異常時はするー
	if(!$FOX->{BBM})		{return 1;}
	#BBMへの問い合わせ
	$SPAM = &foxDNSquery2($AHOST);
#$SPAM = "127.0.0.0";
	#焼かれているやつ、書きこみだめー
	if($SPAM eq "127.0.0.2")	{return 0;}
	#BBMが止まっています判定
	elsif($SPAM eq "127.0.0.0")	{ $FOX->{BBM} = 0; }

	#ここまで来たものは特に問題なし
	return 1;
}
#############################################################################
#
#############################################################################
sub BBXcheck
{
	my ($GB) = @_	;

	#IsKoukoku実行フラグがリセットされている時
	#(特別サーバかLAが高い)はスルー
	if(!$FOX->{ISKOUKOKU})			{return 0;}
	#以下の板はするー
	if(&KiseiOFF($GB))			{return 0;}
	if($GB->{FORM}->{'bbs'} eq "sec2chd")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "sec2ch")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "newservant"){return 0;}
	if($GB->{FORM}->{'bbs'} eq "ad")	{return 0;}
#	if($GB->{FORM}->{'bbs'} eq "campus")	{return 0;}
#	if($GB->{FORM}->{'bbs'} eq "news")	{return 0;}
#	if($GB->{FORM}->{'bbs'} eq "news4vip")	{return 0;}

	# IPv6環境ではBBXは(まだ)なし
	if($GB->{IPv6})				{return 0;}

	#IsKoukokuを実行する(スキップする)サーバかどうかのチェックは、
	#bbs-entry.cgiのmumumuIsIsKoukoku()でまとめてやるようにした
	#★でトラックバックじゃない時はスルー
#	if($GB->{CAP} && !$GB->{TBACK})		{return 0;}
	#●はスルー
	#if($GB->{MARU})			{return 0;}
	#広告かな?
	my $NG_word = &IsKoukoku($GB)	;
	if($NG_word eq '')			{return 0;}

	# それぞれの値を取り出したいときは、以下のようにデリファレンスすれば・・・
	my @NG_word_status = @{$NG_word};

	# このようにそれぞれに値が代入されます。
	# $NG_word_status[0] には規制文字列 [Shift_JIS]
	# $NG_word_status[1] には MD5 値
	# $NG_word_status[2] には フラグ

	# BBR へ送信（NGワード追跡装置？） @2005/01/22 by 未承諾広告※
	# MD5-該当ワードに付けられたmd5値.さくらフラグ.投稿者のIPアドレス.サブスクライバ.スレッド番号.板名.鯖名.bbr.2ch.net.
	# 返り値はいらないけれどもTimeOut処理が要りそうだからNet::DNSを使った方がよいかな？

	my $SubNo = $GB->{IDNOTANE}; # _ → - 変換しなきゃかもなので。
	$SubNo =~ tr/_/-/;

	# docomo携帯では「小文字フラグ」をつけてからBBR/BBNを呼ぶ
	if(length($SubNo) eq 7 && ($GB->{KEITAI} || $GB->{KEITAIBROWSER}))
	{
		$SubNo = &MakeImodeIDforDNS($SubNo);
	}

	my $CHOST =
		sprintf qq|MD5-%s.%d.%s.%s.%d.%s.%s.bbr.2ch.net.|,
		$NG_word_status[1], # MD5値
		$NG_word_status[2] ? 1 : 0, # さくらフラグ。空っぽだとイヤンなので
		$ENV{REMOTE_ADDR}, # IPアドレス（ひっくり返さなくてもいぃことにしよう♪）
		$SubNo !~ /\./ ? $SubNo : '0', # サブスクライバじゃないみたいときには '0' にしておく。
		$GB->{FORM}->{'key'}, # スレッド番号
		$GB->{FORM}->{'bbs'}, # 板名（ディレクトリ名）
		$ENV{SERVER_NAME}, # 鯖名(FQDN)
	;
	if($FOX->{BBR})
	{
		$FOX->{BBR} = &foxDNSquery($CHOST, $FOX->{DNSSERVER}->{BBR});
	}

	# このときに・・・
	if ($NG_word_status[2] == 1) # フラグが 1 のときは「いっぱつフラグ」なのでその時の処理。
	{
		&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：さくらが咲いてますよ。");
	}

	# DNS問い合わせ部分
	my $HHH = "";
	my $AHOST = "";
	if($GB->{KEITAI} || $GB->{KEITAIBROWSER} || $GB->{P22CH})
	{
		# DNSが既にしくっていたらスルー
		if(!$FOX->{BBN})	{return 0;}

		# 携帯または公式p2: bbn.2ch.net
		# ここに来るまでに、$SubNoに _ => - 変換済みの情報が入っている
		# BBMと同じフォーマットで問い合わせの種を作る
		$HHH = "$GB->{NOWTIME}.$$.c.$GB->{FORM}->{'bbs'}.$GB->{FORM}->{'key'}.$GB->{NEWTHREAD}.B.C.D.$GB->{KEITAI}.$SubNo";
		$AHOST = "$HHH.bbn.2ch.net.";
	}
	else
	{
		# DNSが既にしくっていたらスルー
		if(!$FOX->{BBX})	{return 0;}

		# 携帯以外: bbx.2ch.net
		# 今のところAIR-EDGE PHONEもこちら
		$HHH = $ENV{REMOTE_ADDR}	;
		$HHH =~ s/(\d+)\.(\d+)\.(\d+)\.(\d+)/$4.$3.$2.$1/;
		$AHOST = "$HHH.bbx.2ch.net.";
	}

	# DNS問い合わ部分は、携帯/PC共通
	my $SPAM = &foxDNSquery2($AHOST);
#	my $SPAM = '127.0.0.0';

	# DNSがしくったら、以後船が自爆するまでDNS問い合わせを停止
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
	# BBX/BBN登録ありの場合
	elsif ($SPAM eq "127.0.0.2")
	{
		my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime($GB->{NOWTIME});
		$mon ++		;
		my $yakinFile = "../_bg/logs/Rock54-$year-$mon-$mday.txt"	;
		open(YAN1,">>$yakinFile");print YAN1 "$GB->{DATE}\t$ENV{REMOTE_ADDR}\t$GB->{HOST4}\t$GB->{IDNOTANE}\t$NG_word_status[0]\n";close(YAN1);

		#&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：ロックは人生だ。");
		&endhtml($GB);
	}
	return 0;
}
#############################################################################
#罠、罠、罠、罠、罠に
#入力：
#IsKoukoku(対象文字列[Shift_JIS],Rock54のファイル名)　現状は無し。sub で定義中。
#返り血ぶしゅー：
#OK ならば 空文字列(偽)
#NG ならば （規制文字列(真)[Shift_JIS], MD5値, フラグ）のリストへのリファレンス
sub IsKoukoku
{
	my ($GB) = @_;

	my $In_Strings = $GB->{FORM}->{'MESSAGE'}; # 長いので代入

	#if($ENV{SERVER_NAME} =~ /bbspink.com/)
	#{
		$In_Strings .= $GB->{FORM}->{'mail'}	;
		$In_Strings .= $GB->{FORM}->{'FROM'}	;
		$In_Strings .= $GB->{FORM}->{'subject'}	;
	#}

	my $ccpp = &CoPiPe($GB,$In_Strings)	;#コピペを判定しようと、、、
	if($ccpp)		{return $ccpp	;}

	# 現在Rock54/54M(IsKoukoku)ありかどうかが、トップページでわかるように
	$GB->{version} .= " +Rock54/54M";

	# 読み込む。。。
	# my @Rock_word = @FOX_Ro54; # メモリの無駄なので省略してみました。

	# では NG ワードのチェック。
	foreach my $NG_word_ref (@FOX_Ro54)
	{
		my $NG_word = $NG_word_ref->[0]; # リファレンスから取り出し。
		if (my $matched = $In_Strings =~ $NG_word ? $& : undef) {
			return [$matched, @$NG_word_ref[1 .. $#$NG_word_ref]];
		} # 合致したらNGワード部分の摘出とリファレンスを返す。
		# 不正 NG ワードがあったり引っかからなければスキップ
	}
	return '';
}
sub CoPiPe
{
	my ($GB,$mes) = @_	;

#return ''	;

	#以下の板はするー
	if($ENV{'SERVER_NAME'} =~ /ex/)			{return '';}
	if($GB->{FORM}->{'bbs'} ne "news")		{return '';}

	my @mm = split(/<br>/,$mes)	;
	$mm[1] =~ s/ |　//g	;
	$mm[2] =~ s/ |　//g	;

	if(length($mm[1]) > 6 && $mm[1] eq $mm[2])	{return $mm[1]	;}

#if(length($mes) < 512)		{return '';}

	if($mes =~ /□□□/)	{return '□□□';}
	if($mes =~ /■■■/)	{return '■■■';}
	if($mes =~ /△△△/)	{return '△△△';}
	if($mes =~ /▲▲▲/)	{return '▲▲▲';}
	if($mes =~ /▽▽▽/)	{return '▽▽▽';}
	if($mes =~ /▼▼▼/)	{return '▼▼▼';}
	if($mes =~ /○○○/)	{return '○○○';}
	if($mes =~ /●●●/)	{return '●●●';}
	if($mes =~ /\|\|\|\|\|/)	{return '|||||';}
	if($mes =~ /／＼/)	{return '／＼';}
	if($mes =~ /（゜）/)	{return '（゜）';}
	if($mes =~ /彡/)	{return '彡';}
	if($mes =~ /（●）/)	{return '（●）';}
	if($mes =~ /┃┃/)	{return '┃┃';}
	if($mes =~ /蠶蠶/)	{return '蠶蠶';}
	if($mes =~ /iiiiiiiii/)	{return 'iiiiiiiii';}
	if($mes =~ /:::::/)	{return ':::::';}

	my $aa = &IsAA($GB,$mes)		;
	if($aa)	{return 'AA'	;}

	return ''	;
}
sub IsAA
{
	my ($GB,$mes) = @_	;
	#★はスルー
	if($GB->{CAP})				{return 0;}
	#●はスルー
	if($GB->{MARU})				{return 0;}

	my $bbb = "　 　 　"		;
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

	#携帯はBBQスルー(BBMでやる)
	if($GB->{KEITAI})			{return 0;}
	if($GB->{KEITAIBROWSER})		{return 0;}

	#以下の板はするー
	if(&KiseiOFF($GB))			{return 0;}
	#if($GB->{FORM}->{'bbs'} eq "campus")	{return 0;}

	# 公式p2では、p2-client-ip: を参照する
	# p2-client-ip: はfoxSetHostで、$GB->{HOST2} に入っている
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
#　ホストの判定
#==================================================
sub foxSetHost
{
	my ($GB) = @_	;

	$GB->{KEITAI} = 0		;
	$GB->{KEITAIBROWSER} = 0	;

	# IPv6では新設の関数を使う
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
	# 串っぽい時の判定
	# とりあえずIPv6の時はスキップしといて、あとで考えよう、、、。
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

	# AIR-EDGE MEGAPLUSだった場合、HTTP_CLIENT_IPをチェックし、
	# 漏れ串として動作させる
	#if (&mumumuIsIP4MegaPlus($ENV{'REMOTE_ADDR'}))
	#{
	#	my $xxx = $ENV{'HTTP_CLIENT_IP'};
	#	#&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：MegaPlus");
	#	$GB->{HOST2} = $xxx if ($xxx);
	#}

	# HTTP_CLIENT_IP (= Client_IP:)が送られてきたら、
	# 一律書き込みをお断りする
	if ($ENV{'HTTP_CLIENT_IP'})
	{
		my $xxx = $ENV{'HTTP_CLIENT_IP'};
		&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：変な情報が送られて来ました。<br>Client_IP: $xxx");
	}

	$GB->{HOST3} = $ENV{'REMOTE_ADDR'};
	$GB->{HOST4} = $GB->{HOST};

	$GB->{HOST} .= "<$GB->{HOST2}>" if ($GB->{HOST2});
	$GB->{HOST5} = $GB->{HOST}			;	#ログ記録用(iモード、EZweb、ボーダフォン！ライブは端末固有情報あり)

	$GB->{IDNOTANE}=$ENV{'REMOTE_ADDR'};

	# 携帯用ブラウザの場合の処理
	&mumumuSetHost4KeitaiBrowser($GB);

	# 公式p2
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
			&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：公式p2からの投稿ではp2-userを送信するようにしてください。");
		}
		# p2-client-ip: から接続ホストの情報を $GB->{HOST2} に得る
		if($ENV{HTTP_USER_AGENT} =~ /p2-client-ip: (\d+)\.(\d+)\.(\d+)\.(\d+)/)
		{
			$GB->{HOST2} = $1 . "." . $2 . "." . $3 . "." . $4;

			# リモートホスト名を記録する(規制が効くように)
			#my $p2host;
			#$p2host = gethostbyaddr(pack('C4',split(/\./, $GB->{HOST2})), 2) || $GB->{HOST2};
			#$GB->{HOST5} .= "($p2host)";
		}
		else
		{
			&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：公式p2からの投稿ではp2-client-ipを送信するようにしてください。");
		}
	}
	# iモード
	if(&mumumuIsIP4IMode($GB->{HOST3}))
	{
		# iモードIDに移行、2008/6/1 by mumumu
		#if($ENV{'HTTP_USER_AGENT'} =~ /ser([\w]{11,})/)
		#{
		#	$GB->{HOST5} .= "(" . $ENV{'HTTP_USER_AGENT'} .")";
		#	$GB->{IDNOTANE} = $1;
		#	$GB->{KEITAI} = 1;
		#}
		#else
		#{
		#	&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：端末固有情報を送信してください。");
		#}
		if($ENV{HTTP_X_DCMGUID} ne '')
		{
			$GB->{HOST5} .= "(" . $ENV{'HTTP_X_DCMGUID'} .")";
			$GB->{IDNOTANE} = $ENV{'HTTP_X_DCMGUID'};
			$GB->{KEITAI} = 1;
		}
		else
		{
			&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：iモードIDが正常に取得できませんでした。");
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
			&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：端末固有情報を送信しない携帯端末からは投稿できません。");
		}
	}
	# ボーダフォン！ライブ
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
			&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：端末シリアル番号を送信しないVodafoneからは投稿できません。");
		}
	}
	# emobile EMnet
	elsif(&mumumuIsIP4EMnet($GB->{HOST3}))
	{
		# HTTPリクエストヘッダの「HTTP_X_EM_UID」を取得することで、
		# EMnet対応端末から通知されるユニークなユーザIDを確認できます。
		# フォーマットは、"u"から始まる18Byteの文字列になります。
		#
		# ユーザIDはユーザの操作によって通知を停止することが可能です。
		# その場合、本拡張ヘッダは付加されません。
		# http://developer.emnet.ne.jp/useragent.html
		if($ENV{HTTP_X_EM_UID} ne '')
		{
			$GB->{HOST5} .= "(" . $ENV{'HTTP_X_EM_UID'} .")";
			$GB->{IDNOTANE} = $ENV{'HTTP_X_EM_UID'};
			# 4 は 味ぽん で使っているため 5 とする
			$GB->{KEITAI} = 5;
		}
		else
		{
			&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：emobileのEMnet接続ではユーザIDを通知しないと投稿できません。");
		}
	}
	$GB->{HOST999} = $GB->{HOST5} . $GB->{HOST2}		;

	# 携帯各社のサーバを数えるぞ
	&countKeitaiServer($GB)					;
}
#######################################################################
# 各種携帯用ブラウザのホスト情報取得
#######################################################################
sub mumumuSetHost4KeitaiBrowser
{
	my ($GB) = @_;
	my $browser = 0;

	# 携帯用ブラウザじゃなければばいばい
	$browser = &mumumuIsKeitaiBrowser($GB);
	if(!$browser) {return 0;}

	# $browser = 1: ibisBrowser
	if($browser == 1)
	{
		if(&ProcessibisBrowser($GB))
		{
			&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：携帯用ブラウザからの情報を正しく取得できませんでした。($browser)");
		}
	}
	# $browser = 2: jig Browser
	elsif($browser == 2)
	{
		if(&ProcessjigBrowser($GB))
		{
			&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：携帯用ブラウザからの情報を正しく取得できませんでした。($browser)");
		}
	}
	# $browser = 3: SoftBank PCサイトブラウザ
	elsif($browser == 3)
	{
		if(&ProcesspcsiteBrowser($GB))
		{
			&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：PCサイトブラウザからの投稿ではシリアル番号を送信するようにしてください。($browser)");
		}
	}
	# $browser = 4: iモードフルブラウザ
	elsif($browser == 4)
	{
		if(&ProcessimodefullBrowser($GB))
		{
			&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：iモードフルブラウザからの投稿ではiモードIDを送信するようにしてください。($browser)");
		}
	}
	# $browser = 5: au PCサイトビューアー
	elsif($browser == 5)
	{
		# PCサイトビューアーからの接続は無条件でエラーにする
		&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：auのPCサイトビューアーから投稿することはできません。($browser)");
	}

	return 0;
}
#######################################################################
# ibisBrowser(携帯用ブラウザの一つ)のためのホスト情報取得
# mumumuSetHost4KeitaiBrowserから呼ばれる
# 戻り値: 0 取得成功
#        -1 取得失敗
#######################################################################
sub ProcessibisBrowser
{
	my ($GB) = @_;

	my $ua = $ENV{'HTTP_USER_AGENT'};
	my $ip = undef;
	my $career = undef;
	my $serial = undef;

	# Mozilla/4.0 (compatible; ibisBrowser; ipIPアドレス; ser端末固定番号)
	# ↓iモードID対応により以下のように変更
	# Mozilla/4.0 (compatible; ibisBrowser; ipIPアドレス; iモードID)
	# ↓SoftBank端末の場合 - 2009/3/25 by mumumu
	# Mozilla/4.0 (compatible; ibisBrowser; ipIPアドレス; SN端末シリアル番号)
	# ↓Windows Mobile版
	# Mozilla/4.0 (compatible; ibisBrowser; ipIPアドレス; IBIS_WM端末固定番号)

	# ibisBrowser でない場合はだめ
	if($ua !~ /ibisBrowser/)	{ return -1; }

	
	# 携帯側IPアドレス情報 ipIPアドレス
	# ID
	# がとれるかどうか(とれなきゃだめ)
	if($ua =~ /ip(\d+)\.(\d+)\.(\d+)\.(\d+)\; (\w+)\)/)
	{
		$ip = $1 . "." . $2 . "." . $3 . "." . $4;
		$serial = $5;
	}
	else
	{
		return -1;
	}

	# IPアドレスが携帯用かどうか調べる
	$career = &IsIP4Mobile($ip);

	# 携帯キャリア別の固有情報処理
	# ここはいずれサブルーチン化したい
	# $career = 1: DoCoMo
	if($career == 1)
	{
		# iモードIDは7文字じゃなきゃだめ
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
		# "SN" + 15文字じゃないとだめ、IDはSNの後の文字のみ抽出
		if($serial =~ /SN([\w]{15,})/)
		{
			$serial = $1;
		}
		else
                {
			return -1;
		}
	}
	# 他
	else
	{
		# Windows Mobile版
		# Mozilla/4.0 (compatible; ibisBrowser; ipIPアドレス; IBIS_WM端末固定番号)
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

	# ここまで来たら$ipと$serialに情報が正しく入っている
	#&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：ip=$ip, serial=$serial");
	$GB->{HOST5} .= "($serial)";
	$GB->{IDNOTANE} = $serial;
	$GB->{KEITAIBROWSER} = 1;

	return 0;
}
#######################################################################
# jig Browser(携帯用ブラウザの一つ)のためのホスト情報取得
# mumumuSetHost4KeitaiBrowserから呼ばれる
# 戻り値: 0 取得成功
#        -1 取得失敗
#######################################################################
sub ProcessjigBrowser
{
	my ($GB) = @_;

	# 携帯側のIPアドレスはX-Forwarded-Forヘッダーで端末固有情報は
	# X-Subscriber-IDヘッダーで送信するようにしています。

	my $ip = $ENV{'HTTP_X_FORWARDED_FOR'};
	my $serialseed = $ENV{'HTTP_X_SUBSCRIBER_ID'};
	my $career = undef;
	my $serial = undef;

	# とれたIPアドレスが携帯用じゃない場合はだめ
	$career = &IsIP4Mobile($ip);
	if(!$career)			{ return -1; }

	# 携帯キャリア別の固有情報処理
	# ここはいずれサブルーチン化したい
	# $career = 1: DoCoMo
	if($career == 1)
	{
		# 7文字(iモードID)かどうか調べ、それ以外はエラー
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
	# Willcom は(とりあえず)未対応とする
	else
	{
		return -1;
	}

	# ここまで来たら$ipと$serialに情報が正しく入っている
	#&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：ip=$ip, serial=$serial");
	$GB->{HOST5} .= "($serial)";
	$GB->{IDNOTANE} = $serial;
	$GB->{KEITAIBROWSER} = 2;

	return 0;
}
#######################################################################
# pcsiteBrowser(ソフトバンク携帯用フルブラウザ)のためのホスト情報取得
# mumumuSetHost4KeitaiBrowserから呼ばれる
# 戻り値: 0 取得成功
#        -1 取得失敗
#######################################################################
sub ProcesspcsiteBrowser
{
	my ($GB) = @_;

	my $ua = $ENV{'HTTP_USER_AGENT'};
	my $serial = undef;

	# Mozilla/4.08 (911T;SoftBank;SN354000000000000) NetFront/3.3

	# SoftBank でない場合はだめ
	if($ua !~ /SoftBank/)	{ return -1; }
	# NetFront でない場合はだめ
	if($ua !~ /NetFront/)	{ return -1; }

	# 固有情報取得処理
	# ここはいずれサブルーチン化したい
	if($ua =~ /SN([\w]+?)\)/)
	{
		$serial = $1;
	}
	else
	{
		return -1;
	}

	# ここまで来たら$serialに情報が正しく入っている
	#&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：serial=$serial");
	$GB->{HOST5} .= "($serial)";
	$GB->{IDNOTANE} = $serial;
	$GB->{KEITAIBROWSER} = 3;

	return 0;
}
#######################################################################
# imodefullBrowser(ドコモ携帯用フルブラウザ)のためのホスト情報取得
# mumumuSetHost4KeitaiBrowserから呼ばれる
# 戻り値: 0 取得成功
#        -1 取得失敗
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

	# ここまで来たら$cidに情報が正しく入っている
	#&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：cid=$cid");
	$GB->{HOST5} .= "(" . $cid .")";
	$GB->{IDNOTANE} = $cid;
	$GB->{KEITAIBROWSER} = 4;

	return 0;
}
#######################################################################
#　新規スレッドと普通の書き込みの情報チェック
#######################################################################
sub foxSetInformation
{
	my ($GB) = @_	;

	my $DATAFILE ="";	#.datファイルを宣言しておく

	# フォームの時間情報がおかしい場合
	if($GB->{FORM}->{'time'} >= $GB->{NOWTIME})
	{
		&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：ブラウザを立ち上げなおしてみてください。");
	}

	# 新スレの場合
	if($GB->{FORM}->{'subject'} ne "")
	{
		# submitがない場合、スレ立てだめ
		if($GB->{FORM}->{'submit'} eq "")
		{
			&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：スレッド立てすぎです。。。");
		}

		# サブジェクトがあれば新規スレなのでキーを現在に設定
		$GB->{FORM}->{'key'} = $GB->{NOWTIME}	;
		# 新スレフラグを立てる
		$GB->{NEWTHREAD} = $GB->{NOWTIME}	;

		###################################################
		#　新規スレブロックがかかってたら飛ばす（subbbs.cgi）
		###################################################
#		if($GB->{FORM}->{'FROM'} =~/fusianasan/){
#		if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_NEWSUBJECT'} ne "" && $GB->{FORM}->{'submit'} =~ /新規/)
#		{
#
#			subbbs($GB);
#		}
		###################################################

		#新規スレッドのキーを得る(下記do～whileの置き換え)
		$GB->{FORM}->{'key'} = &mumumuAllocateThreadKey($GB);
		$DATAFILE = $GB->{DATPATH} . $GB->{FORM}->{'key'} . ".dat";
# このコードだと既に $DATAFILE が存在していた場合、ここで無限ループに陥る
#		do {
#			#サブジェクトがあれば新規スレなのでキーを現在に設定
#			$GB->{FORM}->{'key'} = $GB->{NOWTIME};
#			#.datファイルの設定
#			$DATAFILE = $GB->{DATPATH} . $GB->{FORM}->{'key'} . ".dat";
#		} while ( -e $DATAFILE ) ;
	}
	# レスの場合
	else
	{
		if(defined($GB->{FORM}->{'key'}))
		{
			#キーが数字じゃない場合ばいばい！
			if($GB->{FORM}->{'key'} =~ /\W/ || $GB->{FORM}->{'key'} eq "")
			{
				&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：キー情報が不正です！");
			}
		}
		else
		{
			if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_PASSWORD_CHECK'} eq "checked")
			{
				# 新規スレッド別画面
				&newbbs($GB);
			}
			else
			{
				#サブジェクトもキーも存在しないならばいばい
				&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：サブジェクトが存在しません！");
			}
		}
		#.datファイルの設定
		$DATAFILE = $GB->{DATPATH} . $GB->{FORM}->{'key'} . ".dat";
		#.datが存在してないか書けないならばいばい
		# 雪だるまでは -w や -s の判定はbbsdにまかせる(ここではしない)
		if(!IsSnowmanServer)
		{
			unless(-w $DATAFILE)
			{
				&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：このスレッドには書き込めません。");
			}
			unless( -s $DATAFILE <= 512000)
			{
				&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：このスレッドは512kを超えているので書けません！");
			}
		}
	}
}
#######################################################################
# 新スレのスレッドキーを決定する
#######################################################################
sub mumumuAllocateThreadKey
{
	my ($GB) = @_;
	my $maxtries = 3;	# スレッドが既にあった時の再試行数
	my $i = 0;
	my $threadkey = $GB->{NOWTIME};
	my $datafile = $GB->{DATPATH} . $threadkey . ".dat";

	# 雪だるまサーバではそのまま使用(bbsdにまかせる)
	if(IsSnowmanServer)
	{
		return $threadkey;
	}

	# 同じスレッドキーがなければ無問題
	# 大抵の場合はここでだいじょうぶ
	if ( ! -e $datafile )
	{
		return $threadkey;
	}
	# 同じファイルが既にあった場合
	# live系じゃない場合、ちょっとがんがってみる
	elsif(!$ENV{'SERVER_NAME'} =~ /live/)
	{
		for ($i = 1; $i <= $maxtries; $i++)
		{
			$threadkey++;
			$datafile = $GB->{DATPATH} . $threadkey . ".dat";
			if ( ! -e $datafile )
			{
				# スレッドキーを更新
				# $GB->{NOWTIME} も更新すること
				$GB->{NOWTIME} = $threadkey;
				return $threadkey;
			}
		}
	}
	# でもやっぱりだめだったからごめんなさい
	&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：別の人が同時刻にスレッドを立てようとしています。ごめんなさい。");
}
#############################################################################
#	スレつぶし
#############################################################################
# >100,101,102たくさんはダメ
sub SureAnc
{
	my ($GB) = @_	;

	#以下の板はするー
	if(&KiseiOFF($GB))			{return 0;}
	if($GB->{FORM}->{'bbs'} eq "sec2ch")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "sec2chd")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "saku")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "saku2ch")	{return 0;}
	#★はスルー
	if($GB->{CAP})				{return 0;}
	#●はスルー
	if($GB->{MARU})				{return 0;}

	my $nnn = ($GB->{FORM}->{'MESSAGE'} =~ s/(\d)/$1/g);
#&DispError2($GB,"ＥＲＲＯＲ！","nnn=$nnn");
	if($nnn < 120)	{return 0;}

#	$nnn = ($GB->{FORM}->{'MESSAGE'} =~ s/([&gt;\d+|-\d+|,\d+])/$1/g);
	$nnn = ($GB->{FORM}->{'MESSAGE'} =~ s/(&gt;\d+)/$1/g);
	if($nnn < 12)	{return 0;}
	$nnn += ($GB->{FORM}->{'MESSAGE'} =~ s/(-\d+)/$1/g);
	$nnn += ($GB->{FORM}->{'MESSAGE'} =~ s/(,\d+)/$1/g);
#&DispError2($GB,"ＥＲＲＯＲ！","nnn=$nnn");
	if($nnn > 10)	{&endhtml($GB);	}

	return 0	;
}
# http://たくさんはダメ
sub SureHttp
{
	my ($GB) = @_	;

	#以下の板はするー
	if(&KiseiOFF($GB))			{return 0;}
	if($GB->{FORM}->{'bbs'} eq "sec2ch")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "sec2chd")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "saku")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "saku2ch")	{return 0;}
	#★はスルー
	if($GB->{CAP})				{return 0;}
	#●はスルー
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
# 鬱が沢山はダメ
sub SureUtsu
{
	my ($GB) = @_	;

	#以下の板はするー
	if(&KiseiOFF($GB))			{return 0;}
	if($GB->{FORM}->{'bbs'} eq "sec2ch")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "sec2chd")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "saku")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "saku2ch")	{return 0;}
	if(&IsAAbbs($GB))			{return 0;}
	#★はスルー
	if($GB->{CAP})				{return 0;}
	#●はスルー
	if($GB->{MARU})				{return 0;}

	if(length($GB->{FORM}->{'MESSAGE'}) < 10)	{return 0;}

	my $bbb = substr($GB->{FORM}->{'MESSAGE'}, 0, 4) ;
	if($bbb =~ /　/)	{return 0;}
#	if($bbb =~ /[0-9a-zA-Z\:\.\;\+\,]/)	{return 0;}
	if($bbb =~ /[\:\.\;]/)	{return 0;}

	if($bbb eq "　＿")	{return 0;}
	if($bbb eq "　　")	{return 0;}
	my $nnn = ($GB->{FORM}->{'MESSAGE'} =~ s/\Q$bbb\E/$bbb/g);
	if($nnn > 20){	&endhtml($GB);	}

	return 0	;
}
# >> が沢山はダメ
sub SureTsubushi
{
	my ($GB) = @_	;

	#以下の板はするー
	if(&KiseiOFF($GB))			{return 0;}
	if($GB->{FORM}->{'bbs'} eq "saku")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "saku2ch")	{return 0;}
	if($GB->{FORM}->{'bbs'} eq "owarai")	{return 0;}
#	if($GB->{FORM}->{'bbs'} eq "campus")	{return 0;}
	#★はスルー
	if($GB->{CAP})				{return 0;}
	#●はスルー
	if($GB->{MARU})				{return 0;}

	my $bbb = "&gt;&gt;";
	my $nnn = ($GB->{FORM}->{'MESSAGE'} =~ s/\Q$bbb\E/$bbb/g);
	if($nnn > 10){	&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：>> が多すぎます！");}

	$bbb = "http://";
	$nnn = ($GB->{FORM}->{'MESSAGE'} =~ s/\Q$bbb\E/$bbb/g);
	if($nnn > 15){	&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：http:// が多すぎます！");}

	$bbb = "https://";
	$nnn = ($GB->{FORM}->{'MESSAGE'} =~ s/\Q$bbb\E/$bbb/g);
	if($nnn > 15){	&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：https:// が多すぎます！");}

	$bbb = "ftp://";
	$nnn = ($GB->{FORM}->{'MESSAGE'} =~ s/\Q$bbb\E/$bbb/g);
	if($nnn > 15){	&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：ftp:// が多すぎます！");}

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
# bbsd経由で書き込む(雪だるま版WriteDatFile)
#############################################################################
sub WriteSnow
{
	my ($GB, $DATALOG) = @_;

	# bbsdに書き込みコマンドを送る
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

	# タイムアウトかどうかチェック
	if(&bbsd_TimeoutCheck($GB, $errmsg))
	{
		#XXX
		return 0;
		&bbsd_TimeoutError($GB, 'WriteSnow');
	}

	# 新スレの時は実際のスレッドキーが来るので、それを保存
	if($GB->{NEWTHREAD})
	{
		#スレッドキーだったら保存して戻り
		if($errmsg !~ /\D/)
		{
			$GB->{FORM}->{'key'} = $errmsg;
			return 0;
		}
		#そうでないときはエラー処理へ
	}

	# $errmsg が空文字列じゃない場合、エラー処理
	if($errmsg)
	{
		$errmsg = +{
			# 書けない場合
			# 1000レス越え・512kB越え
			do{local $! = EDQUOT;} => 'このスレッドは1000レスまたは512kを超えているので書けません！',
			# スレッドストップ
			do{local $! = EACCES;} => 'このスレッドには書き込めません。',
			# ないスレッドに書こうとした
			do{local $! = ENOENT;} => 'スレッドがありません。',
			# bbsdでのスレ立てリトライ回数を超えた
			do{local $! = EEXIST;} => '別の人が同時刻にスレッドを立てようとしています。ごめんなさい。'
		}->{$errmsg}
			# その他のエラー
			|| "不明なエラーが発生しました。<br>(board:$GB->{FORM}{bbs} key:$GB->{FORM}{key} errmsg:$errmsg)<br>このメッセージをコピペして、運用情報板で報告していただけるとありがたいです。";
		&DispError2($GB, 'ＥＲＲＯＲ！', "ＥＲＲＯＲ：$errmsg");
	}

	return 0;
}
#############################################################################
# bbs.cgi メインルーチン、ここから↓
#############################################################################
sub bbs_main
{
	my ($GB) = @_			;

#&DispError2($GB,"不動楽 ★","<font color=green>不動楽 ★</font>　む？どこで失くしたのかな？($GB->{FORM}->{bbs})<br>($GB->{FORM}->{get})");
#&DispError2($GB,"FOX ★","<font color=green>FOX ★</font>　いよいよ本体($GB->{FORM}->{bbs})<br>time=$GB->{NOWTIME}<br>mail=$GB->{FORM}->{mail} kihon=$GB->{FORM}->{kihon}");

	require "jcode.pl"		;
	require "bbs-yakin.cgi"		;
	&YakinInit			;

	&foxSetHost($GB)		;	#　ホストの判定
	#↑ここまでは外すと動かないと思う

	#if(&IsP2($GB))	{&DispError2($GB,"ＥＲＲＯＲ！","p2お断り");}

	# 2006年5月20日、914事件の緊急対応 by む
	#if($GB->{FORM}->{'key'} =~ /^914/)
	#{
	#	&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：このスレッドには書き込めません。ごめんなさい。");
	#}

	# 2006年7月23日、be事件の緊急対応 by む
	#if($GB->{FORM}->{bbs} eq 'be')
	#{
	#	&DispError2($GB,"ＥＲＲＯＲ！","ＥＲＲＯＲ：be板は現在調整中です。ごめんなさい。");
	#}

	# IsCentiSecが真の場合、1/100秒まで表示する
	# &Yamadaで$GB->{DATE}を参照しているので、ここで実行する必要がある
	if(&IsCentiSec($GB))
	{
		my $csec = sprintf("%02d", int($GB->{NOWMICROTIME} / 10000));
		$GB->{DATE} .= '.' . $csec;
	}

	#&Yamada($GB)	;
	&Saga($GB)	;	#佐賀ウィルス

	#↓ここから※ははずしても動く予定
	&foxSetInformation($GB)		;	#　新規スレッドと普通の書き込みの情報チェック

#疲れたのでここまで、
#&DispError2($GB,"FOX ★","<font color=green>FOX ★</font>　疲れたのでここまで($GB->{FORM}->{bbs})<br>time=$GB->{NOWTIME}");

	#クッキーの処理(トラックバックではスキップ)
	if(!$GB->{TBACK})
	{
		#クッキーを発行
		#  NAME= と MAIL= のクッキーは bbs.cgi ではなく、
		#  JavaScript 経由で発行することにする
		#  JavaScript は MakeIndex4PC / newbbs で以下の .js を読み込み
		#    http://www2.2ch.net/snow/index.js
		#&PutCookie($GB);
		#クッキーを食ったかチェック
		unless($ENV{'HTTP_COOKIE'} || $GB->{FORM}->{'get'} ne '' || $GB->{FORM}->{kihon} ne 'suriashi')
		{
			#投稿確認画面を出して、exitする
			#注意: いつも出ている投稿確認画面は
			#foxIkinariで出ていて、ここではない
			&ToukouKakunin($GB);
			exit;
		}
		#&DispError2($GB,"root ★","クッキー調整中 HTTP_COOKIE: $ENV{'HTTP_COOKIE'}");
	}

#==================================================
#　情報のチェックと修正
#==================================================

	# IsKoukokuを実行するかどうか
	# 既に$FOX->{ISKOUKOKU} = 0なら再チェックしない
	if($FOX->{ISKOUKOKU})
	{
		if(!&mumumuIsIsKoukoku($GB)) { $FOX->{ISKOUKOKU} = 0; }
	}

	#subject.txt/subback.htmlの実行をさぼるかどうか
	if(&Saborin($GB))
	{
		$GB->{SABORIN} = 1;
	}

	#●の処理
	&ProcessMaru($GB);

	##############################################
	#ニュー速の補完
	$GB->{FORM}->{'FROM'} =~ s/^ //g;
	$GB->{FORM}->{'FROM'} =~ s/^　//g;

	&NanashiReplace4vip($GB);
	##############################################

	#名前欄・メール欄の禁止名(「削除」「管理」「山崎渉」など)の処理
	&NGNameReplace($GB);

	#ハンドル（トリップ）の処理
	#&jcode::tr(\$GB->{FORM}->{'FROM'}, '＃', '#');
	#if($GB->{FORM}->{'FROM'} =~ /([^#]*)#(.+)/)
	if(defined $GB->{TRIPKEY})
	{
		&ProcessTrip($GB, $GB->{FORM}{FROM}, $GB->{TRIPKEY});
		# 呪われたトリップかどうかチェック
		&BadTripCheck($GB);
	}

	#ハンドル（キャップ）の処理
	&jcode::tr(\$GB->{FORM}->{'mail'}, '＃', '#');
	if($GB->{FORM}->{'mail'} =~ /([^#]*)#(.+)/)
	{
		&ProcessCap($GB, $1, $2);
	}

	#キャップじゃない時、neet4vip/neet4pinkの特殊処理
	if(!$GB->{CAP})
	{
		if($GB->{FORM}->{'bbs'} =~ /neet/)
		{
			# neet系は強制名無し
			$GB->{FORM}->{'FROM'} = $FOX->{$GB->{FORM}->{'bbs'}}->{'BBS_NONAME_NAME'};
			# neet4pinkはトリップ有効
			if($GB->{FORM}->{'bbs'} =~ /neet4pink/)
			{
				# トリップ文字列がある場合
				if($GB->{TRIPSTRING} ne "")
				{
					$GB->{FORM}->{'FROM'} .= "</b> ◆$GB->{TRIPSTRING} <b>";
				}
			}
		}
	}

	# 名前入力チェック、名無し補完と処理、heaven4vipの名無し置換処理
	&ProcessNanashi($GB);

	# tasukeruyoの処理
	if($GB->{FORM}->{'FROM'} =~ /tasukeruyo/)
	{
		# operate/operate2 と dso サーバでのみ有効
		# ipv6 板でも有効にしてみた
		if(	$GB->{FORM}->{'bbs'} eq 'ihou' ||
			$GB->{FORM}->{'bbs'} =~ "operate" ||
			$GB->{FORM}->{'bbs'} =~ "ipv6" ||
			$ENV{'SERVER_NAME'} =~ /dso/)
		{
			&Tasukeruyo($GB);
		}
	}

	# fusianasanの処理
	if($GB->{FORM}->{'FROM'} =~ /fusianasan/)
	{
		&Fusianasan($GB);
	}

	# 地震関連板の県名追加
	&EQfromWhere($GB);

	#ユニコード変換
	if($FOX->{$GB->{FORM}->{bbs}}->{'BBS_UNICODE'} eq "change")
	{
		$GB->{FORM}->{'MESSAGE'} =~ s/\&\#[0-9;]*/？/gi;
	}

	#株主優待 ＠株主 ★
	if($GB->{KABUU})
	{
		if($GB->{FORM}->{'FROM'} =~ s/＠株主 ☆/＠株主 ★/)
		{
			$GB->{FORM}->{'FROM'} =~ s/＠株主 ★//	;
			$GB->{FORM}->{'FROM'} .= "＠株主 ★"	;
		}
	}

#&DispError2($GB,"FOX ★","<font color=green>FOX ★</font>　いろいろチェック直後　<br>FROM=$GB->{FORM}->{'FROM'}<br>MESSAGE=[$GB->{FORM}->{'MESSAGE'}]<br>mail=$GB->{FORM}->{'mail'}<br>");

#==================================================
#　エラーレスポンス（普通のエラーはまとめてばいばい）
#==================================================

	#フォーム情報のチェック(板名に変な文字、時間が読めない)
	&FormInfoCheck($GB);

	#refererチェック(ブラウザ変ですよん)
	if(!$GB->{TBACK} && ($GB->{FORM}->{'submit'} ne "かきこむ" || $ENV{'HTTP_USER_AGENT'} =~ /Mozilla/))
	{
		&BraHen($GB);
	}

#==================================================
#　フィールドサイズの判定
#==================================================

	# スレタイ、名前、メアド、本文の長さチェック
	&FieldSizeCheck($GB);

	# 本文の行数と長すぎる行のチェック
	&FieldLineCheck($GB);

	# >> が沢山はダメ等
#	&SureTsubushi($GB)	;
#	&SureUtsu($GB)		;	# 鬱が沢山はダメ
#	&SureHttp($GB)		;	# http:が沢山はダメ
#	&SureAnc($GB)		;	# >100が沢山はダメ
	#お試し●漏れ防止
	&OtameshiMaru($GB)	;
	#英語板
	&NoJapanese($GB)	;
	
#==================================================
#　板別の特殊処理
#==================================================

	# 板別の特殊処理
	&ItabetsuSpecial($GB);

#&DispError2($GB,"FOX ★","<font color=green>FOX ★</font>　いっきに40%進んでみる　<br>($GB->{HOST})<br>$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE'}<br>");

#==================================================
#　撃退系各種処理
#==================================================

	&GeroTrap($GB)		;

	&checkPragma($GB)	;

	&checkProxyAtAll($GB)	;	#公開プロクシ規制

	&checkDenyList($GB)	;	#アク禁リスト(proxy999.cgi)をなめまわす

	&vip931($GB)		;	#VIP臭い

	&bybySaru($GB)		;	#バイバイさるさん

	&antiHosyu($GB)		;	#自動保守ツール撃退

	&BBMcheck($GB)		;	#BBM (携帯規制)

	&BBXcheck($GB)		;	#Rock54/Rock54M (広告爆撃を迎撃)

	&ToolGekitai0($GB)	;	#Samba24 (新連続投稿規制)

	&GooMorningKeitai($GB)	;	#BBM2 携帯での規約みせ

#&DispError2($GB,"FOX ★","<font color=green>FOX ★</font>　撃退されなかった　<br>($GB->{HOST})<br>$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE'}<br>");

#&DispError2($GB,"FOX ★","<font color=green>FOX ★</font>　いっきに50%進んでみる　<br>($GB->{HOST},$GB->{HOST999},$GB->{IDNOTANE})<br>$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE'}<br>$GB->{MARU}<br>");

#==================================================
#　スレ立て制限＆連続カキコ
#==================================================

	# 新スレの場合、スレ立てチェック
	if($GB->{FORM}->{'subject'} ne "")
	{
		#ニュー速sakuでの●焼きチェック
		&VipQ2MaruyakiCheck($GB)	;
		#各種スレ立てチェックをまとめて実施
		&SuretateTotalCheck($GB)	;
	}

	# timecount/timeclose(連続投稿ですか？ x回)の処理
	&Check_HardPosting($GB);

#==================================================
#　トラックバック
#==================================================

	#トラックバック処理
	&foxTrackBack($GB)		;

#==================================================
#　VIPクオリティ
#==================================================

	#株価の表示
	&ReplKabuka($GB)		;

	#VIPクオリティ(おみくじとかお年玉とかIQとか船とか)
	&ReplOmikuji($GB)		;
	&ReplOtoshidama($GB)		;
	&ReplIQ($GB)			;
	&ReplShip($GB)			;

	#VIPクオリティ2.0
	&VipQ2($GB)			;	#!vip2:command:

#==================================================
#　レスポンスアンカー（本文）
#==================================================

	# レスアンカーの処理 (>>レス番号 >>レス番号-レス番号)
	&ResAnchor($GB);

#==================================================
#　ファイル操作（ＤＡＴファイル更新）
#==================================================

	# BEかどうか
	if($GB->{isBE})
	{
		# ポイントに応じた、BE用の文字列を作成する
		# $GB->{xBE} に格納される
		&MakeBEString($GB);
	}
	else
	{
		# BEじゃない場合
		$GB->{xBE} = "";
	}

	# トラックバックの場合、名前欄は固定
	if($GB->{TBACK})	{$GB->{FORM}->{'FROM'} = "トラックバック ★";}

	# IDのところに表示する文字列と、芋掘りの芋を作る
	# $GB->{xID} と $GB->{LOGDAT} に格納される
	&MakeIdStringAndLogdat($GB);

	# 1ユニット分のdatを作る
	# $GB->{OUTDAT} に格納される
	&MakeOutdat($GB);

	# 芋のファイル名(フルパス)
	my $DATALOG = $GB->{LOGPATH} . $GB->{FORM}->{'key'} . ".cgi";

	# datのファイル名(フルパス)
	my $DATAFILE = $GB->{DATPATH} . $GB->{FORM}->{'key'} . ".dat";

#==================================================
#　dat書き込み、datデータ読み込み、1000超え処理
#==================================================

	if(IsSnowmanServer)
	{
		# ログのディレクトリがなければ作成
		unless(IsSnowmanServer == BBSD->{REMOTE} || -e $GB->{LOGPATH})
		{
			#umask(0);
			mkdir($GB->{LOGPATH},0777);
		}
		# 最強キャップでは、924にもレス可能
		if($GB->{FORM}->{'key'} =~ /^924/ && !$GB->{STRONGCAP})
		{
			#スレッド924 = 書き込めないスレッド
			&Update924($GB, $DATAFILE);
		}
		else
		{
			# 書き込み処理
			&WriteSnow($GB, $DATALOG);
		}
	}
	else
	{
		# 通常の処理(雪だるまじゃない場合)
		# 最強キャップでは、924にもレス可能
		if($GB->{FORM}->{'key'} =~ /^924/ && !$GB->{STRONGCAP})
		{
			#スレッド924 = 書き込めないスレッド
			&Update924($GB, $DATAFILE);
		}
		else
		{
			# datファイル書き込み
			&WriteDatFile($GB, $DATAFILE, $GB->{OUTDAT}, 0);
			# ログのディレクトリがなければ作成
			unless(-e $GB->{LOGPATH})
			{
				#umask(0);
				mkdir($GB->{LOGPATH},0777);
			}
			# ログファイル書き込み
			&WriteDatFile($GB, $DATALOG, $GB->{LOGDAT}, 1);
		}

		# <チラシの裏>
		# datに追記する前にdatの情報を入手したほうが、何かと
		# いいような気もする。例えば、同じのが連投されてたら
		# 書き込みを許さないとか、そういう処理もできるだろうし、
		# 1000超えの処理も楽になるような気もする。
		#
		# しかし他への影響がでかいと思われるし、いろいろな
		# 副作用も考えられるので、今はとりあえず、こうしておく。
		# 11/11/2005 by む
		# </チラシの裏>

		# datの情報を入手し、$GBにセットしておく
		# こいつらは後で/html/の下を作る(MakeWorkFile)のに使う
		# $GB->{DATNUM}, $GB->{DAT1}, $GB->{DATLAST}
		&GetDatInfo($GB, $GB->{FORM}->{'key'});

		#&DispError2($GB,"root ★","レス数: $GB->{DATNUM} <br>1の内容: $GB->{DAT1} <br>DATLASTの頭: $GB->{DATLAST}[0]");

		# 1000超えの処理をする
		if($GB->{DATNUM} > 999)
		{
			&Over1000($GB, $DATAFILE);
			# 1050超え緊急ストッパー
			if($GB->{DATNUM} > 1049)
			{
				&EmergOver1000($GB, $DATAFILE);
				# 1100超え緊急ストッパー(最後の手段)
				if($GB->{DATNUM} > 1099)
				{
					&EmergOver1000Final($GB, $DATAFILE);
				}
			}
		}
		#VIPクォリティでのスレスト
		if($GB->{VIPQ2STOP})
		{
			chmod(0555, $DATAFILE);
		}
	}

#==================================================
# bby.2ch.net に通知。新スレッドが立った。
#==================================================

	if($GB->{NEWTHREAD})
	{
		&NotifyBBY($GB);
	}

#==================================================
# bbs.2ch.net に通知。書きこみ情報
#==================================================

	&NotifyBBS($GB);

$GB->{DEBUG} .= "いっきに60%進んでみる<br>";
#&DispError2($GB,"FOX ★","<font color=green>FOX ★</font>　いっきに60%進んでみる　<br>datへの追記が終ったところ<br>($GB->{HOST},$GB->{HOST999},$GB->{IDNOTANE})<br>$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE'}<br>$GB->{MARU}<br>");

#==================================================
#　ファイル操作（subject.txt & subback.html）
#==================================================

	# 雪だるまサーバでは、以降のファイル処理はしない(bbsdが実行)
	if(IsSnowmanServer)
	{
		&endhtml($GB);
	}

	# subject.txtを更新する
	# ここで @{$GB->{NEWSUB}} にサブジェクトが入ってくる
	# $GB->{SUBLINE} もここで準備される
	# $GB->{FILENUM} にはここでsubject.txtの行数が入るようだ
	&UpdateSubject($GB);

	#&DispError2($GB,"root ★","newsubの頭: ${$GB->{NEWSUB}}[0]");

	# html/ の下を作る
	&MakeWorkFile($GB, $GB->{FORM}->{'key'});

	#subback.htmlを更新する
	#Saborinフラグが立っていたらさぼる
	if(!$GB->{SABORIN})
	{
		&UpdateSubback($GB);
	}

#==================================================
#　本ＨＴＭＬ吐き処理 (index.html)
#==================================================

	#携帯用のindexを作る(/i/index.html)
	#saku/saku2chでも、携帯用の index.html は作る
	if(!$GB->{SABORIN})
	{
		&MakeIndex4Keitai($GB);
	}

	#Saborinフラグが立っている or
	# saku/saku2chでは index.html の更新をさぼる (sakudでは作るので注意)
	if(!$GB->{SABORIN} && !($GB->{FORM}->{'bbs'} eq "saku" || $GB->{FORM}->{'bbs'} eq "saku2ch"))
	{
		&MakeIndex4PC($GB);
	}

	$GB->{DEBUG}  .= "ここに飛んで欲しいとbbs.cgiは思っている=$GB->{INDEXFILE}<br>";
	#&DispError2($GB,"FOX ★","<font color=green>FOX ★</font>　最後どうなってるんだ?　<br><br>");

	# 一番最後のところの処理
	&endhtml($GB);

#&DispError2($GB,"FOX ★","<font color=green>FOX ★</font>　いっきに最後まで進んでみる　<br>datへの追記が終ったところ<br>($GB->{HOST},$GB->{HOST999},$GB->{IDNOTANE})<br>$FOX->{$GB->{FORM}->{bbs}}->{'BBS_TITLE'}<br>$GB->{MARU}<br>");
}
sub KiseiOFF
{
	my ($GB) = @_			;
#	if($GB->{FORM}->{bbs} eq 'ghard')	{return 1;}
#	if($ENV{'SERVER_NAME'} =~ /bbspink/)	{return 1;}
	return 0	;
}
#############################################################################
# メインルーチン終わり。お疲れ様でした。
#############################################################################
1;
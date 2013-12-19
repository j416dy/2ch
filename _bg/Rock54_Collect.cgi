#!/usr/bin/perl --

# R54_Collect.cgi
# Rock54.txt を取ってくる装置
=comment
2.00	2008/02/24	丁稚どん改
2.01	2008/12/29	あれ？なんだっけ。。。
2.02	2009/06/28	update時のレスポンスヘッダがおかしかったので改竄
2.03	2010/01/03	丁稚どんのPASSってなんだっけ？（汗）と、、、文法のチェック（苦笑）
=cut

use LWP::UserAgent;
use strict;

# 自分自身の名前
my $My_name = "Rock54_Collect";
my $Version = '2.03(2010/01/03)';

# FreeBSD ではこうしないと止まっちゃうみたい。。。
$SIG{'ALRM'} = "IGNORE";

# 取ってきたリストを設置する場所。
my $Collect_PATH = '.';
my $Rock54_Text = "$Collect_PATH/Rock54.txt";

# rock54 鯖のURI
my $Rock54_server_name = "rock54.2ch.net";

# rock54 鯖へのリクエスト
my $Collect_URI = "Rock54/_Collect/Rock54.txt";

# rock54 鯖へのリクエスト（ Rock54_Collect.cgi 取得用）
my $CollectCGI_URI = "Rock54/_Collect/Rock54_Collect.txt";

# LWP::UserAgentオブジェクト
my $UserAgent = LWP::UserAgent->new(
	agent           => "Monazilla/1.00 Rock54_Collect (+http://rock54.2ch.net/)",
	timeout         => 5,
);

# ファイルハンドル用
my $FileHandle;

# 取得桶フラグ用
my $GetList;

# HTML テンプレート。
my %Html;

# --- おきまりのリプライメッセージのエンティティヘッダとか
$Html{content} = <<"EOS";
Content-type: text/html; charset=Shift_JIS
Rock54-Collect-Version: %s
Rock54-Collect-Status: %s

EOS

# --- HTMLヘッダ部分（sprintfで出力しること）
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

# --- 最後のところ
$Html{footer} =<<"EOS";
<address>Rock54_Collect $Version</address>
</body>
</html>
EOS

# しぐなるはんどらぁ
{
	$SIG{'PIPE'} = $SIG{'INT'} = $SIG{'HUP'} = $SIG{'QUIT'} = $SIG{'TERM'} = \&SigExit;
}

# 止められたとき
sub SigExit{
	Error("94", shift);
}

# エラー
sub Error{
	my $number = shift;
	my $err    = shift;
	my %Messages = (
		'00',"とってｷﾀ━━━(ﾟ∀ﾟ)━━━ｯ!!",
		'01',"とってｷﾀｷﾀｷﾀ━━━(ﾟ∀ﾟ)━━━ｯ!!!",

		'90',"うっさいハゲ氏ね。",
		'91',"とれませんでした[01]（´・ω・｀）ｼｮﾎﾞｰﾝ",
		'92',"とれませんでした[02]（´・ω・｀）ｼｮﾎﾞｰﾝ",
		'93',"とれませんでした[03]（´・ω・｀）ｼｮﾎﾞｰﾝ",
		'94',"とれませんでした[04]（´・ω・｀）ｼｮﾎﾞｰﾝ",

		'95',"とれませんでした[05]（´・ω・｀）ｼｮﾎﾞｰﾝ",
		'96',"とれませんでした[06]（´・ω・｀）ｼｮﾎﾞｰﾝ",
		'97',"とれませんでした[07]（´・ω・｀）ｼｮﾎﾞｰﾝ",
		'98',"とれませんでした[08]（´・ω・｀）ｼｮﾎﾞｰﾝ",
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
#	$| = 1; # 垂れ流しを止めてみる。
	print $Html{message};
	exit;
}

################################################################################
# ここから。
MAIN:
{
	# 呼び出した人のチェックいろいろ。
	$ENV{REMOTE_HOST} eq ''               and
#	$ENV{REMOTE_ADDR} ne '206.223.147.35' and # banana238
	$ENV{REMOTE_ADDR} ne '206.223.151.67' and # tiger509
#	$ENV{REMOTE_ADDR} ne '192.168.1.21'   and # baila6.jp用
		Error('90');

	 Error('90') unless $ENV{HTTP_USER_AGENT} eq "Monazilla/1.00 Rock54_Summon (+http://rock54.2ch.net/)"
		or $ENV{HTTP_USER_AGENT} eq "Monazilla/1.00 Rock54_Cron (+http://rock54.2ch.net/)";

	# 早速 Rock54.txt を取りに行く。
	# $UserAgent->default_header('Authorization' => 'Basic Q29sbGVjdDpkZWNjaURvbg==');
	# BASIC認証
	$UserAgent->credentials("$Rock54_server_name:80", "Entrance Rock54", "Collect", "borracho");

	my $Response = $UserAgent->get("http://$Rock54_server_name/$Collect_URI");
	# お取り込み成功
	if ($Response->is_success) {
		my $Get_Rock54list = $Response->content;

		# 仮名で書き込み
		open   $FileHandle, ">$Rock54_Text.tmp" or Error('92', $!); # 取得に失敗
		print  $FileHandle $Get_Rock54list;
		close  $FileHandle;

		# 名前を書き換える。
		rename "$Rock54_Text.tmp", $Rock54_Text or Error('93', $!); # 名前変更に失敗
		$GetList = 1; # 取得ＯＫ
	}
	else {
		Error('91',$Response->status_line); # 取得に失敗
	}

	# Rock54_Collect.cgi の更新情報が有ればそれも取りに行く。
	if ($ENV{QUERY_STRING} eq 'update') {
		# 早速 Rock54_Collect.cgi を取りに行く。
		my $Response = $UserAgent->get("http://$Rock54_server_name/$CollectCGI_URI");

		# お取り込み成功
		if ($Response->is_success) {
			my $Get_Rock54_CollectCGI = $Response->content;

			# 仮名で書き込み
			open  $FileHandle, ">$Collect_PATH/$My_name.txt" or Error('95', $!); # 取得に失敗;
			print $FileHandle $Get_Rock54_CollectCGI;
			close $FileHandle;

			# 現在のパーミッションを取得
			my $CGI_Permission = (stat "$Collect_PATH/$My_name.cgi")[2];

			# 文法テスト
			my $Perl_Response = system 'perl', '-wc', "./$My_name.txt";
			Error('98', $Perl_Response) if $Perl_Response;

			# 名前書き換え
			rename "$Collect_PATH/$My_name.txt", "$Collect_PATH/$My_name.cgi" or Error('96', $!); # 名前変更に失敗
			chmod $CGI_Permission, "$Collect_PATH/$My_name.cgi"; # パーミッションを合わせる。
			$GetList = 2; # 取得ＯＫ
		}
		else {
			# お取り込みに失敗したら何もしない。
			Error('97',$Response->status_line); # 取得に失敗
		}
	}

	Error('00') if $GetList == 1; # リストのみ取得成功
	Error('01') if $GetList == 2; # リスト＋丁稚どん取得成功

	# おしまい。
	exit;
}

__END__

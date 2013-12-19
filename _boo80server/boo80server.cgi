#!/usr/bin/perl -w
use CGI;
use LWP::UserAgent;
use HTTP::Request;
use HTTP::Status;

$|=1			;
$cgi = new CGI		;

##############################################################################
$result = "He(She) doesn't use any proxy."			;
$xxx    = ""		;#受け取ったURL
$srTime = ""		;#受け取った時刻
$srID   = ""		;#受け取ったID
$koredaHOST = ""	;#取り出してきたIP
$koredaREMO = ""	;#取り出してきたリモホ
$ita = ""		;#板名
$key = ""		;#スレッド番号
$fName			;#ログのファイル名
##############################################################################

&readArgument		;

&getRemoteHost		;

&htmlOut("Done-xxx-----xxx$koredaHOST-xxx-----xxx$koredaName-xxx-----xxx$koredaREMO-xxx-----xxx")	;

exit			;
##############################################################################
##############################################################################
sub getRemoteHost
{
	if(!open(LOGDAT,"$fName"))	{&htmlOut("Good bye 2111 ログファイルが開けませんでした");}
	@loglog = <LOGDAT>		;
	close(LOGDAT)			;
	foreach(@loglog)
	{
		chomp($_);
		#FOX ★<>sage<>03/09/06 20:35 IDIDIDID<>TEST<>123<>リモホ<>IP<>456
		($dmy0,$dmy1,$logTime,$dmy3,$dmy4,$logRemoteHost,$logRemoteAddr,$dmy7) = split(/<>/,$_)	;
		if($logTime eq '')		{next;}
		if($logRemoteHost eq '')	{next;}
		if($logRemoteAddr eq '')	{next;}
		if($logTime =~ /$srTime/)
		{
			if($logTime !~ /$srID/){next;}
			$koredaName=$dmy0		;
			$koredaREMO=$logRemoteHost	;
			$koredaHOST=$logRemoteAddr	;
			return				;
		}
	}
	&htmlOut("Good bye 2222　探せなかった。存在しない。");
}
##############################################################################
sub readArgument
{
	$ppp = $cgi->param('kinsan')	;
	if($ppp ne 'sugoi')	{&htmlOut("500 Server error");}	

	$xxx = $cgi->param('boo80')	;
	$xxx =~ s/ //g			;
	if($xxx eq '')			{&htmlOut("Good bye 1122 URLがない");}

	$srTime = $cgi->param('boo80time')	;
	if($srTime eq '')		{&htmlOut("Good bye 1111　時刻がない");}
# 050406 曜日に対応。曜日がなくても通る。 by さ
	if($srTime !~ /..\/..\(?.*\)? ..:../)	{&htmlOut("Good bye 1112　時刻の形が違う");}
	$srID   = $cgi->param('boo80id')	;
	if($srID eq "???")		{&htmlOut('Good bye 1113　ID が ??? の時は何も入れないでください');}

	if($xxx !~ /2ch\.net\//)	{&htmlOut("Good bye 1222 URL がおかしい");}
	$xxx =~ /([a-z0-9]+)\.2ch\.net\/test\/read.cgi\/([0-9A-Za-z]+)\/([0-9]+)/;
	if(!$1 || !$2 || !$3)		{&htmlOut("Good bye 1333 URLがおかしい、そんな板スレッドはない");}
	$ita = $2			;
	$key = $3			;
	$cmd0 = $2 . "dat/$3"		;
	$fName = "../../test/ggg/$cmd0" . ".cgi"	;
	if(!(-e $fName)) 		{&htmlOut("Good bye 1444 ログがなかった。");}
}
##############################################################################
sub htmlOut
{
print "Content-Type: text/plain\n\n";
print "$_[0]";
	exit;
}
##############################################################################
exit;
#
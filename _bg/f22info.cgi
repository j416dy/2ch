;#################################
sub setF22info
{
	my ($bbs) = @_	;

	$resNumMax  = 700		;
	$resNumMaxL = $resNumMax + 50	;
	$daresNum = 20			;
	$daresDay = 14*24		;

	$Rule150 = 9999			;

	if($bbs eq 'liveuranus')	{$resNumMax  = 300;$resNumMaxL = $resNumMax + 8;}
	if($bbs eq 'news4vip')
	{
		$resNumMax  = 700		;
		$resNumMaxL = $resNumMax + 20	;
		$daresNum = 120		;
		$daresDay = 4		;	#hour
		$Rule150 = 7		;
	}
	if($bbs eq 'news')
	{
		$Rule150 = 2			;
		$resNumMax  = 350		;
		$resNumMaxL = $resNumMax + 30	;
		$daresDay = 4			;	#hour
	}
	if($bbs eq 'poverty')
	{
		$Rule150 = 2			;
		$resNumMax  = 300		;
		$resNumMaxL = $resNumMax + 50	;
		$daresDay = 1*24		;	#hour
	}
	if($bbs eq 'morningcoffee')
	{
		$Rule150 = 120			;
		$daresNum = 10		;
		$daresDay = 7*24	;	#hour
		$Rule150 = 120		;
	}
	if($bbs eq 'market')		{$resNumMax  = 300;$resNumMaxL = $resNumMax + 8;}
	if($bbs eq 'stock')		{$resNumMax  = 300;$resNumMaxL = $resNumMax + 8;$daresNum = 30;$daresDay = 4*24;}
	if($bbs eq 'ogame')		{$resNumMax  = 300;$resNumMaxL = $resNumMax + 8;$daresNum = 30;$daresDay = 4*24;}
	if($bbs eq 'ogame3')		{$resNumMax  = 300;$resNumMaxL = $resNumMax + 8;$daresNum = 30;$daresDay = 4*24;}
	if($bbs eq 'stockb')		{$resNumMax  = 300;$resNumMaxL = $resNumMax + 8;$daresNum = 30;$daresDay = 4*24;}
	if($bbs eq 'mmonews')		{$resNumMax  = 300;$resNumMaxL = $resNumMax + 8;$daresNum = 30;$daresDay = 4*24;}
	if($bbs eq 'warhis')	{$Rule150 = 99999	;$daresDay=14*24;}
	if($bbs eq 'anime4vip')	{$Rule150 = 90	;$resNumMax=250;$resNumMaxL=280;}
	if($bbs eq 'campus')	{$Rule150 = 30	;}
	if($bbs eq 'accuse')	{$Rule150 = 30	;$daresNum = 10;$daresDay = 3*24;}
	if($bbs eq 'ad')	{$Rule150 = 30	;}
	if($bbs eq 'pc2nanmin')	{$Rule150 = 99999	;}

	if($bbs eq 'mnewsplus')		{$Rule150 = 4	;}
	if($bbs eq 'newsplus')		{$Rule150 = 4	;}
	if($bbs eq 'moeplus')		{$Rule150 = 60	;}

	if($bbs eq 'namazuplus')	{$Rule150 = 60	;}
	if($bbs eq 'femnewsplus')	{$Rule150 = 60	;}
	if($bbs eq 'scienceplus')	{$Rule150 = 60	;}
	if($bbs eq 'owabiplus')		{$Rule150 = 60	;}

	if($bbs eq 'news5plus')		{$Rule150 = 60	;}
	if($bbs eq 'liveplus')		{$Rule150 = 30	;}
	if($bbs eq 'wildplus')		{$Rule150 = 30	;}
#	if($bbs eq 'dqnplus')		{$Rule150 = 30	;}

	if($bbs eq 'bizplus')		{$Rule150 = 30	;}
	if($bbs eq 'news4plus')		{$Rule150 = 30	;}

	if($bbs eq 'comicnews')		{$Rule150 = 150	;}
	if($bbs eq 'musicnews')		{$Rule150 = 150	;}

	if($bbs eq 'livemarket1')	{$resNumMax  = 300;$resNumMaxL = $resNumMax + 50;}
	if($bbs eq 'livemarket2')	{$resNumMax  = 300;$resNumMaxL = $resNumMax + 50;}
	if($bbs eq 'liveplus')		{$starRule = {NonMax => 20, StarMax => 380, CAP => 1};}

	$rotateLog = [ 'news4vip' ]	;
}
##################################
1;

RegRead, VPN, HKEY_CURRENT_USER, Software\Psiphon3, UserSkipVPN
if %VPN% = 0
{
	RegWrite, REG_DWORD, HKEY_CURRENT_USER, Software\Psiphon3, UserSkipVPN, 1
	TrayTip, 切换至SSH模式, 已切换至SSH模式。,3,1
}
else
{
	RegWrite, REG_DWORD, HKEY_CURRENT_USER, Software\Psiphon3, UserSkipVPN, 0
	TrayTip, 切换至VPN模式, 已切换至VPN模式。,3,1
}
;为了保持TrayTip存在
Sleep,2500
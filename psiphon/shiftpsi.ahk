RegRead, VPN, HKEY_CURRENT_USER, Software\Psiphon3, UserSkipVPN
if %VPN% = 0
{
	RegWrite, REG_DWORD, HKEY_CURRENT_USER, Software\Psiphon3, UserSkipVPN, 1
	TrayTip, �л���SSHģʽ, ���л���SSHģʽ��,3,1
}
else
{
	RegWrite, REG_DWORD, HKEY_CURRENT_USER, Software\Psiphon3, UserSkipVPN, 0
	TrayTip, �л���VPNģʽ, ���л���VPNģʽ��,3,1
}
;Ϊ�˱���TrayTip����
Sleep,2500
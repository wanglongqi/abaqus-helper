#! coding:utf8
#该脚本会设置Psiphon3的注册表选项中的是否使用VPN项，以方便两种模式的切换。
import _winreg  as reg
key = reg.OpenKey(reg.HKEY_CURRENT_USER, r'Software\Psiphon3', 0, reg.KEY_ALL_ACCESS)
k,t=reg.QueryValueEx(key, "UserSkipVPN")
if k == 0:
    reg.SetValueEx(key,"UserSkipVPN",0,t,1)
else:
    reg.SetValueEx(key,"UserSkipVPN",0,t,0)
reg.CloseKey(key)

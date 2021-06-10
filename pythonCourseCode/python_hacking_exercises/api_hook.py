#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2020/11/17 16:16 
# @Author   : wangqiang
# @File     : api_hook.py  
# @Project  : python_course
# @Python   : 3.7.5
import utils, sys
from pydbg import *
from pydbg.defines import *

"""
BOOL WINAPI WriteFile( 
    _InHANDLE hFile, 
    _InLPCVOID 1pBuffer, 
    _InDWORD nNumberofBytesToWrite, 
    _out_optLPDWORD 1pNumberofBytesWritten, 
    _Inout_opt_LPOVERLAPPED 1pOverlapped 
）;
"""
dbg = pydbg()
isProcess = False
orgPattern = "love"
repPattern = "hate"
processName = "notepad.exe"

"""1.声明回调函数：声明回调函数，发生调试事件时调用。该函数内部含有钩取代码。"""
def replacestring(dbg, args):
    """2.读取内存值：从指定地址读取指定长度的内存地址，并返回其中值。
    内存中保存的值被记录到文件。（kernel32.ReadProcessMemory)"""
    buffer = dbg.read_process_memory(args[1], args[2])

    """3.在内存值中检查模式：在内存值中检查是否有想修改的模式。"""
    if orgPattern in buffer:
        print("[APTHoOking] Before: %s" % buffer)
        """4.修改值：若搜到想要的模式，则将其修改为黑客指定的值。"""
        buffer = buffer.replace(orgPattern, repPattern)
        """5.写内存：将修改值保存到内存。这是黑客希望在回调函数中执行的操作。
        将love修改为hate，并保存到内存。（kernel32.WriteProcessMemory)"""
        replace = dbg.write_process_memory(args[1], buffer)
        print("[APIHooking] After: %s" % dbg.read_process_memory(args[1], args[2]))
    return DBG_CONTINUE

"""6.获取进程D列表：获取Windows操作系统运行的所有进程ID列表。
（kemel32.CreateToolhelp32Snapshot)"""
for (pid, name) in dbg.enumerate_processes():
    if name.lower() == processName:
        isProcess = True
        hooks = utils.hook_container()
        """7.获取进程句柄：获取用于操纵进程资源的句柄，保存到类的内部。进程需要的动作通过句柄得到支持。
        （kermel32.OpenProcess、kernel32.DebugActiveProcess)"""
        dbg.attach(pid)
        print("Saces a process handle in self.h_process of pid[%d]" % pid)

        """8.获取要设置断点的函数地址：使用句柄访问进程的内存值。查找目标Win32API，返回相应地址。"""
        hookAddress = dbg.func_resolve_debuggee("kernel32.dll", "WriteFile")

        if hookAddress:
            """9.设置断点：向目标函数设置断点，注册回调函数，发生调试事件时调用。"""
            hooks.add(dbg, hookAddress, 5, replacestring, None)
            print("sets a breakpoint at the designated address: 0x%08x" % hookAddress)
            break
        else:
            print("Error:couldnot resolve hook address")
            sys.exit(-1)

if isProcess:
    print("waiting for occurring debugger event")
    """10.启动调试：无限循环状态下，等待调试事件发生。调试事件发生时，调用回调函数。"""
    dbg.run()
else:
    print("Error:There in no process [%s]" % processName)
    sys.exit(-1)
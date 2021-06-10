#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2020/11/19 15:59 
# @Author   : wangqiang
# @File     : dll_injection2.py  
# @Project  : pythonCrouse
# @Python   : 3.7.5
# -*- coding: utf-8 -*-
from ctypes import *
import psutil
import win32api


def injectDll(string=None):
    PAGE_READWRITE = 0x04
    PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
    VIRTUAL_MEM = (0x1000 | 0x2000)

    dll_path = 'd://softdp//pyworkspace//wechat_demo//WechatDB.dll'.encode('ascii', 'ignore')

    dll_len = len(dll_path)
    print(dll_len)
    kernel32 = windll.kernel32

    # 第一步获取整个系统的进程快照
    pids = psutil.pids()
    # 第二步在快照中去比对进程名
    for pid in pids:
        p = psutil.Process(pid)
        if p.name() == string:
            break
    print('pid:', pid)
    # 第三步用找到的pid去打开进程获取到句柄

    h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, int(pid))
    if not h_process:
        print('could not acquire a handle to pid')

    arg_adress = kernel32.VirtualAllocEx(h_process, None, dll_len, VIRTUAL_MEM, PAGE_READWRITE)
    written = c_int(0)
    whhh = kernel32.WriteProcessMemory(h_process, arg_adress, dll_path, dll_len, byref(written))
    print('arg_address:%x' % arg_adress, whhh)

    h_kernel32 = win32api.GetModuleHandle('kernel32.dll')
    h_loadlib = win32api.GetProcAddress(h_kernel32, 'LoadLibraryA')
    print('%x' % h_kernel32, '%x' % h_loadlib)
    thread_id = c_ulong(0)
    handle = kernel32.CreateRemoteThread(h_process, None, 0, h_loadlib, arg_adress, 0, byref(thread_id))
    print(handle)
    return h_kernel32
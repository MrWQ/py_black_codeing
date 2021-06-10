#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2020/12/16 16:14 
# @Author   : ordar
# @File     : file_monitor.py
# @Project  : dll_injection2.py
# @Python   : 3.7.5
import tempfile
import threading
import win32file
import win32con
import os


# 1. 典型的临时文件所在目录
dirs_to_monitor = ['c:\\WINDOWS\\Temp', tempfile.gettempdir()]
print(dirs_to_monitor)

# 文件修改行为对应常量
FILE_CREATED = 1
FILE_DELETED = 2
FILE_MODIFIED = 3
FILE_RENAMED_FROM = 4
FILE_RENAMED_TO = 5


def start_monitor(path_to_watch):
    FILE_LIST_DIRECTORY = 0x0001

    # 2. 获取需要监控的文件目录的句柄
    h_directory = win32file.CreateFile(path_to_watch, FILE_LIST_DIRECTORY,
                                       win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
                                       None, win32con.OPEN_EXISTING, win32con.FILE_FLAG_BACKUP_SEMANTICS, None)
    while True:
        try:
            # 3. 监控目录改变
            results = win32file.ReadDirectoryChangesW(h_directory, 1024, True,
                                                      win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                                                      win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                                                      win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                                                      win32con.FILE_NOTIFY_CHANGE_SIZE |
                                                      win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                                                      win32con.FILE_NOTIFY_CHANGE_SECURITY,
                                                      None, None)
            # 4. 枚举改变类型
            for action, file_name in results:
                full_filename = os.path.join(path_to_watch, file_name)
                if action == FILE_CREATED:
                    print('[+] Created %s' % full_filename)
                elif action == FILE_DELETED:
                    print('[-] Deleted %s' % full_filename)
                elif action == FILE_MODIFIED:
                    print('[*] Modified %s' % full_filename)
                    # 输出文件内容
                    print("[*] Dumping contents:")
                    # 5. 尝试读取文件内容
                    try:
                        with open(full_filename, 'rb') as f:
                            print(f.read())
                        print("[*] Dump Success")
                    except:
                        print('[-] Dump Filed')
                elif action == FILE_RENAMED_FROM:
                    print('[>] Renamed from %s' % full_filename)
                elif action == FILE_RENAMED_TO:
                    print('[<] Renamed to %s' % full_filename)
                else:
                    print('[-] Unknown: %s' % full_filename)
        except:
            pass


# 为每个监控器创建一个线程
for path in dirs_to_monitor:
    monitor_thread = threading.Thread(target=start_monitor, args=(path,))
    monitor_thread.start()
    print("[+] File monitor thread for path : %s" % path)

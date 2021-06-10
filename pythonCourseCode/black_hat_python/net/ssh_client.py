#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2020/11/24 10:54 
# @Author   : ordar
# @File     : ssh_client.py  
# @Project  : pythonCourse
# @Python   : 3.7.5
from paramiko.client import SSHClient, AutoAddPolicy


# ssh认证，认证通过返回ssh连接
def ssh_connect(host_ip, host_port, username, passwd):
    ssh_client = SSHClient()
    try:
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.connect(host_ip, int(host_port), username=username, password=passwd)
    except Exception as e:
        print(e)
        exit(1)
    return ssh_client


# 通过ssh连接执行命令
def ssh_command(ssh_client, cmd):
    try:
        stdin, stdout, stderr = ssh_client.exec_command(cmd)
        print(stdout.read().decode())
    except Exception as e:
        print(e)


if __name__ == '__main__':
    ssh_client = ssh_connect("172.28.131.166", 22, "root", "aoeyuvcyber123..")
    while True:
        cmd = input("<ssh command #>")
        if cmd == 'exit':
            ssh_client.close()
            exit(0)
        ssh_command(ssh_client, cmd)

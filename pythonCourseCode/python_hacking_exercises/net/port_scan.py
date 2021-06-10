#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2020/11/24 17:13 
# @Author   : ordar
# @File     : port_scan.py  
# @Project  : pythonCourse
# @Python   : 3.7.5
import nmap

# 创建 PortScanner对象：在Python中创建PortScanner对象，以使用nmap。
# 若尚未在PC中安装Nmap程序，则会触发PortScanner异常。
nm = nmap.PortScanner()
#     运行端口扫描：接收2~3个参数，执行端口扫描。
#     主机：使用类似于scanme.nmap.org、198.116.0-255.1-127或216.163.128.20/20形式，设置主机信息。
#     端口：使用类似于22,53，110，143-4564的形式，设置要扫描的端口。
#     参数：使用类似于-sU-sX-sC的形式，设置运行Nmap所需选项。
nm.scan("127.0.0.1", "1-10")

# 获取主机列表：以列表形式返回scan）函数参数指定的主机信息。
for host in nm.all_hosts():
    print("[*] Host: {}({})".format(host, nm[host].hostname()))
    print("[*] State: {}".format(nm[host].state()))
    for proto in nm[host].all_protocols():
        print("[*] Protool: {}".format(format(proto)))
        lport = list(nm[host][proto].keys())
        lport.sort()
        for port in lport:
            print("[*] Port:{} State: {}".format(port, nm[host][proto][port]))

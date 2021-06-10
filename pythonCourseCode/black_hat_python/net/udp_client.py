#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2020/11/20 14:30 
# @Author   : ordar
# @File     : udp_client.py  
# @Project  : pythonCrouse
# @Python   : 3.7.5
import socket

# 定义我们的目标
target_host = "127.0.0.1"
target_port = 80
# 目标应该用元组的格式
target = (target_host, target_port)

# 建立一个socket对象
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 发送一些数据
client.sendto("AABBCC".encode('utf-8'), target)

# 接受返回的数据,客户端接受数据需要指定缓存区最大长度,指定接收的大小 为1024字节
data, address = client.recvfrom(1024)

print(data)

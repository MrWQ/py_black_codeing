#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2020/11/20 14:08 
# @Author   : ordar
# @File     : tcp_client.py
# @Project  : pythonCrouse
# @Python   : 3.7.5
import socket

# 定义我们的目标
target_host = "localhost"
target_port = 8080
# 目标应该用元组的格式
target = (target_host, target_port)

# 建立一个socket对象
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 建立连接
client.connect(target)

# 发送一些数据，这里我们发送一个GET请求,python3只接收btye流
client.send("GET / HTTP/1.1\r\n\r\n".encode('utf-8'))

# 接受返回的数据,客户端接受数据需要指定缓存区最大长度,指定接收的大小 为1024字节
respon = client.recv(1024)

print(respon)

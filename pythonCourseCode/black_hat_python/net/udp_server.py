#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2020/11/20 15:18 
# @Author   : ordar
# @File     : udp_server.py  
# @Project  : pythonCourse
# @Python   : 3.7.5
import socket

# 定义允许连接此服务端的ip和服务端端口，0.0.0.0代表任意ip都可以连接这个服务端
bind_ip = "0.0.0.0"
bind_port = 80
# 服务地址应该是元组格式
bind_server = (bind_ip, bind_port)

# 建立一个socket对象
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 1.服务端绑定服务地址到套接字， ("127.0.0.1", 80)，即本地主机的 UDP 80 端口。
server.bind(bind_server)
print("UDP bond on {}:{}".format(bind_ip, bind_port))

# 循环等待客户端连接
while True:
    # 2.接收客户端发来的数据，包括 bytes 对象 data，以及客户端的 IP 地址和端口号 addr，其中 addr 为二元组 (host, port)。
    data, address = server.recvfrom(1024)
    print("Received from {}".format(address))
    print("Received data: {}".format(data))
    # 返还一个数据包
    server.sendto("UDP ACK".encode('utf-8'), address)


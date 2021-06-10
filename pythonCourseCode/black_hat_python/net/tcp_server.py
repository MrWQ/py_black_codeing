#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2020/11/20 14:43 
# @Author   : ordar
# @File     : tcp_server.py  
# @Project  : pythonCourse
# @Python   : 3.7.5
import socket
import threading

# 定义允许连接此服务端的ip和服务端端口，0.0.0.0代表任意ip都可以连接这个服务端
bind_ip = "0.0.0.0"
bind_port = 80
# 服务地址应该是元组格式
bind_server = (bind_ip, bind_port)

# 建立一个socket对象
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 1.服务端绑定服务地址到套接字，
server.bind(bind_server)
# 2.监听端口，backlog 指定在拒绝连接之前，操作系统可以挂起的最大连接数量。该值至少为 1，大部分应用程序设为 5 就可以了。
server.listen(5)
print("Listen on {}:{}".format(bind_ip, bind_port))


# 3.定义客户端处理线程,打印客户端传来的数据并回应
def handle_client(client_socket):
    request = client_socket.recv(1024)
    print("Received: {}".format(request))
    # 返还一个数据包，然后关闭连接
    client_socket.send("ACK".encode('utf-8'))
    client_socket.close()


# 循环等待客户端连接
while True:
    # 4.被动接受TCP客户端连接,(阻塞式)等待连接的到来
    client, address = server.accept()
    print("Accept connection from: {}:{}".format(address[0], address[1]))

    # 创建客户端线程，处理传入的数据
    client_handle_thread = threading.Thread(target=handle_client, args=(client,))
    # 5.启动线程
    client_handle_thread.start()





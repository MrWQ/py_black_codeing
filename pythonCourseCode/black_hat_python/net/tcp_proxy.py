#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2020/11/23 17:00 
# @Author   : ordar
# @File     : tcp_proxy.py  
# @Project  : pythonCourse
# @Python   : 3.7.5
import sys
import socket
import threading


# 监听函数，接收本地请求
def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except:
        print("Failed to listen on {}:{}".format(local_host, str(local_port)))
        sys.exit(0)
    print("Listen on {}:{}".format(local_host, str(local_port)))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        # 打印连接信息
        print("[==>] Received incoming connection form {}:{}".format(local_host, str(local_port)))
        # 启动线程处理请求
        client_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))
        client_thread.start()


def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    # 如果必要，先从远程主机获取数据
    if receive_first:
        remote_buffer = received_from(remote_socket)
        print(hexdump(remote_buffer))

        # 发送给响应处理，修改包
        remote_buffer = response_handler(remote_buffer)
        # 如果有数据，发送给本地客户端
        if remote_buffer:
            print("[<==] Sending {} bytes to localhost.".format(str(len(remote_buffer))))
            client_socket.send(remote_buffer)

    # 从本地循环读取数据，然后发送给远程主机和本地主机
    while True:
        local_buffer = received_from(client_socket)
        if local_buffer:
            print("[==>] Received {} bytes from localhost.".format(str(len(local_buffer))))
            print(hexdump(local_buffer))    # 这个是修改前的请求
            local_buffer = request_handler(local_buffer)
            print(hexdump(local_buffer))    # 这个是修改后的请求
            remote_socket.send(local_buffer)
            print("[==>] Send to remote.")

        remote_buffer = received_from(remote_socket)
        if remote_buffer:
            print("[<==] Received {} bytes from remote.".format(str(len(remote_buffer))))
            print(hexdump(remote_buffer))   # 这个是修改前的请求
            remote_buffer = response_handler(remote_buffer)
            print(hexdump(remote_buffer))   # 这个是修改后的请求
            client_socket.send(remote_buffer)
            print("[<==] Send to localhost.")

        # 如果两边都没有数据，关闭连接
        if not local_buffer and remote_buffer:
            client_socket.close()
            remote_socket.close()
            print("[*] No more data.closing connections")
            break


# 数据接收函数，从tcp连接中接收数据。因为有多个地方要从tcp连接中接收数据，所以封装一个函数来处理。
def received_from(connection):
    buffer = b""
    # 设置10的超时
    connection.settimeout(10)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except:
        pass
    return buffer


def hexdump(src):
    # 此处转储流量，比如保存流量到文件
    with open('a.txt', 'a') as f:
        f.write(src.decode('utf-8'))
    return src


# 对目标是远程主机的请求进行修改
def request_handler(buffer):
    # 执行修改
    buffer = buffer.decode('utf-8').replace("GET", "HEAD").encode('utf-8')
    return buffer


# 对目标是本地主机的响应进行修改
def response_handler(buffer):
    # 执行修改
    return buffer


if __name__ == '__main__':
    if len(sys.argv[1:]) != 5:
        print("Usage: tcp_proxy.py [local_host] [local_port] [remote_host] [remote_port] [receive_first]")
        print("Example: tcp_proxy.py 127.0.0.1 9999 192.168.1.2 80 True")
        sys.exit(0)

    # 设置本地监听参数
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    # 设置远程目标
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    # 告诉代理在发送给远程主机之前先连接和接受远程数据
    receive_first = sys.argv[5]
    if "true" in receive_first.lower():
        receive_first = True
    else:
        receive_first = False

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

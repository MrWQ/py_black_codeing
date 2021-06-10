#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2020/12/9 9:57 
# @Author   : ordar
# @File     : tcp_tunnel.py  
# @Project  : pythonCourse
# @Python   : 3.7.5
import socket
import sys
import re
from threading import Thread

class TCP_Client(object):
    """
    处理TCP请求和响应
    """
    def __init__(self,src_addr=None,dst_addr=None):
        self.src_addr = src_addr
        self.dst_addr = dst_addr

    def request(self,data):
        return data

    def response(self,data):
        return data

class HTTP_Client(TCP_Client):
    """
    处理HTTP请求和响应
    """
    def request(self,data):
        data = re.sub('Host:.*?\r\n','Host: %s:%s\r\n'%(self.dst_addr),data.decode())
        return data.encode()


# 自定义路由
ROUTES = [
    {
        'name'      :'HTTP',
        'addr'      :('127.0.0.1',80),
        'route'     :b'^(GET|POST)',
        'client'      :HTTP_Client,
    },{
        'name'      :'SSH',
        'addr'      :('127.0.0.1',22),
        'route'     :b'^SSH',
        'client'      :TCP_Client,
    },{
        'name'      :'RDP',
        'addr'      :('127.0.0.1',3389),
        'route'     :b'^\x03\x00\x00',
        'client'      :TCP_Client,
    },{
        'name'      :'JRMP',
        'addr'      :('127.0.0.1',8009),
        'route'     :b'^JRMI',
        'client'      :TCP_Client,
    },{
        'name'      :'PostgreSQL',
        'addr'      :('127.0.0.1',5432),
        'route'     :b'^\x00\x00\x00\x08\x04',
        'client'      :TCP_Client,
    },{
        'name'      :'Oracle',
        'addr'      :('127.0.0.1',1521),
        'route'     :b'^\x00(\xec|\xf1)\x00\x00\x01\x00\x00\x00\x019\x01',
        #'route'     :b'\(DESCRIPTION=\(CONNECT_DATA=\(SERVICE_NAME=',
        'client'      :TCP_Client,
    },{
        'name'      :'MSSQL',
        'addr'      :('127.0.0.1',1433),
        'route'     :b'^\x12\x01\x00',
        'client'      :TCP_Client,
    },{
        'name'      :'NC',
        'addr'      :('127.0.0.1',51),
        'route'     :b'.*',
        'client'      :TCP_Client,
    }
]


class TCP_Tunnel(Thread):
    """
    TCP隧道。
    """
    SOCKS = {}
    def __init__(self,srcsock,srcaddr):
        Thread.__init__(self)
        # 来源套接字
        self.srcsock = srcsock
        # 来源地址
        self.srcaddr = srcaddr
        # 目标套接字
        self.dstsock = self.SOCKS[srcsock] if srcsock in self.SOCKS else socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # 标志位，判断是否保持连接
        self.iskeep  = True

    def handle_thread(self, dstsock, srcsock):
        """
        线程处理函数，从目标地址接收响应并返回给来源地址
        :param dstsock:
        :param srcsock:
        :return:
        """
        while self.iskeep:
            try:
                buff = dstsock.recv(10240)
            except Exception as e:
                break
            buff = self.client.response(buff)
            print('recv',buff)
            srcsock.sendall(buff)
            if not buff:
                self.iskeep = False
                break
        srcsock.close()

    def run(self):
        """
        逻辑处理函数，通过正则表达式匹配请求的流量特征来判断是哪一个服务，从而转发流量到对应服务的端口
        :return: 
        """
        while self.iskeep:
            # 接收源地址的请求
            try:
                buff = self.srcsock.recv(10240)
            except Exception as e:
                break
            if not buff:
                self.iskeep = False
                break
            # 通过正则表达式匹配请求符合哪个路由，然后创建对应的客户端对象
            if self.srcsock not in self.SOCKS:
                for value in ROUTES:
                    # 正在表达式匹配
                    if re.search(value['route'],buff,re.IGNORECASE):
                        print('[+]Connect %s%s <--> %s'%(value['name'],str(value['addr']),str(self.srcaddr)))
                        # 创建客户端对象
                        self.client = value['client'](self.srcaddr, value['addr'])
                        self.dstsock.connect(value['addr'])
                        break
                self.SOCKS[self.srcsock] = self.dstsock
                # 创建线程并启动
                Thread(target=self.handle_thread, args=(self.dstsock, self.srcsock,)).start()
            buff = self.client.request(buff)
            print('send',buff)
            self.dstsock.sendall(buff)
        self.dstsock.close()
        print('[+]DisConnect %s%s <--> %s'%(value['name'],str(value['addr']),str(self.srcaddr)))


class Socket_Proxy(object):
    """
    代理在本机某个端口，默认是1111端口
    """
    def __init__(self,host='0.0.0.0',port=1111,listen=100):
        self.host = host
        self.port = port
        self.listen = listen
        self.socks = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socks.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socks.bind((self.host,self.port))

    def start(self):
        self.socks.listen(self.listen)
        print('Start Proxy Listen - %s:%s'%(self.host,self.port))
        while True:
            sock,addr = self.socks.accept()
            T = TCP_Tunnel(sock, addr)
            T.start()


if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except:
        port = 1111
    try:
        c = Socket_Proxy('0.0.0.0', port)
        c.start()
    except KeyboardInterrupt:
        sys.exit()

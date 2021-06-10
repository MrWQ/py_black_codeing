#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2020/11/24 16:01 
# @Author   : ordar
# @File     : arp_poison.py
# @Project  : pythonCourse
# @Python   : 3.7.5
from scapy.all import *
import os
import sys
import threading
import signal

from scapy.layers.l2 import Ether, ARP


def restore_tartget():
    pass


# 通过ip获取到mac地址
def get_mac(ip_address):
    resopnses, unanswered = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip_address), timeout=3, retry=5)
    # 从响应中获取MAC地址
    for s, r in resopnses:
        return r[Ether].src
    return None


# 投毒线程
def poison_target(gateway_ip, gateway_mac, target_ip, target_mac):
    poison_tar = ETH_P_ARP()
    poison_tar.op = 2
    poison_tar.psrc = gateway_ip
    poison_tar.pdst = target_ip
    poison_tar.hwdst = target_mac



if __name__ == '__main__':
    interface = "eth2"
    target_ip = "192.168.181.1"
    gateway_ip = "192.168.181.1"
    packet_count = 1000

    # # 关闭输出
    # conf.verb = 0

    print("[*] Setting up {}".format(interface))

    # 获取网关mac地址
    gateway_mac = get_mac(gateway_ip)
    print(gateway_mac)
    if gateway_mac is None:
        print("[-] Failed to get gateway MAC.")
        sys.exit(0)
    else:
        print("[*] Gateway {} is at {}".format(gateway_ip, gateway_mac))

    # 获取目标机器mac地址
    target_mac = get_mac(target_ip)
    if gateway_mac is None:
        print("[-] Failed to get target MAC.")
        sys.exit(0)
    else:
        print("[*] Target {} is at {}".format(gateway_ip, gateway_mac))

    # poison_thread = threading.Thread(target=poison_target, args=(gateway_ip, gateway_mac, target_ip, target_mac))
    # poison_thread.start()
    # try:
    #     print("[*] Start sniffer for {} packets".format(str(packet_count)))
    #     packets = sniff(filter="ip host {}".format(target_ip), iface=interface, count=packet_count)
    #
    #     # 将捕获到底数据包输出到文件
    #     wrpcap('arp_poison.pcap', packets)
    #
    #     # 还原网络设置
    #     restore_tartget()
    #
    # except:
    #     restore_tartget()
    #     sys.exit(0)


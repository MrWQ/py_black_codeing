#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2020/11/24 15:20 
# @Author   : ordar
# @File     : sniffer.py
# @Project  : pythonCourse
# @Python   : 3.7.5
from scapy.all import *

def packet_callback(packet):
    if packet["TCP"].payload:
        sniffer_packet = packet["TCP"].payload
        # if "user" in str(sniffer_packet).lower() or "pass" in str(sniffer_packet).lower():
        print("[*] Server: {}".format(packet["IP"].dst))
        print("[*] {}".format(sniffer_packet))


sniff(filter="tcp port 21", prn=packet_callback, store=0)

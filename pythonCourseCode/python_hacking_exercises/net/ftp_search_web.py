#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2020/11/25 9:51 
# @Author   : ordar
# @File     : ftp_search_web.py  
# @Project  : pythonCourse
# @Python   : 3.7.5
from ftplib import FTP

dir_list = [""]
path_list = []


# 列出ftp目录里的所有文件
def find_web(ftp):
    global dir_list
    while len(dir_list):
        this_dir = dir_list[len(dir_list) - 1]
        new_dir_list = ftp.nlst(this_dir)
        dir_list = dir_list[0:len(dir_list) - 1]
        if new_dir_list:
            # 判断为文件,将文件路径添加到path_list
            if len(new_dir_list) == 1 and new_dir_list[0] == this_dir:
                path_list.append(this_dir)
            else:
                # 判断为文件夹且文件夹内容不为空,将新的list添加到dir_list，参与循环
                dir_list.extend(new_dir_list)
        else:
            # 判断为空文件夹，什么都不做
            pass
        # print(dir_list)
    # 路径列表排序
    path_list.sort()
    print(path_list)
    write_to_file(path_list)


# 将文件路径写入文件
def write_to_file(path_list):
    with open('file_path.txt', 'w') as f:
        for path in path_list:
            f.write(path + '\n')


if __name__ == '__main__':
    ftp = FTP("172.28.131.166", "test", "test")
    find_web(ftp)

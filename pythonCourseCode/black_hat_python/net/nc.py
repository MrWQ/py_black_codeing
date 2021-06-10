#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2020/11/20 15:49 
# @Author   : ordar
# @File     : nc.py  
# @Project  : pythonCourse
# @Python   : 3.7.5
import sys
import socket
import getopt
import threading
import subprocess

# 定义一些全局变量
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0


# 创建主函数处理命令行参数和调用我们编写的其他函数
def usage():
    print("My netcat")
    print("Usage: nc.py -t target_host -p port")
    print("-l --listen                  - listen on [host]:[port] for incoming connections")
    print("-e --execute=file_to_run     - execute the given file upon receiving a connection")
    print("-c --command                 - initialize a command shell")
    print("-u --upload=destination      - upon receiving connection upload a file and write to [destination]")
    print("\n\n")
    print("Examples:")
    print("nc.py -t 192.168.0.1 -p 5555 -l -c")
    print("nc.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
    print("nc.py -t 192.168.0.1 -p 5555 -l -e='cat /etc/passwd'")
    print("echo 'abcd122334' | ./nc.py -t 192.168.0.1 -p 5555")
    sys.exit(0)


def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    # 读取命令行参数
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
                                   ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as e:
        print(str(e))
        usage()
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--command"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"
    # 判断监听还是从标准输入发送数据
    if listen:
        # 执行监听函数，因为这个函数还没有实现，所以IDE里这里报错
        server_loop()
    if not listen and len(target) and port > 0:
        # 从命令行读数据
        # 这里将阻塞，所以不向标准输入发送数据是发送CTRL-D
        # buffer = sys.stdin.read()
        buffer = input("")
        # 执行发送数据函数，因为这个函数还没有实现，所以IDE里这里报错
        client_sender(buffer)


# 发送数据函数，用pass占位符简单实现
def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # 连接到目标主机
        client.connect((target, port))
        # 发送数据
        if buffer:
            client.send(buffer.encode('utf-8'))
        while True:
            # 等待回传
            recv_len = 1
            response = ""
            # 通过循环以4096字节为大小来获取全部数据，
            # 如果数据小于4096就跳出循环
            # 如果数据大于4096就以4096为单位循环获取，直到剩余数据小于4096，小于4096时跳出循环
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data.decode('utf-8')
                if recv_len < 4096:
                    break
            print(response)

            # 等待更多输入
            buffer = input("")
            buffer += "\n"
            client.send(buffer.encode('utf-8'))

    except Exception as e:
        print(e)
        print("[*] Execption! exiting.")
    finally:
        client.close()


# 监听函数，用pass占位符简单实现
def server_loop():
    global target
    # 如果没有定义目标，那么监听所有
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # 启动线程处理请求
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()


# 处理请求函数，先用pass占位符简单实现
def client_handler(client_socket):
    global upload
    global execute
    global command

    # 检测上传文件
    if upload_destination:
        # 读取所有的字符
        file_buffer = b""
        # 持续读取直到没有符合的数据
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer += data
        # 将数据写到目标文件
        try:
            with open(upload_destination, 'wb') as f:
                f.write(file_buffer)
                client_socket.send("Successfully save file to {}".format(upload_destination).encode('utf-8'))
        except Exception as e:
            print(e)
            client_socket.send("Failed to save file to {}".format(upload_destination).encode('utf-8'))
    # 检测命令执行，执行单次命令
    if execute:
        output = run_command(execute)
        client_socket.send(output.encode('utf-8'))

    # 如果需要一个命令行shell，那么进入一个循环
    if command:
        while True:
            client_socket.send("<nc:#>".encode('utf-8'))
            # 接受数据直到出现换行符
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024).decode('utf-8')
            print("Received: {}".format(cmd_buffer))
            # 将命令输出结果返回
            response = run_command(cmd_buffer)
            client_socket.send(response.encode('utf-8'))


# 执行命令函数
def run_command(command):
    # 处理末尾换行
    command = command.rstrip()
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        output = output.decode('utf-8')
    except Exception as e:
        print(e)
        output = "Failed to execute command."
    return output


if __name__ == '__main__':
    main()

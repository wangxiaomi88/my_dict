from socket import *
from multiprocessing import Process
import signal, sys, os
from getpass import getpass

def do_search(name):
    while True:
        word=input("请输入单词，$退出：")
        if word == "$":
            return
        else:
            msg = "Q %s %s" % (name, word)
            s.send(msg.encode())
            data=""
            while True:
                frame = s.recv(128).decode()
                data += frame
                if frame[-1]=="$":
                    break



            temp=data.split("#")
            if temp[0]=="OK":
                print(temp[1])
            elif temp[0]=="FAIL":
                print("查无此词")


def do_hist(name):
    print("以下是%s的查询记录："%(name))
    msg = "H %s" % (name)
    s.send(msg.encode())
    data = ""
    while True:
        frame = s.recv(128).decode()
        if frame[-1] == "$":
            break
        data += frame

    temp = data.split("|")
    for line in temp:
        print(line)



def interface_second(name):
    while True:
        print("""
        =============================
        1.查单词 2.历史记录 3.注销
        =============================
        """)
        cmd = input("请输入二级界面指令：")

        if cmd == "1":
            do_search(name)
        elif cmd == "2":
            do_hist(name)
        elif cmd == "3":
            return
        else:
            print("二级界面指令错误")


def do_register():
    while True:
        name = input("用户名：")
        passwd = getpass("密码：")
        passwd_check = getpass("密码确认：")

        if passwd != passwd_check:
            print("密码确认错误")
            continue
        if (" " in name) or (" " in passwd):
            print("用户名和密码中不能有空格")
            continue

        msg="R %s %s"%(name,passwd)
        s.send(msg.encode())
        data = s.recv(128).decode()
        if data=="OK":
            print("注册成功")
            interface_second(name)
        else:
            print("注册失败")
        return


def do_login():
    name = input("用户名：")
    passwd = getpass("密码：")

    msg = "L %s %s" % (name, passwd)
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == "OK":
        print("登录成功")
        interface_second(name)
    else:
        print("登录失败")
    return



# 服务器地址
HOST = "127.0.0.1"
PORT = 8000
ADDR = (HOST, PORT)
s = socket()
s.connect(ADDR)


# 启动函数
def main():
    while True:
        print("""
        ==============================
        1.注册  2.登录  3.退出
        ==============================
        """)

        cmd = input("请输入一级界面指令：")
        if cmd == "1":
            do_register()
        elif cmd == "2":
            do_login()
        elif cmd == "3":
            s.send("E".encode())
            s.close()
            break
        else:
            print("请输入正确选项")


if __name__ == "__main__":
    main()

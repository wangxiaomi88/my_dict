from socket import *
from multiprocessing import Process
import signal, sys, os
from dict_db import Database
import time

HOST = "127.0.0.1"
PORT = 8000
ADDR = (HOST, PORT)

db=Database()

def do_search(c,name,word):
    db.record(name,word)
    flag,mean=db.search(name,word)
    if flag:
        msg="OK#"+mean+"#$"
        c.send(msg.encode())
    else:
        msg = "FAIL#"+"$"
        c.send(msg.encode())


def do_hist(c,name):
    r=db.hist(name)
    for line in r:
        msg="条目"+str(line[0])+"，用户名："+line[2]+"，查询单词："+line[3]+"，查询时间："+str(line[4])+"；"+"|"
        c.send(msg.encode())

    time.sleep(0.1)
    c.send("$".encode())

def do_register(c,name,passwd):
    if db.register(name,passwd):
        c.send("OK".encode())
    else:
        c.send("FAIL".encode())

def do_login(c,name,passwd):
    if db.login(name,passwd):
        c.send("OK".encode())
    else:
        c.send("FAIL".encode())



# 处理客户端请求
def new_client(c):
    db.create_cur() #每个子进程分别生成一个游标

    while True:
        data = c.recv(1024).decode()
        temp=data.split(" ")
        # print(c.getpeername(),":",data)
        if temp[0] == "R":
            do_register(c,temp[1],temp[2])
        elif temp[0] == "L":
            do_login(c,temp[1],temp[2])
        elif temp[0] == "Q":
            do_search(c,temp[1],temp[2])
        elif temp[0] == "H":
            do_hist(c,temp[1])
        elif temp[0] == "E" or not temp:
            break

    db.cur.close()
    c.close()
    print("该用户已退出")







# 启动函数
def main():
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(5)


    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    print("开始监听端口8000")

    while True:
        try:
            c, addr = s.accept()
            print("连接到来自{}的请求".format(addr))

        except KeyboardInterrupt:
            s.close()
            db.close()
            sys.exit()
        except Exception as e:
            print(e)
            continue

        p = Process(target=new_client, args=(c,))
        p.daemon = True
        p.start()



if __name__ =="__main__":
    main()
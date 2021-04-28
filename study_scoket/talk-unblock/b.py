#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 
# @File    : server.py

import threading
from threading import Lock,Thread
import socket


HOST = "127.0.0.1"
PORT = 8009
get_link = 0


client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #声明socket类型，同时生成链接对象
try:
    client.connect((HOST,PORT)) #建立一个链接，连接到本地的6969端口
    get_link = 1
    #尝试链接

except ConnectionRefusedError:
    print("Can not find server")
    get_link = 0

msg = "online-----------"
client.sendall(msg.encode('utf-8'))  #发送一条信息 python3 只接收btye流
        
count = 0
def talk(t1):

    while get_link:

        user_input = input("b: ")
        msg = "-----------"+user_input+"-----------" 
        client.sendall(msg.encode('utf-8'))  #发送一条信息 python3 只接收btye流
        #print("waiting...")

        # if msg == "-----------"+"end"+"-----------":
        #     print("unlinking")
        #     client.close() 
        #     break
        #     #当用户输入end则关闭链接


def listen(t1):

    while get_link:

        global count
        data = client.recv(4096) #接收一个信息，并指定接收的大小 为4096字节
        print('other:'+str(count),data.decode()) #输出我接收的信息



t1 = threading.Thread(target=listen,args=('t1',))     # target是要执行的函数名（不是函数），args是函数对应的参数，以元组的形式存在
t2 = threading.Thread(target=talk,args=('t1',))

t1.start()
t2.start()
#if get_link:
    #当链接成功



    #t1.start()
    # if msg == "-----------"+"end"+"-----------":
    #     print("unlinking")
    #     client.close() 
    #     break
    #     #当用户输入end则关闭链接
    #t2.start()


    
    

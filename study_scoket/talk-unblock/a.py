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


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# IPV4 TCP

sock.bind((HOST, PORT))
sock.listen( 100)
conn, addr = sock.accept()
sock.setblocking(False)
count = 0
def listen(t1):

    while True:
        global count
        request = conn.recv( 4096) #等待接收信息，阻塞
        msg = request.decode()
        
        count +=1
        print("other: "+str(count),msg)
        # if msg == "-----------"+"end"+"-----------":
        #     #客户端断开链接
        #     print("b leave...")
        #     print("waiting link...")
        #     conn, addr = sock.accept()#等待客户端接入，阻塞
        #     print("someone online")

# def online(t1):
#     while True:
#         conn, addr = sock.accept()#等待客户端接入，阻塞
#         print("someone online")

def talk(t1):

    while True:
        user_input = input("a: ")
        content = "-----------"+user_input+"-----------"
        conn.sendall(content.encode('utf-8'))

#进入
#离开
#发消息
#监听

if __name__ =="__main__":

    t1 = threading.Thread(target=listen,args=('t1',))     # target是要执行的函数名（不是函数），args是函数对应的参数，以元组的形式存在
    t2 = threading.Thread(target=talk,args=('t1',))
#t3 = threading.Thread(target=online,args=('t1',))   
    




    #信息接受
    t1.start()
    t2.start()
#t3.start()
    # if msg == "-----------"+"end"+"-----------":
    #     #客户端断开链接
    #     print("b leave...")
    #     print("waiting link...")
    #     conn, addr = sock.accept()#等待客户端接入，阻塞
    #     print("someone online")



    #信息发送 btye

#sock.close() #关闭这个链接  
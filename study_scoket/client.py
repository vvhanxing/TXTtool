#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：client.py
import socket               # 导入 socket 模块
longth = 8
s = socket.socket()         # 创建 socket 对象
host = "127.0.0.1" # 获取本地主机名
port = 54321            # 设置端口好
s.connect((host, port))
length = 8



def handler(var):
    print("handler "+var)

def recv_msg(socket_obj, handler, length=8, sep="$$"):
    """receive datas from socket, and convey complete messages to message hander.
    
    Args:
      socket_obj: socket object,
      handler: function object with str param
      length: length of receiving data everytime 
      sep: the signal to split receiving strings into complete messages
    
    Returns:
      Bool, False means the socket is cloesd by the other endpoint. 

    """
    data = ''
    while True:
        new_data = socket_obj.recv(length).decode()
        print("new_data",new_data)
        if not new_data:
            print("[Main][Socket] receive empty data")
            return False
        data += new_data
        print("[Socket Raw Msg] %s" % data)

        splits = data.split(sep)
        for _ in range(len(splits) - 1):
            handler(splits.pop(0))
        if not splits[0]:
            print("finish recv")
            break

        else:
            data = splits[0]
            print("[Socket Raw Msg] remain incomplete data: %s" % data)

    print data,len(data)
    socket_obj.sendall(data)
    print("-----------------------")
    return True
#
while True:

    recv_msg(s,handler)

s.close()
        


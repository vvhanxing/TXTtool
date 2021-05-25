#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket              
import random
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)       
host = "127.0.0.1"  
port = 54321
print(host, "port", port)
s.bind((host, port))     
s.listen(5)                 

info = ["0--0","1--1","EN$$"]

req, addr = s.accept() 


def run(count):
    
    msg = ""
    for i in range(2):
        msg += random.choice(info)
    
    msg = msg+str(count)+"$$"
    msg = "".join(["#" for i in range(16-len(msg))])+msg

    print(count,msg)
    req.sendall(msg.encode()) 
    req.recv(1024)

count = 0 
while True:
    #req, addr = s.accept()
    count += 1
    run(count)
    if count>1000:
        #s.close()
        req, addr = s.accept()
        #break
    
    # req.sendall(b"12345aaabcde$$12$$abcdef$$end") 



# -*- coding: utf-8 -*-
"""
Created on Sat Oct 01 16:27:33 2016

@author: gopal_a
"""
import zmq
import sys

port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)
    
if len(sys.argv) > 2:
    port1 =  sys.argv[2]
    int(port1)

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:%s" % port)
if len(sys.argv) > 2:
    socket.connect ("tcp://localhost:%s" % port1)
socket.setsockopt(zmq.SUBSCRIBE, 'AAPL')

while True:
    data = socket.recv()
    print(data)
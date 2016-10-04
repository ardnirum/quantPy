# -*- coding: utf-8 -*-
"""
Created on Sat Oct 01 10:03:55 2016

@author: gopal_a
"""
import zmq
import random
import sys
import time

port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)
context  = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)

AAPL = 100.0

while True:
    AAPL += random.gauss(0, 1)
    msg = 'AAPL %f' % AAPL
    socket.send(msg)
    print(msg)
    time.sleep(random.random() * 3)
    
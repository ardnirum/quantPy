# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 17:58:18 2016

@author: gopal_a
"""

import zmq
import time
import random
context = zmq.Context()

socket = context.socket(zmq.PUB)
socket.bind('tcp://0.0.0.0:9999')

number = 100.

while True:
    number += random.gauss(0, 1)
    print('number %.3f' % number)
    socket.send_string('number %.3f' % number)
    time.sleep(random.random())
    
    
socket = context.socket(zmq.SUB)
socket.connect('tcp://0.0.0.0:9999')
socket.setsockopt(zmq.SUBSCRIBE, 'number')

while True:
    data = socket.recv_string()
    print(data)
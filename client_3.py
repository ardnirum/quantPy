# -*- coding: utf-8 -*-
"""
Created on Sat Oct 01 16:27:33 2016

@author: gopal_a
"""
import zmq
import pandas as pd
import datetime

df = pd.DataFrame()
t1 = 5
t2 = 10

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect('tcp://0.0.0.0:9999')
socket.setsockopt(zmq.SUBSCRIBE, 'AAPL')

position = 0
while True:
    data = socket.recv_string()
    print(data)
    sym, value = data.split()
    value = float(value)
    ticktime = datetime.datetime.now()
    df = df.append(pd.DataFrame({'price': value}, index = [ticktime]))
    #if len(df) >= t2:
    df['t1'] = df['price'].rolling(t1).mean()
    df['t2'] = df['price'].rolling(t2).mean()
    print(df.ix[-1])
    if position is in [0, -1]:
        if df.t1.ix[-1] > df.t2.ix[-1]:
            position = 1
            print('\ngoing long\n')
            # send buy order to broker
            # ...
    if position is in [0, 1]:
        if df.t1.ix[-1] < df.t2.ix[-1]:
            positon = -1
            print('\ngoing short\n')
            # send sell order ot broker
            # ....

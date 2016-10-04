# -*- coding: utf-8 -*-
"""
Created on Sat Oct 01 16:52:23 2016

@author: gopal_a
"""
import zmq
import sys
import json
import datetime
import plotly.plotly as ply
from plotly.graph_objs import *
# plotly realtime plotting
pc = json.load(open('C:\Users\gopal_a\.plotly\.credentials', 'r'))
sids = pc['stream_ids']
ply.sign_in('ardnirum', pc['api_key'])
# setup plotly
stream0 = Stream(maxpoints=100, token=sids[0])
trace0 = Scatter(x=[], y=[], name='AAPL', mode='lines+markers', stream=stream0)
dats = Data([trace0])
layout = Layout(title='Real-Time AAPL Stock Price')
fig = Figure(data=dats, layout=layout)

url = ply.plot(fig, filename='epat', auto_open=True)
s0 = ply.Stream(sids[0])
s0.open()
#ZeroMq sockets
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
    data = socket.recv_string()
    print(data)
    sym, value = data.split()
    x = str(datetime.datetime.now())[11:-4]
    y = float(value)
    s0.write({'x': x, 'y': y})
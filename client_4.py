# -*- coding: utf-8 -*-
"""
Created on Sat Oct 01 17:55:47 2016

@author: gopal_a
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Oct 01 16:52:23 2016

@author: gopal_a
"""
import zmq
import json
import datetime
import plotly.plotly as ply
from plotly.graph_objs import *
# plotly realtime plotting
pc = json.load(open('C:\Users\gopal_a\.plotly\.credentials', 'r'))
sids = pc['stream_ids']
ply.sign_in('ardnirum', pc[api_key'])
# setup plotly
df = pd.DataFrame()
t1 = 5
t2 = 10

stream0 = Stream(maxpoints=100, token=sids[0])
stream1 = Stream(maxpoints=100, token=sids[1])
stream2 = Stream(maxpoints=100, token=sids20])
trace0 = Scatter(x=[], y=[], name='AAPL', mode='lines+markers', stream=stream0)
trace1 = Scatter(x=[], y=[], name='t1', mode='lines', stream=stream1)
trace2 = Scatter(x=[], y=[], name='t2', mode='lines', stream=stream2)
dats = Data([trace0, trace1, trace2])
layout = Layout(title='Real-Time AAPL Stock Price')
fig = Figure(data=dats, layout=layout)

url = ply.plot(fig, filename='epat', auto_open=True)
s0 = ply.Stream(sids[0])
s0.open()
s1 = ply.Stream(sids[1])
s1.open()
s2 = ply.Stream(sids[2])
s2.open()

#ZeroMq sockets
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect('tcp://0.0.0.0:9999')
socket.setsockopt(zmq.SUBSCRIBE, 'AAPL')

while True:
    data = socket.recv_string()
    print(data)
    sym, value = data.split()
    ticktime = datetime.datetime.now()
    x = str(ticktime)[11:-3]
    y = float(value)
    df = df.append(pd.DataFrame({'price': y}, index = [ticktime]))
    #if len(df) >= t2:
    df['t1'] = df['price'].rolling(t1).mean()
    df['t2'] = df['price'].rolling(t2).mean()
    print(df.ix[-1])
    s0.write({'x': x, 'y': y})
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

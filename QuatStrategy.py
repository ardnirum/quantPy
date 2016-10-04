# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 17:22:53 2016

@author: gopal_a
"""

"""
Created on Tue Dec 22 16:56:08 2015

#http://www.quantifiedstrategies.com/trade-the-boring-consumer-stocks-when-they-open-down-and-yesterday-was-a-down-day/

@author: iRagecap
"""
import numpy as np
import pandas as pd
import pandas.io.data as web
import matplotlib.pyplot as plt
#Second, retrieve the data from, say, Google itself:
stock = web.DataReader('PFC.NS',data_source='yahoo',start='3/14/2009', end='4/14/2014')


#stratData = pd.DataFrame(index=ohlc.index)

Data = pd.DataFrame(stock)

del Data['Volume']

#Data.plot()

#plt.plot(Data['Open'])
#Data.Open

Data['cc'] = 100*Data['Close'].pct_change()
#Per_Data['Open']=100*Data.Open.pct_change()
Data[['Close','cc']].head(15)
#stratData['cc'] = Data.Close.pct_change()# close-to-close change in %
Data['co'] = 100*(Data['Open']/Data['Close'].shift(1)-1) # previous close to open change in %
Data['oc'] = 100*(Data['Close']/Data['Open']-1) # open to close change in %
#Data.plot()
#plt.plot(Data[['Close','cc','co','oc']])

#Data.cumsum().plot(grid=True)

indicator = (Data['cc']<-0.25).shift(1) & (Data['co'] < -0.1) # find days that satisfy the strategy rules
indicator[0] = False # fill first entry with False (needed because .shift(1) adds a NaN in the first element)

Data['buy'] = indicator
Data['pnl'] = 0. # init pnl column with zeros (Watch out: if initialized with integer value (0), an error will pop later on)
Data['pnl'][indicator] = Data['oc'][indicator] # set pnl column values to daily return wehere 'goLong' is true

Data.head(20) # show last 10 rows of stratData 

#Data['pnl'].cumsum().plot(grid=False)
Data2=Data['pnl'].cumsum()
plt.plot(Data2)
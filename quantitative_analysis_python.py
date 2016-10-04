# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 14:59:11 2016

@author: gopal_a
"""
import numpy as np
import statsmodels.api as sm
import statsmodels.tsa.stattools as ts
import numpy as np
import pandas as pd
import pandas.io.data as web
import matplotlib.pylab as plt

#regression analysis

data1 = web.DataReader('^NSEI', data_source='yahoo',
start='4/4/2008', end='4/4/2016')

data2 = web.DataReader('ACC.NS', data_source='yahoo',
start='4/4/2008', end='4/4/2016')

data1['key']=data1.index
data2['key']=data2.index
result = pd.merge(data1, data2, on='key')

x1=result['Close_x']

y1=result['Close_y']

ret_data1 = np.log(x1 /x1.shift(1))

ret_data2 = np.log(y1 /y1.shift(1))

ret_data1 = ret_data1[~np.isnan(ret_data1)]

ret_data2 = ret_data2[~np.isnan(ret_data2)]


model = pd.ols(y=ret_data2, x=ret_data1)


plt.plot(ret_data1, ret_data2)
ax = plt.axis() # grab axis values
x = np.linspace(ax[0], ax[1] + 0.01)
plt.plot(x, model.beta[1] + model.beta[0] * x, 'b', lw=2)
plt.grid(True)
plt.axis('tight')
plt.xlabel('Nifty Returns')
plt.ylabel('ACC Returns')


np.correlate(ret_data1,ret_data2)


pd.rolling_corr(ret_data1,ret_data2,window=252).plot(grid=True, style='b')

# Augmented Dicky Fuller Test

stock = web.DataReader('AMBUJACEM.NS', data_source='yahoo',
start='4/4/2008', end='4/4/2016')

x=stock['Close']


ret_stock = np.log(x /x.shift(1))


ret_stock = ret_stock[~np.isnan(ret_stock)]

lag=1


ts.adfuller(ret_stock,lag)

########################################

#Cointegration


data1 = web.DataReader('AMBUJACEM.NS', data_source='yahoo',
start='4/4/2008', end='4/4/2016')


data2 = web.DataReader('ACC.NS', data_source='yahoo',
start='4/4/2008', end='4/4/2016')


data1['key']=data1.index

data2['key']=data2.index

result = pd.merge(data1, data2, on='key')


x1=result['Close_x']


y1=result['Close_y']


coin_result = ts.coint(x1, y1)

score = coin_result[0]

pvalue = coin_result[1]

x1.plot()

y1.plot()

diff_series= x1 - y1

diff_series.plot()


#http://statsmodels.sourceforge.net/devel/generated/statsmodels.tsa.stattools.adfuller.html


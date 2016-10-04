# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 15:41:24 2016

@author: gopal_a
"""
#%%
import numpy as np
import pandas as pd
import pandas.io.data as web
import matplotlib.pyplot as plt

# kst oscillator
# r1,r2, r3 and r4 stand for ROC periods in days
# n1, n2, n3 and n4 stand for SMA in days

def KST(df, r1, r2, r3, r4, n1, n2, n3, n4, s):
    M = df['Close'].diff(r1)
    N = df['Close'].shift(r1)
    ROC1 = (M/N)*100
    M = df['Close'].diff(r2)
    N = df['Close'].shift(r2)
    ROC2 = (M/N)*100
    M = df['Close'].diff(r3)
    N = df['Close'].shift(r3)
    ROC3 = (M/N)*100
    M = df['Close'].diff(r4)
    N = df['Close'].shift(r4)
    ROC4 = (M/N)*100
    KST = pd.Series(pd.rolling_mean(ROC1, n1) +
                    pd.rolling_mean(ROC2, n2) * 2 +
                    pd.rolling_mean(ROC3, n3) * 3 +
                    pd.rolling_mean(ROC4, n4) * 4, name = 'KST')
    Sig = pd.Series(pd.rolling_mean(KST, s), name='Signal')
    print KST, Sig
    df = df.join(KST)
    df = df.join(Sig)
    return df
    

data = web.DataReader('ACC.NS', data_source='yahoo', start='9/9/2012',
                      end='9/8/2016')
data = pd.DataFrame(data)

data = KST(data, 10, 15, 20, 30, 10, 10, 10, 15, 9)

# Removing NA
data = data.dropna()
ndays = data.shape[0]

data['Trade'] = pd.Series(np.zeros(ndays), name='Trade')
k = data['KST']
s = data['Signal']
t = data['Trade']

# 1 for buy and -1 for sell
# we buy and sell at the closing price

for i in range(1, ndays):
    if k[i-1] <= s[i-1] and k[i] > s[i]:
        t[i] = 1
    if k[i-1] >= s[i-1] and k[i] < s[i]:
        t[i] = -1

data = data.dropna()
ndays = data.shape[0]
Initial_equity = 10000
Brokerage = 20

# Add colmns to the existing dataframe and initialize them to zero
data['Starting Capital'] = 10000
sc = data['Starting Capital']
data['Profit_Loss'] = 0
pl = data['Profit_Loss']
data['Capital_available'] = 10000
cp = data['Capital_available']
data['Shares'] = 0
sh = data['Shares']
data['Invested'] = 0
vs = data['Invested']
data['Cash'] = 0
cash = data['Cash']

for i in range(ndays):
    if i == 0:
        sc[i] = Initial_equity
        pl[i] = 0
        cp[i] = sc[i] + pl[i]
        sh[i] = np.floor((cp[i] - Brokerage)/data['Close'][i])
        vs[i] = sh[i] * data['Close'][i]
        cash[i] = cp[i] - vs[i]
    else:
        sc[i] = vs[i-1]+cash[i-1]
        if data['Trade'][i] == -1:
            pl[i] = (data['Close'][i-1]-data['Close'][i])*sh[i-1]-Brokerage
        else:
            pl[i] = (data['Close'][i]-data['Close'][i-1])*sh[i-1]-Brokerage
        cp[i] = sc[i]+pl[i]
        if i < (ndays - 1):
            sh[i] = np.floor(cp[i] / data['Close'][i] + Brokerage)
            vs[i] = sh[i] * data['Close'][i]
            cash[i] = cp[i] - vs[i]
        else:
            sh[i] = 0
            vs[i] = 0
            cash[i] = cp[i]

data.to_csv('ATP-3-Batch30.csv')
#%%
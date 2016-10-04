# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 17:10:45 2016

@author: gopal_a
"""

from pandas.io.data import DataReader
ticker = "SPY"
source = 'yahoo'
start = '01/01/2012'
end = '03/22/2014'
spy = DataReader(ticker, source, start, end)
print spy.head()
print spy.tail()
spy.to_csv('D:\\SPY.csv')

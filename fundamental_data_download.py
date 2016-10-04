# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 15:08:09 2016

@author: gopal_a
"""
#%%
import time
import urllib2

from urllib2 import urlopen

nse=["ACC.NS", "ADANIPORTS.NS", "AMBUJACEM.NS"]

def KeyStats(stock):
    try:
        sourceCode=urllib2.urlopen('https://in.finance.yahoo.com/q/ks?s='+stock).read()
        pbr=sourceCode.split('Price/Book (mrq):</td><td class="yfnc_tabledata1">')[1].split('</td')[0]
        print('price to book raito:', stock, pbr)
        
    except Exception, e:
        print 'failed in the loop', str(e)
        
for eachStock in nse:
    KeyStats(eachStock)
#%%
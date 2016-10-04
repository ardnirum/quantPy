# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 15:55:20 2016

@author: gopal_a

complex number class re-implemented (partl)
"""

class Complex(object):
    def __init__ (self, real, imag):
        self.real = real
        self.imag = imag
        
    def __repr__(self):
        if self.imag >= 0:
            return '(%s+%sj)' % (self.real, self.imag)
        else:
            return '(%s%sj)' % (self.real, self.imag)
        
        
    def __add__(self, other):
        return Complex(self.real + other.real, self.imag + other.imag)
        
    def __sub__(self,other):
        return Complex(self.real - other.real, self.imag - other.imag)
        


#%%
#
# Implementing a mean variance portfolio class
#
import numpy as np
import pandas as pd
from pandas_datareader import data as web

class mean_variance_portfolio(object):
    def __init__(self, symbols, weights):
        self.symbols = symbols
        self.weights = weights
        self.get_data()
    
    def get_data(self):
        self.data = pd.DataFrame()
        for sym in self.symbols:
            self.data[sym] = web.DataReader(sym, data_source='yahoo')['Adj Close']
        self.returns = np.log(self.data / self.data.shift(1)).dropna()
    
    def calculate_return(self):
        return np.dot(self.returns.mean() * 252, self.weights)
        
    def calculate_volatility(self):
        return np.dot(self.weights, np.dot(self.returns.cov() *252, self.weights))
        
    def equal_weights(self):
        noa = len(self.symbols)
        self.weights = noa *[1. / noa]
    
    def add_symbol(self, symbol):
        self.symbols.append(symbol)
        self.get_data()
        self.equal_weights()
        
    def remove_symbol(self, symbol):
        self.symbols.remove(symbol)
        self.get_data()
        self.equal_weights()
        
    def simulate_weights(self, N):
        prets = []
        pvols = []
        for i in range(N):
            w = np.random.random(len(self.symbols))
            w /= w.sum()
            self.weights = w
            prets.append(p.calculate_return())
            pvols.append(p.calculate_volatility())
        return pvols, prets
        
    
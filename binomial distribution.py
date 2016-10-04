# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 17:18:26 2016

@author: gopal_a
"""

from math import exp

dt = input("Enter the timestamp:")
S = input("Enter the stock price:")
r = input("Enter risk free interest rate:")
K = input("Enter the option strike price:")
p = input("Enter the asset growht probability:")
u = input("Enter the asset growth factor:")
N = input("Enter the number of steps till expiration")
call = raw_input("Is this call or put option? (C/P)").upper().startswith("C")

# to compute stock price after k timestamps, us growth and k-us fall
def price(k, us):
    return S*(u**(2*us-k))
    

def bop(k, us):
    stockPrice = price(k, us)
    if call:
        exerciseProfit = max(0, stockPrice - K)
    else:
        exerciseProfit = max(0, K - stockPrice)

    if k == N:
        return exerciseProfit
    decay = exp(-r * dt)
    expected = p * bop(k+1, us+1) + (1 - p) * bop(k+1, us)
    binomial = decay * expected
    return max(binomial, exerciseProfit)
    
print 'Computed option price: $%.2f'% bop(0,0)
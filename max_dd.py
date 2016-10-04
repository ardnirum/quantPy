# -*- coding: utf-8 -*-
"""
Created on Fri Sep 09 16:37:44 2016

@author: gopal_a
"""

import numpy as np
import matplotlib.pyplot as plt
n = 1000
xs = np.random.randn(n).cumsum()
i = np.argmax(np.maximum.accumulate(xs) - xs) # end of the period
j = np.argmax(xs[:i]) # start of period

plt.plot(xs)
plt.plot([i, j], [xs[i], xs[j]], '*', color='Red', markersize=10)
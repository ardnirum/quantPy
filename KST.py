
# Load the required packages and modules 
import numpy as np
import pandas as pd
import pandas.io.data as web
import matplotlib.pyplot as plt

# KST Oscillator function
# r1,r2,r3,r4 stand for the ROC periods in days, while n1,n2,n3,n4 stand for the
# SMA for these ROC periods respectively. s stands for the SMA days used for 
# computing the signal line from the KST values.
def KST(df, r1, r2, r3, r4, n1, n2, n3, n4,s):  
    M = df['Close'].diff(r1)  
    N = df['Close'].shift(r1)  
    ROC1 = (M / N)*100
    M = df['Close'].diff(r2)  
    N = df['Close'].shift(r2)  
    ROC2 = (M / N)*100
    M = df['Close'].diff(r3)  
    N = df['Close'].shift(r3)  
    ROC3 = (M / N)*100
    M = df['Close'].diff(r4)  
    N = df['Close'].shift(r4)  
    ROC4 = (M / N)*100
    KST = pd.Series(pd.rolling_mean(ROC1, n1) + pd.rolling_mean(ROC2, n2) * 2 + 
          pd.rolling_mean(ROC3, n3) * 3 + pd.rolling_mean(ROC4, n4) * 4, name = 'KST')  
    Sig = pd.Series(pd.rolling_mean(KST, s), name = 'Signal')
    df = df.join(KST)  
    df = df.join(Sig)
    #df = df.round(2)
    return df
    
# Retrieve the S&P 500 data from Yahoo finance:
data = web.DataReader('AAPL',data_source='yahoo',start='6/18/2014', end='1/1/2016')
data = pd.DataFrame(data['Close']) 

# Applying the KST function on the Closing price of GSPC
data = KST(data, 10,15,20,30,10,10,10,15,9)

# Removing the rows with NAs
data = data.dropna()

ndays = data.shape[0]
data['Trade'] = pd.Series(np.zeros(ndays),name='Trade')
k = data['KST'] 
s = data['Signal']
t = data['Trade']

# 1 stands for buy and -1 for Sell. 
# Assumption - buying/selling at the close price when we get the signals
for i in range (1, ndays):
    if k[i-1] <= s[i-1] and k[i] > s[i]:
        t[i] = 1               
    if k[i-1] >= s[i-1] and k[i] < s[i]:
        t[i] = -1

# Plotting the Price Series chart and the KST Oscillator below
fig = plt.figure(figsize=(7,5))
ax = fig.add_subplot(2, 1, 1)
ax.set_xticklabels([])
plt.plot(data['Close'],lw=1.5)
plt.title('S&P 500 Price Chart')
plt.ylabel('Close Price')
plt.grid(True)
bx = fig.add_subplot(2, 1, 2)
plt.plot(k,'k',lw=1.5,label='KST')
plt.plot(s,'r',lw=1.5,label='Signal Line')
plt.legend(loc=0,prop={'size':9})
plt.ylabel('KST & Signal line values')
plt.grid(True)
plt.setp(plt.gca().get_xticklabels(), rotation=30)

# Keeping only the rows with Buy/Sell Signals
data = data.dropna()

ndays = data.shape[0] # Computing the number of rows in the data frame

Initial_equity = 100000  # Initial Equity
Brokerage      = 0.50    # Dollars per share

# Adding Columns to the existing data frame and initializing them to 0
data['StartingCapital'] = 0 ; data['Profit_Loss'] = 0 ; data['Capital_Availabel'] = 0 ; 
data['Shares'] = 0 ; data['Invested'] = 0 ; data['Cash'] = 0;

# Assigning a short name to the columns
sc = data['StartingCapital'] ; pl = data['Profit_Loss'] ; cp = data['Capital_Availabel'];
sh = data['Shares'] ; vs = data['Invested'] ; cash = data['Cash'] ; 

# Computing the Starting Capital, Invested Capital, Cash, 
# Shares bought and PL for each trade undertaken based on the signals
for i in range(ndays):    
   if i == 0:
      sc[i] = Initial_equity
      pl[i] = 0
      cp[i] = sc[i] + pl[i]
      sh[i] = np.floor(cp[i] / (data['Close'][i] + Brokerage))
      vs[i] = sh[i] * data['Close'][i]
      cash[i] = cp[i] - vs[i]      
   else: 
      sc[i] = vs[i-1] + cash[i-1]
      if data['Trade'][i] == 1 :
         pl[i] = (data['Close'][i-1] - data['Close'][i] - Brokerage) * sh[i-1]
      else:
         pl[i] = (data['Close'][i] - data['Close'][i-1] - Brokerage) * sh[i-1]
      cp[i] = sc[i] + pl[i]      
      if i < (ndays-1):      
         sh[i] = np.floor(cp[i] / (data['Close'][i] + Brokerage))
         vs[i] = sh[i] * data['Close'][i]
         cash[i] = cp[i] - vs[i]      
      else:
         sh[i] = 0
         vs[i] = 0
         cash[i] = cp[i]
    
# Writing the output to a csv file
data.to_csv('KST Oscillator Strategy.csv')

# Plotting the Strategy Performance
plt.figure(figsize=(7,4))
plt.plot(cp,lw=1.5)
plt.plot(cp,'ro')
plt.grid(True)
plt.title('KST Oscillator Strategy Performance')
plt.xlabel('Dates')
plt.ylabel('Equity ($)')
plt.setp(plt.gca().get_xticklabels(), rotation=30)



# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 01:57:15 2016

@author: gopal_a

1) Download all the Nifty stocks.
2) Calculate beta of each stock w.r.t Nifty using one year rolling window.
3) Divide the 50 stocks into two parts, high beta and low beta.
    Level of beta to be chosen based on the observation.
4) Every month go long on stocks with low beta & go short with high beta stocks
5) Re-balance the portfolio every month.

Decide on the back test date
Go back one year and start the test for a year
set startdate and enddate for the first month
GETDATA:::  Get data for the month
identify the beta for that month
first trading day of the following month
If the stock is not bought or sold
    If the stock beta is low, buy stock, subtract from the profit
    If the stock beta is high, sell stock, add to the profit
If the stock is already bought in portfolio
    If the stock beta is low, skip
    if the stock beta is high, sell and go short  - add twice to the profit
If the stock is already sold
    If the stock beta is high, skip
    If the stock beta is low, buy and go long - subtract twice from the profit
identify portfolio cost
write the record for the date to an excel
set startdate and enddate for the next month
GOTO GETDATA
"""
import pandas as pd
import numpy as np
import StringIO
import requests
import datetime as dt
from dateutil.relativedelta import relativedelta
from pandas_datareader import data as web  # data retrieval
#from contextlib import closing
#import csv


class ValidateDate(object):
    def __init__(self, datetest):
        self.datetest = datetest

    def get_wk_day(self):
        self.wkday = dt.datetime.weekday(self.datetest)
        if self.wkday == 5 or self.wkday == 6:
            print("%s is on a weekend %3d" % (str(self.datetest), self.wkday))
            return False
        else:
            print("%s is a weekday %3d" % (str(self.datetest), self.wkday))
            return True

    def get_first_trdngday_of_the_month(self):
        while len(web.DataReader('^NSEI', data_source='yahoo',
                                 start=self.datetest,
                                 end=self.datetest)['Adj Close']) == 0:
            self.datetest += relativedelta(days=1)
        return self.datetest


class GetTradeDetails(object):
    def __init__(self, datetest, symbol):
        self.datetest = datetest
        self.symbol = symbol

    def trade_price(self):
        tradeprice = float(0)
        while float(tradeprice) < 0.1:
            tradeprice = web.DataReader(self.symbol, data_source='yahoo',
                                 start=self.datetest,
                                 end=self.datetest)['Open']
            self.datetest += relativedelta(days=1)
#        print("\n", self.symbol, self.datetest, tradeprice)
        return float(tradeprice), dt.date.isoformat(self.datetest)

betathreshold = 1.0
BUY = 'BUY'
SELL = 'SELL'
url = "https://www.nseindia.com/content/indices/ind_nifty50list.csv"
csvfromurl = requests.get(url).content
csvfordf = pd.read_csv(StringIO.StringIO(csvfromurl.decode('utf-8')))  # StringIO with utf-8
nifty50df = pd.DataFrame(csvfordf)
histdata = {}
betadf = pd.DataFrame()
backtestdt = dt.date(2011, 01, 01)
startdate = dt.date(2010, 01, 01)
while dt.date.isoformat(backtestdt) > dt.date.isoformat(startdate):
    takeinput = raw_input("Continue")
    if str(takeinput).upper() != 'Y':
        break
    enddate = startdate + relativedelta(months=1) - relativedelta(days=1)
    histdata['NIFTY'] = web.DataReader('^NSEI', data_source='yahoo',
                                     start=startdate, end=enddate)['Adj Close']
    niftydf = pd.DataFrame(histdata['NIFTY'])
    niftydf['log_rets'] = np.log(niftydf['Adj Close'] /
                             niftydf['Adj Close'].shift(1))
    tempdf = pd.DataFrame(index=[dt.date.isoformat(enddate)])
    for eachscrip in nifty50df['Symbol']:
        scrip = eachscrip+'.NS'
        try:
            histdata[eachscrip] = web.DataReader(scrip, data_source='yahoo',
                                start=startdate, end=enddate)['Adj Close']
            stockdf = pd.DataFrame(histdata[eachscrip])
            stockdf['log_rets'] = np.log(stockdf['Adj Close'] /
                                     stockdf['Adj Close'].shift(1))
            result = pd.concat([niftydf, stockdf], axis=1)
            result.dropna(inplace=True)
            tempdf[eachscrip] = np.cov(result.ix[:, 1],
                                result.ix[:,3])[0][1] / np.var(result.ix[:, 1])
            getdtfollmth = ValidateDate(startdate + relativedelta(months=1))
            trddtfollmth = getdtfollmth.get_first_trdngday_of_the_month()
            trddetls = GetTradeDetails(trddtfollmth, scrip)
            trdprice, trddate = trddetls.trade_price()
            colnmp = eachscrip + " TRD PRC"
            colnmt = eachscrip + " TRD DTL"
            tempdf[colnmp] = float()
            tempdf[colnmt] = str()
            tempdf['Profit'] = float()
            try:
                if betadf[colnmt][-1] == BUY:
                    if tempdf[eachscrip][0] < betathreshold:
                        tempdf[colnmt][0] = betadf[colnmt][-1]
                        tempdf[colnmp][0] = betadf[colnmp][-1]
                    else:
                        tempdf[colnmt][0] = SELL
                        tempdf[colnmp][0] = -1 * trdprice
                        tempdf['Profit'][0]=(2 * trdprice - betadf[colnmp][-1])
                else:
                    if tempdf[eachscrip][0] < betathreshold:
                        tempdf[colnmt][0] = BUY
                        tempdf[colnmp][0] = trdprice
                        tempdf['Profit'][0]=(betadf[colnmp][-1] - 2 * trdprice)
                    else:
                        tempdf[colnmt][0] = betadf[colnmt][-1]
                        tempdf[colnmp][0] = betadf[colnmp][-1]
            except KeyError, e:
                print 'KeyError - reason "%s"\n' % str(e)
                if tempdf[eachscrip][0] < betathreshold:
                    tempdf[colnmt][0] = BUY
                    tempdf['Profit'][0] -= trdprice
                    tempdf[colnmp][0] = trdprice
                else:
                    tempdf[colnmt][0] = SELL
                    tempdf['Profit'][0] += trdprice
                    tempdf[colnmp][0] = -1 * trdprice
                continue
        except Exception, e:
            print scrip, str(e), startdate, enddate
            continue
    betadf = betadf.append(tempdf)
    startdate = startdate + relativedelta(months=1)
# dd = {k: histdata[k] for k in histdata.keys()[0:1]}

""""
try:
    nifty50 = pd.read_csv(url)
except urllib2.HTTPError, e:
    print e.fp.read()

content = nifty50.read()
print content

THIS GAVE AN ERROR ACCESS DENIED

import cStringIO
cccc=pd.read_csv(cStringIO.StringIO(s))         ## cStringIO without utf
i = 0
with closing(requests.get(url, stream=True)) as r:
    readerl = csv.reader(r.iter_lines(), delimiter=',', quotechar='"')
    for row in readerl:
        # Handle each row here...
        print row

chkdt = ValidateDate(backtestdt)
x12 = chkdt.get_wk_day()
x12 = chkdt.get_first_trdngday_of_the_month()
trddetls = GetTradeDetails(x12, 'ACC.NS')
trdprice1, trddate1 = trddetls.trade_price()


"""
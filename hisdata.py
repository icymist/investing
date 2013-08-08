#! /usr/bin/env python

from config import data_dir
import os
import pandas as pd
from pandas.tseries.offsets import DateOffset, BDay
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import date
import numpy as np
from dateparser import dateparser
import re
from indexconstituents import IndexConstituents as ic

company_names = ic().company_names

today = datetime.today()
today = datetime(today.year, today.month, today.day)

index_file = lambda index: os.path.join(data_dir, 'indices', index + '.csv')
stock_file = lambda bsecode: os.path.join(data_dir, 'stocks', bsecode+'.csv')

index_cols_1 = ['date', 'open', 'high', 'low', 'close', 'volume',
                'turnover', 'pe', 'pb', 'div_yield']
index_cols_2 = ['date', 'open', 'high', 'low', 'close',
                'shares_traded', 'turnover']
stock_cols = ['date', 'open', 'high', 'low', 'close', 'volume',
                        'bonus', 'divdend', 'd3', 'split']

class HistoricalData(object):
    def __init__(self, file_name, start=None, end=None, **kwargs):

        self._file = file_name

        self._df = pd.read_csv(self._file,
                               skiprows = kwargs.get('skiprows', 0),
                               header = None,
                               names = kwargs.get('cols'),
                               index_col = False)

        self._df.index = pd.to_datetime(self._df.date)


        if start:
            d = dateparser(start)
            #self._df = self._df[self._df.index >= d]
            self._df = self._df[d:]
        if end:
            d = dateparser(end)
            #self._df = self._df[self._df.index < d]
            self._df = self._df[:d]
        if start and end:
            sd = dateparser(start)
            ed = dateparser(end)
            #self._df = self._df[self._df.index >= d]
            #self._df = self._df[self._df.index < d]
            self._df = self._df[sd:]
            self._df = self._df[:ed]

    @property
    def df(self):
        return self._df

    @property
    def close(self):
        return self._df.close

    @property
    def pe(self):
        return self._df.pe

    @property
    def pb(self):
        return self._df.pb

    @property
    def div_yield(self):
        return self._df.div_yield

    @property
    def ma50(self):
        return pd.rolling_mean(self.close, 50)

    @property
    def ma100(self):
        return pd.rolling_mean(self.close, 100)

    @property
    def ma200(self):
        return pd.rolling_mean(self.close, 200)

    def get_return(self, d):
        try:
            #print self.close.index[-1], self.close[-1]
            #print self.close.truncate(after=d).index[-1], self.close.truncate(after=d)[-1]
            ret = self.close[-1]/self.close.truncate(after=d)[-1]
            #print ret
            return ret
        except IndexError:
            return None

    @property
    def m1(self):
        d = today - DateOffset(months=1)
        return self.get_return(d)

    @property
    def m3(self):
        d = today - DateOffset(months=3)
        return self.get_return(d)

    @property
    def m6(self):
        d = today - DateOffset(months=6)
        return self.get_return(d)

    @property
    def y1(self):
        d = today - DateOffset(years=1)
        #print 'calculating 1 yr return'
        return self.get_return(d)

    @property
    def y2(self):
        d = today - DateOffset(years=2)
        return self.get_return(d)

    @property
    def y3(self):
        d = today - DateOffset(years=3)
        #print 'calculating 3 yr return'
        return self.get_return(d)

    @property
    def y4(self):
        d = today - DateOffset(years=4)
        return self.get_return(d)

    @property
    def y5(self):
        d = today - DateOffset(years=5)
        #print 'calculating 5 yr return'
        return self.get_return(d) 

    @property
    def y6(self):
        d = today - DateOffset(years=6)
        return self.get_return(d) 

    @property
    def y7(self):
        d = today - DateOffset(years=7)
        return self.get_return(d) 

    @property
    def y8(self):
        d = today - DateOffset(years=8)
        return self.get_return(d) 

    @property
    def y9(self):
        d = today - DateOffset(years=9)
        return self.get_return(d) 

    @property
    def y10(self):
        d = today - DateOffset(years=10)
        #print 'calculating 10 yr return'
        return self.get_return(d)

    @property
    def returns(self):
        return {'1m': self.m1,
                '3m': self.m3,
                '6m': self.m6,
                '1y': self.y1,
                '2y': self.y2,
                '3y': self.y3,
                '4y': self.y4,
                '5y': self.y5,
                '6y': self.y6,
                '7y': self.y7,
                '8y': self.y8,
                '9y': self.y9,
                '10y': self.y10}

    def rolling_cagr(self, avg='monthly'):
        close = self._df.close
        last_year = (close.index[-1].year - close.index[0].year) + 1
        #rng = range(1, 24)
        rng = range(1, int(last_year))

        if avg == 'daily':
            # sample to every day
            close = close.asfreq('D', method='pad')
            # compute rolling average over 365 days
            ra = {i: close.pct_change(i*365) for i in rng}
        elif avg == 'monthly':
            # sample down to first business day of the month
            close = close.asfreq('BMS', method='pad')
            # compute rolling average over 1 yr, 2 yrs, 3 yrs, ...
            ra = {i: close.pct_change(i*12) for i in rng}
        elif avg == 'yearly':
            # sample down to first business day of calendar year
            close = close.asfreq('BAS', method='pad')
            # compute rolling average 1 yr, 2 yrs, 3 yrs, ...
            ra = {i: close.pct_change(i) for i in rng}

        # sample down all the computed averages to start of the year
        rs = {i: ra[i].resample('BAS', how='mean') for i in rng}

        # calculate cagr in %
        cagr = {i: 100*((rs[i]+1)**(1/float(i))-1) for i in rng}

        # make them into a dataframe
        df = pd.DataFrame(cagr)

        return df

    def benchmark_against(self, benchmark):

        stk = self.rolling_cagr(avg='monthly')
        bm = benchmark.rolling_cagr()

        df1 = stk[1:]
        try:
            c1 = bm.ix[stk.index[1]:]
        except IndexError:
            return None, None, None
        df2 = c1.iloc[:,:len(stk.columns)]
        #print df2

        pts = df1.copy()
        for i in range(len(pts)):
            for j in range(len(pts.columns)):
                if not pd.isnull(df1.iloc[i,j]):
                    if df1.iloc[i,j] > df2.iloc[i,j]:
                        pts.iloc[i,j] = 1
                    else:
                        pts.iloc[i,j] = 0

        return stk, df2, pts

class Index(HistoricalData):
    def __init__(self, index, file=None, start=None, end=None):
        if file:
            self._file = file
        else:
            self._file = index_file(index)

        if index in ['bse_bankex', 'bse_midcap', 'bse_power', 'bse_psu',
                     'bse_realty', 'bse_sensex', 'bse_smallcap', 'bse_teck',
                     'bse_200', 'bse_500']:
            cols = index_cols_1
        else:
            cols = index_cols_2

        super(Index, self).__init__(self._file,
                                    start = start,
                                    end = end,
                                    skiprows=1,
                                    cols=cols)


class Stock(HistoricalData):

    def __init__(self, bsecode=None, file_name=None, start=None, end=None):
        if file_name:
            self._file = file
        else:
            self._file = stock_file(bsecode)

        super(Stock, self).__init__(self._file,
                                    start = start,
                                    end=end,
                                    skiprows=0,
                                    cols=stock_cols)


def stock_search(s):
    return company_names[company_names.str.contains(s.upper())]


    #def sip(self, date=None, freq='MS', value=1000):
    #    print date
    #    closing_prices = self._df[self._df.index > date].close.resample(freq)
    #    units = value/closing_prices
    #    df = pd.DataFrame({'price': closing_prices, 'units': units})
    #    return df

if __name__ == '__main__':

    print stock_search('HIND')

    #arb = Stock('500008', start=(2000, 1, 1))
    #sensex = Index('bse_sensex', start='-10y')#start=(2000, 1, 1))
    #print arb.ma50.tail()
    #arb_norm = 100*arb.close/arb.close[0]
    #sensex_norm = 100*sensex.close/sensex.close[0]
    #fig, axes = plt.subplots(nrows=2, ncols=1)
    #print sensex.pe.describe()
    #print sensex.div_yield.describe()
    #sensex.close.plot(label='sensex')
    #plt.legend()
    #sensex.div_yield.plot(secondary_y=True, style='r', label='div_yield')
    #sensex.div_yield.plot(ax=axes[0])
    #sensex.close.plot(ax=axes[1])
    #plt.savefig('sensex_vs_div_yield.png')
    #plt.show()
    #arb_norm.plot()
    #sensex_norm.plot()
    #print s.df['d3'].dropna()
    #start_date = (2007, 1, 1)
    #sensex = Index('bse_sensex', start=start_date)
    #midcap = Index('bse_midcap', start=start_date)
    #smallcap = Index('bse_smallcap', start=start_date)

    #print sensex.pe.describe()
    #print midcap.pe.describe()
    #print smallcap.pe.describe()

    #sensex.pe.plot()
    #midcap.pe.plot()
    #smallcap.pe.plot()
    #plt.show()
    #amt = 10000
    #sip = sensex.sip(date=datetime(1999, 06, 10), freq='AS', value=amt)
    #total_units = sip.units.sum()
    #print 'total units', total_units
    #print 'print invested amount', len(sip)*amt
    #present_value = total_units*sensex.close[-1]
    #print 'present value', present_value
    #rate_of_return = np.rate(len(sip), -amt, 0, present_value)
    #print 'return', (1+rate_of_return)
    #print 'return on index', ((sip.price[-1]/sip.price[0])**(1./len(sip)))
    #print sip.head()
    #sip.plot()
    #plt.show()
    #bse100 = Index('bse_100').start(start_date)
    #bse500 = Index('bse_500').start(start_date)
    
    #print "===== Sensex ====="
    #print sensex.pe.describe()
    #print
    #print "===== BSE 100 ====="
    #print bse100.pe.describe()
    #print
    #print "===== BSE 500 ====="
    #print bse500.pe.describe()
    #print


    #plt.figure()
    #sensex.pe.plot()
    #plt.figure()
    #bse100.pe.plot()
    #plt.figure()
    #bse500.pe.plot()
    #plt.show()


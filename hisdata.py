#! /usr/bin/env python

from config import indices_dir
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

index_file = lambda index: os.path.join(indices_dir, index + '.csv')

index_cols_1 = ['date', 'open', 'high', 'low', 'close', 'volume',
                'turnover', 'pe', 'pb', 'div_yield']
index_cols_2 = ['date', 'open', 'high', 'low', 'close',
                'shares_traded', 'turnover']

class Index:
    def __init__(self, index, file=None, start=None, end=None):

        if file:
            self._file = file
        else:
            self._file = index_file(index)

        if index in ['bse_bankex', 'bse_midcap', 'bse_power', 'bse_psu',
                     'bse_realty', 'bse_sensex', 'bse_smallcap', 'bse_teck']:
            cols = index_cols_1
        else:
            cols = index_cols_2

        print cols

        self._df = pd.read_csv(self._file, skiprows=1, header=None,
                               names=cols, index_col=False)
        self._df.index = pd.to_datetime(self._df.date)

        if start:
            d = datetime(*start)
            self._df = self._df[self._df.index > d]
        if end:
            d = datetime(*end)
            self._df = self._df[self._df.index < d]
        if start and end:
            sd = datetime(*start)
            ed = datetime(*end)
            self._df = self._df[self._df.index > d]
            self._df = self._df[self._df.index < d]

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

    def sip(self, date=None, freq='MS', value=1000):
        print date
        closing_prices = self._df[self._df.index > date].close.resample(freq)
        units = value/closing_prices
        df = pd.DataFrame({'price': closing_prices, 'units': units})
        return df

if __name__ == '__main__':
    start_date = (2007, 1, 1)
    sensex = Index('bse_sensex', start=start_date)
    midcap = Index('bse_midcap', start=start_date)
    smallcap = Index('bse_smallcap', start=start_date)

    print sensex.pe.describe()
    print midcap.pe.describe()
    print smallcap.pe.describe()

    sensex.pe.plot()
    midcap.pe.plot()
    smallcap.pe.plot()
    plt.show()
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


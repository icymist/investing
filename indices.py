#! /usr/bin/env python

from config import indices_dir
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

index_file = lambda index: os.path.join(indices_dir, index + '.csv')

cols1 = ['date', 'open', 'high', 'low', 'close', 'volume',
         'turnover', 'pe', 'pb', 'div_yield']


class Index:
    def __init__(self, index):
        self._file = index_file(index)
        self._df = pd.read_csv(self._file, skiprows=1, header=None, names = cols1, index_col=False)
        self._df.index = pd.to_datetime(self._df['date'])

    def start(self, date=None):
        if date:
            d = datetime(*date)
            return self._df[self._df.index > d]
        else:
            return self._df

    def sip(self, date=None, freq='MS'):
        return self._df[self._df.index > date].close.resample(freq)


if __name__ == '__main__':
    start_date = (2003, 1, 1)
    sensex = Index('sensex')
    sensex_data = sensex.start(start_date)
    sip = sensex.sip(date=datetime(2000, 1, 1))
    sip.plot()
    plt.show()
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


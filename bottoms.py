#! /usr/bin/env python

"""
Script to find stocks which have bottomed out.

The idea is that the 50, 100 and 200 day simple moving averages are all within
10% from the lowest of the three.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from hisdata import Stock
from indexconstituents import useful_companies
from multiprocessing import cpu_count, Pool

# relative standard deviation
def rstd(lst):
    array = np.array(lst)
    print array
    return array.std()/array.mean()

#rstd = {}
#for bsecode in useful_companies.index:
#    stk = Stock(bsecode)
#    print bsecode, rstd([stk.ma50[-1], stk.ma100[-1], stk.ma200[-1]])

df = useful_companies#[:50]
df = pd.DataFrame(df)
print df

def try_getting(parameter):
    try:
        #print parameter[-1]
        return parameter[-1]
    except:
        'caught exception'
        return None

ma50 = lambda bsecode: try_getting(Stock(bsecode).ma50)
ma100 = lambda bsecode: try_getting(Stock(bsecode).ma100)
ma200 = lambda bsecode: try_getting(Stock(bsecode).ma200)

df['ma50'] = df.index.map(ma50)
df['ma100'] = df.index.map(ma100)
df['ma200'] = df.index.map(ma200)
df['rstd'] = df.std(axis=1)/df.mean(axis=1)

df.to_csv('bottoms.csv', index_label='bsecode')

df[['rstd']].boxplot()
plt.show()

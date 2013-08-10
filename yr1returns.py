#! /usr/bin/env python

import os
from hisdata import Stock, Index, HistoricalData 
from indexconstituents import IndexConstituents as ic
import pandas as pd
from pandas.tseries.offsets import DateOffset
from multiprocessing import cpu_count, Pool
from config import moneycontrol_data_dir

# latest stock data
latest_stock_data_file = os.path.join(moneycontrol_data_dir, 'latest_stock_data.csv')
ldf = pd.read_csv(latest_stock_data_file)
ldf.bsecode = ldf.bsecode.astype(str)
ldf = ldf.set_index('bsecode')

ncpus = cpu_count()

# does not work with multiprocessing if Pool is initialized here
# always initialize pool just before the parallel processing starts
# p = Pool(ncpus)

def yr1_return(bsecode):
    try:
        ret = Stock(bsecode).y1
    except IOError:
        print '%s does not exist' % bsecode
        ret = 0.0
    return ret


# does not work with multiprocessing
# always define an explicit function
#yr1_return = lambda bsecode: Stock(bsecode).y1

def get_1yr_returns(index):
    if index == 'bse_sensex':
        idx = ic().bse_sensex
    elif index == 'bse_midcap':
        idx = ic().bse_midcap
    elif index == 'bse_200':
        idx = ic().bse_200
    elif index == 'bse_500':
        idx = ic().bse_500
    elif index == 'bse_smallcap':
        idx = ic().bse_smallcap

    stk_bsecodes = idx.bsecode
    stk_company_names = idx.company_name

    p = Pool(ncpus)
    returns = p.map(yr1_return, stk_bsecodes)

    #stk_bsecodes.append(index)
    #stk_company_names.append(index)
    #returns.append(Index(index).y1)

    #print len(stk_bsecodes), len(stk_company_names), len(returns)

    df = pd.DataFrame({'bsecode': stk_bsecodes, 'company_name': stk_company_names, 'returns': returns})
    idx_returns = pd.DataFrame({'bsecode': [index], 'company_name': [index], 'returns': [Index(index).y1]})

    df = pd.concat([df, idx_returns])
    df = df.set_index('bsecode')

    return df

if __name__ == '__main__':
    #idxs = ['bse_sensex', 'bse_200', 'bse_500', 'bse_midcap', 'bse_smallcap']
    idxs = ['bse_500']#, 'bse_midcap', 'bse_smallcap']
    for idx in idxs:
        print idx
        df = get_1yr_returns(idx)
        df = df.sort('returns', ascending=False)
        df1 = df.join(ldf)
        df1['adjusted_returns'] = df1['returns'] - df1.ix[idx]['returns']
        print df1[df1.pe < 25].sort('adjusted_returns', ascending=False)[
                ['company_name', 'pe', 'div_yield', 'adjusted_returns']]
        df1.to_csv('yr1returns_' + idx + '.csv')

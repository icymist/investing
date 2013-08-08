#! /usr/bin/env python

from hisdata import Stock, Index, HistoricalData 
from indexconstituents import IndexConstituents as ic
import pandas as pd
from pandas.tseries.offsets import DateOffset
from multiprocessing import cpu_count, Pool
ncpus = cpu_count()

# does not work with multiprocessing if Pool is initialized here
# always initialize pool just before the parallel processing starts
# p = Pool(ncpus)

def yr1_return(bsecode):
    return Stock(bsecode).y1

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
    idx = 'bse_200'
    df = get_1yr_returns('bse_200')
    df = df.sort('returns', ascending=False)
    df.to_csv('yr1returns_' + idx + '.csv')

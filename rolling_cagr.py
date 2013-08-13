#! /usr/bin/env python

"""
Script to display the calculated rolling CAGR of a given stock along with a
given reference index.  The reference index defaults to the BSE Sensex.
"""

import sys
import pandas as pd
from hisdata import Stock, Index, stock_search
import argparse
from displayoptions import display_options
#pd.set_printoptions(precision=1)
pd.set_option('precision', 2)
pd.set_option('display.max_columns', 50)

def benchmark_against(bsecode, index):
    stk = Stock(bsecode)
    idx = Index(index)
    
    stk_returns, bm_returns, pts = stk.benchmark_against(idx)
    try:
        combined = stk_returns.join(bm_returns, rsuffix = '_bse')
    except AttributeError:
        combined = None

    if pts:
        pts_mean = pts.mean().mean()
    else:
        pts_mean = 0.0
    #print stk_returns, bm_returns, combined, pts, pts_mean
    return stk_returns, bm_returns, combined, pts, pts_mean

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    #parser.add_argument('bsecode')#, required=True)
    parser.add_argument('-s', '--search', default=True)
    parser.add_argument('-index', '--index', default='bse_sensex')

    args = parser.parse_args()

    if args.search:
        matches = stock_search(args.search)
        if len(matches) > 1:
            choice = display_options(matches)
            bsecode = matches.index[choice]
        elif len(matches) == 0:
            print 'Company not in any of the indices'
            print
            sys.exit(-1)
        elif len(matches) == 1:
            choice = 0
            bsecode = matches.index[0]
        print matches[choice]

    stk_returns, bm_returns, combined, pts, pts_mean = benchmark_against(bsecode, args.index)

    printcols = []
    if stk_returns:
        for i in range(1,len(stk_returns)):
            printcols.append('%i' % i)
            printcols.append('%i_bse' % i)
        #print printcols
        print combined[printcols]
        print
        print pts
        print pts_mean
        #print printcols
        #print stk_returns
        #print bm_returns
        #print pts

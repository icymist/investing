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

    stk = Stock(bsecode)
    idx = Index(args.index)
    
    stk_returns, bm_returns, pts = stk.benchmark_against(idx)
    print stk_returns
    print bm_returns
    print pts
    print pts.mean().mean()

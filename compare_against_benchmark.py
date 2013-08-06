#! /usr/bin/env python

from hisdata import Index, Stock
import pandas as pd

#sx = Index('bse_sensex')

#ab = Stock('500800') # tata global beverage
#ab = Stock('500008') # amara raja batteries
#ab = Stock('500086') # exide
#ab = Stock('532977') # bajaj auto
#ab = Stock('500182') # hero motocorp
#ab = Stock('500477') # ashok leyland
#ab = Stock('500696') # hul
#ab = Stock('500103') # bhel
#ab = Stock('500510') # larsen toubro
#ab = Stock('500312') # ongc
#ab = Stock('532461') # pnb
#ab = Stock('532488') # divis
#ab = Stock('500420') # torrent pharma
#ab = Stock('500124') # dr reddys
#ab = Stock('500257') # lupin
#ab = Stock('500087') # cipla
#ab = Stock('500680') # pfizer
#ab = Stock('524715') # sun pharma
#ab = Stock('524494') # ipca labs
#ab = Stock('500359') # ranbaxy
#ab = Stock('500302') # piramal
#ab = Stock('500470') # tata steel
#ab = Stock('532454') # bharti airtel
#ab = Stock('500480') # cummins
#ab = Stock('500290') # mrf
#ab = Stock('524667') # savita oil technologies

def compare_against(stock, benchmark):

    stk = Stock(stock).rolling_cagr()
    print stk
    bm = Index(benchmark).rolling_cagr()

    df1 = stk[1:]
    c1 = bm.ix[stk.index[1]:]
    df2 = c1.iloc[:,:len(stk.columns)]
    print df2

    pts = df1.copy()
    for i in range(len(pts)):
        for j in range(len(pts.columns)):
            if not pd.isnull(df1.iloc[i,j]):
                if df1.iloc[i,j] > df2.iloc[i,j]:
                    pts.iloc[i,j] = 1
                else:
                    pts.iloc[i,j] = 0

    return pts

for stock in ['532461', '532179', '500112', '532174']:
    pts = compare_against(stock, 'bse_sensex')
    print pts
    print pts.mean().mean()

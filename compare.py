#! /usr/bin/env python

from hisdata import Index, Stock
from indexconstituents import IndexConstituents, company_names
import pandas as pd
import matplotlib.pyplot as plt

company_name = lambda bsecode: company_names.get(bsecode)

bsecodes_sensex = IndexConstituents().bse500.bsecode
#print sensex

benchmark = Index('bse_sensex')
# collect all the points
pts_d = []
company_names_d = []
for bsecode in bsecodes_sensex:
    #print bsecode, company_names[bsecode]
    try:
        stk =  Stock(bsecode)
    except IOError:
        pts_d.append(None)
        continue
    stk_returns, bm_returns, pts = stk.benchmark_against(benchmark)
    if pts: pts_mean = pts.mean().mean()
    if pts_mean and pts_mean > 0.75:
        print company_names[bsecode], pts_mean
        #print pts
        #print
        #print stk_returns
        #print bm_returns
        #print pts.mean().mean()
    
    pts_d.append(pts_mean)
    company_names_d.append(company_names[bsecode])

df = pd.DataFrame.from_dict({'bsecode': bsecodes_sensex, 'pts': pts_d})
df['company_name'] = df.bsecode.map(company_name)
df = df.set_index('bsecode')#, drop=False)
df.to_csv('bse500_best.txt')
df.boxplot()
plt.show()

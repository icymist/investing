#! /usr/bin/env python

"""

Script to create a list of companies that I want to watch.  The base list is
all the unique companies in the BSE indices list.  On this there will be a
ignore list and an include list.

We remove all the companies in the ignore list and then include companies in
the include list if they do not already exist.

"""

import os
import pandas as pd
from indexconstituents import useful_companies
from config import data_dir
from rolling_cagr import benchmark_against

mywatchlist = os.path.join(data_dir, 'mywatchlist.csv')
bse_companies = os.path.join(data_dir, 'bse_companies.csv')

useful_companies.to_csv(bse_companies, index_label='bsecode')

# ignore list 1
# companies that did not consistently beat the index
def get_companies_that_did_not_beat_index():
    didnotbeatindex_file = os.path.join(data_dir, 'didnotbeatindex.csv')
    cdnbi = {}
    cdnbi['bsecode'] = []
    cdnbi['company_name'] = []
    cdnbi['pts'] = []

    for bsecode in useful_companies.index:
        try:
            pts = benchmark_against(bsecode, 'bse_sensex')[-1]
        except IndexError:
            pts = 0
        #if pts < 0.6:
        print pts, useful_companies.ix[bsecode, 'company_name']
        cdnbi['bsecode'].append(bsecode)
        cdnbi['company_name'].append(useful_companies.ix[bsecode, 'company_name'])
        cdnbi['pts'].append(pts)

    df = pd.DataFrame.from_dict(cdnbi)
    df = df.set_index('bsecode')
    #df.to_csv(didnotbeatindex_file, index_label='bsecode', cols=['company_name', 'pts'])

if __name__ == '__main__':
    get_companies_that_did_not_beat_index()

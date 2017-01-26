#! /usr/bin/env python

import pandas as pd
from latest_stock_data import get_latest_stock_data
from indexconstituents import get_all_indices_constituents

latest_stock_data = get_latest_stock_data()
indices_constituents = get_all_indices_constituents()
indices = indices_constituents.keys()

cols = ['bsecode', 'company', 'market_cap', 'pe', 'pb', 'div_yield',
        'eps', 'bv', 'pe_industry', 'div_pc']

xl_writer = pd.ExcelWriter('latest_stock_data.xlsx')

for ix in indices:
    df = indices_constituents[ix][['bsecode']].merge(latest_stock_data,
                                                on='bsecode', how='inner')
    df[cols].to_excel(xl_writer, ix[:31])

xl_writer.save()

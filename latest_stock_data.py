#! /usr/bin/env python

import os
from glob import glob
from config import data_dir
import pandas as pd

def get_latest_stock_data():

    mc_stock_data_files = glob(os.path.join(data_dir, 'moneycontrol', '*_mc_stock_data.csv'))

    latest_stock_data_file = sorted(mc_stock_data_files)[-1]

    df = pd.read_csv(latest_stock_data_file, na_values='-', thousands=',')

    df.columns = ['bsecode', 'fv', 'market_lot', 'company', 'market_cap',
                  'eps', 'pc', 'pe_industry', 'pb', 'div_pc', 'div_yield',
                  'deliverables', 'pe', 'bv', 'dummy0']

    del df['dummy0']

    # pd.to_numeric(df[['bsecode', 'fv', 'market_lot', 'company', 'market_cap',
    #                   'eps', 'pc', 'pe_industry', 'pb', 'div_pc', 'div_yield',
    #                   'deliverables', 'pe', 'bv', 'dummy0']], errors='coerce')

    int_cols = ['market_lot']

    float_cols = ['fv', 'market_cap', 'eps', 'pc', 'pe', 'pe_industry', 'pb', 'div_pc', 'div_yield',
                  'bv']

    for c in float_cols:
        print c
        df[c] = df[c].fillna('').astype(str).str.replace('%', '')
        df[c] = pd.to_numeric(df[c], errors=coerce)

    for c in int_cols:
        df[c] = df[c].fillna('').astype(str).str.replace('%', '')
        df[c] = pd.to_numeric(df[c], errors=coerce)

    return df


if __name__ == '__main__':
    df = get_latest_stock_data()
    print df.head()

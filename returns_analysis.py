#! /usr/bin/env python

import pandas as pd
import numpy as np
from indexconstituents import IndexConstituents as ic

company_names = ic().company_names

pd.set_option('display.max_rows', 500)

def apply_filter(f):
    df = pd.read_csv(f+'_relative_returns.csv', na_values='na', index_col=0)
    df.index.astype(str)

    for i in ['1m', '3m', '6m']: del df[i]

    df1 = df.copy()

    # remove the company_name column
    del df1['company_name']

    # set the number to 1 or 0 depending on the return
    df1[df >= 1.] = 1
    df1[df < 1.] = 0

    # average all the returns over the years
    df['score'] = df.mean(axis=1)
    # to count the number of years the company beat the index
    df1['score'] = df1.fillna(1).sum(axis=1)

    # make another dataframe with just the scores and the company name
    df2 = pd.DataFrame({'score1': df['score'],
                        'score2': df1['score'],
                        'company_name': df['company_name']})

    # weed out the weak companies
    df3 = df2[ (df2.score1 > 1.0) & (df2.score2 >= 7)]
    #df3.sort('score1', ascending=False)[['company_name', 'score1', 'score2']]
    return df3

if __name__ == '__main__':
    bsecodes = []
    # collect all the dataframes
    dfs = {}
    for f in ['sensex', 'midcap', #'smallcap',
              'bse100', 'bse200', #'bse500',
              'capital_goods', 'consumer_durables',
              'fmcg', 'health_care', 'it', 'metal',
              'oilgas', 'auto', 'psu', 'teck',
              'bankex', 'realty', 'power']:
        print "====== %s ======" % (f)
        df = apply_filter(f)
        dfs[f] = df
        bsecodes.extend(df.index.values)
        print df.sort('score1', ascending=False)[['company_name', 'score1', 'score2']]
        print
        print

# concat all the dataframes and drop the duplicates
final_df = pd.concat(dfs.values()).drop_duplicates()
final_df.to_csv('masterlist.csv')

print final_df.head()

for bsecode in set(bsecodes):
    print bsecode, company_names.ix[bsecode]
print len(set(bsecodes))

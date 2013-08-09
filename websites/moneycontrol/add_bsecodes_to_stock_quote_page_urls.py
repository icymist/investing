#! /usr/bin/env python

"""
Script to extract bsecodes from downloaded moneycontrol stock quote pages to
make a csv file with bsecode, moneycontrol_stock_quote_page_url

Files to be parse are read from preliminary stock_quote_page_urls_1 file where
only the urls are listed and no bsecodes
"""

import os, re
import pandas as pd
from glob import glob
from multiprocessing import cpu_count, Pool
from investing.config import moneycontrol_data_dir

ncpus = cpu_count()

# Regular expression to extract the bsecode
m = re.compile(r'BSE: (\d{6})')

def get_stock_quote_page_file(stock_quote_page_url):
    head = os.path.join(moneycontrol_data_dir, 'stock_quote_pages')
    tail = stock_quote_page_url.split('/')[-1] + '.html'
    return os.path.join(head, tail)

def get_bsecode(f):
    if os.path.exists(f):
        matches = m.findall(open(f).read())
    else:
        print '%s does not exist' % (f)
        matches = None
    if matches:
        return matches[0]#.split()[-1]
    else:
        return None

def run():
    # Get the urls from the stock_quote_page_urls_1 file
    df = pd.read_csv(os.path.join(moneycontrol_data_dir, 'stock_quote_page_urls_1.csv'))
    stock_quote_page_urls = df['stock_quote_page_url']
    # Get the location of all the files
    stock_quote_page_files = [get_stock_quote_page_file(url) for url in stock_quote_page_urls]
    # Add the location to the existing dataframe
    df['stock_quote_page_file'] = stock_quote_page_files

    p = Pool(ncpus)
    # Get the bsecodes
    bsecodes = p.map(get_bsecode, stock_quote_page_files)
    # Add column of bsecodes to the existing dataframe
    df['bsecode'] = bsecodes
    # Remove files which do not have bsecodes
    df = df.dropna()
    # Write them to file
    stock_quote_urls_file = os.path.join(moneycontrol_data_dir,
                                         'stock_quote_page_urls.csv')
    df.to_csv(stock_quote_urls_file, index=False,
              cols=['bsecode', 'stock_quote_page_url', 'stock_quote_page_file'])

if __name__ == '__main__':
    run()

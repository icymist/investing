#! /usr/bin/env python

import os
from string import ascii_uppercase
from bs4 import BeautifulSoup
from investing.config import moneycontrol_data_dir
import pandas as pd

alphabet_pages_dir = os.path.join(moneycontrol_data_dir, 'alphabets')
mc_urls_file_name = os.path.join(moneycontrol_data_dir, 'stock_quote_page_urls_1.csv')

def get_urls(file_name):
    urls = []
    soup = BeautifulSoup(open(file_name).read(), 'html5lib', from_encoding="utf-8")
    for atag in soup.find_all('a'):
        href = atag.get('href', None)
        if href and 'stockpricequote' in href:
            urls.append(href)
    print file_name, len(urls)
    return urls

def run():
    urls = []
    alphabet_page_files = [os.path.join(alphabet_pages_dir, s+'.html') for s in ascii_uppercase]
    print alphabet_page_files
    for alphabet_page_file in alphabet_page_files:
        urls.extend(get_urls(alphabet_page_file))

    df = pd.DataFrame({'stock_quote_page_url': urls})
    df.to_csv(mc_urls_file_name, index=False)

if __name__ == '__main__':
    run()

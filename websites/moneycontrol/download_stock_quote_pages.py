#! /usr/bin/env python

import os
import pandas as pd
from downloader import parallel_download
from investing.config import moneycontrol_data_dir


dst_dir = os.path.join(moneycontrol_data_dir, 'stock_quote_pages')

def dst_file_name(s):
    file_name = s.strip().split('/')[-1]
    return os.path.join(dst_dir, file_name+'.html')

def run():
    mc_urls_file = os.path.join(moneycontrol_data_dir, 'stock_quote_page_urls_1.csv')
    mc_urls = pd.read_csv(mc_urls_file)['stock_quote_page_url'].values
    dst_file_names = [dst_file_name(s) for s in mc_urls]
    parallel_download(mc_urls, dst_file_names, nthreads=64, download_if_dst_exists=False)

if __name__ == '__main__':
    run()

#! /usr/bin/env python

import os
import pandas as pd
from downloader import parallel_download
from investing.config import moneycontrol_data_dir

mc_urls_file = os.path.join(moneycontrol_data_dir, 'mc_urls.csv')
mc_urls = pd.read_csv(mc_urls_file)['mc_stock_quote_page_urls'].values

dst_dir = os.path.join(moneycontrol_data_dir, 'stock_quote_pages')

def dst_file_name(s):
    file_name = s.strip().split('/')[-1]
    return os.path.join(dst_dir, file_name+'.html')

dst_file_names = [dst_file_name(s) for s in mc_urls]
parallel_download(mc_urls, dst_file_names, nthreads=64, download_if_no_file=True)

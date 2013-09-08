#! /usr/bin/env python
"""
Script to download the alphabet pages with all the stock quote page urls
"""

import os
from string import ascii_uppercase
from downloader import parallel_download
from investing.config import moneycontrol_data_dir
import argparse

dst_dir = os.path.join(moneycontrol_data_dir, 'alphabets')

root_url = 'http://www.moneycontrol.com/india/stockmarket/pricechartquote'
page_url = lambda s: '/'.join([root_url, s])

alphabet_urls = [page_url(s) for s in ascii_uppercase]
alphabet_urls.append(page_url('others'))

dst_file_names = [os.path.join(dst_dir, s + '.html') for s in ascii_uppercase]
dst_file_names.append(os.path.join(dst_dir, 'others.html'))

def download_alphabet_pages(download_if_dst_exists=False):
    parallel_download(alphabet_urls,
                      dst_file_names,
                      nthreads=2,
                      download_if_dst_exists=download_if_dst_exists)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--fresh', default=False, action='store_true',
            help = 'to download all the files afresh')

    args = parser.parse_args()
    if args.fresh:
        download_alphabet_pages(download_if_dst_exists=True)
    else:
        download_alphabet_pages(download_if_dst_exists=False)

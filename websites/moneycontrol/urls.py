#! /usr/bin/env python

import os
from string import ascii_uppercase
from urllib2 import urlopen
from downloader import parallel_download
#from investing.webscraping import tables_lxml
from bs4 import BeautifulSoup

tmp_dir = 'tmp'
root_url = 'http://www.moneycontrol.com/india/stockmarket/pricechartquote'
page_url = lambda s: '/'.join([root_url, s])

alphabet_urls = [page_url(s) for s in ascii_uppercase]
alphabet_urls.append(page_url('others'))

dst_file_names = [os.path.join(tmp_dir, s + '.html') for s in ascii_uppercase]
dst_file_names.append(os.path.join(tmp_dir, 'others.html'))

def download_files():
    parallel_download(alphabet_urls, dst_file_names, nthreads=13)

def get_urls():
    collect_urls = {}
    for f in dst_file_names:
        soup = BeautifulSoup(open(f).read(), from_encoding="utf-8")
        for td in soup.find_all('td'):
            atags = td.find_all('a')
            for tag in atags:
                href = tag.get('href', None)
                company_name = tag.get_text().encode('ascii', 'ignore')
                collect_urls[company_name] = href
        #for l in open(f).readlines():
        #    line = l.strip()
        #    if 'stockpricequote' in line:
        #        urls = BeautifulSoup(line).find_all('a')
        #        for url in urls:
        #            href = url.get('href', None)
        #            company_name = str(url.get_text())
        #            #print company_name, href
        #            collect_urls[company_name] = href

    return collect_urls

def get_stock_quote_pages(urls):
    def dst_file_name(s):
        file_name = s.strip().split('/')[-1]
        return os.path.join(tmp_dir, 'stock_quote_pages', file_name+'.html')

    dst_file_names = [dst_file_name(s) for s in urls]
    print len(urls)
    print len(dst_file_names)
    print dst_file_names
    parallel_download(urls, dst_file_names, nthreads=64)

if __name__ == '__main__':
    #download_files()
    company_names_urls_dict = get_urls()
    for name, url in company_names_urls_dict.items():
        print name, url

    get_stock_quote_pages(company_names_urls_dict.values())

#! /usr/bin/env python

import os, sys
import argparse
import yaml
import pandas as pd
from investing.config import company_groups_file, moneycontrol_data_dir
from investing.config import historical_stock_data_dir
from investing import indexconstituents
from functools import partial
#from multiprocessing import Pool
#import updater
from downloader import parallel_download
#import re
#from bs4 import BeautifulSoup

#map_bsecode_url = yaml.load(open('map_bsecode_to_stock_quote_page_url.yaml'))['urls']
stock_quote_page_urls_file = os.path.join(moneycontrol_data_dir, 'stock_quote_page_urls.csv')
df_stock_quote_pages = pd.read_csv(stock_quote_page_urls_file, index_col=0)
df_stock_quote_pages.index = df_stock_quote_pages.index.astype(str)
useful_companies = indexconstituents.useful_companies
df = useful_companies.join(df_stock_quote_pages)

def get_url(bsecode, s=None):
    root = 'http://www.moneycontrol.com/india/stockpricequote'
    financials = 'http://www.moneycontrol.com/financials'
    company_facts = 'http://www.moneycontrol.com/company-facts'
    historical_stock_data_base_url = 'http://www.moneycontrol.com'

    try:
        pricequote_url = df_stock_quote_pages.ix[bsecode]['stock_quote_page_url']
    except:
        pricequote_url = ''
        print 'url not available for %s' % (bsecode)
        
    if pricequote_url:
        key1, key2 = pricequote_url.replace(root, '').split('/')[-2:]
        key1, key2 = [i.replace('-', '') for i in [key1, key2]]

        if s == 'stock_quote_pages':
            return pricequote_url

        if s == 'quarterly_results':
            return '/'.join([financials, key1, 'results', 'quarterly-results', key2])
        
        if s == 'yearly_results':
            return '/'.join([financials, key1, 'results', 'yearly', key2])
    
        elif s == 'yearly_results_consolidated':
            return '/'.join([financials, key1, 'results', 'consolidated-yearly', key2])
        
        elif s == 'balance_sheet':
            return '/'.join([financials, key1, 'balance-sheet', key2])
        
        elif s == 'balance_sheet_consolidated':
            return '/'.join([financials, key1, 'consolidated-balance-sheet', key2])
        
        elif s == 'cash_flow':
            return '/'.join([financials, key1, 'cash-flow', key2])
        
        elif s == 'cash_flow_consolidated':
            return '/'.join([financials, key1, 'consolidated-cash-flow', key2])
        
        elif s == 'ratios':
            return '/'.join([financials, key1, 'ratios', key2])
        
        elif s == 'ratios_consolidated':
            return '/'.join([financials, key1, 'consolidated-ratios', key2])
        
        elif s == 'share_holding':
            return '/'.join([company_facts, key1, 'shareholding-pattern', key2])
        
        elif s == 'historical_stock_data':
            stock_quote_page = os.path.join(moneycontrol_data_dir,
                                        'stock_quote_pages', key2+'.html')
            if os.path.exists(stock_quote_page):
                t = open(stock_quote_page).read()
                for i, l in enumerate(t.split()):
                    if 'his' in l and 'csv' in l:
                        url_tail = l.strip(',').strip("'")
                        return historical_stock_data_base_url + url_tail
                        break
                return ''
                #soup = BeautifulSoup(open(stock_quote_page).read())
                #try:
                #s = soup.find_all(text=re.compile('bse.*csv'))[0]
                #s = soup.find_all(text=re.compile('bse.*csv'))
                #print s
                #url_tail = s.split(',')[4].strip().strip("'")
                #except:
                #    print 'Caught exception', bsecode
    else:
        return None
    
def get_dst_fname(bsecode, s=None):
    if s == 'stock_quote_pages':
        dst_fname = os.path.join(moneycontrol_data_dir, 'stock_quote_pages', bsecode+'.html')
    if s == 'quarterly_results':
        dst_fname = os.path.join(moneycontrol_data_dir, 'quarterly_results', bsecode+'.html')
    if s == 'yearly_results':
        dst_fname = os.path.join(moneycontrol_data_dir, 'yearly_results', bsecode+'.html')
    elif s == 'yearly_results_consolidated':
        dst_fname = os.path.join(moneycontrol_data_dir, 'yearly_results_consolidated', bsecode+'.html')
    elif s == 'balance_sheet':
        dst_fname = os.path.join(moneycontrol_data_dir, 'balance_sheet', bsecode+'.html')
    elif s == 'balance_sheet_consolidated':
        dst_fname = os.path.join(moneycontrol_data_dir, 'balance_sheet_consolidated', bsecode+'.html')
    elif s == 'cash_flow':
        dst_fname = os.path.join(moneycontrol_data_dir, 'cash_flow', bsecode+'.html')
    elif s == 'cash_flow_consolidated':
        dst_fname = os.path.join(moneycontrol_data_dir, 'cash_flow_consolidated', bsecode+'.html')
    elif s == 'ratios':
        dst_fname = os.path.join(moneycontrol_data_dir, 'ratios', bsecode+'.html')
    elif s == 'ratios_consolidated':
        dst_fname = os.path.join(moneycontrol_data_dir, 'ratios_consolidated', bsecode+'.html')
    elif s == 'share_holding':
        dst_fname = os.path.join(moneycontrol_data_dir, 'share_holding', bsecode+'.html')
    elif s == 'historical_stock_data':
        dst_fname = os.path.join(historical_stock_data_dir, bsecode+'.csv')
        
    return dst_fname
    
def download(bsecodes, s, update):
    get_urls = partial(get_url, s=s)
    get_dst_fnames = partial(get_dst_fname, s=s)


    urls = map(get_urls, bsecodes)
    dst_fnames = map(get_dst_fnames, bsecodes)

    #print urls, dst_fnames

    #d = {bsecode: [url, dst_fname] for (bsecode, url, dst_fname) in zip(bsecodes, urls, dst_fnames)}

    #if update == 'update':
    #    files_not_to_download = []
    #    for bsecode, url_dst_fname in d.items():
    #        if updater.file_exists(url_dst_fname[1]):
    #            files_not_to_download.append(bsecode)
    #    for key in files_not_to_download:
    #        del d[key]
    #elif update == 'refresh':
    #    pass

    #urls, dst_fnames = zip(*d.values())
    parallel_download(urls, dst_fnames, nthreads=32, download_if_dst_exists=False)
        
    return None

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-qr', '--quarterly_results', action='store_true')
    parser.add_argument('-qrc', '--quarterly_results_consolidated', action='store_true')
    parser.add_argument('-yr', '--yearly_results', action='store_true')
    parser.add_argument('-yrc', '--yearly_results_consolidated', action='store_true')
    parser.add_argument('-bs', '--balance_sheet', action='store_true')
    parser.add_argument('-bsc', '--balance_sheet_consolidated', action='store_true')
    parser.add_argument('-cf', '--cash_flow', action='store_true')
    parser.add_argument('-cfc', '--cash_flow_consolidated', action='store_true')
    parser.add_argument('-ra', '--ratios', action='store_true')
    parser.add_argument('-rac', '--ratios_consolidated', action='store_true')
    #parser.add_argument('-cg', '--company_group', default='moneycontrol_all_companies')
    parser.add_argument('-cg', '--company_group', default='bse_active_companies')
    parser.add_argument('-sq', '--stockquote_pages', action='store_true')
    parser.add_argument('-sh', '--historical_stock_data', action='store_true')
    parser.add_argument('-sp', '--share_holding', action='store_true')
    parser.add_argument('-u', '--update', choices=['refresh', 'update'], default='update')
    
    args = parser.parse_args()
    
    # get the bsecodes companies whose data should be downloaded
    #company_groups = yaml.load(open(company_groups_file))
    #bsecodes = company_groups[args.company_group]
    bsecodes = df.index
    print len(bsecodes)

    update = args.update
    
    if args.quarterly_results:
        download(bsecodes, 'quarterly_results', update)
        
    if args.quarterly_results_consolidated:
        download(bsecodes, 'quarterly_results_consolidated', update)
    
    if args.yearly_results:
        download(bsecodes, 'yearly_results', update)

    if args.yearly_results_consolidated:
        download(bsecodes, 'yearly_results_consolidated', update)
        
    if args.balance_sheet:
        download(bsecodes, 'balance_sheet', update)
        
    if args.balance_sheet_consolidated:
        download(bsecodes, 'balance_sheet_consolidated', update)
        
    if args.cash_flow:
        download(bsecodes, 'cash_flow', update)
        
    if args.cash_flow_consolidated:
        download(bsecodes, 'cash_flow_consolidated', update)
        
    if args.ratios:
        download(bsecodes, 'ratios', update)
        
    if args.ratios_consolidated:
        download(bsecodes, 'ratios_consolidated', update)
        
    if args.stockquote_pages:
        download(bsecodes, 'stock_quote_pages', update)
        
    if args.historical_stock_data:
        download(bsecodes, 'historical_stock_data', update)
        
    if args.share_holding:
        download(bsecodes, 'share_holding', update)

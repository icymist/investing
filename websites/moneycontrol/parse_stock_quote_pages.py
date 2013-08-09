#! /usr/bin/env python

"""Parse the moneycontrol stock quote page and return all
useful information in a dictionary
"""

import os, re
from glob import glob
from bs4 import BeautifulSoup
from investing.config import moneycontrol_data_dir
import pandas as pd

#def get_string(tag):
#    t = BeautifulSoup(tag)
#    return t.string

#def get_string(tag):
#    try:
#        s = BeautifulSoup(tag).string
#        if s:
#            s.encode('ascii', 'replace')
#        return s
#    except:
#        return ''

def get_string(tag):
    r = re.compile('>.*<')
    try:
        s = r.findall(tag)[0]
    except:
        print tag
        sys.exit(-1)
    s = s.replace('>', '').replace('<', '')
    return s
    
def remove_commas(s):
    return s.replace(',', '')
    
#get_string = lambda tag: BeautifulSoup(tag).string.encode('ascii', 'replace')
#remove_commas = lambda s: s.replace(',', '')

def try_to_get_float(s):
    try:
        return float(s)
    except:
        return 0.0


def parse_stock_quote_page_file(file):
    #d = {'bsecode': '',
    #     'company_name': '',
    #     'market_cap': 0.0,
    #     'pe': 0.0,
    #     'pb': 0.0,
    #     'eps_ttm': 0.0,
    #     'bv': 0.0,
    #     'div': 0.0,
    #     'div_yield': 0.0,
    #     'industry_pe': 0.0,
    #     'deliverables': 0.0,
    #    }
    d = {}
    lines = open(file).readlines()
    try:
        for i, l in enumerate(lines):
             if 'MARKET CAP (Rs Cr)' in l:
                 d['market_cap'] = try_to_get_float(remove_commas(get_string(lines[i+1])))
                 
             if '>P/E<' in l and not 'INDUSTRY' in l:
                 d['pe'] = try_to_get_float(remove_commas(get_string(lines[i+1])))
                 
             if 'BOOK VALUE (Rs)' in l:
                 d['bv'] = try_to_get_float(remove_commas(get_string(lines[i+1])))
                 
             if 'DIV (%)' in l:
                 d['div'] = try_to_get_float(remove_commas(get_string(lines[i+1])).replace('%', ''))
         
             if 'INDUSTRY P/E' in l:
                 d['industry_pe'] = try_to_get_float(remove_commas(get_string(lines[i+1])))
         
             if 'EPS (TTM)' in l:
                 d['eps_ttm'] = try_to_get_float(remove_commas(get_string(lines[i+1])))
    
             if 'PRICE/BOOK' in l:
                 d['pb'] = try_to_get_float(remove_commas(get_string(lines[i+1])))
                 
             if 'DIV YIELD.(%)' in l:
                 d['div_yield'] = try_to_get_float(remove_commas(get_string(lines[i+1])).replace('%', ''))

             if 'FACE VALUE (Rs)' in l:
                 d['fv'] = try_to_get_float(remove_commas(get_string(lines[i+1])).replace('%', ''))
    except:
        pass
        # print l
                
    return d

def run():
    df1 = pd.read_csv(os.path.join(moneycontrol_data_dir, 'stock_quote_page_urls.csv'))
    df1.bsecode = df1.bsecode.astype(str)
    bsecodes = df1.bsecode
    stock_quote_files = df1.stock_quote_page_file
    latest_data = {}
    for bsecode, filename in zip(bsecodes, stock_quote_files):
        latest_data[bsecode] = parse_stock_quote_page_file(filename)
    df = pd.DataFrame.from_dict(latest_data, orient='index')
    df.to_csv(os.path.join(moneycontrol_data_dir, 'latest_stock_data.csv'), index_label='bsecode')
            
if __name__ == '__main__':
    run()

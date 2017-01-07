#! /usr/bin/env python

import urllib2 as urllib2
from bs4 import BeautifulSoup

def make_csv(table, sep=','):
    rows = table.find_all('tr')
    t = ''
    for tr in rows:
        cols = tr.find_all('td')
        r = ''
        for td in cols:
            r = r + td.text.strip() + sep
        t = t+r+'\n'
    return t
    

def get_tables(file=None, url=None, html=None, sep=','):
    if url:
        stream = urllib2.urlopen(url)
        soup = BeautifulSoup(stream.read(), 'lxml')
    elif html:
        soup = BeautifulSoup(html, 'lxml')
    elif file:
        soup = BeautifulSoup(open(file).read(), 'lxml')
    tables = soup.find_all('table')
    table_list = []
    for table in tables:
        table_list.append(make_csv(table, sep=sep))
    return table_list
    

if __name__ == '__main__':
    tables = get_tables('http://www.moneycontrol.com/financials/indianhotels/results/consolidated-yearly/IHC')
    for i, table in enumerate(tables):
        print "======== Table %i ========" % (i)
        print table
        
    print tables[4]

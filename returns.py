#! /usr/bin/env python

import os
import pandas as pd
import hisdata
import indexconstituents
from config import data_dir
from multiprocessing import Pool, cpu_count

ncpus = cpu_count()

stock_data_dir = os.path.join(data_dir, 'stocks')
stock_data_file_name = lambda bsecode: os.path.join(stock_data_dir, bsecode+'.csv')

def _get_stock_returns(bsecode):
    return hisdata.Stock(bsecode).returns

def get_relative_returns(index):
    csv_file_returns = index + '_returns.csv'
    csv_file_relative_returns = index + '_relative_returns.csv'

    if index == 'sensex':
        const = indexconstituents.IndexConstituents().sensex
    elif index == 'midcap':
        const = indexconstituents.IndexConstituents().midcap
    elif index == 'smallcap':
        const = indexconstituents.IndexConstituents().smallcap
    elif index == 'bse100':
        const = indexconstituents.IndexConstituents().bse100
    elif index == 'bse200':
        const = indexconstituents.IndexConstituents().bse200
    elif index == 'bse500':
        const = indexconstituents.IndexConstituents().bse500
    elif index == 'capital_goods':
        const = indexconstituents.IndexConstituents().capital_goods
    elif index == 'consumer_durables':
        const = indexconstituents.IndexConstituents().consumer_durables
    elif index == 'fmcg':
        const = indexconstituents.IndexConstituents().fmcg
    elif index == 'health_care':
        const = indexconstituents.IndexConstituents().health_care
    elif index == 'it':
        const = indexconstituents.IndexConstituents().it
    elif index == 'metal':
        const = indexconstituents.IndexConstituents().metal
    elif index == 'oilgas':
        const = indexconstituents.IndexConstituents().oilgas
    elif index == 'auto':
        const = indexconstituents.IndexConstituents().auto
    elif index == 'psu':
        const = indexconstituents.IndexConstituents().psu
    elif index == 'teck':
        const = indexconstituents.IndexConstituents().teck
    elif index == 'bankex':
        const = indexconstituents.IndexConstituents().bankex
    elif index == 'realty':
        const = indexconstituents.IndexConstituents().realty
    elif index == 'power':
        const = indexconstituents.IndexConstituents().power

    company_names = const.company_name
    sensex_returns = hisdata.Index('bse_sensex').returns

    # keep only bsecodes of files whose data exists
    bsecodes = [bsecode for bsecode in const.bsecode if os.path.exists(stock_data_file_name(bsecode))]

    # compute the returns of the companies
    #returns = {bsecode: hisdata.Stock(bsecode).returns for bsecode in bsecodes}
    # using multiprocessing
    p = Pool(ncpus)
    returns = p.map(_get_stock_returns, bsecodes)
    returns = dict(zip(bsecodes, returns))

    # get the returns of the sensex as index
    returns['sensex'] = hisdata.Index('bse_sensex').returns

    # make a dataframe of the results
    returns = pd.DataFrame.from_dict(returns, orient='index')

    # get the relative returns
    relative_returns = returns/returns.ix['sensex']

    # add the company names to the dataframe
    returns['company_name'] = company_names
    relative_returns['company_name'] = company_names

    # sort the results based on the 10y return and write to file
    returns = returns.sort('10y') 
    relative_returns = relative_returns.sort('10y')

    # write to file
    cols_to_write = ['company_name', '1m', '3m', '6m', '1y', '2y', '3y', '4y', '5y',
                                     '6y', '7y', '8y', '9y', '10y']
    returns.to_csv(csv_file_returns, cols=cols_to_write, na_rep='na')
    relative_returns.to_csv(csv_file_relative_returns, cols=cols_to_write, na_rep='na')

for index in ['sensex', 'midcap', 'smallcap',
              'bse100', 'bse200', 'bse500',
              'capital_goods', 'consumer_durables',
              'fmcg', 'health_care', 'it', 'metal',
              'oilgas', 'auto', 'psu', 'teck',
              'bankex', 'realty', 'power']:
    get_relative_returns(index)

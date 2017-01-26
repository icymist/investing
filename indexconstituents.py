#! /usr/bin/env python

import os
import pandas as pd
from config import bse_indices_data_dir
from glob import glob


def get_index_name(index_file_name):
    s = os.path.split(os.path.splitext(index_file_name)[0])[-1]
    s = s.replace('S&P BSE ', '')
    s = s.replace('index_Constituents', '')
    s = s.replace('& ', '').replace(' ', '_')
    s = s.lower()
    s = 'bse_' + s

    return s

def test_get_index_name():
    assert get_index_name('S&P BSE SmallCapindex_Constituents.csv') == 'bse_smallcap'


bse_index_files = glob(os.path.join(bse_indices_data_dir, '*BSE*.csv'))

bse_index_names = [get_index_name(f) for f in bse_index_files]

index_name_to_file_map = {get_index_name(f): f for f in bse_index_files}


def get_index_constituents(index_name):
    df = pd.read_csv(index_name_to_file_map.get(index_name))
    df.columns = ['bsecode', 'company', 'isin', 'close']
    return df

def get_all_indices_constituents():
    bse_indices = {index: get_index_constituents(index) for index in bse_index_names}

    return bse_indices

if __name__ == '__main__':
    for ix in bse_indices.keys():
        print ix
        print bse_indices.get(ix)._df.head()[['bsecode', 'company']]
        print

    print bse_indices.get('bse_sensex_50')._df[['company']]


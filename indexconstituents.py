#! /usr/bin/env python

import os
import pandas as pd
from config import indices_dir

index_groups = """
S&P BSE SENSEX
S&P BSE 500
S&P BSE 100
S&P BSE 200
S&P BSE CAPITAL GOODS
S&P BSE CONSUMER DURABLES
S&P BSE FMCG
S&P BSE HEALTHCARE
S&P BSE IT
S&P BSE METAL
S&P BSE OIL & GAS
S&P BSE AUTO
S&P BSE PSU
S&P BSE TECK
S&P BSE BANKEX
S&P BSE MID CAP
S&P BSE SMALL CAP
S&P BSE REALTY
S&P BSE POWER
S&P BSE IPO
S&P BSE GREENEX
S&P BSE SME IPO
S&P BSE CARBONEX
""".strip().split('\n')

index_constituents_file = os.path.join(indices_dir, 'bse_index_constituents.csv')
cols = ['index_name', 'bsecode', 'company_name', 'free_float', 'industry']

class IndexConstituents:
    def __init__(self):
        self._file = index_constituents_file
        self._df = pd.read_csv(index_constituents_file, skiprows=2,
                header=None, names=cols, skipinitialspace=True)
        self._df.bsecode = self._df.bsecode.astype(str)
        self._df = self._df.set_index('bsecode', drop=False)

    @property
    def df(self):
        return self._df

    @property
    def sensex(self):
        return self._df[self._df.index_name == 'S&P BSE SENSEX']

    @property
    def bse500(self):
        return self._df[self._df.index_name == 'S&P BSE 500']

    @property
    def bse100(self):
        return self._df[self._df.index_name == 'S&P BSE 100']

    @property
    def bse200(self):
        return self._df[self._df.index_name == 'S&P BSE 200']

    @property
    def capital_goods(self):
        return self._df[self._df.index_name == 'S&P BSE CAPITAL GOODS']

    @property
    def consumer_durables(self):
        return self._df[self._df.index_name == 'S&P BSE CONSUMER DURABLES']

    @property
    def fmcg(self):
        return self._df[self._df.index_name == 'S&P BSE FMCG']

    @property
    def health_care(self):
        return self._df[self._df.index_name == 'S&P BSE HEALTHCARE']

    @property
    def it(self):
        return self._df[self._df.index_name == 'S&P BSE IT']

    @property
    def metal(self):
        return self._df[self._df.index_name == 'S&P BSE METAL']

    @property
    def oilgas(self):
        return self._df[self._df.index_name == 'S&P BSE OIL & GAS']

    @property
    def auto(self):
        return self._df[self._df.index_name == 'S&P BSE AUTO']

    @property
    def psu(self):
        return self._df[self._df.index_name == 'S&P BSE PSU']

    @property
    def teck(self):
        return self._df[self._df.index_name == 'S&P BSE TECK']

    @property
    def bankex(self):
        return self._df[self._df.index_name == 'S&P BSE BANKEX']

    @property
    def midcap(self):
        return self._df[self._df.index_name == 'S&P BSE MID CAP']

    @property
    def smallcap(self):
        return self._df[self._df.index_name == 'S&P BSE SMALL CAP']

    @property
    def realty(self):
        return self._df[self._df.index_name == 'S&P BSE REALTY']

    @property
    def power(self):
        return self._df[self._df.index_name == 'S&P BSE POWER']

    @property
    def ipo(self):
        return self._df[self._df.index_name == 'S&P BSE IPO']

    @property
    def greenex(self):
        return self._df[self._df.index_name == 'S&P BSE GREENEX']

    @property
    def smeipo(self):
        return self._df[self._df.index_name == 'S&P BSE SME IPO']

    @property
    def carbonex(self):
        return self._df[self._df.index_name == 'S&P BSE CARBONEX']

    def exclude_useless_companies(self):
        # exclude greenex, carbonex, ipo, sme ipo
        df = self._df[self._df.index_name != 'S&P BSE GREENEX']
        df = self._df[self._df.index_name != 'S&P BSE CARBONEX']
        df = self._df[self._df.index_name != 'S&P BSE IPO']
        df = self._df[self._df.index_name != 'S&P BSE SME IPO']
        return df

    @property
    def companies(self):
        companies = self.exclude_useless_companies()
        return set(companies.bsecode)

    @property
    def company_names(self):
        df = self._df['company_name'].drop_duplicates()
        return df

    @property
    def industries(self):
        return set(self._df.industry)

    @property
    def consumer_durables_companies(self):
        pass


if __name__ == '__main__':
    ic = IndexConstituents()
    #print ic.sensex.company_name
    #print ic.midcap.company_name
    #print ic.smallcap.company_name
    print ic.company_names

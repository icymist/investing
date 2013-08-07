#! /usr/bin/env python

"""
Script to search for a given stock based on regular expression. Only returns
the bsecode if the stock is in any one of the BSE Indices.
"""

import argparse
from hisdata import stock_search

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('string')

    args = parser.parse_args()

    print stock_search(args.string)

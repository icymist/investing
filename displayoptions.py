#! /usr/bin/env python

"""
Script to display option and return the selected option as an integer. The
choices that have to be passed should be iterable and should be printable.
"""
from hisdata import stock_search

def display_options(lst):
    for i, option in enumerate(lst):
        print '%2.2i. %s' % (i, option)
    print
    s = raw_input('Choose an option: ')
    return int(s)


if __name__ == '__main__':
    matches = stock_search('tata')
    choice = display_options(matches)
    print matches.index[choice]

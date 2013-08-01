#! /usr/bin/env python

from datetime import datetime
import pandas as pd

def dateparser(d):
    if type(d) is type((0,1)):
        date = datetime(*d)
        return date
    else:
        return d

if __name__ == '__main__':
    d = datetime.now()
    pd_date = pd.to_datetime([d])
    print pd_date
    print type(pd_date)

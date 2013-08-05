#! /usr/bin/env python

import re
from datetime import datetime
import pandas as pd
from pandas.tseries.offsets import DateOffset

today = datetime.today()
today = datetime(today.year, today.month, today.day)

re_years = re.compile(r'-(\d+)y')
re_months = re.compile(r'-(\d+)m')
re_years_months = re.compile(r'-(\d+)y(\d+)m')
re_years_months_days = re.compile(r'-(\d+)y(\d+)m(\d+)d')

def dateparser(d):
    # order is important
    # first check for custom types and finally check for generic type
    if isinstance(d, type((0,1))):
        date = datetime(*d)
        return date
    elif re_years_months_days.match(d):
        years, months, days = re_years_months_days.match(d).groups()
        years, months, days = int(years), int(months), int(days)
        return today - DateOffset(years=years, months=months, days=days)
    elif re_years_months.match(d):
        years, months = re_years_months.match(d).groups()
        years = int(years)
        months = int(months)
        return today - DateOffset(years=years, months=months)
    elif re_years.match(d):
        years = re_years.match(d).groups()[0]
        years = int(years)
        #print years
        return today - DateOffset(years=years)
    elif re_months.match(d):
        months = re_months.match(d).groups()[0]
        months = int(months)
        #print months
        return today - DateOffset(months=months)
    elif isinstance(d, type('string')):
        date = pd.to_datetime(d)
        return date
    else:
        return d

if __name__ == '__main__':
    print dateparser('-5y')
    print dateparser('-10y')
    print dateparser('-3m')
    print dateparser('-6m')
    print dateparser('-9m')
    print dateparser('-5y2m')
    print dateparser('-5y1m1d')
    print dateparser('2013-01-01')
    print dateparser((2010, 1, 1))

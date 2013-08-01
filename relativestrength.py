#! /usr/bin/env python

import hisdata
import indexconstituents

# sensex constituents
sensex_const = indexconstituents.IndexConstituents().smallcap

#start_date = (2000, 1, 1)

for bsecode in sensex_const.bsecode:
    try:
        close = hisdata.Stock(bsecode).close
        start_date = close.index[0]
        print type(start_date)
    except:
        print 'unable to get data for %s' %  (bsecode)
        continue

    # sensex closing data
    sensex_close = hisdata.Index('bse_sensex', start=start_date).close
    #print sensex_close.head()
    sensex_gains = sensex_close[-1]/sensex_close[0]

    # scrip gains
    gains = close[-1]/close[0]
    if gains > sensex_gains:
        for i in sensex_const[sensex_const.bsecode == bsecode]['company_name']:
            print i
        print sensex_gains, gains, gains/sensex_gains
        print

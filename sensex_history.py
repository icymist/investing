#! /usr/bin/env python

from hisdata import Index
import pandas as pd
import matplotlib.pyplot as plt

start_date = '-10y1m'
end_date = None
bse_sensex = Index('bse_sensex', start=start_date, end=end_date)
bse_midcap = Index('bse_midcap', start=start_date, end=end_date)
bse_smallcap = Index('bse_smallcap', start=start_date, end=end_date)

d = pd.DataFrame.from_dict({'bse_sensex': bse_sensex.returns,
                            'bse_midcap': bse_midcap.returns,
                            'bse_smallcap': bse_smallcap.returns})

# historical returns
print "==== Historical returns ===="
#d = (d-1)*100
print d[['bse_sensex', 'bse_midcap', 'bse_smallcap']].ix[[
            '3m', '6m', '1y', '2y', '3y', '4y', '5y', '6y', '7y', '8y', '9y', '10y']]

# Plot normalized to the start date 
d = pd.DataFrame.from_dict({'bse_sensex': bse_sensex.close/bse_sensex.close[0],
                            'bse_midcap': bse_midcap.close/bse_midcap.close[0],
                            'bse_smallcap': bse_smallcap.close/bse_smallcap.close[0]})
d.plot()

# sensex p/e statistics
print "==== Sensex P/E statistics ===="
print bse_sensex.pe.describe()

# sensex dividend yield statistics
print "==== Sensex dividend yield statistics ===="
print bse_sensex.div_yield.describe()

# plot sensex and the div_yield together
plt.figure()
bse_sensex.close.plot(label='sensex')
bse_sensex.div_yield.plot(secondary_y=True, style='r', label='div_yield')
plt.legend()
plt.savefig('sensex_vs_div_yield.png')

# plot sensex P/E and the div_yield together
plt.figure()
bse_sensex = Index('bse_sensex', start='2000-01')
bse_sensex.pe.plot(label='sensex')
bse_sensex.div_yield.plot(secondary_y=True, style='r', label='div_yield')
plt.legend()
plt.savefig('sensex_pe_vs_div_yield.png')

# plot the dividend yields of the three indices
start_date = '2006-06'
end_date = None
bse_sensex = Index('bse_sensex', start=start_date, end=end_date)
bse_midcap = Index('bse_midcap', start=start_date, end=end_date)
bse_smallcap = Index('bse_smallcap', start=start_date, end=end_date)
d = pd.DataFrame.from_dict({'bse_sensex': bse_sensex.div_yield,
                            'bse_midcap': bse_midcap.div_yield,
                            'bse_smallcap': bse_smallcap.div_yield})
d.plot()

# sensex midcap dividend yield statistics
print "==== Sensex Midcap dividend yield statistics ===="
print bse_midcap.div_yield.describe()

# sensex smallcap dividend yield statistics
print "==== Sensex Smallcap dividend yield statistics ===="
print bse_smallcap.div_yield.describe()

plt.show()

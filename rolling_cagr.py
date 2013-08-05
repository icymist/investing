#! /usr/bin/env python

import pandas as pd
from hisdata import Index
#import matplotlib.pyplot as plt
#pd.set_option('display.max_columns', 30)

sensex = Index('bse_sensex')
sensex_daily = sensex.close.asfreq('D', method='pad')
sensex_monthly = sensex.close.resample('MS')#, method='pad')
sensex_yearly = sensex.close.resample('AS')#, method='pad')

# rolling averages
ra_daily = {i: sensex_daily.pct_change(i*365) for i in range(1,24)}
ra_monthly = {i: sensex_monthly.pct_change(i*12) for i in range(1,24)}
ra_yearly = {i: sensex_yearly.pct_change(i) for i in range(1,24)}

# resample down
rs_daily = {i: ra_daily[i].resample('BAS', how='mean') for i in range(1,24)}
rs_monthly = {i: ra_monthly[i].resample('BAS', how='mean') for i in range(1,24)}
rs_yearly = {i: ra_yearly[i].resample('BAS', how='mean') for i in range(1,24)}

# calculate cagrs
cagr_daily = {i: 100*((rs_daily[i]+1)**(1/float(i))-1) for i in range(1,24)}
cagr_monthly = {i: 100*((rs_monthly[i]+1)**(1/float(i))-1) for i in range(1,24)}
cagr_yearly = {i: 100*((rs_yearly[i]+1)**(1/float(i))-1) for i in range(1,24)}

# make them into a dataframe
df_daily = pd.DataFrame(cagr_daily)
df_monthly = pd.DataFrame(cagr_monthly)
df_yearly = pd.DataFrame(cagr_yearly)

# write to csv files
df_daily.to_csv('rolling_cagr_daily.csv')
df_monthly.to_csv('rolling_cagr_monthly.csv')
df_yearly.to_csv('rolling_cagr_yearly.csv')

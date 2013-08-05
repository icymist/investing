#! /usr/bin/env python

import pandas as pd
from hisdata import Index
import matplotlib.pyplot as plt

bse_sensex = Index('bse_sensex', start='-6y')#start='2006-06-02', end='2012-06-02')
pe = bse_sensex.pe
pe_ma200 = pd.rolling_mean(pe, 200)
pe_std200 = pd.rolling_std(pe, 200)
pe_ma200_l_1std = pe_ma200 - pe_std200
pe_ma200_p_1std = pe_ma200 + 1.5*pe_std200
pe_mean = pd.Series(pe.mean(), index=pe.index)
pe_l_1std = pe_mean - pe.std()
pe_p_1std = pe_mean + pe.std()
resampled = bse_sensex.pe.resample('BAS', how='mean')
le_1std = pe[pe < pe.mean() - pe.std()]

print pe.describe()

fig, axes = plt.subplots(nrows=2, ncols=1)
pe_mean.plot(ax=axes[0], style='k', lw=1.5)
pe_l_1std.plot(ax=axes[0], style='k--', lw=1.5)
pe_p_1std.plot(ax=axes[0], style='k--', lw=1.5)
pe.plot(ax=axes[0], style='b', lw=0.5)
pe_ma200.plot(ax=axes[0], style='g', lw=1.5)
pe_ma200_l_1std.plot(ax=axes[0], style='g--', lw=1.5)
pe_ma200_p_1std.plot(ax=axes[0], style='g--', lw=1.5)

x1 = 1.5*pe_std200
x1.plot(ax=axes[1])
x2 = pe_std200
x2.plot(ax=axes[1])
y = x1-x2
y.plot(ax=axes[1])
#resampled.plot()

plt.figure()
pe_std200.plot()

plt.figure()
le_1std.plot()

plt.show()

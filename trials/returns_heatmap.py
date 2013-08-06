#! /usr/bin/env python

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv('sensex_relative_returns.csv', na_values='na', index_col=0)
#df = pd.read_csv('sensex_returns.csv', na_values='na', index_col=0)
df.index.astype(str)
df = df.fillna(0)
del df['company_name']
df = df.sort('5y', ascending=True)
fig, ax = plt.subplots()
heatmap = ax.pcolor(df[['1y', '3y', '5y', '10y']], norm=None, cmap=plt.cm.Blues, alpha=0.8)
df = df.sort('5y', ascending=False)
print df
plt.show()

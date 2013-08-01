#! /usr/bin/env python

import os

home_dir = os.environ['HOME']

investing_dir = os.path.join(home_dir, 'mytools', 'investing')

data_dir = os.path.join(home_dir, 'data', 'investing')

indices_dir = os.path.join(data_dir, 'indices')

# bhavcopies
bse_bhavcopy_data_dir = os.path.join(data_dir, 'bhavcopy', 'bse')
nse_bhavcopy_data_dir = os.path.join(data_dir, 'bhavcopy', 'nse')

# bse indices
bse_indices_data_dir = os.path.join(data_dir, 'indices')
bse30_data_file = os.path.join(bse_indices_data_dir, 'bse_sensex.csv')
midcap_data_file = os.path.join(bse_indices_data_dir, 'bse_midcap.csv')
smlcap_data_file = os.path.join(bse_indices_data_dir, 'bse_smallcap.csv')
bse100_data_file = os.path.join(bse_indices_data_dir, 'bse_100.csv')
bse200_data_file = os.path.join(bse_indices_data_dir, 'bse_200.csv')
bse500_data_file = os.path.join(bse_indices_data_dir, 'bse_500.csv')

# nse indices
nse_indices_data_dir = os.path.join(data_dir, 'nse', 'indices')

insider_trading_data_dir = os.path.join(data_dir, 'insider_trading')

# company_groups
company_groups_file = os.path.join(data_dir, 'company_groups.yaml')

# moneycontrol data
moneycontrol_data_dir = os.path.join(data_dir, 'moneycontrol')

# historical stock price data
historical_stock_data_dir = os.path.join(data_dir, 'stocks')

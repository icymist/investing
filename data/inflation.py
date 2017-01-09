import os
import pandas as pd

investing_data_dir = os.environ['INVESTING_DATA_DIR']

def cpi():
    f = os.path.join(investing_data_dir, 'macro', 'consumer_price_inflation.csv')
    df = pd.read_csv(f, parse_dates=True, index_col='year')

    df = df.sort_index()

    return df

import os
import pandas as pd

data_dir = os.environ['INVESTING_DATA_DIR']


def sensex():

    file_hist_sensex_monthly = os.path.join(data_dir, 'bse', 'hist_sensex_monthly.csv')

    df = pd.read_csv(file_hist_sensex_monthly,
                     index_col = 'date',
                     parse_dates = True,
                     dayfirst = True,
                     thousands = ',',
                     na_values = '-')

    df = df.sort_index()

    # add yearly returns

    for i, s in zip([1, 2, 3, 5, 10],
                    ['y1', 'y2', 'y3', 'y5', 'y10']):
        df[s] = df.close.pct_change(periods=i*12).shift(periods=-i*12)


    for i, p2p_return, annual_return in zip(
            [1, 2, 3, 5, 10],
            ['y1', 'y2', 'y3', 'y5', 'y10'],
            ['ay1', 'ay2', 'ay3', 'ay5', 'ay10']):
        df[annual_return] = ((df[p2p_return]+1)**(1./i)) - 1

    return df 


if __name__ == '__main__':
    print(sensex())

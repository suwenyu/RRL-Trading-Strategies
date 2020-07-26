from typing import List, Set, Dict, Tuple, Optional
from utils import read_dax

import numpy as np
import normalization
import objectivefunc
import os
import pandas as pd
import random
import scipy.optimize as opt


def read_data(data_path: str) -> pd.DataFrame:
    return pd.read_csv(data_dir + data_name, header=None)


def process_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    # TODO: add column name to be more flexible
    # check the usage of the time series

    df['avg_price'] = (df[3] + df[4]) / 2.0
    df.drop(columns=[0, 6], inplace=True)

    # split data into train test
    train_len = int(len(df) * 2 / 3)
    train_data_df = df[:train_len]
    test_data_df = df[train_len:]

    return train_data_df, test_data_df


if __name__ == "__main__":
    data_dir = os.path.dirname(os.path.realpath(__file__)) + "/data/"
    data_name = 'data.csv'

    df = read_data(data_dir + data_name)
    tr_df, te_df = process_data(df)

    train_data = tr_df.to_numpy()
    data = tr_df['avg_price'].to_numpy()
    # print(tr_df['avg_price'].diff())
    # tr_df['return'] = tr_df['avg_price'][1:].values / tr_df['avg_price'][:-1]-1
    # X = tr_df['return'][:-1].to_numpy()

    m = 10
    t = 100

    # data = np.asarray(data, dtype=np.float64)
    # data_ret = np.asarray(data_ret, dtype=np.float64)

    data = (data[1:] / data[:-1] - 1)

    X = data[:m+t]

    # theta_debug = np.asarray([0.8415, 0.9093, 0.1411, -0.7568, -0.9589, -0.2794, 0.6570],  dtype=np.float64)

    X_norm, mu, sigma = normalization.normalize(X)
    theta = np.random.randn(m + 2)

    J, grad = objectivefunc.objective(theta, X_norm, X, m)
    # print(J, grad)

    result = opt.fmin_tnc(objectivefunc.objective, theta, args=[X_norm, X, m],
                          maxfun=100, ftol=1e-3, disp=5)
    print(result)

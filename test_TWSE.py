from typing import List, Set, Dict, Tuple, Optional
from utils import read_dax

import matplotlib.pyplot as plt
import numpy as np
import normalization
import objectivefunc
import os
import pandas as pd
import random
import rewardfunc
import scipy.optimize as opt
import updatefunc


def plot_data(data, Ft, Ret):
    fig, ax = plt.subplots(3)
    ax[0].plot([i for i in range(len(data))], data, label='twse stock')
    ax[0].legend()

    ax[1].plot([i for i in range(len(Ft[1:]))], Ft[1:], label='ft')
    ax[1].legend()

    ax[2].plot([i for i in range(len(Ret))], Ret, label='ret')
    ax[2].legend()
    plt.show()


if __name__ == "__main__":
    data, data_ret = read_dax.read_twse()
    data = np.asarray(data, dtype=np.float64)
    sharp_data = []

    m = 5
    t = 600  # The number of time series inputs to the trader
    N = 100

    X = data_ret

    theta = np.random.randn(m + 2)
    X_norm, mu, sigma = normalization.normalize(X)
    J, grad = objectivefunc.objective(theta, X_norm[:m+t], X[:m+t], m)

    # first traning
    theta, cost, EXITFLAG = opt.fmin_tnc(objectivefunc.objective, theta,
                                         args=[X_norm[:m+t], X[:m+t], m],
                                         maxfun=100, ftol=1e-3, disp=5)

    Ft = updatefunc.updateFt(X_norm[: m+t], theta, t)
    miu = 1
    delta = 0.001

    Ret, sharp = rewardfunc.reward(X[: m+t], miu, delta, Ft, m)
    Ret = Ret + 1

    Ret = [Ret[i-1] * Ret[i] for i in range(1, len(Ret))]
    # TODO: plot first training result
    plot_data(data[m+1: m+t+1], Ft, Ret)

    pI = 10
    Ret = np.zeros(pI*N, )
    Ft = np.zeros(pI*N, )

    for i in range(0, pI-1):
        J, grad = objectivefunc.objective(theta, X_norm[i*N:i*N+m+t], X[i*N:i*N+m+t], m)

        theta, cost, EXITFLAG = opt.fmin_tnc(objectivefunc.objective, theta,
                                             args=[X_norm[i*N:i*N+m+t], X[i*N:i*N+m+t], m],
                                             maxfun=100, ftol=1e-3, disp=5)

        Ftt = updatefunc.updateFt(X_norm[t+i*N: t+(i+1)*N+m], theta, N)
        Rett, sharp = rewardfunc.reward(X[t+i*N: t+(i+1)*N+m], miu, delta, Ftt, m)
        sharp_data.append(sharp)
        Rett = Rett + 1
        Ret[i*N:(i+1)*N] = Rett

        for j in range(i*N, (i+1)*N+1):
            if j != 0:
                Ret[j] = Ret[j-1] * Ret[j]

        Ft[i*N:(i+1)*N] = Ftt[1:]

    D = data[m+t+1:m+t+1+pI*N]
    print(sharp_data)
    plot_data(D, Ft, Ret)

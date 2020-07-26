from typing import List, Tuple, Dict, Sequence

import numpy as np
import numpy.matlib
import rewardfunc
import updatefunc


def objective(theta: np.ndarray, Xn: np.ndarray, X: np.ndarray, m: int) -> Tuple[np.float64, np.ndarray]:

    # initialize parameters
    delta = 0.001  # transaction fee
    miu = 1  # how much to buy
    threshold = 0.4
    origin_capital = 10
    t = len(X) - m

    Ft = updatefunc.updateFt(Xn, theta, t)
    Ret, sharp = rewardfunc.reward(X, miu, delta, Ft, m)

    J = sharp * (-1)

    xt = np.zeros(m + 2)
    dFt = np.zeros((m+2, t+1))

    for i in range(1, t):
        xt[0] = 1
        xt[1: m+1] = Xn[i-1: i+m-1]
        xt[m+1] = Ft[i-1]

        dFt[:, i] = (1-np.square(np.tanh(np.sum(theta * xt)))) * (xt + theta[m+1] * dFt[:, i-1])

    dRtFt = -1 * miu * delta * np.sign(Ft[1:]-Ft[:-1])

    dRtFtt = miu * X[m:t+m] + miu * delta * np.sign(Ft[1:]-Ft[:-1])

    A = np.sum(Ret) / t
    B = np.sum(np.multiply(Ret, Ret)) / t
    S = A / np.sqrt(B - A ** 2)

    # dSdA = S * (1 + S ** 2) / A
    # dSdB = -0.5 * (S ** 3) / (A ** 2)

    x = 1 / np.power((np.square(A) + B), (1/2))
    y = np.square(A) / np.power((B - np.square(A)), (3/2)) / m
    z = (-A / (2 * np.power((B - np.square(A)), (3/2)))) * 2 * Ret / t
    z = np.expand_dims(z, axis=1)

    # (-A/(2*(B - A^2)^(3/2))) * 2 * Ret / M
    x_y = np.matlib.repmat(x+y, t, 1)
    # x_y_z = x_y + z
    prefix = np.add(x_y, z)

    grad = np.sum(np.matlib.repmat(prefix.T, m+2, 1) * np.matlib.repmat(dRtFt.T, m+2, 1) * dFt[:,1:] + np.matlib.repmat(dRtFtt.T, m+2, 1) * dFt[:,:t], axis=1)
    # print(grad.shape)
    grad = grad * -1
    return J, grad

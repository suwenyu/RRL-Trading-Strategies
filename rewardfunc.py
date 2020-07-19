from typing import List, Tuple, Dict, Sequence


import numpy as np
import sharpratio


def reward(X: np.ndarray, miu: int, delta: float, Ft:np.ndarray, M: int) -> Tuple[np.ndarray, np.float64]:
    T = len(Ft) - 1

    Ret = miu * (np.multiply(Ft[:T], X[M:M+T]) - delta * abs((Ft[1:]-Ft[:-1])))
    # print(Ret.shape)

    sharp = sharpratio.sharpratio(Ret)

    return Ret, sharp
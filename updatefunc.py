from typing import List, Tuple, Dict, Sequence
import numpy as np


def updateFt(X: np.ndarray, theta: np.ndarray, t: int) -> np.ndarray:

    m = len(theta) - 2
    Ft = np.zeros(t+1)
    Xt = np.zeros(m + 2)

    for i in range(1, t+1):
        Xt[0] = 1
        Xt[1: m+1] = X[i-1: i+m-1]
        Xt[m+1] = Ft[i-1]

        Ft[i] = np.tanh(np.sum(Xt * theta))
        # Ft[i] = 1 if val > threshold else 0

    return Ft

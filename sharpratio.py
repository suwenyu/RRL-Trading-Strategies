from typing import List, Tuple, Dict, Sequence

import numpy as np


def sharpratio(Ret: np.ndarray):
    T = len(Ret)
    ER = np.sum(Ret) / T
    ERS = np.sum(np.power(Ret, 2)) / T
    sharp = ER / np.sqrt(ERS - np.power(ER, 2))
    return sharp

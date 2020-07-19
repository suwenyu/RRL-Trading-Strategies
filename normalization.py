from typing import List, Tuple, Dict, Sequence

import numpy as np


def normalize(X: np.ndarray) -> Tuple[np.ndarray, np.float64, np.float64]:
    X_norm = (X - np.mean(X)) / np.std(X)

    mu = np.mean(X)
    sigma = np.std(X)

    return X_norm, mu, sigma


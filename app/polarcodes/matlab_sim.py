"""
Simulates the behaviour of Matlab operations
"""
import numpy as np


def div(a, b):

    if a == np.Inf and b == 0:
        return np.inf

    if a == 0 and b == 0:
        return np.nan

    if a > 0 and b == 0:
        return np.inf

    return a / b


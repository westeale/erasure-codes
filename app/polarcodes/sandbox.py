from random import random

import numpy as np

a = np.array([1, np.nan])

b = np.array([1, 0])

c = np.bitwise_xor(a, b)

print(c)


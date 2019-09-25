from random import random

import numpy as np

true_counter = 0
false_counter = 0
n = 10000000

for i in range(n):
    is_true = random() < 0.2
    if is_true:
        true_counter += 1
    else:
        false_counter += 1

print(true_counter / n)


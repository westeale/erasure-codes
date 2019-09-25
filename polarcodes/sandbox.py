from random import shuffle

import numpy as np

from polarcodes.channel_finder import find_good_channels

encoded_input = np.array([0, 0, 1, 0, 1, 1, 1, 0])

EPSILON = 0.2

n_bits_to_erase = int(len(encoded_input) * EPSILON)

positions = [True] * n_bits_to_erase + [False] * (len(encoded_input) - n_bits_to_erase)

shuffle(positions)

print(positions)

u = [1, 2, 3, 4, 5, 6, 7, 8]
j = 6

u = u[:j-1]

print(u)


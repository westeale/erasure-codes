"""
 Simulate a BEC channel by erasing (=> NaN) each component with
 probability EPSILON.

 received_output = simulate_BEC_channel(encoded_input, EPSILON)

 INPUT
   encoded_input   1 x BLOCKLENGTH vector
   EPSILON         scalar

 OUTPUT
%  received_output 1 x BLOCKLENGTH vector
"""
from random import shuffle

import numpy as np


def simulate_bec_channel(encoded_input, EPSILON):

    n_bits_to_erase = int(len(encoded_input) * EPSILON)

    # TODO remove line
    n_bits_to_erase = 0

    positions = [True] * n_bits_to_erase + [False] * (len(encoded_input) - n_bits_to_erase)

    shuffle(positions)

    # TODO delete line
    positions = [False] * 8
    positions[1] = True

    for i in range(len(encoded_input)):
        if positions[i]:
            encoded_input[i] = np.nan




    return encoded_input

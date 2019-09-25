"""
 Encode the input vector, by adding the frozen bits and performing the
 polar transform.

 encoded_input = encode_input(input, frozen_bits, A, A_c)

 INPUT
   input           1 x K vector (in increasing order)
   frozen_bits     1 x (BLOCKLENGTH-K) vector (in increasing order)
   A               1 x BLOCKLENGTH logical vector
   A_c             1 x BLOCKLENGTH logical vector

 OUTPUT
   encoded_input   1 x BLOCKLENGTH vector
"""
import numpy as np


def encode_input(input, frozen_bits, A, A_c, blocklength):

    # Concatenate input and frozen bits
    # TODO use bitwise operations to combine bits and frozen bits
    bits_to_combine = np.zeros(blocklength)

    input_idx = 0
    frozen_idx = 0

    for i in range(blocklength):
        if A[i]:
            bits_to_combine[i] = input[input_idx]
            input_idx += 1
        else:
            bits_to_combine[i] = frozen_bits[frozen_idx]
            frozen_idx += 1

    # Recursively combine the bits using polar transformation
    encoded_input = combine_bits(bits_to_combine, blocklength)

    return encoded_input



"""
 Recursively combine the bits using polar transformation
 See Arikan paper figure 3
 
 INPUT
   u               1 x BLOCKLENGTH vector
   BLOCKLENGTH     scalar
 
 OUTPUT
   x               1 x BLOCKLENGTH vector
"""
def combine_bits(u, blocklength):
    if blocklength == 1:
        x = u
        return x

    #TODO Check if correctly ended
    u_odd = u[::2]
    u_even = u[1::2]

    # TODO find out which bitwise operation instead
    s_odd = (u_odd + u_even) % 2
    s_even = u_even

    # Reverse shuffle operation R_N
    v_first_half = s_odd
    v_second_half = s_even

    # recursevely encode v
    x_first_half = combine_bits(v_first_half, blocklength / 2)
    x_second_half = combine_bits(v_second_half, blocklength / 2)

    x = np.concatenate([x_first_half, x_second_half])

    return x
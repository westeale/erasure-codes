import numpy as np


def encode_input(input, frozen_bits, a, blocklength):
    """
    Encode the input vector, by adding the frozen bits and performing the
    polar transform.

    :param input: the message to transfer
    :param frozen_bits: the bits which are frozen
    :param a: positions of the frozen bits
    :param blocklength: length of block
    :return: the encoded message after polar transform
    """
    # Concatenate input and frozen bits
    bits_to_combine = np.zeros(blocklength)

    input_idx = 0
    frozen_idx = 0

    for i in range(blocklength):
        if a[i] == 1:
            bits_to_combine[i] = input[input_idx]
            input_idx += 1
        else:
            bits_to_combine[i] = frozen_bits[frozen_idx]
            frozen_idx += 1

    # Recursively combine the bits using polar transformation
    encoded_input = combine_bits(bits_to_combine, blocklength)


    return encoded_input


def combine_bits(u, blocklength):
    """
    Recursively combine the bits using polar transformation
    See Arikan paper figure 3
    :param u: bits to combine
    :param blocklength: length of the current block
    :return: encoded message
    """
    if blocklength == 1:
        x = u
        return x

    u_odd = u[::2]
    u_even = u[1::2]

    s_odd = np.logical_xor(u_odd, u_even)
    s_even = u_even

    # Reverse shuffle operation R_N
    v_first_half = s_odd
    v_second_half = s_even

    # recursevely encode v
    x_first_half = combine_bits(v_first_half, blocklength / 2)
    x_second_half = combine_bits(v_second_half, blocklength / 2)

    x = np.concatenate([x_first_half, x_second_half])

    return x
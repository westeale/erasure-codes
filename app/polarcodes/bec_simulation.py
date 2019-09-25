"""
 Simulate a BEC channel by erasing (=> NaN) each component with
 probability EPSILON.
"""
from random import shuffle, random
import numpy as np


def simulate_bec_channel(encoded_input, epsilon, true_random=False):
    """
    Replaces random bits with NaN values

    :param encoded_input_copy: Numpy array with either 0 or 1
    :param epsilon: probability of bit erasure
    :param true_random: if true: every bit gets possibility of epsilon to get erased.
            if false: guaranteed amount of epsilon % bits erased

    :return: Numpy array with erased bits
    """
    length = len(encoded_input)

    if true_random:
        positions = _get_random_erasures(length, epsilon)
    else:
        positions = _get_percentage_erasures(length, epsilon)

    for i in range(length):
        if positions[i]:
            encoded_input[i] = np.nan

    return encoded_input


def erase_bits(encoded_input, bits_to_erase):
    """
    Erase bits based on boolean list

    :param encoded_input_copy: numpy array of bits
    :param bits_to_erase: list of boolean (same length as input)
    :return: numpy array with erased bits (NaN)
    """
    encoded_input_copy = encoded_input.copy()

    for i in range(len(encoded_input_copy)):
        if bits_to_erase[i]:
            encoded_input_copy[i] = np.nan

    return encoded_input_copy


def _get_random_erasures(length, epsilon):
    erasure_positions = [False] * length

    for i in range(length):
        if random() < epsilon:
            erasure_positions[i] = True

    return erasure_positions


def _get_percentage_erasures(length, epsilon):
    n_bits_to_erase = int(length * epsilon)
    erasure_positions = [True] * n_bits_to_erase + [False] * (length - n_bits_to_erase)
    shuffle(erasure_positions)
    return erasure_positions

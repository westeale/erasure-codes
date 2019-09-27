import numpy as np


def find_good_channels(z, k, blocklength):
    """
    Find the K channels with the smallest value Z
    :param z: 1 x BLOCKLENGTH vector of bhattacharyya parameters
    :param k: scalar
    :param blocklength: length of the block
    :return: k channels with smalles value z
    """

    # Calculate sorted indizes of Z
    sorted_indices = np.argsort(z)

    A = np.zeros(blocklength)

    for i in range(k):
        A[sorted_indices[i]] = 1

    return A
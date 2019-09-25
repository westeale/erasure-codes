"""
 Find the K channels with the smallest value Z

 [A, A_c] = find_good_channels(Z, K)

 INPUT
   Z       1 x BLOCKLENGTH vector
   K       scalar

 OUTPUT
   A       1 x BLOCKLENGTH logical vector
   A_c     1 x BLOCKLENGTH logical vector
"""
import numpy as np


def find_good_channels(Z, K, blocklength):
    # TODO: make better performance
    # Calculate sorted indizes of Z
    sorted_indices = np.argsort(Z)

    A = [False] * blocklength
    A_c = [False] * blocklength

    for i in range(K):
        A[sorted_indices[i]] = True

    # TODO: improve performance by inverting list
    for i in range(K, len(sorted_indices)):
        A_c[sorted_indices[i]] = True


    return A, A_c
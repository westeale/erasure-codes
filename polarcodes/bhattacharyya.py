"""
Compute the bhattacharyya parameters for the synthetic channels obtained
from BEC channels. This will allow to choose which bits should be frozen.

Z = compute_bhattacharyya_BEC(EPSILON, BLOCKLENGTH)

 Note that the implementation is recursive (for understanding purpose
 rather that performance purpose).

 Also note that BLOCKLENGTH has to be a power of 2.

 INPUT
   EPSILON     scalar
   BLOCKLENGTH scalar

 OUTPUT
   Z           vector 1 x BLOCKLENGTH
"""
import numpy as np

def compute_bhattacharyya_BEC(epsilon, blocklength):

    if blocklength == 1:
        # Terminate recursion
        Z = np.array([epsilon])
    else:
        # Recursively compute bhattacharyya parameters for half the blocklength
        Z_half = compute_bhattacharyya_BEC(epsilon, blocklength / 2)

        # Compute odd and even-indices bhattacharyya parameters that we obtain when
        # performing one more transform
        Z_half_odd = (2 * Z_half) - Z_half ** 2
        Z_half_even = Z_half ** 2
        Z_append = np.array([Z_half_odd, Z_half_even])

        # Merge odd and even indices into a 1 x BLOCKLENGTH vector
        Z = np.reshape(Z_append, (1, int(blocklength)), order='F')[0]

    return Z
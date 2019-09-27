import numpy as np


def compute_bhattacharyya_bec(epsilon, blocklength):
    """
    Compute the bhattacharyya parameters for the synthetic channels obtained
    from BEC channels. This will allow to choose which bits should be frozen.

    :param epsilon: Erasure rate of BEC
    :param blocklength: Must be a power of 2
    :return: bhattacharyya parameters
    """
    if blocklength == 1:
        # Terminate recursion
        z = np.array([epsilon])
    else:
        # Recursively compute bhattacharyya parameters for half the blocklength
        z_half = compute_bhattacharyya_bec(epsilon, blocklength / 2)

        # Compute odd and even-indices bhattacharyya parameters that we obtain when
        # performing one more transform
        z_half_odd = (2 * z_half) - z_half ** 2
        z_half_even = z_half ** 2
        z_appended= np.array([z_half_odd, z_half_even])

        # Merge odd and even indices into a 1 x BLOCKLENGTH vector
        z = np.reshape(z_appended, (1, int(blocklength)), order='F')[0]

    return z
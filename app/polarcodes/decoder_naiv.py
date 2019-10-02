"""
 Decode the received vector in a naive way (without dynamic programming).

 decoded_output = decode_output_BEC_naive(received_output, frozen_bits, A, A_c)
"""
import numpy as np

from app.polarcodes.exceptions.exceptions import CouldNotDecodeError, InvalidCharacterInMessage, UnexpectedLikeliHood
from app.polarcodes.helper import div


def decode_output_naive(received_output, frozen_bits, a):
    """
    Decodes message without lookup-tables
    -->   Complexity: O(N^2)
    :param received_output: output to decode
    :param frozen_bits: frozen bits for the BEC channel
    :param a: position of the frozen bits
    :return: decoded message
    """
    blocklength = len(received_output)

    # Put frozen bits in a 1 x BLOCKLENGTH vector, at positions A_c for easyier access
    frozen_bits_expanded = np.empty(blocklength)
    frozen_bits_expanded[:] = np.nan

    input_idx = 0
    for i in range(blocklength):
        if a[i] == 0:
            frozen_bits_expanded[i] = frozen_bits[input_idx]
            input_idx += 1

    # Decoding bit by bit (without reusing previous results
    decoded_output = np.empty(blocklength)
    decoded_output[:] = np.nan

    for j in range(1, blocklength + 1):
        if a[j-1] == 0:

            # If the bit is frozen, we dont need to compute anything
            decoded_output[j-1] = frozen_bits_expanded[j-1]

        else:

            # To decode, first compute the likelihood ratio using the previously decoded bits
            current_lr = compute_lr(received_output, decoded_output[:j-1], blocklength, j)

            # Then decide according to the lr
            decoded_output[j-1] = decide(current_lr)

            # If we cannot recover (erasure), we stop decoding
            if np.isnan(decoded_output[j-1]):
                raise CouldNotDecodeError

    decode_index = 0
    decoded_plain = np.zeros(np.count_nonzero(a))
    # Return the information bits
    for i in range(blocklength):
        if a[i] == 1:
            decoded_plain[decode_index] = decoded_output[i]
            decode_index += 1

    return decoded_plain


def compute_lr(y, u, n, j):
    """
    Compute the likelihood ration using channels outputs and decoded bits
    See Arikan formula 74 and 75
    :param y: 1 x N vector (reduced by 2 at each recursive call)
    :param u: 1 x (j-1) vector
    :param n: scalar
    :param j: scalar
    :return: lr
    """
    # Recursion terminantion condition l(y) = W(y|0) / W(y|1)
    # Note that only this part is specific to BEC

    # j should be integer
    j = int(j)

    if n == 1:
        l = 0
        if y == 0:
            l = np.inf
        elif y == 1:
            l = 0
        elif np.isnan(y):
            l = 1
        else:
            raise InvalidCharacterInMessage

        return l

    # Use formula 74 or 75 according to the parity of j
    if j % 2 == 1:

        u_odd =  u[:j-2:2]
        u_even = u[1:j-1:2]

        n_index = int(n / 2)

        L1 = compute_lr(y[:n_index], (u_odd + u_even) % 2, n_index, (j+1)/2)

        L2 = compute_lr(y[n_index:n], u_even, n_index, (j + 1) / 2)

        # Use table decision for border cases (make diagram to understand)
        if (L1 == 0 and L2 == 0) or (np.isinf(L1) and np.isinf(L2)):
            l = np.inf
        elif (L1 == 0 and np.isinf(L2)) or (np.isinf(L1) and L2 == 0):
            l = 0
        elif (L1 == 1 and np.isinf(L2)) or (np.isinf(L1) and L2 == 1):
            l = 1
        else:
            l = (L1 * L2 + 1) / (L1 + L2)

    else:

        u_odd = u[:j-3:2]
        u_even = u[1:j-2:2]

        n_index = int(n / 2)

        L1 = compute_lr(y[:n_index], (u_odd + u_even) % 2, n_index, j/2)

        L2 = compute_lr(y[n_index:n], u_even, n_index, j/2)

        if u[j-2] == 0:
            l = L2 * L1
        else:
            l = div(L2, L1)

    return l


def decide(current_lr):
    """
    Decide according to the lr
    :param current_lr:
    :return: bit in return
    """

    decoded_bit = 0
    if current_lr == 0:
        decoded_bit = 1
    elif current_lr == np.inf:
        decoded_bit = 0
    elif current_lr == 1:
        decoded_bit = np.nan
    else:
        raise UnexpectedLikeliHood

    return decoded_bit





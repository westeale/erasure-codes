"""
 Decode the received vector in an efficient way (with dynamic programming).

 decoded_output = decode_output_BEC_naive(received_output, frozen_bits, A, A_c)

"""

import numpy as np

from app.polarcodes.exceptions.exceptions import CouldNotDecodeError, InvalidCharacterInMessage, UnexpectedLikeliHood
from app.polarcodes.helper import div


def decode_output_efficient(received_output, frozen_bits, a):
    """
    Decodes message with lookup-tables
    -->  Comploexity O(N Log N)
    :param received_output: received_output: output to decode
    :param frozen_bits: frozen bits for the BEC channel
    :param a: position of the frozen bits
    :return: decoded message
    """
    blocklength = len(received_output)

    initial_level = 1
    initial_shift_j = 0

    # Put frozen bits in a 1 x BLOCKLENGTH vector, at positions A_c, for easier access
    frozen_bits_expanded = np.empty(blocklength)
    frozen_bits_expanded[:] = np.nan

    input_idx = 0
    for i in range(blocklength):
        if a[i] == 0:
            frozen_bits_expanded[i] = frozen_bits[input_idx]
            input_idx += 1

    # Decode bit by bit in an optimized way (reusing previous results)
    l_rs = np.empty((blocklength, int(np.log2(blocklength)+1)))
    l_rs[:] = np.nan

    decoded_output = np.empty(blocklength)
    decoded_output[:] = np.nan

    for j in range(1, blocklength + 1):
        if a[j - 1] == 0:

            # If the bit is frozen, we dont need to compute anything
            decoded_output[j - 1] = frozen_bits_expanded[j - 1]

        else:

            # To decode, first compute the likelihood ratio using the previously decoded bits
            l_rs, l = compute_lr(received_output, decoded_output[:j-1], blocklength, j, l_rs, initial_shift_j, initial_level)

            # Then decide according to the lr
            decoded_output[j - 1] = decide(l)

            # If we cannot recover (erasure), we stop decoding
            if np.isnan(decoded_output[j - 1]):
                raise CouldNotDecodeError

    decode_index = 0
    decoded_plain = np.zeros(np.count_nonzero(a))
    # Return the information bits
    for i in range(blocklength):
        if a[i] == 1:
            decoded_plain[decode_index] = decoded_output[i]
            decode_index += 1

    return decoded_plain

def compute_lr(y, u, n, j, lr_s, shift_j, level):
    """
    Compute the likelihood ration using channels outputs and decoded bits
    See Arikan formula 74 and 75
     shift_j allows to compute quickly where the local j is in the LRs table
    (abs_j = j + shift_j).

    """
    # Convert to integers
    shift_j = int(shift_j)
    level = int(level)
    j = int(j)

    j_abs = shift_j + j

    # If the desired likelihood ratio already exists in the table, return
    if not np.isnan(lr_s[j_abs - 1][level - 1]):
        return lr_s, lr_s[j_abs - 1][level - 1]

    # Recursion terminantion condition L(y) = W(y|0) / W(y|1)
    # Note that only this part is specific to BEC

    if n == 1:
        if y == 0:
            l = np.inf
        elif y == 1:
            l = 0
        elif np.isnan(y):
            l = 1
        else:
            raise InvalidCharacterInMessage

        lr_s[j_abs - 1][level - 1] = l
        return lr_s, l

    # Use formula 74 or 75 according to the parity of j
    # First compute the recursive likelihood ratio (same are used)

    if j % 2 == 1:
        j_even = j + 1
    else:
        j_even = j

    u_odd = u[:j_even-2:2]
    u_even = u[1:j_even-1:2]

    n_index = int(n / 2)

    lr_s, L1 = compute_lr(y[:n_index], (u_odd + u_even) % 2, n_index, j_even / 2, lr_s, shift_j, level + 1)

    lr_s, L2 = compute_lr(y[n_index:n], u_even, n_index, j_even / 2, lr_s, shift_j + n_index, level + 1)

    # Then combine the likelihood ratio
    if j % 2 == 1:
        # Use table decision for border cases 0/0, Inf/Inf (make diagram to understand)
        if (L1 == 0 and L2 == 0) or (np.isinf(L1) and np.isinf(L2)):
            lr_s[j_abs - 1][level - 1] = np.inf
        elif (L1 == 0 and np.isinf(L2)) or (np.isinf(L1) and L2 == 0):
            lr_s[j_abs - 1][level - 1] = 0
        elif (L1 == 1 and np.isinf(L2)) or (np.isinf(L1) and L2 == 1):
            lr_s[j_abs - 1][level - 1] = 1
        else:
            lr_s[j_abs - 1][level - 1] = (L1 * L2 + 1) / (L1 + L2)
    else:
        if u[j-2] == 0:
            lr_s[j_abs - 1][level - 1] = L2 * L1
        else:
            lr_s[j_abs - 1][level - 1] = div(L2, L1)

    return lr_s, lr_s[j_abs - 1][level - 1]


def decide(current_lr):
    """
    Decide according to the lr
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




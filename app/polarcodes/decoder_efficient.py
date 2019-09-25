"""
 Decode the received vector in an efficient way (with dynamic programming).

 decoded_output = decode_output_BEC_naive(received_output, frozen_bits, A, A_c)

 Comploexity O(N Log N)  (Almost linear)

 INPUT
   received_output     1 x BLOCKLENGTH vector
   frozen_bits         1 x (BLOCKLENGTH - K) vector
   A                   1 x BLOCKLENGTH logical vector
   A_c                 1 x BLOCKLENGTH logical vector

 OUTPUT
   decoded_output      1 x K vector
"""
import numpy as np

from app.polarcodes.matlab_sim import div


def decode_output_efficient(received_output, frozen_bits, A, A_c):
    blocklength = len(received_output)

    INITIAL_LEVEL = 1
    INITIAL_SHIFT_J = 0

    # Put frozen bits in a 1 x BLOCKLENGTH vector, at positions A_c, for easier access
    frozen_bits_expanded = np.empty(blocklength)
    frozen_bits_expanded[:] = np.nan

    # TODO: make it more efficient
    input_idx = 0
    for i in range(blocklength):
        if A_c[i]:
            frozen_bits_expanded[i] = frozen_bits[input_idx]
            input_idx += 1

    # Decode bit by bit in an optimized way (reusing previous results)

    LRs = np.empty((blocklength, int(np.log2(blocklength)+1)))
    LRs[:] = np.nan

    decoded_output = np.empty(blocklength)
    decoded_output[:] = np.nan

    for j in range(1, blocklength + 1):
        if A_c[j - 1]:

            # If the bit is frozen, we dont need to compute anything
            decoded_output[j - 1] = frozen_bits_expanded[j - 1]

        else:

            # To decode, first compute the likelihood ratio using the previously decoded bits
            LRs, L = compute_lr(received_output, decoded_output[:j-1], blocklength, j, LRs, INITIAL_SHIFT_J, INITIAL_LEVEL)

            # Then decide according to the lr
            decoded_output[j - 1] = decide(L)

            # If we cannot recover (erasure), we stop decoding
            if np.isnan(decoded_output[j - 1]):
                print("Decoded Failed!")
                return received_output

    # TODO: make it more efficient
    decode_index = 0
    decoded_plain = np.zeros(A.count(True))
    # Return the information bits
    for i in range(blocklength):
        if A[i]:
            decoded_plain[decode_index] = decoded_output[i]
            decode_index += 1

    return decoded_plain


"""
 Compute the likelihood ration using channels outputs and decoded bits.
 See Arikan formula 74 and 75

 We complete the table LRs to avoid recomputing the same likelihood ratio.
 
 level indicates the recursion level (1 for decision level, log2(N)+1 for
 channel level).
 
 shift_j allows to compute quickly where the local j is in the LRs table
 (abs_j = j + shift_j).
 
 For convenience, return L := LRs(j)

 INPUT
   y           1 x N vector (reduced by 2 at each recursive call)
   u           1 x (j-1) vector (reduced by 2 at each recursive call)
   N           scalar (reduced by 2 at each recursive call)
   j           scalar (in a range {1, ..., N})
   LRs         N x N_LEVELS array, with N_LEVELS := log2(N)+1
   shift_j     scalar
   level       scalar

 OUTPUT
   LRs         N x N_LEVELS array, with N_LEVELS := log2(N)+1
   L           scalar
"""

def compute_lr(y, u, N, j, LRs, shift_j, level):
    # Convert to integers
    shift_j = int(shift_j)
    level = int(level)
    j = int(j)

    # TODO rearange those two indices: (-1)
    j_abs = shift_j + j

    # If the desired likelihood ratio already exists in the table, return
    if not np.isnan(LRs[j_abs-1][level-1]):
        return LRs, LRs[j_abs-1][level-1]

    # Recursion terminantion condition L(y) = W(y|0) / W(y|1)
    # Note that only this part is specific to BEC

    if N == 1:
        if y == 0:
            L = np.inf
        elif y == 1:
            L = 0
        elif np.isnan(y):
            L = 1
        else:
            print("Invalid character in message: {}".format(y))

        LRs[j_abs-1][level-1] = L
        return LRs, L

    # Use formula 74 or 75 according to the parity of j
    # First compute the recursive likelihood ratio (same are used)

    if j % 2 == 1:
        j_even = j + 1
    else:
        j_even = j

    u_odd = u[:j_even-2:2]
    u_even = u[1:j_even-1:2]

    n_index = int(N / 2)

    LRs, L1 = compute_lr(y[:n_index], (u_odd + u_even) % 2, n_index, j_even/2, LRs, shift_j, level+1)

    LRs, L2 = compute_lr(y[n_index:N], u_even, n_index, j_even / 2, LRs, shift_j + n_index, level + 1)

    # Then combine the likelihood ratio
    if j % 2 == 1:
        # Use table decision for border cases 0/0, Inf/Inf (make diagram to understand)
        if (L1 == 0 and L2 == 0) or (np.isinf(L1) and np.isinf(L2)):
            LRs[j_abs-1][level-1] = np.inf
        elif (L1 == 0 and np.isinf(L2)) or (np.isinf(L1) and L2 == 0):
            LRs[j_abs - 1][level - 1] = 0
        elif (L1 == 1 and np.isinf(L2)) or (np.isinf(L1) and L2 == 1):
            LRs[j_abs - 1][level - 1] = 1
        else:
            LRs[j_abs - 1][level - 1] = (L1*L2 + 1)/(L1+L2)
    else:
        if u[j-2] == 0:
            LRs[j_abs - 1][level - 1] = L2 * L1
        else:
            LRs[j_abs - 1][level - 1] = div(L2, L1)

    return LRs, LRs[j_abs-1][level-1]


"""
Decide according to the lr
"""
def decide(current_lr):
    decoded_bit = 0
    if current_lr == 0:
        decoded_bit = 1
    elif current_lr == np.inf:
        decoded_bit = 0
    elif current_lr == 1:
        decoded_bit = np.nan
    else:
        print("Unexpected likelihood ratio")

    return decoded_bit




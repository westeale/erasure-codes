"""
Migrated the code based on MATLAB code
"""

# The amount of lost data (Parameter of the channnel)
import numpy as np

from polarcodes.bec_simulation import simulate_bec_channel
from polarcodes.bhattacharyya import compute_bhattacharyya_BEC
from polarcodes.channel_finder import find_good_channels
from polarcodes.decoder_efficient import decode_output_efficient
from polarcodes.decoder_naiv import decode_output_naive
from polarcodes.encoder import encode_input

EPSILON = 0.2

# The block-length (note that it must be a power of 2)
BLOCKLENGTH = 8

# The Rate of information bits per Block
RATE = 0.5

# The number of information bits per block
K = int(RATE * BLOCKLENGTH)


# ----------------- Finding the good sythetic channels (A): --------------------------------
# Compute the bhattacharyya parameters
Z = compute_bhattacharyya_BEC(EPSILON, BLOCKLENGTH)

# Find the K channels with the smallest value Z
# Note that A and A_c are logical vectors of length N
A, A_c = find_good_channels(Z, K, BLOCKLENGTH)

# ----------------- Choose the frozen Bits: --------------------------------
# For a binary symetric channel the frozen bits doesnt matter
frozen_bits = np.zeros(BLOCKLENGTH - K)


# ----------------- Generate a binary input vector of size 1 x K: --------------------------------
# input = np.random.randint(low=0, high=2, size=K)
input = np.array([1, 0, 1, 0])

# ----------------- Encode the input vector: --------------------------------
encoded_input = encode_input(input, frozen_bits, A, A_c, BLOCKLENGTH)


# ----------------- Simulate the channel: --------------------------------
received_output = simulate_bec_channel(encoded_input, EPSILON)


# ----------------- Decode the received message: --------------------------------
# decoded_output = decode_output_naive(received_output, frozen_bits, A, A_c)
decoded_output = decode_output_efficient(received_output, frozen_bits, A, A_c)


if np.array_equal(input, decoded_output):
    print("Could transmit!")
else:
    print("Transmistion Failed")

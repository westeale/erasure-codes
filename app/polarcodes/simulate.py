"""
Simulation of polarcodes
"""

# ------------------- Setting parameters for polarcode simulation -------------------
from app.polarcodes.helper import format_printing
from app.polarcodes.polarcodes import Polarcodes

BLOCKLENGTH = 8

MESSAGE = [0, 1, 1]

K_INFORMATION_BITS = len(MESSAGE)

EPSILON = 0.25

# O(N log N) decoder?
EFFICIENT_DECODER = True

# Using % amount of random erased bits
TRUE_RANDOM = False


# ------------------- Calculating frozen bits positions -----------------------------
polarcoder = Polarcodes(EPSILON, BLOCKLENGTH, K_INFORMATION_BITS)

Z_PARAMETERS = polarcoder.z_parameters
format_printing("Z-Parameters: {}".format(Z_PARAMETERS))

FROZEN_BITS_POSITIONS = polarcoder.a
format_printing("Frozen bits positions: {}".format(FROZEN_BITS_POSITIONS))


# ------------------- Plain message ----------------------------------------------
format_printing("Message: {}".format(MESSAGE))


# ------------------- Encoding message ----------------------------------------------
ENCODED_MESSAGE = polarcoder.encode_input(MESSAGE)
format_printing("Encoded Message: {}".format(ENCODED_MESSAGE))


# ------------------- Simulating BEC channel ----------------------------------------
ERASED_MESSAGE = polarcoder.simulate_bec_channel(ENCODED_MESSAGE, TRUE_RANDOM)
format_printing("Received message: {}".format(ERASED_MESSAGE))

# ------------------- Decoding message ----------------------------------------------
DECODED_MESSAGE = polarcoder.decode_output(ERASED_MESSAGE, EFFICIENT_DECODER)
format_printing("Decoded message: {}".format(DECODED_MESSAGE))










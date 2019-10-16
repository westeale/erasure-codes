"""
Evaluating different epsilons
"""

import numpy as np
import time
from app.polarcodes.exceptions.exceptions import CouldNotDecodeError
from app.polarcodes.polarcodes import Polarcodes
import matplotlib.pyplot as plt


# ------------------- Parameters: ---------------------------------------------------

BLOCKLENGTH = 128 # Has to be to the power of 2

K_INFORMATION_BITS_RATE = 0.5

ITERATIONS_PER_EPSILON = 100

SIMULATING_TRUE_BEC = False

# O(N log N) decoder?
EFFICIENT_DECODER = True

# Recunfiguring polarcodes after each change of epsilon?
RECONFIGURATION_EPSILON = True

MAX_EPSILON = 1
EPSIOLON_STEPS = 0.25

# ------------------- Running evaluation: -------------------------------------------
blocklength = 2
while blocklength < BLOCKLENGTH:
    blocklength = blocklength*2

count_errors = []
encoding_times = []
decoding_times = []
epsilons = []

n_iterations = 0
n_errors = 0

epsilon = 0
k_information_bits = round(K_INFORMATION_BITS_RATE * blocklength)
polarcoder = Polarcodes(epsilon, blocklength, k_information_bits)

while epsilon <= MAX_EPSILON:
    if RECONFIGURATION_EPSILON:
        polarcoder = Polarcodes(epsilon, blocklength, k_information_bits)

    iteration_errors = 0
    added_encoding_time = 0
    added_decoding_time = 0

    for i in range(ITERATIONS_PER_EPSILON):
        n_iterations += 1

        # Generating random message
        message = np.random.uniform(size=k_information_bits)
        message = list(map(lambda x: int(round(x)), message))

        start_encode = time.time()
        encoded_message = polarcoder.encode_input(message)
        end_decode = time.time()

        erased_message = polarcoder.simulate_bec_channel(encoded_message, SIMULATING_TRUE_BEC)

        added_encoding_time += (end_decode - start_encode)

        start_decode = time.time()

        try:
            decoded_message = polarcoder.decode_output(erased_message, EFFICIENT_DECODER)
        except CouldNotDecodeError:
            iteration_errors += 1
            n_errors += 1
            continue

        end_decode = time.time()
        added_decoding_time += (end_decode - start_decode)

    encoding_times.append(added_encoding_time / ITERATIONS_PER_EPSILON)
    decoding_times.append(added_decoding_time / (ITERATIONS_PER_EPSILON))

    count_errors.append(iteration_errors / ITERATIONS_PER_EPSILON)

    epsilons.append(epsilon)

    epsilon += EPSIOLON_STEPS


# ------------------- Plotting results: ---------------------------------------------
print("Amount of errors: {}".format(n_errors))
print("Amount of iterations: {}".format(n_iterations))
print("Chosen blocklength: {}".format(blocklength))

plt.figure(1)
plt.scatter(epsilons, count_errors)
plt.plot(epsilons, count_errors)
plt.ylabel('Error rate')
plt.xlabel('Epsilon')
plt.title('Average error rate')



plt.figure(2)
plt.scatter(epsilons, encoding_times)
plt.plot(epsilons, encoding_times)
plt.ylabel('Average time for encoding')
plt.xlabel('Epsilon')
plt.title('Average time for encoding')



plt.figure(3)
plt.scatter(epsilons, decoding_times)
plt.plot(epsilons, decoding_times)
plt.ylabel('Average time for decoding')
plt.xlabel('Epsilon')
plt.title('Average time for decoding')
plt.show()



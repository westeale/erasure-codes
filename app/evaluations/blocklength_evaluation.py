"""
Evaluation of time complexity of polar codes by varieng blocklength
"""

import numpy as np
import matplotlib.pyplot as plt
import time

from app.polarcodes.exceptions.exceptions import CouldNotDecodeError
from app.polarcodes.polarcodes import Polarcodes

# ------------------- Parameters: ---------------------------------------------------


MAXIMUM_BLOCKLENGTH = 1024
MINIMUM_BLOCKLENGTH = 4 # Has to be to the power of 2

K_INFORMATION_BITS_RATE = 0.5

ITERATIONS_PER_BLOCKLENGTH = 10

SIMULATING_TRUE_BEC = False

# O(N log N) decoder?
EFFICIENT_DECODER = True

EPSILON = 0.25


# ------------------- Running evaluation: -------------------------------------------

blocklength = MINIMUM_BLOCKLENGTH

count_errors = []
encoding_times = []
decoding_times = []
blocklengths = []

n_iterations = 0
n_errors = 0

while blocklength <= MAXIMUM_BLOCKLENGTH:
    k_information_bits = round(K_INFORMATION_BITS_RATE * blocklength)
    polarcoder = Polarcodes(EPSILON, blocklength, k_information_bits)

    iteration_errors = 0
    added_encoding_time = 0
    added_decoding_time = 0

    for i in range(ITERATIONS_PER_BLOCKLENGTH):

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



    encoding_times.append(added_encoding_time / ITERATIONS_PER_BLOCKLENGTH)

    decoding_times.append(added_decoding_time / (ITERATIONS_PER_BLOCKLENGTH))

    count_errors.append(iteration_errors / ITERATIONS_PER_BLOCKLENGTH)
    blocklengths.append(blocklength)
    blocklength = blocklength * 2


# ------------------- Plotting results: ---------------------------------------------

print("Amount of errors: {}".format(n_errors))
print("Amount of iterations: {}".format(n_iterations))

plt.figure(1)
plt.scatter(blocklengths, count_errors)
plt.plot(blocklengths, count_errors)
plt.xscale('log')
plt.ylabel('Error rate')
plt.xlabel('Blocklength')
plt.title('Average error rate')



plt.figure(2)
plt.scatter(blocklengths, encoding_times)
plt.plot(blocklengths, encoding_times)
plt.xscale('log')
plt.ylabel('Average time for encoding')
plt.xlabel('Blocklength')
plt.title('Average time for encoding')


plt.figure(3)
plt.scatter(blocklengths, decoding_times)
plt.plot(blocklengths, decoding_times)
plt.xscale('log')
plt.ylabel('Average time for decoding')
plt.xlabel('Blocklength')
plt.title('Average time for decoding')
plt.show()








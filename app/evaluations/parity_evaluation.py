"""
Evaluating different
"""
import numpy as np
import time
from app.polarcodes.exceptions.exceptions import CouldNotDecodeError
from app.polarcodes.polarcodes import Polarcodes
import matplotlib.pyplot as plt

BLOCKLENGTH = 128 # Has to be to the power of 2

# K information bitrate
MAX_K_RATE = 0.8

K_START = 0.2

K_STEPS = 0.1

ITERATIONS_PER_K = 10

EPSILON = 0.6

SIMULATING_TRUE_BEC = False

# O(N log N) decoder?
EFFICIENT_DECODER = True

# ------------------- Running evaluation: -------------------------------------------
blocklength = 2
while blocklength < BLOCKLENGTH:
    blocklength = blocklength*2

count_errors = []
encoding_times = []
decoding_times = []
ks = []

n_iterations = 0
n_errors = 0

k = K_START

while k <= MAX_K_RATE:
    k_information_bits = round(k * blocklength)
    polarcoder = Polarcodes(EPSILON, blocklength, k_information_bits)

    iteration_errors = 0
    added_encoding_time = 0
    added_decoding_time = 0

    for i in range(ITERATIONS_PER_K):
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

        encoding_times.append(added_encoding_time / ITERATIONS_PER_K)
        decoding_times.append(added_decoding_time / (ITERATIONS_PER_K))

        count_errors.append(iteration_errors / ITERATIONS_PER_K)

        ks.append(k)

        k += K_STEPS

# ------------------- Plotting results: ---------------------------------------------
print("Amount of errors: {}".format(n_errors))
print("Amount of iterations: {}".format(n_iterations))
print("Chosen blocklength: {}".format(blocklength))

plt.figure(1)
plt.scatter(ks, count_errors)
plt.plot(ks, count_errors)
plt.ylabel('Error rate')
plt.xlabel('Epsilon')
plt.title('Average error rate')



plt.figure(2)
plt.scatter(ks, encoding_times)
plt.plot(ks, encoding_times)
plt.ylabel('Average time for encoding')
plt.xlabel('Epsilon')
plt.title('Average time for encoding')



plt.figure(3)
plt.scatter(ks, decoding_times)
plt.plot(ks, decoding_times)
plt.ylabel('Average time for decoding')
plt.xlabel('Epsilon')
plt.title('Average time for decoding')
plt.show()



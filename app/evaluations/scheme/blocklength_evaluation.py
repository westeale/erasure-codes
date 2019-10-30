"""
Evaluation of a Security Enhanced Encryption Scheme

Comparision of complexity with regular block ciphers
"""
import numpy as np
import time
import matplotlib.pyplot as plt
from app.cipher.block_cipher import BlockCipher

# ------------------- Parameters: ---------------------------------------------------
from app.polarcodes.exceptions.exceptions import CouldNotDecodeError
from app.security_scheme import Scheme

START_BLOCKLENGTH = 64
END_BLOCKLENGTH = 1024

BEC_INFORMATION_RATE = 0.25

ERASURE_RATE = 0.25

BLOCK_CIPHER = BlockCipher.DES

KEY_SIZE = 64

ITERATIONS = 100


# ------------------- Running evaluation: -------------------------------------------
blocklength = START_BLOCKLENGTH

n_iterations = 0
n_errors = 0

encoding_times_scheme = []
encoding_times_cipher = []
decoding_times_scheme = []
decoding_times_cipher = []
count_errors = []
blocklengths = []
start_total_time = time.time()


while blocklength <= END_BLOCKLENGTH:

    iteration_errors = 0
    added_scheme_encode_time = 0
    added_cipher_encode_time = 0
    added_scheme_decode_time = 0
    added_cipher_decode_time = 0

    bec_blocklength = round(blocklength / BEC_INFORMATION_RATE)
    scheme = Scheme(BLOCK_CIPHER, KEY_SIZE, blocklength, ERASURE_RATE, bec_blocklength)
    cipher = BlockCipher(BLOCK_CIPHER, KEY_SIZE, blocklength)

    # Setting keys
    key = np.random.uniform(size=KEY_SIZE)
    key = list(map(lambda x: int(round(x)), key))
    scheme.set_key(key)
    cipher.set_secret_key(key)

    for i in range(ITERATIONS):
        n_iterations += 1

        # Generating random message
        message = np.random.uniform(size=blocklength)
        message = list(map(lambda x: int(round(x)), message))

        # Simple block cipher for comparison
        start_encode = time.time()
        encoded_message = cipher.encrypt_message(message)
        end_encode = time.time()

        added_cipher_encode_time += (end_encode - start_encode)

        start_decode = time.time()
        cipher.decrypt_message(encoded_message)
        end_decode = time.time()

        added_cipher_decode_time += (end_decode - start_decode)

        start_encode = time.time()
        encoded_message = scheme.encode(message)
        end_encode = time.time()

        added_scheme_encode_time += (end_encode - start_encode)

        start_decode = time.time()
        try:
            decoded_message = scheme.decode(encoded_message)
            if decoded_message != message:
                iteration_errors += 1
                n_errors += 1
        except CouldNotDecodeError:
            iteration_errors += 1
            n_errors += 1
            continue

        end_decode = time.time()
        added_scheme_decode_time += (end_decode - start_decode)

    encoding_times_scheme.append(added_scheme_encode_time / ITERATIONS)
    decoding_times_scheme.append(added_scheme_decode_time / ITERATIONS)
    encoding_times_cipher.append(added_cipher_encode_time / ITERATIONS)
    decoding_times_cipher.append(added_cipher_decode_time / ITERATIONS)

    count_errors.append(iteration_errors / ITERATIONS)
    blocklengths.append(blocklength)

    blocklength = blocklength * 2

end_total_time = time.time()

# ------------------- Plotting results: ---------------------------------------------
print("Amount of errors: {}".format(n_errors))
print("Amount of iterations: {}".format(n_iterations))
print("Total time: {}".format((end_total_time - start_total_time)))

plt.figure(1)
plt.scatter(blocklengths, count_errors)
plt.plot(blocklengths, count_errors)
plt.xscale('log')
plt.ylabel('Error rate')
plt.xlabel('Blocklength')
plt.title('Average error rate')



plt.figure(2)
plt.scatter(blocklengths, encoding_times_scheme)
plt.plot(blocklengths, encoding_times_scheme)
plt.scatter(blocklengths, encoding_times_cipher)
plt.plot(blocklengths, encoding_times_cipher)
plt.xscale('log')
plt.ylabel('Average time for encoding')
plt.xlabel('Blocklength')
plt.title('Average time for encoding')
plt.legend(("Scheme", "Regular Cipher"))


plt.figure(3)
plt.scatter(blocklengths, decoding_times_scheme)
plt.plot(blocklengths, decoding_times_scheme)
plt.scatter(blocklengths, decoding_times_cipher)
plt.plot(blocklengths, decoding_times_cipher)
plt.xscale('log')
plt.ylabel('Average time for decoding')
plt.xlabel('Blocklength')
plt.title('Average time for decoding')
plt.legend(("Scheme", "Regular Cipher"))
plt.show()



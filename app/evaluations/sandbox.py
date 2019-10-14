import numpy as np

from des import DesKey

from speck import SpeckCipher


# encode
def bits_to_bytes(bits):
    s = ''.join(str(e) for e in bits)
    return int(s, 2).to_bytes(len(s) // 8, byteorder='big')


# back to bits
def bytes_to_bits(bytes):
    bits = []

    for byte in bytes:
        result = list(bin(byte)[2::])
        result = list(map(int, result))
        result = [0] * (8 - len(result)) + result
        bits = bits + result

    return bits


def bits_to_hex(bits):
    s = ''.join(str(e) for e in bits)
    return int(s, 2)


def hex_2_bits(number, bit_size):
    bin_string = bin(number)[2:]
    bits = [int(i) for i in bin_string]



    return [0] * (bit_size - len(bits)) + [int(i) for i in bin_string]



bittext = message = np.random.uniform(size=96)
bittext = list(map(lambda x: int(round(x)), bittext))

print(bittext)

key = bits_to_hex(bittext)
# print(key)

my_speck = SpeckCipher(key, key_size=96, block_size=64)

bit_key = hex_2_bits(key, 96)

print(bit_key)







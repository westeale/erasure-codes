"""
Helper functions for encryption
"""

def bits_to_bytes(bits):
    s = ''.join(str(e) for e in bits)
    return int(s, 2).to_bytes(len(s) // 8, byteorder='big')


def bytes_to_bits(byts):
    bits = []

    for byte in byts:
        result = list(bin(byte)[2::])
        result = list(map(int, result))
        result = [0] * (8 - len(result)) + result
        bits = bits + result

    return bits


def bits_to_hex(bits):
    s = ''.join(str(e) for e in bits)
    return int(s, 2)


def hex_to_bits(number, bit_size):
    bin_string = bin(number)[2:]
    bits = [int(i) for i in bin_string]
    return [0] * (bit_size - len(bits)) + [int(i) for i in bin_string]


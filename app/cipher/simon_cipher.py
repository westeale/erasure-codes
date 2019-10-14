"""
Implementation of Simon cipher
"""
from simon import SimonCipher

from app.cipher.exceptions.exceptions import InvalidCipherBlockLength, InvalidKeyLength
from app.cipher.helper import bits_to_hex, hex_to_bits

VALID_PARAMS = {32: [64], 48: [72, 96], 64: [96, 128], 96: [96, 144], 128: [128, 192, 256]}


class Simon:
    def __init__(self, key_size, blocklength):
        if blocklength not in VALID_PARAMS:
            raise InvalidCipherBlockLength("Only blocklengths of 32, 48, 64, 96, 128 are allowed in Simon cipher")

        if key_size not in VALID_PARAMS[blocklength]:
            raise InvalidKeyLength("{} is not a valid keylength for the blocklength of {}".format(key_size, blocklength))

        self._key = None
        self._key = key_size
        self._blocklength = blocklength


    def set_key(self, key):
        hex_key = bits_to_hex(key)

        self._key = SimonCipher(hex_key)

    def encrypt(self, message):
        hex_message = bits_to_hex(message)

        encrypted_hex = self._key.encrypt(hex_message)

        return hex_to_bits(encrypted_hex, self._blocklength)

    def decrypt(self, message):
        hex_message = bits_to_hex(message)

        decrypted_hex = self._key.decrypt(hex_message)

        return hex_to_bits(decrypted_hex, self._blocklength)

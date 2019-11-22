"""
Implementation of Simon cipher
"""
from simon import SimonCipher

from app.cipher.exceptions.exceptions import InvalidCipherBlockLength, InvalidKeyLength
from app.cipher.helper import bits_to_hex, hex_to_bits


class Simon:
    def __init__(self, key_size, blocklength):
        if key_size != 96:
            raise InvalidKeyLength("Keylength of Simon must be 96 bits!")

        if blocklength % 64 != 0:
            raise InvalidCipherBlockLength("Blocklength of Simon should be multiplier of 64")

        self._key = None
        self._key_size = key_size
        self._blocklength = blocklength

    def set_key(self, key):
        hex_key = bits_to_hex(key)

        self._key = SimonCipher(hex_key, key_size=96, block_size=64)

    def encrypt(self, message):
        split_message = [message[x:x+64] for x in range(0, len(message), 64)]

        encrypted_message = []

        for single_message in split_message:
            hex_message = bits_to_hex(single_message)
            encrypted_hex = self._key.encrypt(hex_message)
            encrypted_message = encrypted_message + hex_to_bits(encrypted_hex, 64)

        return encrypted_message

    def decrypt(self, message):

        split_message = [message[x:x + 64] for x in range(0, len(message), 64)]
        decrypted_message = []

        for single_message in split_message:
            hex_message = bits_to_hex(single_message)
            decrypted_hex = self._key.decrypt(hex_message)
            decrypted_message = decrypted_message + hex_to_bits(decrypted_hex, 64)

        return decrypted_message

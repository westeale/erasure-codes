"""
Implementation of DES cipher
"""

from des import DesKey

from app.cipher.exceptions.exceptions import InvalidKeyLength, InvalidCipherBlockLength, WrongConfiguration
from app.cipher.helper import bits_to_bytes, bytes_to_bits


class DES:
    def __init__(self, key_size, blocklength):
        if key_size != 64:
            raise InvalidKeyLength("Keylength of DES must be 64 bits!")

        if blocklength % 64 != 0:
            raise InvalidCipherBlockLength("Blocklength of DES should be multiplier of 64")

        self._key = None

    def set_key(self, key):
        string_key = bits_to_bytes(key)

        self._key = DesKey(string_key)

        if not self._key.is_single():
            raise WrongConfiguration("3DES has been configured")

    def encrypt(self, message):
        byte_message = bits_to_bytes(message)

        encrypted_bytes = self._key.encrypt(byte_message)
        return bytes_to_bits(encrypted_bytes)

    def decrypt(self, message):
        byte_message = bits_to_bytes(message)

        decrypted_bytes = self._key.decrypt(byte_message)

        return bytes_to_bits(decrypted_bytes)





"""
A Security Enhanced Encryption Scheme and
Evaluation of Its Cryptographic Security

Based on the paper of "A Security Enhanced Encryption Scheme and
Evaluation of Its Cryptographic Security"

"""
import random

import numpy as np

from app.cipher.block_cipher import BlockCipher
from app.cipher.helper import bits_to_hex
from app.polarcodes.polarcodes import Polarcodes


class Scheme:

    def __init__(self, cipher=BlockCipher.DES, key_size=64, blocklength=64, erasure_rate=0.25, bec_block=128):
        """
        Scheme with leightweight block encryption + simulated bec channel
        :param cipher: Simon, Speck, DES
        :param key_size: bit size of key
        :param blocklength: bit size of message
        :param erasure_rate: bec erasure rate
        :param bec_block: bit size of polarcode block
        """
        self._block_cipher = BlockCipher(cipher, key_size, blocklength)
        self._information_rate = blocklength / bec_block
        self._erasure_rate = erasure_rate
        self._polarcodes = Polarcodes(erasure_rate, bec_block, blocklength)
        self._n_transmitted_messages = 0
        self._bec_block = bec_block
        self._erasure_rate = erasure_rate

    def set_key(self, key):
        """
        Setting the key
        :param key: key for encoding
        """
        self._block_cipher.set_secret_key(key)
        self._key = key

    def encode(self, message):
        """
        Encoding the message
        :param message: bit message
        :return: encoded message
        """
        encrypted_message = self._block_cipher.encrypt_message(message)
        erasure_positions = self.get_bec_positions(self._key)
        encoded_message = self._polarcodes.encode_input(encrypted_message)
        erased_message = self._polarcodes.erase_bits(encoded_message, erasure_positions)
        bec_message = erased_message[~np.isnan(erased_message)]
        return bec_message

    def get_bec_positions(self, key):
        """
        Getting the positions of the simulated bec channel
        :param key: bit key for the seed
        :return: list of booleans of bits to be erased
        """
        # n erased bits
        positions = [True] * round(self._bec_block * self._erasure_rate)
        n_erased = len(positions)

        # n kept bits
        positions = positions + [False] * (self._bec_block - n_erased)
        seed = bits_to_hex(key) + self._n_transmitted_messages
        random.Random(seed).shuffle(positions)

        return positions

    def decode(self, encoded_message):
        """
        decoding the message based on the scheme
        :param encoded_message: encoded message
        :return: decoded message
        """
        erased_bit_positions = self.get_bec_positions(self._key)
        erased_message = np.zeros(len(erased_bit_positions))
        erased_index = 0

        for i in range(len(erased_bit_positions)):
            if erased_bit_positions[i]:
                erased_message[i] = np.nan
            else:
                erased_message[i] = encoded_message[erased_index]
                erased_index += 1

        encrypted_message = self._polarcodes.decode_output(erased_message)
        encrypted_message = [int(i) for i in encrypted_message]
        decrypted_message = self._block_cipher.decrypt_message(encrypted_message)

        return decrypted_message

    def successfully_transmitted(self):
        """
        Incrementing seed for erased bits
        """
        self._n_transmitted_messages+= 1


if __name__ == '__main__':
    example = Scheme()

    key = np.random.uniform(size=64)
    key = list(map(lambda x: int(round(x)), key))

    example.set_key(key)

    message = np.random.uniform(size=64)
    message = list(map(lambda x: int(round(x)), message))

    encoded_message = example.encode(message)
    decrypted_message = example.decode(encoded_message)

    assert message == decrypted_message

    example.successfully_transmitted()

    message = np.random.uniform(size=64)
    message = list(map(lambda x: int(round(x)), message))

    encoded_message = example.encode(message)
    decrypted_message = example.decode(encoded_message)

    assert message == decrypted_message







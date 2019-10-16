"""
A simulation of polar codes (error correction) using a binary erasure channel
(BEC)
Two decoder impoemented: A "naiv" one (O(N^2)) and an "efficient" one (O(N log N))
"""
import numpy as np

from app.polarcodes import bec_simulation
from app.polarcodes.bhattacharyya import compute_bhattacharyya_bec
from app.polarcodes.channel_finder import find_good_channels
from app.polarcodes.decoder_efficient import decode_output_efficient
from app.polarcodes.decoder_naiv import decode_output_naive
from app.polarcodes.encoder import encode_input
from app.polarcodes.helper import is_power_of_2


class Polarcodes:

    def __init__(self, epsilon, blocklength=8, k_information_bits=4):
        """
        Initilazing polarcodes simulation
        :param epsilon: Erasure rate of BEC (E.g 0.2)
        :param blocklength: Must be a power of 2
        :param n_information_bits: amount of Information bits in the Block
        """
        assert is_power_of_2(blocklength), 'blocklength should be the power of 2 (E.g 8)'

        self._epsilon = epsilon
        self._blocklength = blocklength
        self._k_information_bits = k_information_bits

        # Computing the bhattacharyya parameters
        self._z_parameters = compute_bhattacharyya_bec(epsilon, blocklength)

        # Find the K channels with the smallest value Z
        # Note that A is logical vectors of length N
        self._a = find_good_channels(self._z_parameters, self._k_information_bits, self._blocklength)

        # Chose frozen bits
        self._frozen_bits = np.zeros(self._blocklength - self._k_information_bits)

    def encode_input(self, message):
        """
        Encodes the message through polar transform
        :param message: bit message of length k_information bits
        :return: the encoded message
        """
        assert len(message) == self._k_information_bits, \
            'message should have {} information bits.'.format(self._k_information_bits)

        return encode_input(message, self._frozen_bits, self._a, self._blocklength)

    def decode_output(self, received_output, efficient=True):

        assert len(received_output) == self._blocklength, \
            'message should have {} block bits.'.format(self._blocklength)

        if efficient:
            return decode_output_efficient(received_output, self._frozen_bits, self._a)
        else:
            return decode_output_naive(received_output, self._frozen_bits, self._a)

    def simulate_bec_channel(self, encoded_input, true_random=False):
        """
        Replaces random bits with NaN values

        :param encoded_input_copy: Numpy array with either 0 or 1
        :param true_random: if true: every bit gets possibility of epsilon to get erased.
                if false: guaranteed amount of epsilon % bits erased

        :return: Numpy array with erased bits
        """
        return bec_simulation.simulate_bec_channel(encoded_input, self._epsilon, true_random)

    def erase_bits(self, encoded_input, bits_to_erase):
        """
        Erase bits according to boolean list
        :param encoded_input: numpy array of bits
        :param bits_to_erase: list of booleans for bits to get erased
        :return: numpy array with NaN values
        """
        return bec_simulation.erase_bits(encoded_input, bits_to_erase)


    @property
    def z_parameters(self):
        return self._z_parameters

    @property
    def a(self):
        return self._a

    @property
    def blocklength(self):
        return self._blocklength

    @staticmethod
    def erase_bits(encoded_input, bits_to_erase):
        """
        Erase bits based on boolean list

        :param encoded_input_copy: numpy array of bits
        :param bits_to_erase: list of boolean (same length as input)
        :return: numpy array with erased bits (NaN)
        """
        return bec_simulation.erase_bits(encoded_input, bits_to_erase)


if __name__ == '__main__':
    example = Polarcodes(0.1)
    print(example.encode_input([0,0,0,0]))
    encoded_message = example.encode_input([1,1,1,0])
    erased_message = example.simulate_bec_channel(encoded_message)

    corrected_message = example.decode_output(erased_message, True)

    print(corrected_message)




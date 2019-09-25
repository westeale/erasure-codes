import unittest

import numpy as np

from app.polarcodes.bec_simulation import simulate_bec_channel, erase_bits
from app.polarcodes.bhattacharyya import compute_bhattacharyya_BEC
from app.polarcodes.channel_finder import find_good_channels
from app.polarcodes.decoder_efficient import decode_output_efficient
from app.polarcodes.decoder_naiv import decode_output_naive
from app.polarcodes.encoder import encode_input


class TestPolarCodes(unittest.TestCase):
    def test_run_integration_test(self):
        # self.assertEqual(True, False)

        # Check for correct configuration
        self._epsilon = 0.5
        self._blocklength = 8

        self._rate = 0.5
        self._k = int(self._rate * self._blocklength)
        self._z = compute_bhattacharyya_BEC(self._epsilon, self._blocklength)

        self.assertAlmostEqual(0.99609375, self._z[0], 4)
        self.assertAlmostEqual(0.87890625, self._z[1], 4)
        self.assertAlmostEqual(0.00390625, self._z[7], 4)

        self._A, self._A_c = find_good_channels(self._z, self._k, self._blocklength)

        self.assertTrue(self._A[3])
        self.assertTrue(self._A[5])
        self.assertTrue(self._A[6])

        self.assertFalse(self._A[0])
        self.assertFalse(self._A[1])

        frozen_bits = np.zeros(self._blocklength - self._k)

        messages = [[1, 0, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 1, 1]]
        erasure_0 = [False] * self._blocklength
        erasure_1 = [False] * self._blocklength
        erasure_1[0] = True

        erasure_2 = [False] * self._blocklength
        erasure_2[4] = True

        erasure_3 = [False] * self._blocklength
        erasure_3[4] = True
        erasure_3[1] = True

        erasure_4 = [False] * self._blocklength
        erasure_4[1] = True
        erasure_4[4] = True
        erasure_4[5] = True

        erasures = [erasure_0, erasure_1, erasure_2, erasure_3, erasure_4]

        for message in messages:
            encoded_input = encode_input(message, frozen_bits, self._A, self._A_c, self._blocklength)

            for erasure in erasures:
                received_output = erase_bits(encoded_input, erasure)

                decoded_output_1 = decode_output_naive(received_output, frozen_bits, self._A, self._A_c)
                decoded_output_2 = decode_output_efficient(received_output, frozen_bits, self._A, self._A_c)


                self.assertCountEqual(message, decoded_output_1)
                self.assertCountEqual(message, decoded_output_2)









if __name__ == '__main__':
    unittest.main()

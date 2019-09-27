import unittest

from app.polarcodes.polarcodes import Polarcodes


class TestPolarCodes(unittest.TestCase):
    def test_run_integration_test(self):

        # Check for correct configuration
        self._coder = Polarcodes(0.5)

        self._z = self._coder.z_parameters

        self.assertAlmostEqual(0.99609375, self._z[0], 4)
        self.assertAlmostEqual(0.87890625, self._z[1], 4)
        self.assertAlmostEqual(0.00390625, self._z[7], 4)

        self._A = self._coder.a
        self._blocklength = self._coder.blocklength

        self.assertTrue(self._A[3])
        self.assertTrue(self._A[5])
        self.assertTrue(self._A[6])

        self.assertFalse(self._A[0])
        self.assertFalse(self._A[1])

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
            encoded_input = self._coder.encode_input(message)

            for erasure in erasures:
                received_output = self._coder.erase_bits(encoded_input, erasure)

                decoded_output_1 = self._coder.decode_output(received_output, efficient=False)
                decoded_output_2 = self._coder.decode_output(received_output, efficient=True)


                self.assertCountEqual(message, decoded_output_1)
                self.assertCountEqual(message, decoded_output_2)


if __name__ == '__main__':
    unittest.main()

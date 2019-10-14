"""
Testing the capabilities of  the lightweight Simon
and Speck families of block ciphers
"""

# Testing Speck ciphers:
from speck import SpeckCipher

from des import DesKey

my_speck = SpeckCipher(0x123456789ABCDEF00FEDCBA987654321)

my_plaintext = "0xCCCCAAAA55553333"

speck_ciphertext = my_speck.encrypt(my_plaintext)


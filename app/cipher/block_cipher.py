"""
Class to use different block ciphers

"""
import numpy as np

from app.cipher.des_cipher import DES
from app.cipher.exceptions.exceptions import InvalidCipherMethod, InvalidKeyLength, InvalidCipherBlockLength, NoKeySet
from app.cipher.simon_cipher import Simon
from app.cipher.speck_cipher import Speck


class BlockCipher:
    DES = "DES"
    SIMON = "SIMON"
    SPECK = "SPECK"

    def __init__(self, cipher=DES, key_size=64, blocklength=64):
        if cipher == BlockCipher.DES:
            self._cipher = DES(key_size, blocklength)

        elif cipher == BlockCipher.SIMON:
            self._cipher = Simon(key_size, blocklength)

        elif cipher == BlockCipher.SPECK:
            self._cipher = Speck(key_size, blocklength)

        else:
            raise InvalidCipherMethod("{} is a invalid Cipher".format(cipher))

        self._key_size = key_size
        self._blocklength = blocklength
        self._key = None


    def set_secret_key(self, key):
        if len(key) != self._key_size:
            raise InvalidKeyLength("Key size ({}) should match the configurations ({})!".format(len(key), self._key_size))

        self._key = key
        self._cipher.set_key(key)


    def encrypt_message(self, message):
        if self._key is None:
            raise NoKeySet("No key has been set")


        if len(message) != self._blocklength:
            raise InvalidCipherBlockLength("Blocklength should be {}".format(self._blocklength))

        return self._cipher.encrypt(message)


    def decrypt_message(self, message):
        return self._cipher.decrypt(message)





if __name__ == '__main__':
    # DES
    example = BlockCipher(BlockCipher.DES, 64, 64)
    des_key = np.random.uniform(size=64)
    des_key = list(map(lambda x: int(round(x)), des_key))

    example.set_secret_key(des_key)

    message = np.random.uniform(size=64)
    message = list(map(lambda x: int(round(x)), message))

    encrypted_message = example.encrypt_message(message)
    decrypted_message = example.decrypt_message(encrypted_message)

    assert message == decrypted_message

    # Simon cipher
    example = BlockCipher(BlockCipher.SIMON, 96, 64)
    simon_key = np.random.uniform(size=96)
    simon_key = list(map(lambda x: int(round(x)), simon_key))

    example.set_secret_key(simon_key)

    encrypted_message = example.encrypt_message(message)
    decrypted_message = example.decrypt_message(encrypted_message)

    assert message == decrypted_message

    # Speck cipher
    example = BlockCipher(BlockCipher.SPECK, 96, 64)
    simon_key = np.random.uniform(size=96)
    simon_key = list(map(lambda x: int(round(x)), simon_key))

    example.set_secret_key(simon_key)

    encrypted_message = example.encrypt_message(message)
    decrypted_message = example.decrypt_message(encrypted_message)

    assert message == decrypted_message










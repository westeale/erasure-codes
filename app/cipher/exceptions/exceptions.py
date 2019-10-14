"""
Custom exceptions for ciphers
"""

class InvalidKeyLength(Exception):
    def __init__(self, code):
        self.code = code


class InvalidCipherBlockLength(Exception):
    def __init__(self, code):
        self.code = code


class InvalidCipherMethod(Exception):
    def __init__(self, code):
        self.code = code


class NoKeySet(Exception):
    def __init__(self, code):
        self.code = code


class WrongConfiguration(Exception):
    def __init__(self, code):
        self.code = code
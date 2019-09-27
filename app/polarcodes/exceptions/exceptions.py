"""
Custom exceptions for polar encoding
"""

class CouldNotDecodeError(Exception):
    """Raised when decoder is not able to decode the message"""
    pass

class InvalidCharacterInMessage(Exception):
    """Raised when an invalid character occures in the decoder"""
    pass

class UnexpectedLikeliHood(Exception):
    "Unexpected likelihood ratio"
    pass
class SsapiException(Exception):
    """The base ssapi exception"""


class MoreThenOneItemError(SsapiException):
    """A sequence contained more than one item where only one was expected"""


class EmptySequenceError(SsapiException):
    """A sequence was unexpectedly empty"""


class InvalidQueryError(SsapiException):
    """An invalid query was received"""

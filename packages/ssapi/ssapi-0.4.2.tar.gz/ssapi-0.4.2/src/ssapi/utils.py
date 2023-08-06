from functools import wraps
from typing import Callable, Any, Iterator, TypeVar

from ssapi.exceptions import MoreThenOneItemError, EmptySequenceError

F = TypeVar("F", bound=Callable[..., Iterator])


def only_one(func: F) -> Callable:
    """Allow only one item from an iterable sequence

    Return the first item of the sequence, then attempt to retrieve a
    second one. If there is indeed a second item, raise an exception.

    Warning: taking the second item will trigger any related side effects.
    """

    @wraps(func)
    def _inner(*args, **kwargs) -> Any:
        seq = func(*args, **kwargs)
        try:
            return next(seq)
        except StopIteration:
            raise EmptySequenceError("No items were found in the sequence")
        finally:
            try:
                next(seq)
            except StopIteration:
                pass
            else:
                raise MoreThenOneItemError(
                    "More than one item was found in the sequence"
                )

    return _inner

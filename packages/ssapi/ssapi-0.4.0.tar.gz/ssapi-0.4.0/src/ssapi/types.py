import abc
import typing as T
from typing import Iterable, Tuple, Protocol, Any, Union

QueryType = T.TypeVar("QueryType", bound=dict[str, T.Union[str, int]])


class Tabular(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def columns(self) -> dict[str, T.Any]:
        ...

    @abc.abstractmethod
    def as_map(self) -> Iterable[Tuple[str, Union[bool, int, float, str]]]:
        ...

    @abc.abstractmethod
    def as_tuple(self) -> tuple:
        ...

    class Constraints:
        ...


class SingletonProtocol(Protocol):
    """"""

    _singleton: Any

    def __call__(self, *args, **kwargs):
        pass


def provides_singleton(func: Any) -> SingletonProtocol:
    return func


class Undefined:
    """Singleton representing an undefined value"""

    def __bool__(self):
        return False

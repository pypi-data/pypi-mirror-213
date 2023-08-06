import os
import sqlite3
from typing import Protocol

from ssapi.types import Tabular, QueryType
from ssapi.exceptions import InvalidQueryError


class DataclassFieldsProtocol(Protocol):
    __dataclass_fields__: dict


class DataclassColumnsMixin:
    """A mixin for classes that use the dataclass fields dunder property"""

    @property
    def columns(self: DataclassFieldsProtocol):
        return self.__dataclass_fields__


class Database:
    """A database"""

    conn: sqlite3.Connection
    engine = "sqlite"

    def __init__(self, name: str) -> None:
        self._name = name
        self.open()

    def open(self):
        self.conn = sqlite3.connect(self._name)
        self._tables_init()

    def _tables_init(self) -> None:
        """Initialize the tables"""

    @property
    def name(self) -> str:
        return self._name

    def drop(self) -> None:
        self.conn.close()
        if self.name != ":memory:":
            os.unlink(self.name)


class Table(DataclassColumnsMixin, Tabular):
    """Base class for a Table"""

    def __post_init__(self):
        for key, val in self.as_map():
            cons = getattr(self.Constraints, key, None)
            if cons:
                comparator, value, operator = cons
                if not operator(comparator(val), value):
                    raise ValueError(f"{key}:{val}")

    def create(self) -> None:
        """Create the table"""
        raise NotImplementedError()

    def as_tuple(self):
        return tuple(val for (key, val) in self)

    def as_map(self):
        try:
            for key in self.columns:
                yield (key, getattr(self, key))
        except AttributeError:
            raise AttributeError(f"Not a dataclass: {type(self).__name__}")

    @classmethod
    def validate_query(cls, query: QueryType) -> dict:
        """Validate the given query according to this table's type information"""
        validated_data = {}
        fields = cls.columns
        for key, value in query.items():
            try:
                field = fields[key]
            except KeyError:
                raise InvalidQueryError(
                    f"Invalid predicate for " f"{cls.__name__}: {key}={value}"
                )
            else:
                validated_data[key] = field.type(value)

        return validated_data

    def __iter__(self):
        return iter(self.as_map())

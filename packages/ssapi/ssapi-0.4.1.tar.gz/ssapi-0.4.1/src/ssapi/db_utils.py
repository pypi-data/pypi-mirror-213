from typing import NamedTuple, Union

from ssapi.types import Undefined


class WhereClause(NamedTuple):
    clause: str
    values: tuple

    def __bool__(self) -> bool:
        return False if self.clause == "" or self.values == () else True

    def AND(self, other_where: "WhereClause") -> "WhereClause":
        if not self:
            return other_where
        elif not other_where:
            return self
        else:
            return WhereClause(
                clause=(
                    f"WHERE ({self._bare_clause}) "
                    f"AND ({other_where._bare_clause})"
                ),
                values=self.values + other_where.values,
            )

    @property
    def _bare_clause(self) -> str:
        return self.clause.removeprefix("WHERE").lstrip()

    @classmethod
    def create(
        cls, **kwargs: Union[Undefined, dict[str, str]]
    ) -> "WhereClause":
        """Create a new WHERE clause using the given key and value"""
        if len(kwargs) != 1:
            raise ValueError("Only one key/value pair supported")

        key, value = list(kwargs.items())[0]

        if isinstance(value, Undefined):
            return WhereClause("", ())
        else:
            return WhereClause(f"WHERE {key}=?", (value,))


def create_date_where_clause(start: str = "", end: str = "") -> WhereClause:
    """Create the WHERE clause from start and end dates"""
    where_keys = []
    where_values = []
    if start:
        where_keys.append("date>=?")
        where_values.append(start)
    if end:
        where_keys.append("date<=?")
        where_values.append(end)
    if where_keys:
        where_keys[0] = "WHERE " + where_keys[0]

    return WhereClause(" AND ".join(where_keys), tuple(where_values))


def create_shop_where_clause(shop: str = "") -> WhereClause:
    """Create the WHERE clause for a given shop"""
    if shop:
        return WhereClause("WHERE shop=?", (shop,))
    else:
        return WhereClause("", ())

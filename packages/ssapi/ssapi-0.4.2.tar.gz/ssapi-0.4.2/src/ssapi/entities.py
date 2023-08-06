import operator
from collections import namedtuple
from dataclasses import dataclass
from typing import Optional

from ssapi.relational import Table

constraint = namedtuple("constraint", ("comparator", "value", "operator"))


@dataclass
class Transaction(Table):
    """A generic transaction"""

    id: Optional[int]
    product: str
    shop: str
    quantity: int
    date: Optional[str] = None

    class Constraints:
        product = constraint(len, 255, operator.lt)
        shop = constraint(len, 255, operator.lt)


@dataclass
class Sale(Transaction):
    """A sale of a certain amount of product"""

    is_discounted: bool = False


class Return(Transaction):
    """A return of a certain amount of product"""

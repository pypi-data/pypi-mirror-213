import typing as T

from ssapi.types import Undefined
from ssapi.entities import Sale, Return
from ssapi.relational import Database
from ssapi.db_utils import (
    create_date_where_clause,
    create_shop_where_clause,
    WhereClause,
)


class ShopDatabase(Database):
    """A database that stores data about shops"""

    def _tables_init(self) -> None:
        """Initialize the tables"""
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS shops" "(" "name VARCHAR(255)" ")"
        )
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS sales"
            "("
            "id INTEGER PRIMARY KEY,"
            "product VARCHAR(255), "
            "shop VARCHAR(255), "
            "quantity INT, "
            "date DATE DEFAULT CURRENT_TIMESTAMP, "
            "is_discounted BOOLEAN"
            ")"
        )
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS returns"
            "("
            "id INTEGER PRIMARY KEY,"
            "product VARCHAR(255), "
            "shop VARCHAR(255), "
            "quantity INT, "
            "date DATE DEFAULT CURRENT_TIMESTAMP"
            ")"
        )

    def add_sales(self, *sales: Sale) -> int:
        """Record sale transactions and return the number of rows created"""
        cur = self.conn.executemany(
            "INSERT INTO sales VALUES(?, ?, ?, ?, ?, ?)",
            (sale.as_tuple() for sale in sales),
        )
        self.conn.commit()
        return cur.rowcount

    def add_returns(self, *returns: Return) -> int:
        """Record sale transactions and return the number of rows created"""
        cur = self.conn.executemany(
            "INSERT INTO returns VALUES(?, ?, ?, ?, ?)",
            (ret.as_tuple() for ret in returns),
        )
        self.conn.commit()
        return cur.rowcount

    def get_shops(self) -> T.Generator[str, None, None]:
        """Get all the shops"""
        cur = self.conn.execute("SELECT DISTINCT shop FROM sales")
        for shop, *_ in cur.fetchall():
            yield shop

    def get_sales(
        self,
        date_start="",
        date_end="",
        is_discounted=Undefined(),
        shop="",
    ) -> T.Generator[Sale, None, None]:
        """Get the sales according to the given criteria"""
        where = create_date_where_clause(date_start, date_end)
        where = where.AND(create_shop_where_clause(shop))
        where = where.AND(WhereClause.create(is_discounted=is_discounted))
        cur = self.conn.execute(
            f"SELECT * FROM sales {where.clause}", where.values
        )
        for result in cur.fetchall():
            yield Sale(*result)

    def get_sale(self, id: int) -> T.Optional[Sale]:
        """Get a specific sale by its id"""
        cur = self.conn.execute("SELECT * FROM sales WHERE id=?", (id,))
        if result := cur.fetchone():
            return Sale(*result)
        else:
            return None

    def get_returns(
        self, date_start=None, date_end=None
    ) -> T.Generator[Return, None, None]:
        """Get the sales according to the given criteria"""
        cur = self.conn.execute("SELECT * FROM returns")
        for result in cur.fetchall():
            yield Return(*result)

    def get_products(self) -> T.Generator[tuple, None, None]:
        cur = self.conn.execute("SELECT DISTINCT product FROM sales")
        for item in cur.fetchall():
            yield item[0]

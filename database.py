import sqlite3

from database_models import Item

DB_NAME = "items.db"


def set_db_name(db_name):
    global DB_NAME
    DB_NAME = db_name


def get_connection():

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL CHECK (length(name) > 0),
        category TEXT NOT NULL,
        price INTEGER NOT NULL CHECK (price >= 0),
        quantity INTEGER NOT NULL CHECK (quantity >= 0)
    )
    """)

    conn.commit()
    conn.close()


def get_list_items(
    conn, category: str | None = None, sort_by: str | None = None, order: str = "asc"
) -> list[Item]:
    query = """
    SELECT *
    FROM items
    """

    parameters = []

    if category is not None:
        query += " WHERE category = ?"
        parameters.append(category)

    sort_options = {
        ("price", "asc"): " ORDER BY price ASC",
        ("price", "desc"): " ORDER BY price DESC",
    }

    if sort_by is not None:
        try:
            query += sort_options[(sort_by, order)]
        except KeyError:
            raise ValueError("Invalid sorting option")

    cursor = conn.execute(query, parameters)

    rows = cursor.fetchall()

    return [
        Item(
            id=row["id"],
            name=row["name"],
            category=row["category"],
            price=row["price"],
            quantity=row["quantity"],
        )
        for row in rows
    ]


def get_item(conn, id: int) -> Item | None:
    cursor = conn.execute(
        """
        SELECT *
        FROM items
        WHERE id = ?
    """,
        (id,),
    )

    row = cursor.fetchone()

    if row is None:
        return None

    item = Item(
        id=row["id"],
        name=row["name"],
        category=row["category"],
        price=row["price"],
        quantity=row["quantity"],
    )

    return item


def create_item(conn, item: Item) -> int:
    cursor = conn.execute(
        """
        INSERT INTO items
        (name, category, price, quantity)
        VALUES (?, ?, ?, ?)
    """,
        (
            item.name,
            item.category,
            item.price,
            item.quantity,
        ),
    )

    return cursor.lastrowid


def delete_item(conn, id: int) -> bool:
    cursor = conn.execute(
        """
        DELETE FROM items
        WHERE id = ?
        """,
        (id,),
    )

    return cursor.rowcount > 0


def update_item(conn, item: Item) -> bool:
    cursor = conn.execute(
        """
        UPDATE items
        SET name = ?,
            category = ?,
            price = ?,
            quantity = ?
        where id = ?
    """,
        (
            item.name,
            item.category,
            item.price,
            item.quantity,
            item.id,
        ),
    )

    return cursor.rowcount > 0

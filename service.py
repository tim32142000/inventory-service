from database import (
    create_item,
    get_items,
    get_item,
    update_item,
    delete_item,
    get_connection,
)
from database_models import Item
from exceptions import BusinessRuleError, ItemNotFoundError

# Business Rule in this file


def validate_item(item: Item):
    if item.quantity > 10000:
        raise BusinessRuleError("Quantity can not greater than 10000")


def get_items_service() -> list[Item]:
    print("service: entered")
    with get_connection() as conn:

        items = get_items(conn)

        return items


def get_item_service(id: int) -> Item:
    with get_connection() as conn:
        result = get_item(conn, id)
        if result is None:
            raise ItemNotFoundError(id)
        return result


def update_item_service(item: Item) -> Item:
    conn = get_connection()

    try:
        before_update = get_item(conn, item.id)

        if before_update is None:
            raise ItemNotFoundError(item.id)

        validate_item(item)

        update_item(conn, item)

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

    return item


def create_item_service(item: Item) -> Item:
    conn = get_connection()

    try:
        validate_item(item)

        new_id = create_item(conn, item)
        item.id = new_id

        conn.commit()
    except Exception:

        conn.rollback()
        raise

    finally:

        conn.close()

    return item


def create_two_items_service(
    item1: Item,
    item2: Item,
) -> list[Item]:
    conn = get_connection()

    try:
        id1 = create_item(conn, item1)
        item1.id = id1

        id2 = create_item(conn, item2)
        item2.id = id2

        conn.commit()
    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

    return [item1, item2]


def delete_item_service(id: int) -> None:
    conn = get_connection()

    try:
        before_delete = get_item(conn, id)

        if before_delete is None:
            raise ItemNotFoundError(id)

        delete_item(conn, id)

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

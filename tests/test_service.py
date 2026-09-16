import pytest

import database
import service

from database_models import Item


@pytest.fixture
def test_db(tmp_path):
    db_path = tmp_path / "test.db"

    database.set_db_name(str(db_path))
    database.init_db()

    return db_path


def test_create_two_items_service_rollback(test_db, monkeypatch):
    item1 = Item(name="item 1", category="test", price=10, quantity=20)
    item2 = Item(name="item 2", category="test", price=20, quantity=25)

    call_count = 0

    def fake_create_item(conn, item):
        nonlocal call_count
        call_count += 1

        if call_count == 1:
            return database.create_item(conn, item)

        raise RuntimeError("forced failure")

    monkeypatch.setattr(
        service,
        "create_item",
        fake_create_item,
    )

    with pytest.raises(RuntimeError, match="forced failure"):
        service.create_two_items_service(item1, item2)

    assert call_count == 2

    with database.get_connection() as conn:
        assert database.get_items(conn) == []

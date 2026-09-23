import pytest
import inventory_service.items.repository as repository


@pytest.fixture
def test_db(tmp_path):
    db_path = tmp_path / "test.db"

    repository.set_db_name(str(db_path))
    repository.init_db()

    return db_path
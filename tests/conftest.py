import pytest
import database


@pytest.fixture
def test_db(tmp_path):
    db_path = tmp_path / "test.db"

    database.set_db_name(str(db_path))
    database.init_db()

    return db_path
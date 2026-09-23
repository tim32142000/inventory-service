import pytest
from sqlalchemy.orm import sessionmaker

import inventory_service.database.session as database_session
import inventory_service.items.repository as repository


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"

    repository.set_db_name(str(db_path))
    repository.init_db()

    test_database_url = f"sqlite:///{db_path.as_posix()}"

    test_engine = database_session.create_database_engine(
        test_database_url,
    )

    test_session_factory = sessionmaker(bind=test_engine)

    monkeypatch.setattr(
        database_session,
        "SessionFactory",
        test_session_factory,
    )

    yield db_path

    test_engine.dispose()

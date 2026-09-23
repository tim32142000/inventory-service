from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from inventory_service.database.config import get_database_url


def create_database_engine(
    database_url: str | None = None,
) -> Engine:
    if database_url is None:
        database_url = get_database_url()

    return create_engine(database_url)


engine = create_database_engine()

SessionFactory: sessionmaker[Session] = sessionmaker(bind=engine)

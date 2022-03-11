import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def database_engine():
    from depart.db.session import engine
    from depart.db import tables

    yield engine


@pytest.fixture(scope="session")
def clean_database(database_engine):
    from depart.db.base import Base

    truncate_query = f"TRUNCATE " + ", ".join(set(Base.metadata.tables))

    def clean():
        with database_engine.begin() as connection:
            connection.execute(truncate_query)

    clean()
    return clean


@pytest.fixture
def db_session(database_engine, clean_database, request):
    from depart.db.session import Session

    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
        clean_database()


@pytest.fixture(scope="session")
def api(request):
    from depart.run_server import prepare_application
    from depart.db.session import db_session as postgres_session

    def mock_database_session():
        yield request.getfixturevalue("db_session")

    app = prepare_application(debug=True)
    app.dependency_overrides[postgres_session] = mock_database_session
    yield TestClient(app)
    app.dependency_overrides.clear()

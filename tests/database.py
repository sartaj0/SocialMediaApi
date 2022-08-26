import pytest

from fastapi.testclient import TestClient
from app.database import get_db
from app.main import app 

from app.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db, Base

SQLALCHEMY_DATABASE_URL =f"sqlite:///fastapi_test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
event.listen(engine, 'connect', lambda c, _: c.execute('pragma foreign_keys=on')) # for sqlite3.x
# engine = create_engine(SQLALCHEMY_DATABASE_URL)


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# Used to drop the table
# Base.metadata.drop_all(engine) 

# Base.metadata.create_all(bind=engine)

# scope module help acces data allow execute fixture only once throught the whole code even if called it more than once


@pytest.fixture(scope="module")
def session():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


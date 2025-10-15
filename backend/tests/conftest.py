import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base

TEST_DATABASE_URL = 'sqlite:///:memory:'

@pytest.fixture(scope='function')
def db_session():
    engine = create_engine(TEST_DATABASE_URL, connect_args={'check_same_thread': False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(autouse=True)
def override_get_db(monkeypatch, db_session):
    def test_get_db():
        yield db_session
    monkeypatch.setattr('backend.main.get_db', test_get_db)
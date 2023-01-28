from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.config import settings
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

SQLALCHEMY_TEST_DATABASE_URL = f'postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOSTNAME}:{settings.DB_PORT}/{settings.DB_NAME}_test'
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def dbSession():
    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(dbSession):
    def override_get_db():
        try:
            yield dbSession
        finally:
            dbSession.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def test_user(client: client):
    user_data = {"email": "hello@gmail.com",
                "password": "heym8"}
    response = client.post("/users",
        json = user_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    new_user = response.json()
    new_user['password'] = user_data["password"]
    return new_user
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app import oauth2, models
from app.config import settings
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import timedelta
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
def test_user(client):
    user_data = {"email": "hello@gmail.com",
                "password": "heym8"}
    response = client.post("/users",
        json = user_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    new_user = response.json()
    new_user['password'] = user_data["password"]
    return new_user

@pytest.fixture()
def unauthorised_test_user(client):
    user_data = {"email": "test@gmail.com",
                "password": "m123"}
    response = client.post("/users",
        json = user_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    new_user = response.json()
    new_user['password'] = user_data["password"]
    return new_user

@pytest.fixture()
def access_token(test_user):
    return oauth2.createAccessToken(
        data = {"user_id": test_user['id']},
        expireDelta = timedelta(minutes = oauth2.ACCESS_TOKEN_EXPIRE_MINUTES))


@pytest.fixture()
def authorise_client(client, access_token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {access_token}"}
    return client


@pytest.fixture()
def generate_posts(test_user, dbSession, unauthorised_test_user):
    test_data = [{"title": "Post1 Title",
                  "content": "Post1 Content",
                  "user_id": test_user['id']},
                  
                  {"title": "Post2 Title",
                  "content": "Post2 Content",
                  "user_id": test_user['id']},
                  
                  {"title": "Post3 Title",
                  "content": "Post3 Content",
                  "user_id": test_user['id']},
                  
                  {"title": "Post4 Title",
                  "content": "Post4 Content",
                  "user_id": unauthorised_test_user['id']}]
    
    postModel = lambda x: models.Post(**x)
    dbSession.add_all(list(map(postModel, test_data)))
    dbSession.commit()
    posts = dbSession.query(models.Post).all()
    return posts


@pytest.fixture()
def generate_votes(test_user, dbSession):
    test_votes = [{"post_id": 1,
                   "user_id": test_user['id']},
                   
                   {"post_id": 2,
                   "user_id": test_user['id']}]

    voteModel = lambda x: models.Vote(**x)
    dbSession.add_all(list(map(voteModel, test_votes)))
    dbSession.commit()
    votes = dbSession.query(models.Vote).all()
    return votes
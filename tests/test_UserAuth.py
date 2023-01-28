from app import schemas
from app.config import settings
from jose import jwt
from fastapi import status
import pytest

#@pytest.mark.skip()
def test_create_user(client):
    response = client.post("/users/",
        json = {"email": "hello@gmail.com",
                "password": "heym8"})
    
    new_user = schemas.UserResponse(**response.json())
    assert response.status_code == status.HTTP_201_CREATED
    assert new_user.email == "hello@gmail.com"

#@pytest.mark.skip()
def test_login_user(client, test_user: dict):
    response = client.post("/login",
        data = {"username": test_user['email'],
                "password": test_user['password']})
    
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token, settings.SECRET_KEY, algorithms = [settings.ALGORITHM])
    id: str = payload.get("user_id")

    assert response.status_code == status.HTTP_200_OK
    assert id == test_user['id']
    assert login_response.token_type == 'bearer'
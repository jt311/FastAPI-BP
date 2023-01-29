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

#@pytest.mark.skip()
@pytest.mark.parametrize('email, password, status_code, detail', [
    ('hello@gmail.com', 'hey', status.HTTP_401_UNAUTHORIZED, 'Invalid Email or Password'),
    ('heo@gmail.com', 'heym8', status.HTTP_401_UNAUTHORIZED, 'Invalid Email or Password'),
    ('helo@gmail.com', 'hey', status.HTTP_401_UNAUTHORIZED, 'Invalid Email or Password'),
    ('hello@gmail.com', None, status.HTTP_422_UNPROCESSABLE_ENTITY, None),
    (None, 'heym8', status.HTTP_422_UNPROCESSABLE_ENTITY, None)
])                        
def test_failed_login(client, test_user, email, password, status_code, detail):
    response = client.post("/login",
        data = {"username": email,
                "password": password})
    
    assert type(test_user) == dict
    assert response.status_code == status_code
    if detail: assert response.json()['detail'] == detail
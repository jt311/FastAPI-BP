from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
import pytest

client = TestClient(app)

@pytest.mark.skip()
def test_root():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello World pushing out to ubuntu"}
import pytest
from utils.api_auth import post_auth, get_authenticated

@pytest.mark.smoke
def test_valid_login_returns_token():
    payload = {"username": "emilys", "password": "emilyspass"}
    response = post_auth("/auth/login", payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "accessToken" in data
    assert len(data["accessToken"]) > 0

@pytest.mark.regression
def test_invalid_login_returns_401():
    payload = {"username": "fakeuser", "password": "wrongpass"}
    response = post_auth("/auth/login", payload)
    
    assert response.status_code == 400
    data = response.json()
    assert "message" in data

@pytest.mark.regression  
def test_authenticated_endpoint_returns_user_data(auth_token):
    response = get_authenticated("/auth/me", auth_token)
    
    assert response.status_code == 200
    user = response.json()
    assert "id" in user
    assert "email" in user
    assert user["username"] == "emilys"

@pytest.mark.regression
def test_protected_endpoint_without_token_returns_401():
    from utils.api_client import get
    response = get("/auth/me")
    
    # Without token, should be rejected
    assert response.status_code == 401
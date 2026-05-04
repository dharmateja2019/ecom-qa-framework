import pytest
from utils.api_auth import post_auth, get_authenticated
from utils.api_auth import add_user, search_user
from utils.test_data import create_user_payload
from utils.api_client import get


@pytest.mark.smoke
def test_create_user():
    payload = create_user_payload()

    response = add_user(payload)
    assert response.status_code == 201
    data = response.json()
    assert data["firstName"] == payload["firstName"]
    assert "id" in data
    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]


@pytest.mark.regression
def test_search_user():
    response = search_user("emilys")

    assert response.status_code == 200
    data = response.json()
    assert "users" in data
    assert len(data["users"]) > 0
    user = data["users"][0]
    assert user["username"] == "emilys"
    assert user["email"] == "emily.johnson@x.dummyjson.com"


@pytest.mark.smoke
def test_valid_login_returns_token():
    payload = {"username": "emilys", "password": "emilyspass"}
    response = post_auth("auth/login", payload)

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
    response = get("/auth/me")
    # Without token, should be rejected
    assert response.status_code == 401

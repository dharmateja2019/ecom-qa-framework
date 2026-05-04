import requests
from config.settings import BASE_URL, TIMEOUT_SECONDS
from utils.logger import get_logger

logger = get_logger()


def post_auth(endpoint, payload=None):
    url = f"{BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"

    logger.info(f"POST AUTH {url}")

    response = requests.post(url, json=payload, timeout=TIMEOUT_SECONDS)

    logger.info(f"AUTH Response {response.status_code}")

    return response


def get_authenticated(endpoint, token, payload=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, json=payload, timeout=TIMEOUT_SECONDS)
    return response


def add_user(user_payload):
    url = f"{BASE_URL}/users/add"
    response = requests.post(url, json=user_payload, timeout=TIMEOUT_SECONDS)
    logger.info(
        f"Adding user {user_payload['username']} with status {response.status_code}"
    )
    return response


def search_user(username):
    url = f"{BASE_URL}/users/search?q={username}"
    response = requests.get(url, timeout=TIMEOUT_SECONDS)
    logger.info(f"Searching user {username} with status {response.status_code}")
    return response

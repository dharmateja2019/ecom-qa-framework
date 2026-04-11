import requests
from config.settings import BASE_URL, TIMEOUT_SECONDS


def post_auth(endpoint, payload=None):
  url = f"{BASE_URL}/{endpoint}"
  response = requests.post(url, json=payload, timeout=TIMEOUT_SECONDS)
  return response

def get_authenticated(endpoint, token, payload=None):
  url = f"{BASE_URL}/{endpoint}"
  headers = {"Authorization": f"Bearer {token}"}
  response = requests.get(url, headers=headers, json=payload, timeout=TIMEOUT_SECONDS)
  return response

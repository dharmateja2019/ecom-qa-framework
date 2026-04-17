import requests
from config.settings import BASE_URL, TIMEOUT_SECONDS
from utils.logger import get_logger

logger = get_logger()


def post_auth(endpoint, payload=None):
  url = f"{BASE_URL}/{endpoint}"
  response = requests.post(url, json=payload, timeout=TIMEOUT_SECONDS)
  logger.info(f"POST AUTH {url}")
  logger.info("Fetching authenticated endpoint")
  return response

def get_authenticated(endpoint, token, payload=None):
  url = f"{BASE_URL}/{endpoint}"
  headers = {"Authorization": f"Bearer {token}"}
  response = requests.get(url, headers=headers, json=payload, timeout=TIMEOUT_SECONDS)
  return response

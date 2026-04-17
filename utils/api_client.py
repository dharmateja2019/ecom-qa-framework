import requests
from config.settings import BASE_URL, TIMEOUT_SECONDS, endpoint
from utils.logger import get_logger

logger = get_logger()

def get(endpoint=endpoint, params=None):
    url = f"{BASE_URL}/{endpoint}"
    logger.info(f"GET {url} params={params}")
    response = requests.get(url, params=params, timeout=TIMEOUT_SECONDS)
    logger.info(f"Response {response.status_code}")
    return response

def post(endpoint=endpoint, payload=None):
  url = f"{BASE_URL}/{endpoint}"
  logger.info(f"POST {url} params={payload}")
  response = requests.post(url, json=payload, timeout=TIMEOUT_SECONDS)
  logger.info(f"Response {response.status_code}")
  return response

def put(endpoint, payload=None):
  url = f"{BASE_URL}/{endpoint}"
  logger.info(f"PUT {url} params={payload}")
  response = requests.put(url, json=payload, timeout=TIMEOUT_SECONDS)
  logger.info(f"Response {response.status_code}")
  return response

def delete(endpoint):
  url = f"{BASE_URL}/{endpoint}"
  logger.info(f"DELETE {url}")
  response = requests.delete(url, timeout=TIMEOUT_SECONDS)
  logger.info(f"Response {response.status_code}")
  return response
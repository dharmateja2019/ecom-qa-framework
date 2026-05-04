import requests
from config.settings import BASE_URL, TIMEOUT_SECONDS, ENDPOINT
from utils.logger import get_logger

logger = get_logger()


def get(endpoint=ENDPOINT, params=None):
    url = f"{BASE_URL}/{endpoint}"
    logger.info("GET %s params=%s", url, params)
    response = requests.get(url, params=params, timeout=TIMEOUT_SECONDS)
    logger.info("Response %s", response.status_code)
    return response


def post(endpoint=ENDPOINT, payload=None):
    url = f"{BASE_URL}/{endpoint}"
    logger.info("POST %s params=%s", url, payload)
    response = requests.post(url, json=payload, timeout=TIMEOUT_SECONDS)
    logger.info("Response %s", response.status_code)
    return response


def put(endpoint, payload=None):
    url = f"{BASE_URL}/{endpoint}"
    logger.info("PUT %s params=%s", url, payload)
    response = requests.put(url, json=payload, timeout=TIMEOUT_SECONDS)
    logger.info("Response %s", response.status_code)
    return response


def delete(endpoint):
    url = f"{BASE_URL}/{endpoint}"
    logger.info("DELETE %s", url)
    response = requests.delete(url, timeout=TIMEOUT_SECONDS)
    logger.info("Response %s", response.status_code)
    return response

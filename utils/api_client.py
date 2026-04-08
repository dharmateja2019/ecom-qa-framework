import requests
from config.settings import BASE_URL, TIMEOUT_SECONDS


def get(endpoint, params=None):
  url = f"{BASE_URL}/{endpoint}"
  response = requests.get(url, params=params, timeout=TIMEOUT_SECONDS)
  return response

def post(endpoint, payload=None):
  url = f"{BASE_URL}/{endpoint}"
  response = requests.post(url, json=payload, timeout=TIMEOUT_SECONDS)
  return response

def put(endpoint, payload=None):
  url = f"{BASE_URL}/{endpoint}"
  response = requests.put(url, json=payload, timeout=TIMEOUT_SECONDS)
  return response

def delete(endpoint):
  url = f"{BASE_URL}/{endpoint}"
  response = requests.delete(url, timeout=TIMEOUT_SECONDS)
  return response
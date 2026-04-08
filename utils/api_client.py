import requests

BASE_URL = "https://fakestoreapi.com"

def get(endpoint, params=None):
  url = f"{BASE_URL}/{endpoint}"
  response = requests.get(url, params=params)
  return response

def post(endpoint, payload=None):
  url = f"{BASE_URL}/{endpoint}"
  response = requests.post(url, json=payload)
  return response

def put(endpoint, payload=None):
  url = f"{BASE_URL}/{endpoint}"
  response = requests.put(url, json=payload)
  return response

def delete(endpoint):
  url = f"{BASE_URL}/{endpoint}"
  response = requests.delete(url)
  return response
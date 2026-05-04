import os

BASE_URL = os.getenv("BASE_URL", "https://dummyjson.com")
ENDPOINT = "/products"
TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", "5"))
SLA_SECONDS = int(os.getenv("SLA_SECONDS", "2"))

import os

BASE_URL = os.getenv("BASE_URL", "https://dummyjson.com")
endpoint = "/products"
TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", "5"))
SLA_SECONDS = int(os.getenv("SLA_SECONDS", "1"))
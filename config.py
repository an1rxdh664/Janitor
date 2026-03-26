import os
from dotenv import load_dotenv

load_dotenv()
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
GITHUB_AUTH_TOKEN = os.getenv("GITHUB_AUTH_TOKEN")
GITHUB_FINE_GRAINED_TOKEN = os.getenv("GITHUB_FINE_GRAINED_TOKEN")
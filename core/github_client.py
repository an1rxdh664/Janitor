import requests
from config import WEBHOOK_SECRET, GITHUB_AUTH_TOKEN

headers = {
    "Accept": "application/vnd.github.v3.diff",
    "Authorization": f"Bearer {GITHUB_AUTH_TOKEN}"
}

async def fetch_diff_data(diff_url):
    response = requests.get(diff_url)

    if response.status_code == 200:
        return response.text
    else:
        return {"error": "could not fetch diff data"}
import requests
from config import GITHUB_FINE_GRAINED_TOKEN

headers = {
    "Accept": "application/vnd.github.v3.diff",
    "Authorization": f"Bearer {GITHUB_FINE_GRAINED_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28"
}

def createURL(body):
    owner = body.get('repository').get('owner').get('login')
    repo = body.get('repository').get('name')
    pull_number = body.get('number')

    return f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}"

def fetch_diff_data(diff_url):    
    response = requests.get(diff_url, headers=headers)
    
    if response.status_code == 200:
        return response.text
    else:
        return {"error": "could not fetch diff data"}
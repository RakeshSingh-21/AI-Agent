import requests
from app.core.config import GITHUB_TOKEN

def get_pr_diff(diff_url):
    headers = {"Accept": "application/vnd.github.v3.diff"}
    return requests.get(diff_url, headers=headers).text


def post_comment(pr_url, comment):
    url = pr_url + "/comments"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }

    data = {"body": comment}

    requests.post(url, headers=headers, json=data)
import requests
import csv
from datetime import datetime

# Insert your GitHub token here
github_token = "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"
headers = {"Authorization": f"token {github_token}"}


def get_repo_info(repo_url):
    repo_name = repo_url.replace("https://github.com/", "")
    api_url = f"https://api.github.com/repos/{repo_name}"
    response = requests.get(api_url, headers=headers)
    data = response.json()
    stars = data["stargazers_count"]
    created_at = datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%SZ")
    updated_at = datetime.strptime(data["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
    now = datetime.now()

    created_days_ago = (now - created_at).days
    updated_days_ago = (now - updated_at).days

    commits_url = f"https://api.github.com/repos/{repo_name}/commits"
    response = requests.get(commits_url, headers=headers)
    commits = len(response.json())

    return stars, commits, created_days_ago, updated_days_ago


with open("matched_plugins.csv", "r") as csvfile, open(
    "new_plugins.csv", "w", newline=""
) as newfile:
    reader = csv.reader(csvfile)
    writer = csv.writer(newfile)

    for row in reader:
        stars, commits, created_days_ago, updated_days_ago = get_repo_info(row[5])
        new_row = row + [stars, commits, created_days_ago, updated_days_ago]
        writer.writerow(new_row)

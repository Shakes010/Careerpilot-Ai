import re
import requests
from typing import Dict, Any, List

GITHUB_API_BASE = "https://api.github.com"
GITHUB_USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,38}$")

def extract_github_username(raw_input: str) -> str:
    """
    Extracts purely the GitHub username from inputs such as:
    - https://github.com/SidharthKa
    - http://github.com/SidharthKa
    - https://www.github.com/SidharthKa
    - github.com/SidharthKa
    - SidharthKa
    - @SidharthKa
    - https://github.com/SidharthKa/
    """
    if not raw_input:
        return ""
    s = str(raw_input).strip()
    
    # Remove query parameters and anchors
    s = s.split("?")[0].split("#")[0].strip()

    # Remove protocol prefix
    for prefix in ["https://", "http://"]:
        if s.lower().startswith(prefix):
            s = s[len(prefix):]
            break

    # Remove www. prefix
    if s.lower().startswith("www."):
        s = s[4:]

    # Remove github.com/ prefix
    if s.lower().startswith("github.com/"):
        s = s[len("github.com/"):].strip()

    # Remove leading @ and trailing slashes
    s = s.lstrip("@").strip("/")

    # If user passed full repo URL like github.com/username/repo, take first part
    parts = [p.strip() for p in s.split("/") if p.strip()]
    if not parts:
        return ""

    return parts[0]


def fetch_github_user_data(username: str) -> Dict[str, Any]:
    """
    Fetches public profile data and public repositories for a given GitHub username.
    Uses official public GitHub REST API.
    """
    cleaned_username = extract_github_username(username)
    if not cleaned_username or not GITHUB_USERNAME_REGEX.match(cleaned_username):
        raise ValueError("Invalid GitHub profile URL.")

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "CareerPilot-AI-App"
    }

    # Fetch user profile
    profile_url = f"{GITHUB_API_BASE}/users/{cleaned_username}"
    try:
        resp = requests.get(profile_url, headers=headers, timeout=10)
    except Exception:
        raise ValueError("GitHub service is currently unavailable. Please check your connection and try again.")

    if resp.status_code == 404:
        raise ValueError("GitHub user not found.")
    elif resp.status_code != 200:
        raise ValueError(f"GitHub API error: HTTP {resp.status_code}")

    profile_data = resp.json()

    # Fetch public repositories (up to 30, sorted by updated)
    repos_url = f"{GITHUB_API_BASE}/users/{cleaned_username}/repos?sort=updated&per_page=30"
    try:
        repos_resp = requests.get(repos_url, headers=headers, timeout=10)
        repos_data = repos_resp.json() if repos_resp.status_code == 200 else []
    except Exception:
        repos_data = []

    parsed_repos = []
    for r in repos_data:
        if isinstance(r, dict):
            parsed_repos.append({
                "name": r.get("name"),
                "description": r.get("description"),
                "html_url": r.get("html_url"),
                "language": r.get("language"),
                "stargazers_count": r.get("stargazers_count", 0),
                "forks_count": r.get("forks_count", 0),
                "is_fork": r.get("fork", False),
                "updated_at_remote": str(r.get("updated_at", ""))
            })

    return {
        "username": profile_data.get("login"),
        "name": profile_data.get("name"),
        "bio": profile_data.get("bio"),
        "avatar_url": profile_data.get("avatar_url"),
        "html_url": profile_data.get("html_url"),
        "public_repos": profile_data.get("public_repos", 0),
        "followers": profile_data.get("followers", 0),
        "following": profile_data.get("following", 0),
        "repositories": parsed_repos
    }


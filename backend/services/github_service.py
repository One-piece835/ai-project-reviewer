import requests
from urllib.parse import urlparse
import urllib3
import base64
import json
from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)

def github_get(url):
    pass


def extract_repo_info(repo_url):

    path_parts = urlparse(repo_url).path.strip("/").split("/")

    if len(path_parts) < 2:
        raise ValueError("Invalid GitHub repository URL")

    owner = path_parts[0]
    repo = path_parts[1]

    return {
        "owner": owner,
        "repo": repo
    }

def get_repository_metadata(owner, repo):
    
    url =  f"https://api.github.com/repos/{owner}/{repo}"

    response = requests.get(
    url,
    headers=HEADERS,
    verify=False
)

    if response.status_code != 200:
        raise Exception(response.json().get("message"))
    
    data = response.json()

    return {
        "name": data.get("name"),
        "description": data.get("description"),
        "stars": data.get("stargazers_count"),
        "forks": data.get("forks_count"),
        "language": data.get("language"),
    }

def get_readme(owner, repo):

    url = f"https://api.github.com/repos/{owner}/{repo}/readme"

    response = requests.get(
        url,
        headers=HEADERS,
        verify=False
    )

    # print("STATUS CODE:", response.status_code)
    # print("RESPONSE:", response.text[:500])

    if response.status_code == 404:
        return {
            "found": False,
            "content": None
        }

    if response.status_code != 200:
        raise Exception(response.json().get("message"))

    data = response.json()

    encoded_content = data.get("content", "")

    decoded_content = base64.b64decode(
        encoded_content
    ).decode("utf-8")

    return {
        "found": True,
        "content": decoded_content
    }


def get_package_json(owner, repo):
    # fetch package.json
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/package.json"

    response = requests.get(
        url,
        headers=HEADERS,
        verify = False
    )

    if response.status_code == 404:
        return {
            "found": False,
            "content": None
        }
    
    if response.status_code != 200:
        raise Exception(response.json().get("message"))
    
    data = response.json()

    encoded_content = data.get("content", "")

    # decode base64
    decoded_content = base64.b64decode(
        encoded_content
    ).decode("utf-8")

    # convert json string to python dict

    json_data = json.loads(decoded_content)

    return {
        "found": True,
        "content": json_data
    }
    

def get_repository_contents(owner, repo):

    url = f"https://api.github.com/repos/{owner}/{repo}/contents"

    response = requests.get(
        url,
        headers=HEADERS,
        verify = False
        )
    
    if response.status_code == 404:
        return {
        "found": False,
        "content": None
}
    
    if response.status_code != 200:
        raise Exception(
    f"GitHub API Error: {response.json().get('message')}"
)
    
    data = response.json()

    return {
        "found": True,
        "content": data
    }


def get_directory_contents(
    owner,
    repo,
    directory_name
):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{directory_name}"

    response = requests.get(
        url,
        headers=HEADERS,
        verify = False
    )
    
    if response.status_code == 404:
        return {
        "found": False,
        "content": None
}
    
    if response.status_code != 200:
        raise Exception(
    f"GitHub API Error: {response.json().get('message')}"
)
    
    src_content = response.json()

    return{
        "found": True,
        "content": src_content
    }
    
def explore_directory(
    owner,
    repo,
    directory_path
):
    contents = get_directory_contents(
        owner,
        repo,
        directory_path
    )

    if not contents["found"]:
        return []

    code_files = []

    for item in contents["content"]:

        if item["type"] == "file":

            if item["name"].endswith(
                (
                    ".js",
                    ".jsx",
                    ".ts",
                    ".tsx",
                    ".py"
                )
            ):
                code_files.append(
                    item["path"]
                )

        elif item["type"] == "dir":

            nested_files = explore_directory(
                owner,
                repo,
                item["path"]
            )

            code_files.extend(
                nested_files
            )

    return code_files


def get_file_contents(
    owner,
    repo,
    file_paths
):
    contents = []

    for file_path in file_paths:

        # GitHub API request

        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"

        response = requests.get(
            url,
            headers=HEADERS,
            verify=False
        )

        if response.status_code == 404:
            continue
    
        if response.status_code != 200:
            continue
    
        data = response.json()

        encoded_content = data.get(
            "content",
            ""
        )

        # decode base64

        decoded_content = base64.b64decode(
            encoded_content
        ).decode("utf-8")

    
        contents.append({
            "path": file_path,
            "content": decoded_content
        })

    return contents
import requests
from config import ENV

api_url = ENV["GITHUB_API_URL"]


def get_github_trends():
    response = []
    try:
        response = requests.get(api_url)
    except Exception as e:
        print("error fetching from github ", e)

    return response.json()


def transform_github_trends_response(response):
    results = response["items"]
    content = "\n# Github python trends"
    for item in results:
        print(item)
        info = f'\n- [{item["repo"]}]({item["repo_link"]}): {item["desc"]} ({item["added_stars"]})'
        content += info

    return content


if __name__ == "__main__":
    response = get_github_trends()
    gh_trends = transform_github_trends_response(response)

    print(gh_trends)

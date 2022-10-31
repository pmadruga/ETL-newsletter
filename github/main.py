import requests
from config import ENV

domain = ENV["GITHUB_API_URL"]


def get_github_trends(language):
    # api_url = f"{domain}/repo?lang={language}&since=weekly"
    api_url = f"{domain}/repositories/{language}?since=weekly"
    print('API URL', api_url)
    response = []
    try:
        response = requests.get(api_url)
    except Exception as e:
        print("error fetching from github ", e)

    return response.json()


def transform_github_trends_response(response, language):
    print('THIS IS RESPONSE', response)
    # results = response["items"]
    results = response
    content = f"\n## **Github {language} trends**"
    for item in results:
        print(item)
        info = f'\n- [{item["repositoryName"]}]({item["url"]}): {item["description"]}'
        content += info

    return content


if __name__ == "__main__":
    response = get_github_trends(language="python")
    gh_trends = transform_github_trends_response(response, language="python")

    print(gh_trends)

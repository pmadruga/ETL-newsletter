import requests
import datetime
from config import ENV


def get_newsletter_title():
    # get week number
    week_number = datetime.date.today().isocalendar()[1]
    return f"Week {week_number}"


def create_draft_newsletter(content="test_body"):
    api_url = ENV["NEWSLETTER_API_URL"]
    body = {"subject": get_newsletter_title(), "body": content}
    header = {"Authorization": ENV["NEWSLETTER_AUTHORIZATION"]}
    try:
        response = requests.post(api_url, json=body, headers=header)
        print(response)
    except Exception as e:
        print("error when creating newsletter draft: ", e)
    return True


# debugging stuff
if __name__ == "__main__":
    print(ENV["NEWSLETTER_API_URL"])
    # create_draft_newsletter()

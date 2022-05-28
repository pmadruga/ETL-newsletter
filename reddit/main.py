import os
import sys
import praw
import reddit.helpers as helpers
from time import sleep
from config import ENV


def get_variable(variable_name):
    print(os.getenv(variable_name.upper()))
    return os.getenv(variable_name.upper())


print(ENV["REDDIT_CLIENT_ID"])


def authentication():
    reddit = praw.Reddit(
        client_id=ENV["REDDIT_CLIENT_ID"],
        client_secret=ENV["REDDIT_CLIENT_SECRET"],
        user_agent=ENV["REDDIT_USER_AGENT"],
        username=ENV["REDDIT_USERNAME"],
        password=ENV["REDDIT_PASSWORD"],
    )
    return reddit


# TODO: there's a better to do this
def format_sub_name(sub_name):
    if sub_name is "DataScience":
        return "Data Science"
    if sub_name is "MachineLearning":
        return "Machine Learning"
    if sub_name is "MLQuestions":
        return "ML Questions"
    if sub_name is "AskStatistics":
        return "Ask Statistics"
    if sub_name is "DataEngineering":
        return "Data Engineering"
    if sub_name is "LatestInML":
        return "Latest in ML"
    if sub_name is "LearnMachineLearning":
        return "Learn Machine Learning"
    return sub_name


def extract_from_reddit(reddit):
    content = "\n## Reddit"
    subs = helpers.data_sub_names()
    for sub in subs:
        content += f"\n\n### *{format_sub_name(sub)}*"

        for submission in reddit.subreddit(sub).top("week", limit=3):
            content += f"\n- {submission.title} ([🔗 link](https://reddit.com{submission.permalink}); ⬆️  {submission.ups} ; 💬 {submission.num_comments})"

            sleep(0.3)

    return content


def get_reddit_content():
    return extract_from_reddit(authentication())

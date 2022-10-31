import os
import sys
from random import random
import pathlib
from datetime import datetime
from airflow.utils.dates import days_ago
from airflow.decorators import dag, task, task_group
from example_extract.helpers import data_sub_names


abs_path = os.path.abspath(os.path.dirname(__file__))


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from reddit.main import get_reddit_content
from feeds.feed_fetcher import (
    get_company_blog_feeds,
    get_podcast_feeds,
    get_youtube_feeds,
)
from github.main import get_github_trends, transform_github_trends_response
from buttondown.main import create_draft_newsletter
from helpers.dates import result
from config import ENV


def get_filename():
    filepath = str(pathlib.Path(__file__).parent.resolve())

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d")
    filename = dt_string + ".md"
    # filepath = pathlib.Path(__file__).parent.resolve()
    final = filepath + "/output/" + filename

    return final


def get_header():
    header = f'# 5 Minutes of Data Science - week {result[0].isocalendar()[1]}\nHighlights from {result[0].strftime("%B %d")} to {result[len(result)-1].strftime("%B %d")}\n\n## **Foreword**\nHello world\nCome say hi on [Twitter](https://twitter.com/pmadruga_)\n\n---'
## 5 Minutes of Data Science - week {result[0].isocalendar()[1]}\n   
#Highlights from {result[0].strftime("%B %d")} to {result[len(result)-1].strftime("%B %d")}\n\n
### **Foreword**\n
#Hello world\n
#Come say hi on [Twitter](https://twitter.com/pmadruga_)\n\n
#--- 
#    """.format(length='multi-line', ordinal='second')
    return header



def start_newsletter_template():
    # create empty file
    output_file = get_filename()
    # adding a nice custom static header
    header_file = f"{abs_path}/assets/header.md"

    with open(header_file, "r", encoding="utf-8") as header_content:
        return header_content.read()


def write_content_to_output_file(content):
    output_file_name = get_filename()
    with open(output_file_name, "w+", encoding="utf-8") as f:
        f.write(content)


args = {"email": [ENV["ADMIN_EMAIL"]], "email_on_failure": True}


@dag(
    # schedule_interval="0 0 0 ? * SUN,MON *",
    schedule_interval="0 5 * * 1",
    start_date=days_ago(2),
    catchup=False,
    default_args=args,
)
def newsletter():
    @task_group(group_id="newsletter_template_init")
    def group_1():
        @task(task_id="init_newsletter_template")
        def init_newsletter_template():
            return get_header()

        template_content = init_newsletter_template()
        return template_content

    #        @task(task_id="fetch_recommended")
    #        def get_recommended():
    #            recommended_feed_url = Variable.get("upwork_feed_recommended")
    #            recommended = feedparser.parse(recommended_feed_url)
    #            return recommended
    #
    #        @task(task_id="fetch_best_match")
    #        def get_best_match():
    #            best_match_feed_url = Variable.get("upwork_feed_best_match")
    #            best_match = feedparser.parse(best_match_feed_url)
    #
    #            return best_match
    #
    #        recommended_jobs = get_recommended()
    #        best_match_jobs = get_best_match()
    #
    #        return [recommended_jobs, best_match_jobs]

    @task_group(group_id="fetch_data_from_sources")
    def group_2(template_content):
        # fetch from reddit, write to file
        @task(task_id="fetch_from_reddit")
        def fetch_from_reddit():
            reddit_content = get_reddit_content()
            return reddit_content

        # fetch from other integrations, write to file
        #         @task(task_id="fetch_from_SOMEWHERE")
        #         def fetch_from_SOMEWHERE():
        #             return True

        @task(task_id="fetch_github_trends_python")
        def fetch_github_trends_python():
            gh_trends = transform_github_trends_response(
                get_github_trends("python"), "python"
            )
            return gh_trends

        @task(task_id="fetch_github_trends_jupyter")
        def fetch_github_trends_jupyter():
            gh_trends = transform_github_trends_response(
                get_github_trends("jupyter-notebook"), "jupyter notebook"
            )
            return gh_trends

        @task(task_id="fetch_company_blogs")
        def fetch_company_blogs():
            company_blogs_content = get_company_blog_feeds()
            return company_blogs_content

        @task(task_id="fetch_podcast_feeds")
        def fetch_podcast_feeds():
            podcast_feeds_content = get_podcast_feeds()
            return podcast_feeds_content

        @task(task_id="fetch_youtube_feeds")
        def fetch_youtube_feeds():
            youtube_feeds_content = get_youtube_feeds()
            return youtube_feeds_content

        @task(task_id="append_to_content")
        def append_to_content(
            data_from_reddit,
            data_from_github_python,
            data_from_github_jupyter,
            template_content,
            data_from_company_blogs,
            data_from_youtube,
            data_from_podcasts,
        ):
            # order matters!
            content = template_content
            content += data_from_company_blogs
            content += data_from_podcasts
            content += data_from_youtube
            content += data_from_reddit
            content += data_from_github_jupyter
            content += data_from_github_python
            return content

        data_from_reddit = fetch_from_reddit()
        data_from_github_python = fetch_github_trends_python()
        data_from_github_jupyter = fetch_github_trends_jupyter()
        data_from_company_blogs = fetch_company_blogs()
        data_from_youtube = fetch_youtube_feeds()
        data_from_podcasts = fetch_podcast_feeds()
        content = append_to_content(
            data_from_reddit,
            data_from_github_python,
            data_from_github_jupyter,
            template_content,
            data_from_company_blogs,
            data_from_youtube,
            data_from_podcasts,
        )

        return content

    @task_group(group_id="load_content")  # to buttondown and to markdown
    def group_3(content_from_datasources):
        # fetch from reddit, write to file
        @task(task_id="load_content_from_reddit_into_output_file")
        def load_from_reddit(data):
            write_content_to_output_file(data)

            return data

        @task(task_id="load_content_to_buttondown")
        def load_to_buttondown(data):
            create_draft_newsletter(data)

            return data

        return [
            load_from_reddit(content_from_datasources),
            load_to_buttondown(content_from_datasources),
        ]

    #    group_1()
    #    data_from_datasources = group_2()
    #    group_3(data_from_datasources)
    #    return True

    return group_3(group_2(group_1()))
    # return group_2 >> group_3 >> group_1


dag = newsletter()

if __name__ == "__main__":
    print("script started")
    # fetch_from_reddit()
    # print(start_newsletter_template())

import numpy as np
import pandas as pd
import feedparser

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

from helpers.dates import result


company_feeds_dict = [
    {"url": "https://deepmind.com/blog/feed/basic/", "blog_name": "DeepMind"},
    # {"url": "http://googleaiblog.blogspot.com/atom.xml", "blog_name": "Google AI"},
    {"url": "https://openai.com/blog/rss/", "blog_name": "Open AI"},
    #  {'url': 'https://feeds.feedburner.com/nvidiablog', 'blog_name': 'NVIDIA'},
    {"url": "https://www.amazon.science/index.rss", "blog_name": "Amazon Science"},
    #     {'url': 'https://aws.amazon.com/blogs/machine-learning/feed/', 'blog_name': 'AWS Machine Learning'},
    {
        "url": "https://machinelearning.apple.com/rss.xml",
        "blog_name": "Apple Machine Learning",
    },
]


podcasts_feeds_dict = [
    {
        "url": "https://feed.podbean.com/datascienceathome/feed.xml",
        "blog_name": "Data Science At Home",
    },
    {"url": "https://dataskeptic.libsyn.com/rss", "blog_name": "Data Skeptic"},
    {
        "url": "https://anchor.fm/s/36b4844/podcast/rss",
        "blog_name": "Towards Data Science",
    },
    {"url": "https://changelog.com/practicalai/feed", "blog_name": "Practical AI"},
    {"url": "https://feeds.megaphone.fm/MLN2155636147", "blog_name": "The TWIML AI"},
    {"url": "https://feeds.sounder.fm/19201/rss.xml", "blog_name": "DataFramed"},
    {"url": "https://anchor.fm/s/41286f68/podcast/rss", "blog_name": "Data Talks"},
    {"url": "https://feeds.buzzsprout.com/682433.rss", "blog_name": "The Data Exchange"},
    {"url": "https://feed.podbean.com/datascienceathome/feed.xml", "blog_name": "Data Science at Home"},
]
youtube_feeds_dict = [
    {
        "url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCMLtBahI5DMrt0NPvDSoIRQ",
        "blog_name": "Machine Learning Street Talk",
    },
    {
        "url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCtYLUTtgS3k1Fg4y5tAhLbw",
        "blog_name": "StatQuest",
    },
    {
        "url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCYO_jab_esuFRV4b17AJtAw",
        "blog_name": "3Blue1Brown",
    },
    {
        "url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCXZCJLdBC09xxGZ6gcdrc6A",
        "blog_name": "Open AI",
    },
    {
        "url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCP7jMXSY2xbc3KCAE0MHQ-A",
        "blog_name": "DeepMind",
    },
]

newsletters_feeds_dict = [
    {
        "url": "https://newsletter.sebastianraschka.com/?format=rss",
        "blog_name": "Sebastian Raschka",
    },
    {"url": "https://lastweekin.ai/feed", "blog_name": "Last Week in AI"},
    {"url": "https://jack-clark.net/feed/", "blog_name": "Import AI"},
    {"url": "https://nathanbenaich.substack.com/feed", "blog_name": "Guide to AI"},
    {"url": "https://raillc.substack.com/feed", "blog_name": "Responsible AI"},
    {"url": "https://newsletter.theaiedge.io/feed", "blog_name": "The AI Edge"},
    {"url": "https://feeds.feedburner.com/zerotomastery/mlm", "blog_name": "Zero To Mastery"},
    {"url": "https://gradientflow.substack.com/feed", "blog_name": "Gradient Flow"},
]


def fetch_feeds(specific_url, blog_name):
    print("fetching feeds for", blog_name)

    uh = feedparser.parse(specific_url)
    entries = []

    # print(uh.entries)

    for item in uh.entries:
        item_date = pd.to_datetime(item.published).tz_localize(None)
        first_date = result[0].tz_localize(None)
        last_date = result[len(result) - 1].tz_localize(None)

        if (item_date > first_date) & (item_date < last_date):
            date_formated = item_date.strftime("%y-%m-%d")

            entries.append(
                {
                    "date": date_formated,
                    "title": item.title,
                    "link": item.link,
                    "name": blog_name,
                }
            )

    return entries


def batch_fetch_feeds(feeds_dict):

    all_feeds = []

    for index, item in enumerate(feeds_dict):
        try:
            posts_per_item = fetch_feeds(item["url"], item["blog_name"])
            all_feeds.append(posts_per_item)

        except:
            continue

    print("all feeds", all_feeds)
    return all_feeds


def format_aggregated_feeds(feeds_aggregated, category):
    """
    Formatting the content.
    """
    print("\n\n\n\n")
    print(feeds_aggregated)
    print("\n\n\n\n")

    final_aggregated_content = f"\n\n## **{category}**\n" "\n"
    # for item in np.array(feeds_aggregated[2]).flatten():
    #     for j in range(0, len(item)):
    #         final_aggregated_content += (
    #             f"- {item[j]['title']}, _by [{item[j]['name']}]({item[j]['link']})_ \n"
    #         )

    for items in feeds_aggregated:
        if len(feeds_aggregated) > 0:
            for item in items:
                final_aggregated_content += (
                    f"- {item['title']}, _by [{item['name']}]({item['link']})_ \n"
                )

    return final_aggregated_content


def get_company_blog_feeds():
    return format_aggregated_feeds(batch_fetch_feeds(company_feeds_dict), "Blogs")


def get_podcast_feeds():
    return format_aggregated_feeds(batch_fetch_feeds(podcasts_feeds_dict), "Podcasts")


def get_youtube_feeds():
    return format_aggregated_feeds(batch_fetch_feeds(youtube_feeds_dict), "Youtube")


def get_newsletter_feeds():
    return format_aggregated_feeds(
        batch_fetch_feeds(newsletters_feeds_dict), "Newsletters"
    )


if __name__ == "__main__":
    print("hey")

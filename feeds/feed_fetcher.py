import numpy as np
import pandas as pd
import feedparser

from helpers.dates import result

                                                                                                                                        

feeds_dict = [
    {"url": "https://deepmind.com/blog/feed/basic/", "blog_name": "DeepMind"},
    {'url': 'http://googleaiblog.blogspot.com/atom.xml', 'blog_name': "Google AI"},
    {'url': 'https://openai.com/blog/rss/', 'blog_name': 'Open AI'},
#     {'url': 'https://feeds.feedburner.com/nvidiablog', 'blog_name': 'NVIDIA'},
    {'url': 'https://www.amazon.science/index.rss', 'blog_name': 'Amazon Science'},
#     {'url': 'https://aws.amazon.com/blogs/machine-learning/feed/', 'blog_name': 'AWS Machine Learning'},
    {'url': 'https://machinelearning.apple.com/rss.xml', 'blog_name': 'Apple Machine Learning'}
]

def fetch_feeds(specific_url, blog_name):

    uh = feedparser.parse(specific_url)
    entries = []

    for item in uh.entries:
        item_date = pd.to_datetime(item.published).tz_localize(None)
        first_date = result[0].tz_localize(None)
        last_date = result[len(result)-1].tz_localize(None)

        if (item_date > first_date) & (item_date < last_date):
            date_formated = item_date.strftime('%y-%m-%d')

            entries.append({'date': date_formated, 'title': item.title,
                           'link': item.link, 'name': blog_name})

    return entries


def batch_fetch_feeds(feeds_dict):

    all_feeds = []

    for index, item in enumerate(feeds_dict):
        posts_per_item = fetch_feeds(item['url'], item["blog_name"])

        all_feeds.append(posts_per_item)
    return all_feeds



def format_aggregated_feeds(feeds_aggregated, category):
    """
    Last step of the process
    """
    final_aggregated_content = f"{category}\n"\
        "---\n"\

    for item in np.array(feeds_aggregated).flatten():
        for j in range(0, len(item)):
            final_aggregated_content += f"- {item[j]['title']}, _by [{item[j]['name']}]({item[j]['link']})_ \n"

    return final_aggregated_content

def get_company_blog_feeds():
    return format_aggregated_feeds(batch_fetch_feeds(feeds_dict), 'Blogs')

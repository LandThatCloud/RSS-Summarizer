import feedparser
import random
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk
nltk.download('punkt')

# A list of RSS feeds for technical articles and blog posts
rss_feeds = [
    'https://aws.amazon.com/about-aws/whats-new/feed/',
    'https://cloud.google.com/blog/feeds/',
    'https://www.oracle.com/cloud/index.html#getstarted-category',
    'https://www.ibm.com/cloud/blog/rss',
    'https://blogs.vmware.com/cloud/feed/',
    'https://www.redhat.com/en/topics/cloud-computing/rss',
    'https://success.docker.com/rss-all'
]

# Variable to track if an article was found
article_found = False

# Loop through each feed until an article is found
for rss_feed in rss_feeds:
    # Parse the RSS feed to get the latest article
    feed = feedparser.parse(rss_feed)

    if len(feed['entries']) > 0:
        # Get the title and link of the latest article
        title = feed['entries'][0]['title']
        link = feed['entries'][0]['link']

        # Summarize the article into 250 words
        parser = HtmlParser.from_url(link, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = ''
        for sentence in summarizer(parser.document, 50):
            summary += str(sentence)

        # Write the summarized article to a text file
        with open("summary.txt", "w") as f:
            f.write("Title: " + title + "\n\nSummary:\n\n" + summary)
            f.write(rss_feed)

        print("Summary written to summary.txt")
        article_found = True
        break

if not article_found:
    print("No articles found in any of the feeds")

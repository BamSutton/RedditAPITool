import pandas as pd
import praw
from Subreddit.Checker import check_subreddit

import praw.exceptions

# This is the object that is used to connect to the Reddit API
# this is using my account details
reddit = praw.Reddit(
    client_id="wQw4KIvUL4GR5wMS1ka8_w",
    client_secret="hAipyADCGDbXWgA9bN61MZEqbiJvAA",
    password="zA4Mn$8n7bWG69&",
    user_agent="Masking Reddit Scraper v0.0.1",
    username="KaoticKowala",
)
# these are the search terms that we care about currently
# they get feed into the below function "check_subreddit" which finds all of the relevant subreddits (see Checker.py)
search_terms = ['Autism','neurodivergent','ASD','neurospicy']
foundlist = check_subreddit(reddit=reddit,search_terms=search_terms)

# this loops through all of the recently found subreddits from "check_subreddit" and searches for all the top posts
# across all time with the query term "unmasking" and prints out the URL to that post into the console log
for subreddit in foundlist:
    print(subreddit)
    for posting in reddit.subreddit(subreddit).search("unmasking", sort='top',time_filter='all', limit= None):
        print(posting.permalink)
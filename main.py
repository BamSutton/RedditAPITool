import pandas as pd
import praw
from Subreddit.Checker import check_subreddit
import config

import praw.exceptions

# This is the object that is used to connect to the Reddit API
# this is using my account details
reddit = praw.Reddit(
    client_id=config.client_id,
    client_secret=config.client_secret,
    password=config.password,
    user_agent="Masking Reddit Scraper v0.0.1",
    username=config.username,
)
# these are the search terms that we care about currently
# they get feed into the below function "check_subreddit" which finds all of the relevant subreddits (see Checker.py)
search_terms = ['Autism','neurodivergent','ASD','neurospicy']
foundlist = check_subreddit(reddit=reddit,search_terms=search_terms)

redditResultList = []
# this loops through all of the recently found subreddits from "check_subreddit" and searches for all the top posts
# across all time with the query term "unmasking" and prints out the URL to that post into the console log
for subreddit in foundlist:
    print(subreddit)
    postingDict = {}
    #for posting in reddit.subreddit(subreddit).search("unmasking", sort='top',time_filter='all', limit= None):
    for posting in reddit.subreddit(subreddit).search("unmasking", sort='top',time_filter='all', limit= 1):
        posting.comments.replace_more(limit=0)
        commentDict = {}
        for comment in posting.comments:
            commentDict[posting.name] = comment.body
        print(f"{commentDict}")
        #postingDict[subreddit] = commentDict
    #redditResultList.append(postingDict)
#print(redditResultList)
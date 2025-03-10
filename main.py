import pandas as pd
import praw
from Subreddit.Checker import check_subreddit
import config
from CSV_creator import createCSVs
from models import Subreddits, Submissions, Comments

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
# they get fed into the below function "check_subreddit" which finds all of the relevant subreddits (see Checker.py)
search_terms = ['Autism','neurodivergent','ASD','neurospicy']
foundSubredditList = check_subreddit(reddit,search_terms)

# this loops through all of the recently found subreddits from "check_subreddit" and searches for all the top posts
# across all time with the query term "unmasking" and prints out the URL to that post into the console log
subredditListData: list[Subreddits] = []
count = 0
for subredditname in foundSubredditList:
    count += 1
    subreddit = reddit.subreddit(subredditname)
    print(f"{count}. --Pulling {subredditname} data--")
    newsubreddit = Subreddits(
        id = subreddit.id,
        name = subreddit.display_name,
        description= subreddit.description,
        time_created= subreddit.created_utc,
        subsrcibers= subreddit.subscribers,
    )
    #for submission in subreddit.search("unmasking", sort='top',time_filter='all', limit= None):
    for submission in subreddit.search("unmasking", sort='top',time_filter='all', limit= 1):
        newSubmission = Submissions(
            id = submission.id, 
            title=submission.title, 
            content=submission.selftext,
            score = submission.score,
            poster = submission.author.name if submission.author else "Deleted", 
            time_created=submission.created_utc,)
        
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            newComment = Comments(
                id=comment.id,
                content=comment.body,
                poster=comment.author.name if comment.author else "Deleted",
                score=comment.score,
                time_created=comment.created_utc,
            )
            newSubmission.commentList.append(newComment)
        newsubreddit.submissionList.append(newSubmission)
    # print (f"Added {(newsubreddit.submissionList)} posts to subredit: {newsubreddit.name}")
    subredditListData.append(newsubreddit)
for s in subredditListData:
    print (f"{s.name} post count:{len(s.submissionList)}")
    for sub in s.submissionList:
        print (f'Number of Comments: {len(sub.commentList)}')

# createCSVs()


# print(subredditList)

# def csv_comment_formatter(comment_list):

#     return None


# -subreddit-
# post1-title-selftext    comment1    comment1.1
#                                     comment1.2
#                                                 comment1.2.1
#                         comment2    comment2.1

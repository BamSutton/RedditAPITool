import pandas as pd
import praw
from Subreddit.Checker import check_subreddit
import config
from models import Subreddits, Submissions, Comments
from CSV_creator import createCSVs

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
search_terms = ['Autism']
foundSubredditList, private_count = check_subreddit(reddit,search_terms)
print(f"Total subreddits found: {len(foundSubredditList) + private_count}")
print(f"Number of private subreddits found: {private_count}")
print(f"Number of unique subreddits used for data pull: {len(foundSubredditList)}")

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
    for submission in subreddit.search("unmasking", sort='top',time_filter='all', limit= 2):
        print (submission.permalink)
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
                    parent_id=comment.parent_id,
                    time_created=comment.created_utc,
                )
            newSubmission.commentList.append(newComment)
        
        for comment in newSubmission.commentList:
            newSubmission.commentMap[comment.parent_id.replace("t1_","")].append(comment)
            
        newsubreddit.submissionList.append(newSubmission)
    # print (f"Added {(newsubreddit.submissionList)} posts to subredit: {newsubreddit.name}")
    subredditListData.append(newsubreddit)
for s in subredditListData:
    print (f"{s.name} post count:{len(s.submissionList)}")
    for sub in s.submissionList:
        print (f'Number of Comments: {len(sub.commentList)}')

createCSVs(subredditListData)
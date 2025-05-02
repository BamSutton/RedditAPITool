import pandas as pd
from constants import *
from datetime import datetime

def get_reddit_dataframes(foundSubredditList, SubmissionSearchTerm):
    
    for subreddit in foundSubredditList:
        subreddit_dict["ID"].append(subreddit.id)
        subreddit_dict["Name"].append(subreddit.display_name)
        subreddit_dict["Created_At"].append(datetime.fromtimestamp(subreddit.created_utc))
        subreddit_dict["Subscribers"].append(subreddit.subscribers)
        subreddit_dict["Description"].append(subreddit.description)
        
        for submission in subreddit.search(SubmissionSearchTerm, sort="top", time_filter="all", limit=None):
            submission_dict["ID"].append(submission.id) 
            submission_dict["Title"].append(submission.title)
            submission_dict["Content"].append(submission.selftext)
            submission_dict["Author"].append(submission.author.name if submission.author else "Deleted") 
            submission_dict["Score"].append(submission.score)
            submission_dict["Created_at"].append(datetime.fromtimestamp(submission.created_utc))
            submission_dict["Subreddit_ID"].append()
            
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                comment_dict["ID"].append(comment.id)
                comment_dict["Content"].append(comment.body)
                comment_dict["Author"].append(comment.author.name if comment.author else "Deleted")
                comment_dict["Score"].append(comment.score)
                comment_dict["Created_at"].append(datetime.fromtimestamp(comment.created_utc))
                comment_dict["Parent_ID"].append(comment.parent_id)
                comment_dict["Submission_ID"].append(submission.id)

    df_subreddits = pd.DataFrame.from_dict(data=subreddit_dict)
    df_subreddits.set_index('ID',inplace=True)

    df_submissions = pd.DataFrame.from_dict(data=submission_dict)
    df_submissions.set_index('ID',inplace=True)

    df_comments = pd.DataFrame.from_dict(data=comment_dict)
    df_comments.set_index('ID',inplace=True)
    
    return df_subreddits, df_submissions, df_comments
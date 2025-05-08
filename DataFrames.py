import pandas as pd
from constants import *
from datetime import datetime

def get_reddit_dataframes(foundSubredditList, SubmissionSearchTerm):
    
    for subreddit in foundSubredditList:
        print(f"--Processing {subreddit.display_name}--")
        subreddit_dict["ID"].append(subreddit.id)
        subreddit_dict["Name"].append(subreddit.display_name)
        subreddit_dict["Created"].append(datetime.fromtimestamp(subreddit.created_utc))
        subreddit_dict["Subscribers"].append(subreddit.subscribers)
        subreddit_dict["Description"].append(subreddit.description)
        
        submissionResultList = list(subreddit.search(SubmissionSearchTerm, sort="top", time_filter="all", limit=None))
        currentSubmission = 0
        for submission in submissionResultList:
            currentSubmission += 1
            print(f'processing {currentSubmission}/{len(submissionResultList)}', end="\r")
            submission_dict["ID"].append(submission.id) 
            submission_dict["Title"].append(submission.title)
            submission_dict["Content"].append(submission.selftext)
            submission_dict["Author"].append(submission.author.name if submission.author else "Deleted") 
            submission_dict["Score"].append(submission.score)
            submission_dict["Created"].append(datetime.fromtimestamp(submission.created_utc))
            submission_dict["Subreddit_ID"].append(subreddit.id)
            
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                comment_dict["ID"].append(comment.id)
                comment_dict["Content"].append(comment.body)
                comment_dict["Author"].append(comment.author.name if comment.author else "Deleted")
                comment_dict["Score"].append(comment.score)
                comment_dict["Created"].append(datetime.fromtimestamp(comment.created_utc))
                comment_dict["Parent_ID"].append(comment.parent_id[3:])
                comment_dict["Submission_ID"].append(submission.id)

    df_subreddits = pd.DataFrame.from_dict(data=subreddit_dict)
    df_submissions = pd.DataFrame.from_dict(data=submission_dict)
    df_comments = pd.DataFrame.from_dict(data=comment_dict)
    
    return df_subreddits, df_submissions, df_comments
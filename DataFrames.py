import pandas as pd
from constants import *
from datetime import datetime

"""
Using the given list of subreddits, this will search each subreddit for the given search term across all posts in that subreddit with 
no limit to the amount of results returned.

With this data, we will then create a data frame for all of the collected Subreddits, Submissions and Comments 
that resulted from the searches and return them in a dictionary for further processing.

Note:   This has the tendency to return a 429 response for being rate limited due to how many calls we end up making to the Reddit API
        once that limit is hit - we stop searching all together and save the results that we have collected.
"""
def get_reddit_dataframes(foundSubredditList, SubmissionSearchTerm):
    try:
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
    except Exception as e:
        print(e)
    finally:
        df_subreddits = pd.DataFrame.from_dict(data=subreddit_dict)
        df_submissions = pd.DataFrame.from_dict(data=submission_dict)
        df_comments = pd.DataFrame.from_dict(data=comment_dict)
        return{
        "subreddits": df_subreddits,
        "submissions" : df_submissions,
        "comments" : df_comments,
        }
    
def create_summary_dataframe(dataframesDict):
    
    summary_dictionary = {
        "total_subreddits": len(dataframesDict["subreddits"]),
        "mean_subscribers": dataframesDict["subreddits"]["Subscribers"].mean(),
        "max_subscribers": dataframesDict["subreddits"]["Subscribers"].max(),
        "min_subscribers": dataframesDict["subreddits"]["Subscribers"].min(),
        "total_submissions": len(dataframesDict["submissions"]),
        "mean_upvotes": dataframesDict["submissions"]["Score"].mean(),
        "max_upvotes": dataframesDict["submissions"]["Score"].max(),
        "min_upvotes": dataframesDict["submissions"]["Score"].min(),
        "total_comments": len(dataframesDict["comments"]),
        "mean_commment_upvotes": dataframesDict["comments"]["Score"].mean(),
        "max_comment_upvotes": dataframesDict["comments"]["Score"].max(),
        "min_comment_upvotes": dataframesDict["comments"]["Score"].min(),
    }
    summary_all_dataframe = pd.DataFrame.from_dict(summary_dictionary)
    
    

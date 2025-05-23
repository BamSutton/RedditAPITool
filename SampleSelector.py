import pandas as pd

"""
Given the dictionary of dataframes provided and the sample size specified,
Return a Sample of the data centred around submissions provided, with the corrosponding subreddits 
and comments that these submissions are linked to.

This returns a dictionary of the dataframes created from the sampling functions 
"""
def create_new_samples(dataframeDict: dict, sample_size: float):
    
    sample_df_submission = dataframeDict("submissions").sample(frac=sample_size, replace=False, random_state=1)
    comment_mask = dataframeDict("comments")['Submission_ID'].isin(sample_df_submission['ID'])
    sample_df_comment = dataframeDict("comments")[comment_mask]
    subreddit_mask = dataframeDict("subreddits")['ID'].isin(sample_df_submission['Subreddit_ID'])
    sample_df_subreddit = dataframeDict("subreddits")[subreddit_mask]
    
    return {"subreddits": sample_df_subreddit, "submissions": sample_df_submission, "comments": sample_df_comment,}
    
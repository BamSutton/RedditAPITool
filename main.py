import praw
from praw import models
from datetime import datetime
import config

from SubredditChecker import find_subreddits
from DataFrames import get_reddit_dataframes
from SampleSelector import create_new_samples
from FileCreator import FileCreator
from constants import search_terms,sample_size


def main():
    #Creates a reddit instance that will be used to pull the data you are after
    reddit = praw.Reddit(
        client_id=config.client_id,
        client_secret=config.client_secret,
        username=config.username,
        password=config.password,
        user_agent=f"python:MaskingResearchApp:v0.1 (by /u/{config.username})",
        ratelimit_seconds=3600,
    )
    
    filecreator = FileCreator()
    filecreator.create_new_directory()

    foundSubredditList = find_subreddits(reddit, search_terms)
    filecreator.save_subreddit_names(foundSubredditList)
     
    dataframeDict = get_reddit_dataframes(foundSubredditList, "Unmasking")

    filecreator.save_dataframe(dataframeDict("subreddits"),"All_Subreddits")
    filecreator.save_dataframe(dataframeDict("submissions"),"All_Submissions")
    filecreator.save_dataframe(dataframeDict("comments"),"All_Comments")

    print(f'Total Subreddits: {len(dataframeDict("subreddits"))}')
    print(f'Total Submissions: {len(dataframeDict("submissions"))}')
    print(f'Total Comments: {len(dataframeDict("comments"))}')

    sample_dataframe_dict = create_new_samples(dataframeDict, sample_size)
    filecreator.save_dataframe(sample_dataframe_dict("subreddits"),"sample_Subreddits")
    filecreator.save_dataframe(sample_dataframe_dict("submissions"),"sample_Submissions")
    filecreator.save_dataframe(sample_dataframe_dict("comments"),"sample_Comments")


if __name__ == "__main__":
    main()
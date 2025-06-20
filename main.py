import praw
from praw import models
from datetime import datetime
import config

from SubredditChecker import find_subreddits
from DataFrames import get_reddit_dataframes
from FileCreator import FileCreator
from constants import reddit_search_terms, submission_search_terms,sample_size


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

    foundSubredditList = find_subreddits(reddit, reddit_search_terms)
    filecreator.save_subreddit_names(foundSubredditList)
     
    dataframeDict = get_reddit_dataframes(foundSubredditList, submission_search_terms)

    filecreator.save_dataframe(dataframeDict["subreddits"],"All_Subreddits")
    filecreator.save_dataframe(dataframeDict["submissions"],"All_Submissions")
    filecreator.save_dataframe(dataframeDict["comments"],"All_Comments")

    print(f'Total Subreddits: {len(dataframeDict["subreddits"])}')
    print(f'Total Submissions: {len(dataframeDict["submissions"])}')
    print(f'Total Comments: {len(dataframeDict["comments"])}')


if __name__ == "__main__":
    main()
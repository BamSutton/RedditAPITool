import praw
from datetime import datetime
import config
import os

from SubredditChecker import find_subreddits
from DataFrames import get_reddit_dataframes
from SampleSelector import create_new_sample

def create_save_directory() -> str:
    try:
        currentDateTime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        directory = f'{currentDateTime}_DataFiles'
        os.mkdir(directory)
        return directory
    except FileExistsError:
        print(f'Directory {directory} already exists')
    except PermissionError:
        print(f'Current user does not have permission to create directory')
    except Exception as e:
        print(f'Error occurred when trying to create save directory with this error: {e}')


def save_subreddit_names(subreddits_list: list, directory):
    writefile = open(f'{directory}/founditems.txt', 'w')
    for subreddit in subreddits_list:
        writefile.write(f'{subreddit.display_name}\n')
    writefile.flush
    writefile.close
    

def main():
    reddit = praw.Reddit(
        client_id=config.client_id,
        client_secret=config.client_secret,
        username=config.username,
        password=config.password,
        user_agent="python:MaskingResearchApp:v0.1 (by /u/kaotickowala)",
        ratelimit_seconds=840,
    )
    
    directory = create_save_directory()
    search_terms = ["Autism"]

    foundSubredditList = find_subreddits(reddit, search_terms)

    df_subreddits, df_submissions, df_comments = get_reddit_dataframes(foundSubredditList, "Unmasking")

    df_subreddits.to_csv(f'{directory}/AllSubredditsDataFrame.csv')
    df_submissions.to_csv(f'{directory}/AllSubmissionsDataFrame.csv')
    df_comments.to_csv(f'{directory}/AllCommentsDataFrame.csv')
    
    print(f'Total Subreddits: {df_subreddits.count}')
    print(f'Total Submissions: {df_submissions.count}')
    print(f'Total Comments: {df_comments.count}')

    create_new_sample(df_subreddits, df_submissions, df_comments)

if __name__ == "__main__":
    main()
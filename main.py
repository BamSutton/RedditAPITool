import praw
from datetime import datetime
import config

from models import Subreddits, Submissions, Comments
from Subreddit.Checker import check_subreddit
from CSV_creator import createCSVs
from submission_selector import SubmissionSelector
from DataFrameCreator import get_reddit_dataframes

reddit = praw.Reddit(
    client_id=config.client_id,
    client_secret=config.client_secret,
    password=config.password,
    user_agent="Masking Reddit Scraper v0.0.1",
    username=config.username,
)

search_terms = ["Autism"]
foundSubredditList, private_count = check_subreddit(reddit, search_terms)
print(f"Total subreddits found: {len(foundSubredditList) + private_count}")
print(f"Number of private subreddits found: {private_count}")
print(f"Number of unique subreddits used for data pull: {len(foundSubredditList)}")

df_subreddits, df_submissions, df_comments = get_reddit_dataframes(foundSubredditList, "Unmasking")

currentDateTime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
df_subreddits.to_csv(f'{currentDateTime}_AllSubredditsDataFrame.csv')
df_submissions.to_csv(f'{currentDateTime}_AllSubmissionsDataFrame.csv')
df_comments.to_csv(f'{currentDateTime}_AllCommentsDataFrame.csv')

subredditListData: list[Subreddits] = []
allSubmissionsList: list[Submissions] = []
count = 0
for subredditname in foundSubredditList:
    count += 1
    subreddit = reddit.subreddit(subredditname)
    print(f"{count}. --Pulling {subredditname} data--")
    newsubreddit = Subreddits(
        id=subreddit.id,
        name=subreddit.display_name,
        description=subreddit.description,
        time_created=subreddit.created_utc,
        subsrcibers=subreddit.subscribers,
    )
    templist = list(
        subreddit.search("unmasking", sort="top", time_filter="all", limit=None)
    )
    submissionCount = 0
    for submission in templist:
        submissionCount += 1
        # for submission in subreddit.search("unmasking", sort='top',time_filter='all', limit= 20):
        newSubmission = Submissions(
            id=submission.id,
            title=submission.title,
            content=submission.selftext,
            score=submission.score,
            poster=submission.author.name if submission.author else "Deleted",
            time_created=submission.created_utc,
        )
        print(f"Adding new submission {submissionCount} / {len(templist)}")

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
            newSubmission.commentMap[comment.parent_id.replace("t1_", "")].append(
                comment
            )

        newsubreddit.submissionList.append(newSubmission)
        allSubmissionsList.append(newSubmission)

    subredditListData.append(newsubreddit)
for s in subredditListData:
    print(f"{s.name} post count:{len(s.submissionList)}")
    for sub in s.submissionList:
        print(f"Number of Comments: {len(sub.commentList)}")

createCSVs(subredditListData)
SubmissionSelector(allSubmissionsList, 2)
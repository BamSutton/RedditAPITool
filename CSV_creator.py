from datetime import datetime
from models import *
import csv
import pandas as pd

def createCSVs(subredditList: list[Subreddits]):
    global csvWriter
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    subredditHeaders = ["Subreddit Name","Subreddit Description","Subscribers","Time Created"]
    submissionHeaders = ["Post Title", "Post Text", "Post Author", "Post Score", "Time Created", "Comment Thread"]

    csvFile = open('temp.csv','w',encoding='utf-8',newline='')
    csvWriter = csv.writer(csvFile)

    for subredditItem in subredditList:
        currentSubreddit = [["---- New Subreddit ----"]]
        currentSubreddit.append(subredditHeaders)
        currentSubreddit.append([subredditItem.name, subredditItem.description, subredditItem.subscribers, subredditItem.time_created])
        csvWriter.writerows(currentSubreddit)
        for submission in subredditItem.submissionList:
            currentSubmission = [["---- New Submission ----"]]
            currentSubmission.append(submissionHeaders)
            currentSubmission.append([submission.title, submission.content, submission.poster, submission.score, submission.time_created])
            currentSubmission.append(["---- Comment Thread Starts Here ----"])
            csvWriter.writerows(currentSubmission)
            for comment in submission.commentMap.get('t3_'+submission.id):
                linemaker(comment,submission.commentMap,[])
            csvWriter.writerow(["---- Comment Thread Ends Here ----"])
            

def linemaker(currentComment: Comments, commentMap: defaultdict, currentLine: list):
    currentLine.append(currentComment.content)
    if commentMap.get(currentComment.id) is None:#iu1uyew
        csvWriter.writerow(currentLine)
        # print(currentLine)
        
    else:
        # print(len(commentMap.get(currentComment.id)))
        for comment in commentMap.get(currentComment.id):
            linemaker(comment, commentMap, currentLine)

    currentLine.pop()
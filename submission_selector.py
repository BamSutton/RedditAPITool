from models import Submissions, Comments
from collections import defaultdict
from datetime import datetime
import csv
import random


def SubmissionSelector(submissionList: list[Submissions], selectionValue):
    print(f"Running random select at {selectionValue}")

    selected_submissions = []
    count = 0
    while count < (len(submissionList) / selectionValue):
        selected_submissions.append(random.choice(submissionList))
        count += 1

    global csvRandomWriter
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    submissionHeaders = [
        "Post Title",
        "Post Text",
        "Post Author",
        "Post Score",
        "Time Created",
        "Comment Thread",
    ]

    csvFile = open(
        f"{current_datetime}_RandomSelection.csv", "w", encoding="utf-8", newline=""
    )
    csvRandomWriter = csv.writer(csvFile)

    for submission in selected_submissions:
        currentSubmission = [["---- New Submission ----"]]
        currentSubmission.append(submissionHeaders)
        currentSubmission.append(
            [
                submission.title,
                submission.content,
                submission.poster,
                submission.score,
                submission.time_created,
            ]
        )
        currentSubmission.append(["---- Comment Thread Starts Here ----"])
        csvRandomWriter.writerows(currentSubmission)
        for comment in submission.commentMap.get("t3_" + submission.id):
            linemaker(comment, submission.commentMap, [])
        csvRandomWriter.writerow(["---- Comment Thread Ends Here ----"])


def linemaker(currentComment: Comments, commentMap: defaultdict, currentLine: list):
    currentLine.append(currentComment.content)
    if commentMap.get(currentComment.id) is None:
        csvRandomWriter.writerow(currentLine)
    else:
        for comment in commentMap.get(currentComment.id):
            linemaker(comment, commentMap, currentLine)

    currentLine.pop()

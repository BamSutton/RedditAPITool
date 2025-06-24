# data frame structure that is used through the App
subreddit_dict = {"ID":[],"Name":[],"Subscribers":[],"Description":[],"Created":[]}
submission_dict = {"ID":[],"Title":[],"Content":[],"Author":[],"Score":[],"Created":[], "Subreddit_ID":[]}
comment_dict = {"ID":[],"Content":[],"Author":[],"Score":[],"Created":[],"Parent_ID":[],"Submission_ID":[]}

#Human readable CSV headers
CSV_subreddit_headers = ["Subreddit Name","Subreddit Description","Subscribers","Time Created"]
CSV_submission_headers = ["Post Title", "Post Text", "Post Author", "Post Score", "Time Created", "Comment Thread"]

# base data that can be changed if new inputs are required
reddit_search_terms = ["Autism"]
submission_search_terms = "unmasking"
sample_size = 0.20
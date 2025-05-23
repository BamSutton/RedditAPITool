# data frame structure that is used through the App
subreddit_dict = {"ID":[],"Name":[],"Subscribers":[],"Description":[],"Created":[]}
submission_dict = {"ID":[],"Title":[],"Content":[],"Author":[],"Score":[],"Created":[], "Subreddit_ID":[]}
comment_dict = {"ID":[],"Content":[],"Author":[],"Score":[],"Created":[],"Parent_ID":[],"Submission_ID":[]}

# base data that can be changed if new inputs are required
search_terms = ["Autism"]
sample_size = 0.05
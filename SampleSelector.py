from FileCreator import FileCreator
from constants import *

class SampleHandler:

    def create_new_samples(dataframeDict: dict, sample_size):
        
        sample_df_submission = dataframeDict["submissions"].sample(frac=sample_size, replace=False, random_state=1)
        
        comment_mask = dataframeDict["comments"]['Submission_ID'].isin(sample_df_submission['ID'])
        sample_df_comment = dataframeDict["comments"][comment_mask]
        
        subreddit_mask = dataframeDict["subreddits"]['ID'].isin(sample_df_submission['Subreddit_ID'])
        sample_df_subreddit = dataframeDict["subreddits"][subreddit_mask]
        
        return {"subreddits": sample_df_subreddit, "submissions": sample_df_submission, "comments": sample_df_comment,}
        
        
directoryHandler = FileCreator()
allDataDict = directoryHandler.load_last_run()
sampleDataDict = SampleHandler.create_new_samples(allDataDict, sample_size)
directoryHandler.save_dataframe(sampleDataDict["subreddits"],f"Sample_Subreddits_{sample_size}_")
directoryHandler.save_dataframe(sampleDataDict["submissions"],f"Sample_Submissions_{sample_size}_")
directoryHandler.save_dataframe(sampleDataDict["comments"],f"Sample_Comments_{sample_size}_")

directoryHandler.createHumanReadableCSVs(sampleDataDict)
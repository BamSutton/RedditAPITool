import pandas as pd
import FileCreator

class SampleHandler:

    def create_new_samples(self, dataframeDict: dict, sample_size):
        
        sample_df_submission = dataframeDict["submissions"].sample(frac=sample_size, replace=False, random_state=1)
        print(sample_df_submission.columns)
        
        comment_mask = dataframeDict["comments"]['Submission_ID'].isin(sample_df_submission['ID'])
        sample_df_comment = dataframeDict["comments"][comment_mask]
        
        subreddit_mask = dataframeDict["subreddits"]['ID'].isin(sample_df_submission['Subreddit_ID'])
        sample_df_subreddit = dataframeDict["subreddits"][subreddit_mask]
        
        return {"subreddits": sample_df_subreddit, "submissions": sample_df_submission, "comments": sample_df_comment,}
        
    def saveSampleDataFrames(self, sampleDataDict: dict):
        sampleDataDict["subreddits"].to_csv(f'{self.directory}/Sample{self.sample_size*100}%_Subreddits.csv')
        sampleDataDict["submissions"].to_csv(f'{self.directory}/Sample{self.sample_size*100}%_submissions.csv')
        sampleDataDict["comments"].to_csv(f'{self.directory}/Sample{self.sample_size*100}%_Comments.csv')
        
directoryHandler = FileCreator()
allDataDict = directoryHandler.load_last_run()
sampleDataDict = SampleHandler.create_new_samples(allDataDict,0.2)
SampleHandler.saveSampleDataFrames(sampleDataDict)
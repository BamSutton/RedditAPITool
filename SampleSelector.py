import pandas as pd

def create_new_sample(df_subreddits: pd.DataFrame, df_submissions: pd.DataFrame, df_comments: pd.DataFrame):
    
    submission_sample_df = df_submissions.sample(frac=0.05, replace=False, random_state=1)
    #submission_sample_df.set_index('ID',inplace=True)
    comment_mask = df_comments['Submission_ID'].isin(submission_sample_df['ID'])
    comment_sample_df = df_comments[comment_mask]
    print (f'Sample of Submissions: \n{submission_sample_df}')
    print (df_submissions)
    print (f'Sample of Comments: \n{comment_sample_df}')
    print (df_comments)
    
    # df1[df1.index.isin(df2.index)]
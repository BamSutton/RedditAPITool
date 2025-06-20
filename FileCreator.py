import os
from datetime import datetime
from pandas import DataFrame
import pandas as pd
from datetime import datetime
import csv
from constants import CSV_subreddit_headers,CSV_submission_headers

class FileCreator:
    """
    This is the class that creates and reads all of the files that are used by this application.
    It creates the directories that the files are saved in based off the current Date and Time that the app was run.
    This will save all of the dataframes to csv files with the given name to that directory.
    """
    global csvWriter
        
    @property
    def directory(self):
        return self._directory
    
    @directory.setter
    def directory(self, directory):
        self._directory = directory
    
    def create_new_directory(self):
        try:
            currentDateTime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.directory = f'{currentDateTime}_DataFiles'
            os.mkdir(self.directory)
            self.save_most_recent_run_directory()
        except FileExistsError:
            print(f'Directory {self.directory} already exists')
        except PermissionError:
            print(f'Current user does not have permission to create directory')
        except Exception as e:
            print(f'Error occurred when trying to create save directory with this error: {e}')
            
    def save_subreddit_names(self,subreddits_list: list):
        writefile = open(f'{self.directory}/founditems.txt', 'w')
        for subreddit in subreddits_list:
            writefile.write(f'{subreddit.display_name}\n')
        writefile.flush
        writefile.close
    
    def save_dataframe(self, dataframe: DataFrame, data_type: str):
        dataframe.to_csv(f'{self.directory}/{data_type}DataFrame.csv')
        
    def load_most_recent_run_directory(self):
        last_run_directory = open('last_run_directory.txt','r')
        directory = last_run_directory.readline()
        print(directory)
        self.directory = directory
        
    def save_most_recent_run_directory(self):
        last_run_directory = open('last_run_directory.txt','w')
        last_run_directory.write(self.directory)
        last_run_directory.flush()
        last_run_directory.close()
        
    def load_last_run(self) :
        self.load_most_recent_run_directory()
        subredditsDataFrame = pd.read_csv(f'{self.directory}/All_SubredditsDataFrame.csv',index_col=0)
        submissionsDataFrame = pd.read_csv(f'{self.directory}/All_SubmissionsDataFrame.csv',index_col=0)
        commentsDataFrame = pd.read_csv(f'{self.directory}/All_CommentsDataFrame.csv',index_col=0)
        return {
            "subreddits": subredditsDataFrame,
            "submissions": submissionsDataFrame,
            "comments": commentsDataFrame,
        }

    def createHumanReadableCSVs(self, dataframeDict: dict):
        
        csvFile = open(f'{self.directory}.csv','w',encoding='utf-8',newline='')
        csvWriter = csv.writer(csvFile)
        
        for subredditIndex, subreddit in dataframeDict['subreddits'].iterrows():
            currentSubreddit = [["---- New Subreddit ----"]]
            currentSubreddit.append(CSV_subreddit_headers)
            currentSubreddit.append([subreddit['Name'], subreddit['Description'], subreddit['Subscribers'], subreddit['Created']])
            print(currentSubreddit)
            # csvWriter.writerows(currentSubreddit)
            subreddit_mask = dataframeDict['submissions']['Subreddit_ID'].isin([subreddit['ID']])
            subredditSubmissions = dataframeDict["submissions"][subreddit_mask]
            
            for submissionIndex, submission in subredditSubmissions.iterrows():
                currentSubmission = []
                currentSubmission.append(CSV_subreddit_headers)
                currentSubmission.append([submission['Title'], submission['Content'], submission['Author'], submission['Score'], submission['Created']])
                print(f'printing Submission: {currentSubmission}')
                # csvWriter.writerows(currentSubmission)
                submission_mask = dataframeDict['comments']['Parent_ID'].isin([submission['ID']])
                submissionComments = dataframeDict["comments"][submission_mask]
                for commentIndex, comment in submissionComments.iterrows():
                    newline = self.print_children(dataframeDict['comments'], comment, [])
                    csvWriter.writerows(newline)

    def print_children(self, comment_df, comment, current_line):
        #check to see if its an end node - if so then no need to continue deeper
        current_line.append([comment['Content'],comment['Author'],comment['Score'],comment['Created']])
        commentmask = comment_df['Parent_ID'].isin([comment['ID']])
        if commentmask:
            #continue the loop
            childrenCommentDF = comment_df[commentmask]
            for commentIndex, comment in childrenCommentDF:
                self.print_children(comment_df, comment, current_line)
           
        else:
            #we are at the end the comment thread and need to print out the line
            return current_line
        
        

        # def linemaker(currentComment: Comments, commentMap: defaultdict, currentLine: list):
        #     currentLine.append(currentComment.content)
        #     if commentMap.get(currentComment.id) is None:
        #         csvWriter.writerow(currentLine)
                
        #     else:
        #         # print(len(commentMap.get(currentComment.id)))
        #         for comment in commentMap.get(currentComment.id):
        #             linemaker(comment, commentMap, currentLine)

        #     currentLine.pop()
            
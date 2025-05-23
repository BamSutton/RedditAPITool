import os
from datetime import datetime
from pandas import DataFrame

class FileCreator:
    """
    This is the class that creates and reads all of the files that are used by this application.
    It creates the directories that the files are saved in based off the current Date and Time that the app was run.
    This will save all of the dataframes to csv files with the given name to that directory.
    """    
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

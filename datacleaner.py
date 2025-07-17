import pandas as pd
import shutil
from FileCreator import FileCreator
    
def replace_tabs_with_spaces(input_filepath, output_filepath, num_spaces_per_tab=4):
    try:
        with open(input_filepath, 'r') as infile:
            content = infile.read()

        # Replace all tab characters ('\t') with the specified number of spaces
        modified_content = content.replace('\t', ' ' * num_spaces_per_tab)

        with open(output_filepath, 'w') as outfile:
            outfile.write(modified_content)

        print(f"Tabs replaced with spaces successfully. Output saved to: {output_filepath}")

    except FileNotFoundError:
        print(f"Error: The file '{input_filepath}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

file = FileCreator()
file.load_most_recent_run_directory()
directory = file.directory

shutil.copy2(f"{directory}/All_SubredditsDataFrame.csv", "Old_All_SubredditsDataFrame.csv")
shutil.copy2(f"{directory}/All_SubmissionsDataFrame.csv", "Old_All_SubmissionsDataFrame.csv")
shutil.copy2(f"{directory}/All_CommentsDataFrame.csv", "Old_All_CommentsDataFrame.csv")

replace_tabs_with_spaces("Old_All_SubredditsDataFrame.csv", f"{directory}/All_SubredditsDataFrame.csv", num_spaces_per_tab=4)
replace_tabs_with_spaces("Old_All_SubmissionsDataFrame.csv", f"{directory}/All_SubmissionsDataFrame.csv", num_spaces_per_tab=4)
replace_tabs_with_spaces("Old_All_CommentsDataFrame.csv", f"{directory}/All_CommentsDataFrame.csv", num_spaces_per_tab=4)

subredditsDataFrame = pd.read_csv(f'{directory}/All_SubredditsDataFrame.csv', index_col=0)
submissionsDataFrame = pd.read_csv(f'{directory}/All_SubmissionsDataFrame.csv', index_col=0)
commentsDataFrame = pd.read_csv(f'{directory}/All_CommentsDataFrame.csv', index_col=0)

file.save_dataframe(subredditsDataFrame, 'All_Subreddits')
file.save_dataframe(submissionsDataFrame, 'All_Submissions')
file.save_dataframe(commentsDataFrame, 'All_Comments')
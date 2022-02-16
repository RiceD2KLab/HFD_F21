import pandas as pd
import os
import glob
 
def stack_datasets(folder_directory,extension):
    """
    Takes a folder directory and extension for desired file type as input and 
    outputs a concatenated file of all of the files in the given folder. 
    """
    all_data = []
    for file in glob.iglob(f'{directory}/*.{extension}'):
        all_data.append(pd.read_csv(file))

    df = pd.concat(all_data, ignore_index=True)
    df.to_csv(f'{directory}/ConcatenatedData.{extension}', index = False)

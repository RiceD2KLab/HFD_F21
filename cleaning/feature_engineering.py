import pandas as pd

full_data = pd.read_csv('full_merge_withincident.csv')

def add_binary_feature(data, col_name, feat):
    """
    Given a column from a dataframe, create a binary feature based on whether or not each row in the column is empty.
   
    data: pandas dataframe, contains column to be analyzed
    col_name: string, name of column in data to be analyzed
    feat: string, name of binary feature to be added to data

    Returns data with feat added as a column. Row values in feat are either 0 or 1 based on if the column col_name is empty or not.
    """

    binaries = []
    empty_status = data[col_name].isnull()

    for idx, val in empty_status.iteritems():
        if val == True:
            binaries.append(0)
        
        else:
            binaries.append(1)
    
    data[feat] = binaries 

    return data

#full_data =  add_binary_feature(full_data, 'INSPTYPE', 'InspectionStatus')
#full_data.to_csv('Full Merged Data with Binary.csv')


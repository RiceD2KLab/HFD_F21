import pandas as pd
from ast import literal_eval
from numpy import nan

# PART 1: BINARY VARIABLES

#full_data = pd.read_csv('full_merge_withincident.csv')

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

# PART 2: TOTAL COUNT COLUMNS

full_data = pd.read_csv('Full_Merged_Data_with_Binary.csv')

# Create Column of Total Number of Inspections
print(full_data.dtypes)

full_data['Total_Inspections'] = full_data['INSPTYPE'].apply(lambda x: len(literal_eval(x)) if type(x)!=float else 0)

# Create Column of Total Number of Incidents

full_data['Total_Incidents'] = full_data['Basic Incident Number (FD1)'].apply(lambda x: len(literal_eval(x)) if type(x)!=float else 0)

# Create Column of Total Number of Violations

#full_data['Total_Violations'] = full_data['VIOLATIONCode'].apply(lambda x: len(literal_eval(x)) if type(x)!=float else 0)

full_data['Total_Violations'] = full_data['VIOLATIONCode'].apply(
   lambda x: sum(1 for list_item in eval(x) if type(list_item)!=float) if type(x)!=float else 0)

full_data.to_csv('Full_Merged_Data_Binaries_Totals.csv')

##Extract statistics for inspection data
inspection = pd.read_csv("INFOR_2018_2021_pk.csv")
inspec_num = len(inspection["Inspection #"].unique())
# print(inspec_num)
inspection.drop_duplicates(inplace=True)
# print(len(inspection.index))
cols = ["Inspection Type", "Application Type", "Result", "Section", "Team"]
dfs = []
for col in cols:
    inspection[col] = inspection[col].str.strip().replace("", "N/A").fillna("N/A")
    dfs.append(inspection[col].value_counts().append(pd.Series([inspec_num], index=[col])))
df = pd.concat(dfs)
df.to_csv("Inspection_features.csv")

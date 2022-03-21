import codecs
import pandas as pd
from ast import literal_eval
import numpy as np
from numpy import NaN, nan
import re
from statistics import mode

# BINARY VARIABLES

#full_data = pd.read_csv('full_merge_no_duplicates.csv')

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

"""

# TOTAL COUNT COLUMNS

# Create Column of Total Number of Inspections

full_data['Total_Inspections'] = full_data['INSPTYPE'].apply(lambda x: len(literal_eval(x)) if type(x)!=float else 0)

# Create Column of Total Number of Incidents

full_data['Total_Incidents'] = full_data['Basic Incident Number (FD1)'].apply(lambda x: len(literal_eval(x)) if type(x)!=float else 0)

# Create Column of Total Number of Violations

#full_data['Total_Violations'] = full_data['VIOLATIONCode'].apply(lambda x: len(literal_eval(x)) if type(x)!=float else 0)

full_data['Total_Violations'] = full_data['VIOLATIONCode'].apply(
   lambda x: sum(1 for list_item in eval(x) if type(list_item)!=float) if type(x)!=float else 0)

full_data.to_csv('Full_Merged_Data.csv')

## PART 3: Extract statistics for inspection data

inspection = pd.read_csv("INFOR_2018_2021_pk_2.csv")
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

"""

# RESULT FEATURE

#data = pd.read_csv('Full_Merged_Data.csv')

def feat_recent(data, feature):
    """
    Given a column from a dataframe in which each row is either a list or NaN, 
    edit the column so that each row contains either the last entry in the list or NaN.
   
    data: pandas dataframe, contains column to be analyzed
    feature: string, name of feature to be edited

    Returns data with the row values of feature edited to be either the last entry of the list or NaN.
    """

    results = data[feature]
    updated_results = []

    for idx, val in results.iteritems():
        if type(val) == float:
            updated_results.append(val)

        else:
            new_res = literal_eval(val)[-1]
            updated_results.append(new_res.replace(' ', ''))

    data[feature] = updated_results

    return data

#df = feat_recent(data, 'Result')
#df.to_csv('Full_Merged_Data_ZS.csv')

# BUILDING CODE VARIABLE

#data = pd.read_csv('Full_Merged_Data_ZS.csv')

def feat_building_code(data):
    """
    Input: Merged Property Dataset
    Output: Merged Property Dataset with new categorical column of the INFOR building category for each 
    property (row) based on the Basic Property Use Code And Description (FD1.46) column.
    """
    property_col = data.loc[:,'Basic Property Use Code And Description (FD1.46)']

    code_list=[]
    for row in property_col:
        property_codes=[]
        if type(row) != float:
            for item in literal_eval(row):
                if len(re.findall("\d+", item))!=0:
                    code = int(re.findall("\d+", item)[0])
                    property_codes.append(code)
            if len(property_codes) != 0:
                code = mode(property_codes)
            else:
                code = 0
        else:
            code=0
        code_list.append(code)

    building_category=[]
    for code in code_list:
        first_digit = int(str(code)[0])
        if first_digit==0:
            building_category.append("Unknown")
        elif first_digit==1:
            building_category.append("Assembly")
        elif first_digit==2:
            building_category.append("Educational")
        elif first_digit==3:
            building_category.append("Health Care, Detention, and Correction")
        elif first_digit==4:
            building_category.append("Residential")
        elif first_digit==5:
            building_category.append("Mercantile, Business")
        elif first_digit==6:
            building_category.append("Industrial, Utility, Defense, Agriculture, Mining")
        elif first_digit==7:
            building_category.append("Manufacturing, Processing")
        elif first_digit==8:
            building_category.append("Storage")
        elif first_digit==9:
            building_category.append("Outside or Special Property")

    data['Property_Code']=building_category

#feat_building_code(data)
#data.to_csv('Full_Merged_Data_TC.csv')
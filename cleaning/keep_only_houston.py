from numpy import row_stack
import pandas as pd

data = pd.read_csv('Full_mergeData.csv')

address_list = data['STADDRESS_x']

for row in address_list:
    if type(row)!=float:
        address_components = str.split(row)
        if 'HOUSTON' not in address_components:
            data.drop(data[data['STADDRESS_x'] == row].index, inplace=True)


data.to_csv('Full_Merged_Data_Houston.csv')



'''
This file is used to aggregate the INFOR data that was has been provided over common placekeys.
The file also drops columns that are unnecessary to our final model, and modifies some entries to common formats.

The merged dataset is then outputted to be observed and viewed.
'''

import pandas as pd

# Read the existing INFOR data with placekeys into a dataframe.
df = pd.read_csv('Valid_INFOR_2018_2021.csv_1.csv')

# Drop unnecessary rows from the dataframe.
df = df.drop(['Inspection #','#','A/P #','Rinspection Date','Scheduled','Completed','Assigned To','Assigned To (Name)','Assigned To Provider','Location','Schedule Order','Unnamed: 18'],axis=1)

# Cleaning values for section
df['Section'] = df['Section'].replace(to_replace = 'School', value ='SCH/INS') # Combine school codes into one
df['Section'] = df['Section'].replace(to_replace = ' ', value ='GO') # Identify blank entries as general occupancy
df['Section'] = df['Section'].fillna(value ='GO') # Identify blank entries as general occupancy

# Convert recorded dates from strings to dates
df['Processed / Last Inspected'] = pd.to_datetime(df['Processed / Last Inspected'], format='%m/%d/%Y %H:%M')

# Aggregate the data by unique placekey
grouped_df = df.groupby('PlaceKey ID').agg(lambda x: list(x))

# Take the first address, rather than a repeating list
for x in range(len(grouped_df["Address"])):
    grouped_df["Address"][x] = grouped_df["Address"][x][0]

# Export the aggregated dataframe
grouped_df.to_csv(r'AggregatedINFOR.csv')
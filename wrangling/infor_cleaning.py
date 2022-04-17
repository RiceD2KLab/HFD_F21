'''
This file is used to aggregate the INFOR data that was has been provided over common placekeys.
The file also drops columns that are unnecessary to our final model, and modifies some entries to common formats.

The merged dataset is then outputted to be observed and viewed.
'''
import os.path

import pandas as pd

import data_io as io

if __name__ == "__main__":
  # Read the existing INFOR data with placekeys into a dataframe.
  infor_dir = os.path.normpath("Data/INFOR Inspection Data")
  df = pd.read_csv(
    os.path.join(infor_dir, "Intermediate Datasets",
                 "INFOR_2018_2021_pk_2.csv"), index_col=0)

  # Drop unnecessary rows from the dataframe.
  df = df.drop(
    ['Inspection #', '#', 'A/P #', 'Rinspection Date', 'Scheduled', 'Completed',
     'Assigned To', 'Assigned To (Name)', 'Assigned To Provider', 'Location',
     'Schedule Order', 'Unnamed: 18'], axis=1)

  # Cleaning values for section
  df['Section'] = df['Section'].replace(to_replace='School',
                                        value='SCH/INS')  # Combine school codes into one
  df['Section'] = df['Section'].replace(to_replace=' ',
                                        value='GO')  # Identify blank entries as general occupancy
  df['Section'] = df['Section'].fillna(
    value='GO')  # Identify blank entries as general occupancy

  # Aggregate the data by unique placekey
  grouped_df: pd.DataFrame = df.groupby('PlaceKey ID').agg(lambda x: list(x))

  # Take the first address, rather than a repeating list
  for x in range(len(grouped_df["Address"])):
    grouped_df["Address"][x] = grouped_df["Address"][x][0]

  # Export the aggregated dataframe
  io.output_to_csv(grouped_df, "AggregatedINFOR.csv")

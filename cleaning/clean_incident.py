import os.path

import pandas as pd

from cleaning.data_wrangling import output_to_csv


def clean_incident(incident_data: pd.DataFrame) -> pd.DataFrame:
  """
  Clean the incident data ('Non-Residential_Incident_pk_2018_2021.csv') by dropping the irrelevant columns
  and replacing the fill values with 'NNN - None'.

  Input: filenames as string type
  Output: cleaned incident data as cvs file
  """
  # drop irrelevant columns
  incident_data = incident_data.drop(labels=['Unnamed: 0',
                                             'Basic Incident Number (FD1)',
                                             'Basic EFD Card Number (FD1.84)',
                                             'Basic Incident Full Street Address',
                                             'Basic Apparatus Call Sign List',
                                             'Basic Property Pre-Incident Value (FD1.37)',
                                             'Basic Property Losses (FD1.35)',
                                             'Apparatus Resource Primary Action Taken Code And Description (FD18.9)'],
                                     axis=1)

  # fill the NaN data in Basic Property Use/Incident Type/Primary Action Taken Code And Desciption with 'NNN - None'
  incident_data[['Basic Property Use Code And Description (FD1.46)',
                 'Basic Incident Type Code And Description (FD1.21)',
                 'Basic Primary Action Taken Code And Description (FD1.48)'
                 ]] = incident_data[
    ['Basic Property Use Code And Description (FD1.46)',
     'Basic Incident Type Code And Description (FD1.21)',
     'Basic Primary Action Taken Code And Description (FD1.48)']].fillna(
    'NNN - None')

  # check the number of unique PlaceKey ID
  num = incident_data.nunique()

  # group the data on PlaceKey ID
  incident_data = incident_data.groupby('PlaceKey ID').agg(lambda x: list(x))
  return incident_data


if __name__ == "__main__":
  incident_dir = os.path.normpath("Data/Incident Data")
  data = pd.read_csv(os.path.join(incident_dir, "Intermediate Datasets",
                                  "Non-Residential_Incident_2018_2021_pk.csv"))

  output_to_csv(clean_incident(data), "cleaned_incident_data")

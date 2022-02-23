from typing import Iterable, Dict

import pandas as pd

# compile address & violation record data for 2020 & 2021
from cleaning.data_wrangling import filter_rows, filter_null

av2020 = pd.read_csv('data/sp22data/Address_&_Violation_Records_data 2020.csv')
av2021 = pd.read_csv('data/sp22data/Address_&_Violation_Records_data 2021.csv')

av2021 = av2021.drop('STARTDTTM', axis=1)

# compile incident data
inc_full2021 = pd.read_csv('data/sp22data/FF--D2K-2021-data_full year 2021.csv')
inc_2018_2021 = pd.read_csv(
  'data/sp22data/D2K Incident Data July 2018 to JAug 10 2021_Export.csv')

inc_2018_2021 = inc_2018_2021.rename({
  'Apparatus Resource Primary Action Taken Code And Description (FD18.9)':
    'Basic Primary Action Taken Code And Description (FD1.48)'})

# stacked address & violation data
address_violation_full = pd.concat([av2020, av2021]).drop_duplicates()

# stacked incident data
incident_full = pd.concat([inc_full2021, inc_2018_2021]).drop_duplicates()

# remove residential rows from incident data
clean_incident = filter_rows(
  incident_full,
  {
    'Basic Property Use Code And Description (FD1.46)':
      ['419 - 1 or 2 family dwelling', 419]
  })
clean_incident.to_csv('Non-Residential Incident Data 2018_2021.csv')

# remove rows with empty address component fields from Address and Violation Data
cleaned_address_violation = filter_null(
  address_violation_full,
  ['STATE', 'STNO', 'CITY', 'STNAME', 'ZIP'])
cleaned_address_violation.to_csv(
  'Cleaned Address and Violation Data 2020_2021.csv')

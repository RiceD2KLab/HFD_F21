import os
from typing import Iterable, Dict

import pandas as pd

# compile address & violation record data for 2020 & 2021
from cleaning.data_wrangling import filter_rows, filter_null


if __name__ == "__main__":
  # compile incident data
  incident_dir = os.path.normpath("Data/Incident Data/Original Datasets")
  inc_full2021 = pd.read_csv(
    os.path.join(incident_dir, "FF--D2K-2021-data_full year 2021.csv"))
  inc_2018_2021 = pd.read_csv(os.path.join(incident_dir,
                                           "D2K Incident Data July 2018 to JAug 10 2021_Export.csv"))

  inc_2018_2021 = inc_2018_2021.rename({
    'Apparatus Resource Primary Action Taken Code And Description (FD18.9)':
      'Basic Primary Action Taken Code And Description (FD1.48)'})

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

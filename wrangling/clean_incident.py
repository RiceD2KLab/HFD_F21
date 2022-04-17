"""

"""
import os.path
from typing import List

import pandas as pd

import wrangling
import data_io as io
import placekey_tagging

INCIDENT_DIR = os.path.normpath("Data/Incident Data")
INCIDENT_ORIG_DIR = os.path.join(INCIDENT_DIR, io.ORIG_DIR)
INCIDENT_INTER_DIR = os.path.join(INCIDENT_DIR, io.INTER_DIR)
INCIDENT_CLEAN_DIR = os.path.join(INCIDENT_DIR, io.CLEAN_DIR)


def clean_incident(incident_data: List[pd.DataFrame],
                   intermediate_output=False,
                   intermediate_output_dir=INCIDENT_INTER_DIR) -> pd.DataFrame:
  """
  Prepare HFD incident data for merging by dropping unnecessary columns,
  filling empty code fields with "None", filtering out single-family homes,
  tagging the data with PlaceKeys and grouping the data by said placekeys.

  The incident dataset(s) should have the following columns:
    Basic Incident Number (FD1)
    Basic EFD Card Number (FD1.84)
    Basic Incident Full Street Address
    Basic Incident Full Address
    Basic Property Use Code And Description (FD1.46)
    Basic Apparatus Call Sign List
    Basic Incident Date Time
    Basic Property Pre-Incident Value (FD1.37)
    Basic Property Losses (FD1.35)
    Basic Incident Type Code And Description (FD1.21)
    Basic Primary Action Taken Code And Description (FD1.48)

  Input: filenames as string type
  Output: cleaned incident data as cvs file
  """
  # concatenate datasets, dropping unnecessary columns
  drop_cols = [
    'Basic Incident Number (FD1)',
    'Basic EFD Card Number (FD1.84)',
    'Basic Incident Full Street Address',
    'Basic Apparatus Call Sign List',
    'Basic Property Pre-Incident Value (FD1.37)',
    'Basic Property Losses (FD1.35)',
    'Apparatus Resource Primary Action Taken Code And Description (FD18.9)']
  incident_full = wrangling.compile_datasets(incident_data,
                                             filter_cols=drop_cols)

  # Fill the NaN data in Basic Property Use/Incident Type/Primary Action Taken
  # Code And Description with 'NNN - None'
  incident_full[['Basic Property Use Code And Description (FD1.46)',
                 'Basic Incident Type Code And Description (FD1.21)',
                 'Basic Primary Action Taken Code And Description (FD1.48)'
                 ]] = incident_full[
    ['Basic Property Use Code And Description (FD1.46)',
     'Basic Incident Type Code And Description (FD1.21)',
     'Basic Primary Action Taken Code And Description (FD1.48)']].fillna(
    'NNN - None')

  # Remove residential rows from incident data
  property_type_col = "Basic Property Use Code And Description (FD1.46)"
  incident_full = wrangling.filter_rows(
    incident_full,
    {
      property_type_col: ['419 - 1 or 2 family dwelling', '419']
    })

  if intermediate_output:
    filename = "Non-Residential Incident 2018_2021"
    io.output_to_csv(incident_full,
                     os.path.join(intermediate_output_dir, filename),
                     keep_index=False)

  # Placekey Tagging
  address_col = "Basic Incident Full Address"
  incident_full = wrangling.filter_null(incident_full, [address_col])
  incident_placekey = placekey_tagging.gen_placekey_from_address(incident_full,
                                                                 address_col)

  with_placekey, without_placekey = placekey_tagging.split_placekey(
    incident_placekey)

  if intermediate_output:
    with_pk_name = "Non-Residential Incident 2018_2021 Placekey"
    without_pk_name = "Non-Residential Incident 2018_2021 No Placekey"
    io.output_to_csv(with_placekey,
                     os.path.join(intermediate_output_dir, with_pk_name))
    io.output_to_csv(without_placekey,
                     os.path.join(intermediate_output_dir, without_pk_name))

  # group the data on PlaceKey ID
  with_placekey = with_placekey.groupby(
    placekey_tagging.PLACEKEY_FIELD_NAME).agg(lambda x: list(x))
  return with_placekey


if __name__ == "__main__":
  # Read in files
  inc_full2021 = pd.read_csv(
    os.path.join(INCIDENT_ORIG_DIR, "FF--D2K-2021-data_full year 2021.csv"))
  inc_2018_2021 = pd.read_csv(
    os.path.join(INCIDENT_ORIG_DIR,
                 "D2K Incident Data July 2018 to JAug 10 2021_Export.csv"))

  # Rename a column so that the datasets can be concatenated properly
  inc_2018_2021 = inc_2018_2021.rename({
    'Apparatus Resource Primary Action Taken Code And Description (FD18.9)':
      'Basic Primary Action Taken Code And Description (FD1.48)'})

  # Perform cleaning, output to CSV
  inc_clean = clean_incident([inc_2018_2021, inc_full2021])
  io.output_to_csv(inc_clean,
                   os.path.join(INCIDENT_CLEAN_DIR,
                                "Cleaned Incident Data"))

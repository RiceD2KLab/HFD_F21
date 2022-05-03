"""
This file is used to aggregate the INFOR data that was has been provided over common placekeys.
The file also drops columns that are unnecessary to our final model, and modifies some entries to common formats.

The merged dataset is then output to be observed and viewed.
"""
import os.path
from typing import List

import pandas as pd

import data_io
import data_io as io
import wrangling
import placekey_tagging as pk

INFOR_DIR = os.path.normpath("Data/INFOR Inspection Data")
INFOR_ORIG_DIR = os.path.join(INFOR_DIR, io.ORIG_DIR)
INFOR_INTER_DIR = os.path.join(INFOR_DIR, io.INTER_DIR)
INFOR_CLEAN_DIR = os.path.join(INFOR_DIR, io.CLEAN_DIR)


def clean_infor(infor_data: List[pd.DataFrame], intermediate_output: bool = True,
                intermediate_output_dir: str = INFOR_INTER_DIR) -> pd.DataFrame:
  """
  Prepare HFD INFOR inspection data for merging by compiling a number of
  datasets, dropping unnecessary columns in the data, and grouping the data by
  location using PlaceKeys.

  The INFOR datasets should have the following columns to be present after
  they are cleaned and tagged:
    | PlaceKey ID
    | Inspection Type
    | Application Type
    | Result
    | Section
    | Team
    | Address
    | Processed / Last Inspected

  :param infor_data: list of INFOR datasets to be compiled and cleaned
  :param intermediate_output: whether to output extra CSV files at
    intermediate steps
  :param intermediate_output_dir: directory to output intermediate CSV files
  :return: a single DataFrame containing the cleaned and compiled INFOR data
  """

  to_drop = ['Inspection #', '#', 'A/P #', 'Rinspection Date', 'Scheduled',
             'Completed', 'Assigned To', 'Assigned To (Name)',
             'Assigned To Provider', 'Location', 'Schedule Order']

  # Compile datasets
  compiled_infor = wrangling.compile_datasets(infor_data, to_drop)
  compiled_infor = wrangling.trim_string_fields(compiled_infor)
  compiled_infor.dropna(axis="columns", how="all", inplace=True)

  if intermediate_output:
    compiled_filename = "Concatenated Infor Data"
    io.output_to_csv(compiled_infor,
                     os.path.join(intermediate_output_dir, compiled_filename))

  # Cleaning values for section
  # Combine school codes into one
  section_col = "Section"
  compiled_infor.replace({section_col: {"School": "SCH/INS"}}, inplace=True)
  print(list(compiled_infor.columns))

  # Identify blank entries as general occupancy
  compiled_infor.replace({section_col: {"": "GO"}}, inplace=True)
  compiled_infor.fillna(value={section_col: "GO"}, inplace=True)
  print(list(compiled_infor.columns))

  # PlaceKey tagging
  addr_col = "Address"
  compiled_infor = wrangling.filter_null(compiled_infor, [addr_col])
  compiled_infor = pk.gen_placekey_from_address(compiled_infor, addr_col)
  print(list(compiled_infor.columns))

  with_pk, without_pk = pk.split_placekey(compiled_infor)
  if intermediate_output:
    with_pk_out = "INFOR Data with Placekey"
    without_pk_out = "INFOR Data without Placekey"
    io.output_to_csv(with_pk,
                     os.path.join(intermediate_output_dir, with_pk_out))
    io.output_to_csv(without_pk,
                     os.path.join(intermediate_output_dir, without_pk_out))

  with_pk: pd.DataFrame = with_pk.groupby(pk.PLACEKEY_FIELD_NAME).agg(list)

  # Take first address, rather than a repeating list
  with_pk[addr_col] = with_pk[addr_col].apply(lambda x: x[0])
  return with_pk


if __name__ == "__main__":
  # Read the existing INFOR data with placekeys into a dataframe.
  all_infor = data_io.read_all_dir_entries_csv(INFOR_ORIG_DIR)
  cleaned_infor_data = clean_infor(all_infor)

  # Export the aggregated dataframe
  io.output_to_csv(cleaned_infor_data,
                   os.path.join(INFOR_CLEAN_DIR, "AggregatedINFOR.csv"))

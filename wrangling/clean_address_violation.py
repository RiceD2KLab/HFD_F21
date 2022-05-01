"""

"""
import os
import data_io as io
from typing import List

import pandas as pd

import wrangling
import placekey_tagging
import location_processing as locations

AV_DIR = os.path.normpath("Data/Address and Violation Records Data")
AV_ORIG_DIR = os.path.join(AV_DIR, io.ORIG_DIR)
AV_INTER_DIR = os.path.join(AV_DIR, io.INTER_DIR)
AV_CLEAN_DIR = os.path.join(AV_DIR, io.CLEAN_DIR)


def aggregate_av_address_fields(data: pd.DataFrame,
                                address_col_name: str) -> pd.DataFrame:
  """
  Concatenates the address columns into one column `address_col_name` with space
  between each column entry, deleting the original address fields.

  This method requires the input dataframe to have the following address-based
  columns:
    "STNO", "STNAME", "SUFFIX", "CITY", "STATE", "ZIP"

  Input:
    data: a DataFrame representing the input dataset
    address_col_name: the name of the new addresss column
  Return: the input DataFrame, with a concatenated address column
  """

  aggregation_cols = ['STNO', 'STNAME', 'SUFFIX', "CITY", "STATE", "ZIP"]
  na_replacements = {"SUFFIX": "", "ZIP": "", "STATE": "", "CITY": ""}

  return locations.coalesce_address(data, new_addr_col=address_col_name,
                                    ordered_aggregation_cols=aggregation_cols,
                                    na_replacements=na_replacements,
                                    zip_col="ZIP")


def clean_address_violation(
    av_data: List[pd.DataFrame],
    intermediate_output: bool = False,
    intermediate_output_dir: str = AV_INTER_DIR) -> pd.DataFrame:
  """

  :param av_data:
  :param intermediate_output:
  :param intermediate_output_dir:
  :return:
  """

  # Initial processing
  av_full = wrangling.compile_datasets(av_data, ["STARTDTTM"])
  av_full = wrangling.filter_null(av_full,
                                  ["STATE", "STNO", "CITY", "STNAME", "ZIP"])

  if intermediate_output:
    cleaned_name = "Cleaned Address and Violation Data 2020_2021"
    io.output_to_csv(av_full,
                     os.path.join(intermediate_output_dir, cleaned_name))
    io.output_to_pkl(av_full,
                     os.path.join(intermediate_output_dir, cleaned_name))

  # Address field aggregation
  address_col = "STADDRESS"
  av_placekey = placekey_tagging.gen_placekey_from_address(
    aggregate_av_address_fields(av_full, address_col),
    address_col)

  # Placekey tagging
  with_placekey, without_placekey = placekey_tagging.split_placekey(av_placekey)

  if intermediate_output:
    with_pk_name = "Cleaned Address and Violation Data 2020_2021 Placekey Test"
    without_pk_name = "Cleaned Address and Violation Data 2020_2021 No Placekey Test"
    io.output_to_csv(with_placekey,
                     os.path.join(intermediate_output_dir, with_pk_name))
    io.output_to_csv(without_placekey,
                     os.path.join(intermediate_output_dir, without_pk_name))

  # Drop Irrelevant cols
  with_placekey = with_placekey.drop(
    labels=["APNO", "APUSEINSPKEY", "COMPDTTM", "DESCRIPT",
            "Remove Duplication", "Code", "FULLNAME", "GPSX", "GPSY", "GPSZ",
            "INSPTYPECAT", "LOC", "Location", "Number of Records",
            "OCCUPANCYTYPE", "PREDIR", "RESULTBY", "RESULTDTTM", "RESULT",
            "SCHEDDTTM", "SUBDIVDESC", "SUPERVISOR", "TEAMDESCRIPTION",
            "ViolationStatus", "WORKTYPE"], axis=1)

  with_placekey = with_placekey.groupby(
    placekey_tagging.PLACEKEY_FIELD_NAME).agg(lambda x: list(x))

  with_placekey = wrangling.get_only_first_elem(with_placekey, "STADDRESS")
  return with_placekey


if __name__ == "__main__":
  # Read in files
  av2020 = pd.read_csv(
    os.path.join(AV_ORIG_DIR, "Address_&_Violation_Records_data 2020.csv"))
  av2021 = pd.read_csv(
    os.path.join(AV_ORIG_DIR, "Address_&_Violation_Records_data 2021.csv"))

  # Perform cleaning, output to CSV
  cleaned_av_data = clean_address_violation([av2020, av2021])
  io.output_to_csv(
    cleaned_av_data,
    os.path.join(AV_CLEAN_DIR, "Address and Violation Data by Property_Test"))

import os.path
from typing import List

import pandas as pd

from cleaning.data_wrangling import output_to_csv, filter_rows, \
  trim_string_fields, compile_datasets

BLD_RES_STATE_CLASS = "property_use_cd"
REAL_ACCT_STATE_CLASS = "state_class"


def filter_single_family(properties: pd.DataFrame,
                         filter_col: str) -> pd.DataFrame:
  """
  Filter aut rows that are not large-scale establishments, such as single-family homes, from a dataframe.
  Args:
    properties: A DataFrame containing the properties to be ignored.

  Returns:
    the filtered DataFrame
  """
  unnecessary_vals = {filter_col: ["A1", "A2", "B2", "B3"]}
  return filter_rows(properties, unnecessary_vals)


def merge_all_building_info(properties: pd.DataFrame,
                            non_residential: pd.DataFrame,
                            residential: pd.DataFrame) -> pd.DataFrame:
  # Compile residential, nonresidential datasets into single dataframe
  keep_cols = ["bld_num", "impr_mdl_cd", "date_erected", "yr_remodel", "dscr",
               "act_ar", "tot_inc"]

  residential["tot_inc"] = 0
  non_residential = non_residential[keep_cols]
  residential = residential[keep_cols]
  building_data = compile_datasets([non_residential, residential])

  # Inner join structure data with real property data
  return pd.merge(properties, building_data, on="acct", how="left")


def preprocess_hcad_data(filename: str, cols_to_keep: List[str] = None,
                         groupby: bool = True) -> pd.DataFrame:
  """
  Preprocess HCAD DataFrames
  :param filename:
  :return:
  """
  # Read in original DataFrame
  df = pd.read_csv(filename, delimiter="\t", encoding="utf-8",
                   encoding_errors='ignore')

  if cols_to_keep is not None:
    df = df[cols_to_keep]

  if groupby:
    # Group by account number
    df = df.groupby("acct").agg(list)

  # Trim and return
  return trim_string_fields(df)


if __name__ == "__main__":
  # import HCAD data - "buildings" (non-residential properties) and "all_properties"
  hcad_path = os.path.normpath("Data/Public Data/HCAD/Original Datasets")

  # Read in non-residential building data
  bld_other_cols_to_keep = ["acct", "bld_num", "impr_mdl_cd", "date_erected",
                            "yr_remodel", "dscr", "act_ar", "tot_inc"]
  bld_other = preprocess_hcad_data(
    os.path.join(hcad_path, "building_other.txt"),
    cols_to_keep=bld_other_cols_to_keep)

  # Read in residential building data
  bld_res_cols_to_keep = ["acct", BLD_RES_STATE_CLASS, "bld_num", "impr_mdl_cd",
                          "date_erected", "yr_remodel", "dscr", "act_ar"]
  bld_res = filter_single_family(
    preprocess_hcad_data(os.path.join(hcad_path, "building_res.txt"),
                         cols_to_keep=bld_res_cols_to_keep),
    BLD_RES_STATE_CLASS)

  # Read in parcel data
  all_props_cols_to_keep = ["acct", REAL_ACCT_STATE_CLASS, "site_addr_1",
                            "site_addr_2", "site_addr_3", "tot_appr_val",
                            "bld_ar", "land_ar"]
  all_properties = filter_single_family(
    preprocess_hcad_data(os.path.join(hcad_path, 'real_acct.txt'),
                         groupby=False, cols_to_keep=all_props_cols_to_keep),
    REAL_ACCT_STATE_CLASS)

  output_to_csv(merge_all_building_info(all_properties, bld_other, bld_res),
                "Non-Residential_Properties")

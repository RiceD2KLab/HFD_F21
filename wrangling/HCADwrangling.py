import os.path
from typing import List

import pandas as pd

import location_processing as locations
import wrangling
import data_io as io
import placekey_tagging as pk

BLD_RES_STATE_CLASS = "property_use_cd"
REAL_ACCT_STATE_CLASS = "state_class"

HCAD_DIR = os.path.normpath("Data/Public Data/HCAD")
HCAD_ORIG_DIR = os.path.join(HCAD_DIR, io.ORIG_DIR)
HCAD_INTER_DIR = os.path.join(HCAD_DIR, io.INTER_DIR)
HCAD_CLEAN_DIR = os.path.join(HCAD_DIR, io.CLEAN_DIR)


def filter_single_family(properties: pd.DataFrame,
                         filter_col: str) -> pd.DataFrame:
  """
  Filter aut rows that are not large-scale establishments, such as single-family
  homes, from a dataframe.

  :param properties: A DataFrame containing the properties to be ignored.
  :param filter_col: The column that holds data about the type of property
  :return: the filtered DataFrame
  """
  unnecessary_vals = {filter_col: ["A1", "A2", "B2", "B3"]}
  return wrangling.filter_rows(properties, unnecessary_vals)


def merge_all_building_info(properties: pd.DataFrame,
                            non_residential: pd.DataFrame,
                            residential: pd.DataFrame) -> pd.DataFrame:
  # Compile residential, nonresidential datasets into single dataframe
  keep_cols = ["bld_num", "impr_mdl_cd", "date_erected", "yr_remodel", "dscr",
               "act_ar", "tot_inc"]

  residential["tot_inc"] = 0
  non_residential = non_residential[keep_cols]
  residential = residential[keep_cols]
  building_data = wrangling.compile_datasets([non_residential, residential])

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
                   encoding_errors='ignore')[:100]

  if cols_to_keep is not None:
    df = df[cols_to_keep]

  if groupby:
    # Group by account number
    df = df.groupby("acct").agg(list)

  # Trim and return
  return wrangling.trim_string_fields(df)


def clean_hcad_data(
    real_acct_path: str,
    building_res_path: str,
    building_other_path: str,
    intermediate_output: bool = True,
    intermediate_output_dir: str = HCAD_INTER_DIR) -> pd.DataFrame:
  # Read in parcel data
  all_props_cols_to_keep = ["acct", REAL_ACCT_STATE_CLASS, "site_addr_1",
                            "site_addr_2", "site_addr_3", "tot_appr_val",
                            "bld_ar", "land_ar"]
  all_properties = filter_single_family(
    preprocess_hcad_data(real_acct_path,
                         groupby=False, cols_to_keep=all_props_cols_to_keep),
    REAL_ACCT_STATE_CLASS)

  # Read in non-residential building data
  bld_other_cols_to_keep = ["acct", "bld_num", "impr_mdl_cd", "date_erected",
                            "yr_remodel", "dscr", "act_ar", "tot_inc"]
  bld_other = preprocess_hcad_data(building_other_path,
                                   cols_to_keep=bld_other_cols_to_keep)

  # Read in residential building data
  bld_res_cols_to_keep = ["acct", BLD_RES_STATE_CLASS, "bld_num", "impr_mdl_cd",
                          "date_erected", "yr_remodel", "dscr", "act_ar"]
  bld_res = filter_single_family(
    preprocess_hcad_data(building_res_path,
                         cols_to_keep=bld_res_cols_to_keep),
    BLD_RES_STATE_CLASS)

  if intermediate_output:
    building_res_filename = os.path.splitext(
      os.path.split(building_res_path)[-1])[0]
    building_other_filename = os.path.splitext(
      os.path.split(building_other_path)[-1])[0]
    real_acct_filename = os.path.splitext(
      os.path.split(building_res_path)[-1])[0]

    io.output_to_csv(all_properties,
                     os.path.join(intermediate_output_dir, real_acct_filename))
    io.output_to_csv(bld_other,
                     os.path.join(intermediate_output_dir,
                                  building_other_filename))
    io.output_to_csv(bld_res,
                     os.path.join(intermediate_output_dir,
                                  building_res_filename))

  merged_data = merge_all_building_info(all_properties, bld_other, bld_res)

  # Placekey tagging
  address_col = "STADDRESS"
  zip_col = "site_addr_3"
  merged_data["state"] = "TX"
  merged_data[zip_col].replace("", "0")
  merged_data[zip_col].replace(" ", "0")
  merged_data = locations.coalesce_address(
    merged_data, address_col,
    ordered_aggregation_cols=["site_addr_1", "site_addr_2", "state",
                              zip_col],
    na_replacements={"site_addr_1": "", "site_addr_2": "", zip_col: "0"},
    zip_col="site_addr_3"
  )

  hcad_placekey = pk.gen_placekey_from_address(merged_data, address_col)
  with_placekey, without_placekey = pk.split_placekey(hcad_placekey)

  if intermediate_output:
    with_pk_name = "HCAD Data With Placekey"
    without_pk_name = "HCAD Data Without Placekey"
    io.output_to_csv(with_placekey,
                     os.path.join(intermediate_output_dir, with_pk_name))
    io.output_to_csv(without_placekey,
                     os.path.join(intermediate_output_dir, without_pk_name))

  with_placekey = with_placekey.groupby(pk.PLACEKEY_FIELD_NAME).agg(lambda x: list(x)[0])
  return with_placekey


if __name__ == "__main__":
  # import HCAD data - "buildings" (non-residential properties) and "all_properties"
  hcad_path = os.path.normpath("Data/Public Data/HCAD/Original Datasets")

  real_acct = os.path.join(HCAD_ORIG_DIR, "real_acct.txt")
  building_other = os.path.join(HCAD_ORIG_DIR, "building_other.txt")
  building_res = os.path.join(HCAD_ORIG_DIR, "building_res.txt")
  io.output_to_csv(
    clean_hcad_data(real_acct_path=real_acct,
                    building_other_path=building_other,
                    building_res_path=building_res),
    "Non-Residential Properties with Placekey")

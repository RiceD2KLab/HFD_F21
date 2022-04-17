import os.path
from typing import List

import pandas as pd

import wrangling
import placekey_tagging as pk
import data_io as io
import location_processing as locations

FIRE_DIR = os.path.normpath("Data/Structure Fire Data")
FIRE_ORIG_DIR = os.path.join(FIRE_DIR, io.ORIG_DIR)
FIRE_INTER_DIR = os.path.join(FIRE_DIR, io.INTER_DIR)
FIRE_CLEAN_DIR = os.path.join(FIRE_DIR, io.CLEAN_DIR)


def clean_structure_fire(
    fire_data: List[pd.DataFrame],
    intermediate_output=False,
    intermediate_output_dir=FIRE_INTER_DIR) -> pd.DataFrame:
  """
  
  :param fire_data:
  :param intermediate_output:
  :param intermediate_output_dir:
  :return:
  """
  # Define columns to drop from data
  drop_cols = ["incident_id", "alternate_id", "station_id",
               "response_priority_description_final", "nfirs_group_final",
               "nfirs_group_description_final", "nfirs_category_final",
               "nfirs_category_description_final", "city", "county", "zip_code",
               "occurred_on_local_time", "dispatched_on_local_time", "day",
               "month_of_year", "year", "hour_of_day"]

  fire_data = wrangling.compile_datasets(fire_data, drop_cols)
  fire_data = wrangling.filter_rows(
    fire_data, {
      "cancelled": ["true", True],
      "property_type": ["419", "419 - 1 or 2 family dwelling"]
    }).drop("cancelled", axis=1)

  if intermediate_output:
    filename = "Structure Fires 2005-2021 without Single-Family"
    io.output_to_csv(fire_data, os.path.join(intermediate_output_dir, filename))

  # Create coalesced address field for Placekey tagging
  address_fields = ["full_address", "city_lookup",
                    "state_lookup", "zip_code_lookup"]
  new_addr_col = "complete_address"
  na_addr_replacements = {"full_address": "", "city_lookup": "Houston",
                          "state_lookup": "TX", "zip_code_lookup": "0"}
  locations.coalesce_address(fire_data, new_addr_col, address_fields,
                             na_addr_replacements, "zip_code_lookup")

  # Generate PlaceKeys, split
  fire_dataset = pk.gen_placekey_from_address(fire_data, new_addr_col)
  data_with_pk, data_wo_pk = pk.split_placekey(fire_dataset)

  if intermediate_output:
    with_pk_filename = "Structure Fire 2005-2021 PK"
    wo_pk_filename = "Structure Fire 2005-2021 No PK"
    io.output_to_csv(data_with_pk,
                     os.path.join(intermediate_output_dir, with_pk_filename))
    io.output_to_csv(data_wo_pk,
                     os.path.join(intermediate_output_dir, wo_pk_filename))

  # Aggregate placekey data by placekey
  aggregated_data = data_with_pk.groupby([pk.PLACEKEY_FIELD_NAME]).agg(
    lambda x: list(x))

  return aggregated_data


if __name__ == "__main__":
  # Drop above-specified columns, removing any "cancelled" incidents
  fire_dataset = pd.read_csv(
    os.path.join(FIRE_ORIG_DIR, "Structure Fires 2005-2021.csv"))

  # Output updated data to CSV
  io.output_to_csv(clean_structure_fire([fire_dataset]),
                   os.path.join(FIRE_CLEAN_DIR,
                                "Structure Fires 2005-2021 Aggregated with PK"))

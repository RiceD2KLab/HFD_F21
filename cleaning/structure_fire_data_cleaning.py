import sys

import pandas as pd

import cleaning.data_wrangling as wrangling
import placekey_tagging as pk

if __name__ == "__main__":
  # Define columns to drop from data
  drop_cols = ["incident_id", "alternate_id", "station_id",
               "response_priority_description_final", "nfirs_group_final",
               "nfirs_group_description_final", "nfirs_category_final",
               "nfirs_category_description_final", "city", "county", "zip_code",
               "occurred_on_local_time", "dispatched_on_local_time", "day",
               "month_of_year", "year", "hour_of_day"]

  # Drop above-specified columns, removing any "cancelled" incidents
  fire_dataset = pd.read_csv("Structure Fires 2005-2021.csv")

  fire_dataset = wrangling.compile_datasets([fire_dataset], drop_cols)
  fire_dataset = wrangling.filter_rows(
    fire_dataset,
    {"cancelled": ["true", True],
     "property_type": ["419", "419 - 1 or 2 family dwelling"]}).drop(
    "cancelled", axis=1)

  # Replace empty city lookup entries with Houston
  fire_dataset["city_lookup"].fillna("Houston", inplace=True)

  # Remove empty ZIP codes, turn to int
  fire_dataset = wrangling.filter_null(fire_dataset, ["zip_code_lookup"])
  fire_dataset["zip_code_lookup"] = fire_dataset["zip_code_lookup"].astype(int)

  # Generate placekeys, split
  address_fields = ["full_address", "city_lookup",
                    "state_lookup", "zip_code_lookup"]
  new_addr_col = "complete_address"
  wrangling.merge_cols_as_str(fire_dataset, address_fields, new_addr_col)
  fire_dataset = pk.gen_placekey_from_address(fire_dataset, new_addr_col)
  data_with_pk, _ = pk.split_placekey(fire_dataset)

  # Aggregate placekey data by placekey
  aggregated_data = data_with_pk.groupby([pk.PLACEKEY_FIELD_NAME]).agg(
    lambda x: list(x))

  # Output updated data to CSV
  wrangling.output_to_csv(aggregated_data, "cleaned_fire_data")

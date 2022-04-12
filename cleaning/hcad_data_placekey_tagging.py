import pandas as pd

from cleaning.data_wrangling import output_to_csv
from cleaning.placekey_tagging import split_placekey, gen_placekey_from_address


def aggregate_address_fields(data: pd.DataFrame,
                             address_col_name: str) -> pd.DataFrame:
  """
  Concatenates the address columns into one column 'STADDRESS' with space
  between each column entry, deleting the orignal address fields.

  This method requires the input dataframe to have the following address-based
  columns:
    "full_address", "city_lookup", "state_lookup", "zip_code_lookup"

  Input:
    data: a DataFrame representing the input dataset
    address_col_name: the name of the new addresss column
  Return: the input DataFrame, with a concatenated address column
  """
  # replace empty fields with empty string
  values = {"site_addr_1": "", "site_addr_2": "", "site_addr_3": "0"}
  data.fillna(value=values, inplace=True)
  data["state"] = "TX"
  data["site_addr_3"] = data["site_addr_3"].astype(str)
  # concatenate in the order of street number, name, suffix
  data[address_col_name] = data[
    ["site_addr_1", "site_addr_2", "state", "site_addr_3"]].agg(' '.join, axis=1)
  data.drop(["site_addr_1", "site_addr_2", "site_addr_3", "state"],
            axis=1, inplace=True)
  return data

if __name__ == "__main__":
  # tag HCAD for placekeys
  address_col = "STADDRESS"
  hcad = pd.read_csv('All_Merged_Data.csv', index_col=0)
  hcad_with_placekey = gen_placekey_from_address(
    aggregate_address_fields(hcad, address_col), address_col)
  with_placekey, without_placekey = split_placekey(hcad_with_placekey)
  output_to_csv(with_placekey, "HCAD_pk.csv")
  output_to_csv(without_placekey, "HCAD_nopk.csv")

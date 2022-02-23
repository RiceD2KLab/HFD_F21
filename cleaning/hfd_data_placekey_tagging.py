# use placekey API addresses with uniquely identifying placekeys
import pandas as pd

from cleaning.placekey_tagging import gen_placekey_from_address, split_placekey


def aggregate_address_fields(data: pd.DataFrame,
                             address_col_name: str) -> pd.DataFrame:
  """
  Concatenates the address columns into one column 'STADDRESS' with space
  between each column entry, deleting the orignal address fields.

  This method requires the input dataframe to have the following address-based
  columns:
    "STNO", "STNAME", "SUFFIX", "CITY", "STATE", "ZIP"

  Input:
    add_vio_data: a DataFrame representing the input dataset
    address_col_name: the name of the new addresss column
  Return: the input DataFrame, with a concatenated address column
  """
  
  # zipcode column has type float, and has trailing .0, convert it to string
  data['ZIP'] = data['ZIP'].astype(int).astype(str)
  
  # replace empty fields with empty string
  values = {"SUFFIX": "", "ZIP": "", "STATE": "", "CITY": ""}
  data.fillna(value=values, inplace=True)
  
  # concatenate in the order of street number, name, suffix
  data[address_col_name] = data[
    ['STNO', 'STNAME', 'SUFFIX', "CITY", "STATE", "ZIP"]].agg(' '.join, axis=1)
  data.drop(['STNO', 'STNAME', 'SUFFIX', "CITY", "STATE", "ZIP"],
            axis=1, inplace=True)
  return data

if __name__ == "__main__":
  # aggregate STNO and STNAME columns in address and violation data to create
  # appropriate input for street_address argument placekey lookup function
  add_vio_data = pd.read_csv('Cleaned Address and Violation Data 2020_2021.csv',
                             index_col=0)
  
  address_col = "STADDRESS"
  add_vio_data_with_placekey = gen_placekey_from_address(
    aggregate_address_fields(add_vio_data, address_col),
    address_col)
  
  with_placekey, without_placekey = split_placekey(add_vio_data_with_placekey)
  
  with_placekey.to_csv("AV_with_PK.csv")
  without_placekey.to_csv("AV_wo_PK.csv")
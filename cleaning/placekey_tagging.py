from typing import Tuple

from placekey.api import PlacekeyAPI
import pandas as pd

# placekey is a free API and you can get an API key by registering on the website
PLACEKEY_API_KEY = 'PLACEKEY_API_KEY_HERE'

PLACEKEY_FIELD_NAME = 'PlaceKey ID'


def gen_placekey_from_address(data: pd.DataFrame,
                              address_column_name: str,
                              placekey_col_name: str = PLACEKEY_FIELD_NAME) -> pd.DataFrame:
  """
  Tags each row with a placekey that serves as a unique identifier for each
  address. If the Placekey API is unable to generate a valid placekey, we put
  "0" as a placeholder.
  
  Note: this method requires the DataFrame to contain a single column with
  properly formatted address data, including a street address, a ZIP code,
  a city, and a state. This method assumes that the country is the US.
  
  Input:
    data - a DataFrame representing the input dataset
    address_column_name - name of the column containing address data
    placekey_col_name (Optional) - name of the placekey column in the dataset
  Return:
    data - the altered input DataFrame with an additional placekey column
  """
  places = []
  for i, row in data.iterrows():
    address = row[address_column_name]
    address = address.split(" ")
    # fills in the dictionary with corresponding street, city, region, zip, country
    # we are assuming the street address has the format: [STREET] [CITY] [STATE] [ZIP]
    places.append({"query_id": str(i), "street_address": ' '.join(address[:-3]),
                   "city": address[-3], "region": address[-2],
                   "postal_code": address[-1], "iso_country_code": "US"})
  # performs lookup by batch
  pk_api = PlacekeyAPI(PLACEKEY_API_KEY)
  placekeys = pk_api.lookup_placekeys(places)
  placekey_col = []
  for pk_dict in placekeys:
    # if the address has a valid placekey, the dict would store placekey: [ID].
    # otherwise, the dict would store error: Invalid address.
    key = pk_dict.get('placekey', "0")
    # if there is a valid placekey, we append it
    # otherwise, we append a 0 as placeholder
    placekey_col.append(key)
  # adds the new column into the DataFrame
  data[placekey_col_name] = placekey_col
  return data


def split_placekey(data: pd.DataFrame,
                   placekey_col_name: str = PLACEKEY_FIELD_NAME) -> Tuple[
  pd.DataFrame, pd.DataFrame]:
  """
  Splits the input dataset based on whether the placekey column has a valid
  placekey.
  
  This method requires that the
  
  Input:
    data - a DataFrame representing the input dataset
    placekey_col_name - name of the placekey column in the dataset
  Return:
    A tuple of two DataFrames for valid and invalid data:
      pk_valid - a DataFrame containing rows with valid placekey
      pk_invalid (Optional) - a DataFrame containing rows with invalid placekey
  """
  # df1:valid placekey
  pk_valid = data[data[placekey_col_name] != '0']
  # df2:invalid placekey
  pk_invalid = data[data[placekey_col_name] == '0']
  return pk_valid, pk_invalid

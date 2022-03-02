from typing import Tuple

from placekey.api import PlacekeyAPI
import placekey as pk
import pandas as pd
import cleaning.data_wrangling as wrangling

# placekey is a free API and you can get an API key by registering on the website
PLACEKEY_API_KEY = 'PLACEKEY_API_KEY_HERE'

PLACEKEY_FIELD_NAME = 'PlaceKey ID'
INVALID_PK = "0"


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
    key = pk_dict.get('placekey', INVALID_PK)
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
  
  Input:
    data - a DataFrame representing the input dataset
    placekey_col_name - name of the placekey column in the dataset
  Return:
    A tuple of two DataFrames for valid and invalid data:
      pk_valid - a DataFrame containing rows with valid placekey
      pk_invalid - a DataFrame containing rows with invalid placekey
  """
  pk_valid = data[data[placekey_col_name] != INVALID_PK]
  pk_invalid = data[data[placekey_col_name] == INVALID_PK]
  return pk_valid, pk_invalid


def generate_geocode(data: pd.DataFrame,
                     placekey_column: str = PLACEKEY_FIELD_NAME,
                     latitude_column: str = "latitude",
                     longitude_column: str = "longitude") -> pd.DataFrame:
  """
  Generate the latitude and longitude value of a location based on its placekey.
  :param data: Dataset with a place key column to generate latitude and
    longitude
  :param placekey_column: column with placekey data
  :param latitude_column: column to place latitude data
  :param longitude_column: column to place longitude data
  :return: A DataFrame with added latitude and longitude columns.
  """
  latitudes = []
  longitudes = []
  for placekey in data[placekey_column]:
    try:
      lat, lng = pk.placekey_to_geo(placekey)
      latitudes.append(lat)
      longitudes.append(lng)
    except ValueError:
      # If placekey not properly formatted, fill with inf
      latitudes.append(float('inf'))
      longitudes.append(float('inf'))

  data[latitude_column] = latitudes
  data[longitude_column] = longitudes
  return data

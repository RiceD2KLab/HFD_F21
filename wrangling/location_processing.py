from typing import Tuple, List, Dict

import pandas as pd
import censusgeocode as cgc
import wrangling


def coalesce_address(data: pd.DataFrame, new_addr_col: str,
                     ordered_aggregation_cols: List[str],
                     na_replacements: Dict[str, str],
                     zip_col: str) -> pd.DataFrame:
  data.fillna(value=na_replacements, inplace=True)
  data[zip_col] = data[zip_col].astype(int).astype(str)

  return wrangling.merge_cols_as_str(data, ordered_aggregation_cols, new_addr_col)


def split_address(data: pd.DataFrame, col_name: str) -> Tuple[
  pd.DataFrame, pd.DataFrame]:
  """
  Split the input dataset based on whether the address column is complete.
  We assume the address column to take the format [STREET] [CITY] [STATE] [ZIP]
  and is separated by space. If the address is not of this format, we categorize
  the row as invalid.

  Input:
    data - a DataFrame representing the input dataset
    col_name - column name of the address column
  Return:
    A tuple of two DataFrames:
      data - a DataFrame containing rows with valid addresses
      invalid_df - a DataFrame containing rows with invalid addresses
  """
  entries = []
  for i, row in data.iterrows():
    address = row[col_name]
    if type(address) is str:
      address = address.split(" ")

      # drop incomplete address row
      if len(address) <= 3:
        entries.append(i)

    # drop invalid row (most likely NaN)
    else:
      entries.append(i)

  # export each datasets
  invalid_df = data.filter(items=entries, axis=0)
  data.drop(entries, inplace=True)
  return data, invalid_df


def get_valid_geocodes(
    data: pd.DataFrame,
    latitude_column: str = "latitude",
    longitude_column: str = "longitude") -> pd.DataFrame:
  """
  Filter rows with valid geocodes (latitude between -90 and 90 and longitude
  between -180 and 180).

  :param data: A dataframe with latitude and longitude data
  :param latitude_column: the name of a latitude column. Must have numeric
    values
  :param longitude_column: the name of a longitude column. Must have numeric
    values
  :return: The DataFrame with proper latitude and longitude columns
  """
  return data[
    (-90 <= data[latitude_column]) & (data[latitude_column] <= 90) &
    (-180 <= data[longitude_column]) & (data[longitude_column] <= 180)]


def get_census_tract(data: pd.DataFrame, latitude_column: str = "latitude",
                     longitude_column: str = "longitude",
                     tract_column: str = "FIPS") -> pd.DataFrame:
  """
  Add column with census tract number corresponding to the location of a
  given row in a dataset with latitude and longitude coordinates.

  :param data: DataFrame with location column fields
  :param latitude_column: name of numeric latitude data column
  :param longitude_column: name of numeric longitude data column
  :param tract_column: name of census tract column to add
  :return: Updated DataFrame with census tract information.
  """
  tracts = []
  for lat, lng in zip(data[latitude_column], data[longitude_column]):
    try:
      census_info = cgc.coordinates(x=lng, y=lat)
      tracts.append(census_info["Census Tracts"][0]["GEOID"])
    except ValueError:
      print("Census data lookup failed for ", (lat, lng))
      tracts.append("0")

  data[tract_column] = tracts
  return data

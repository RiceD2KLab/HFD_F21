from typing import Tuple

import pandas as pd


def split_address(data: pd.DataFrame, col_name: str) -> Tuple[
  pd.DataFrame, pd.DataFrame]:
  """
  Splits the input dataset based on whether the address column is complete.
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

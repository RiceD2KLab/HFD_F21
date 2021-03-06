from ast import literal_eval

import pandas as pd
from collections import defaultdict
from numpy import NaN, nan
from typing import Callable, Iterable


def frequency_histogram_column(data: pd.DataFrame, column: str,
                               concat_column: str = None) -> pd.DataFrame:
  """
  Given DataFrame data and a column with categorical data, create a histogram
  of the column's entries.

  :param data:
  :param column:
  :param concat_column: Optional: specifies the column to create with the
    with the histogram.
  :return: A new data frame with an added column including the histogram data.
  """

  if concat_column is None:
    concat_column = column + "_hist"

  frequencies = []
  for row in data[column]:
    hist = defaultdict(int)
    if type(row) == float:
      elems = []
    else:
      elems: list = literal_eval(row)
    for elem in elems:
      hist[elem] += 1

    frequencies.append([dict(hist)])

  data[concat_column] = frequencies
  return data


def frequency_histogram_column_split(
    data: pd.DataFrame, column: str,
    col_mapper: Callable[[str], str] = None) -> pd.DataFrame:
  """
  Given a DataFrame a specified column, and an optional grouping function,
  adds extra columns for grouped characteristics based on the specified column
  mapper.

  :param data: a DataFrame
  :param column: categorical or numerical column for the histogram
  :param col_mapper: mapping function for deciding the data categories
  :return: a DataFrame with the updated data counts split into columns
  """
  if col_mapper is None:
    col_mapper = lambda x: x

  frequencies = []
  col_names = set([])
  for row in data[column]:
    hist = defaultdict(int)

    if type(row) == float:
      elems = []
    else:
      elems: list = literal_eval(row)
    for elem in elems:
      col_name = col_mapper(elem)
      col_names.add(col_name)
      hist[col_name] += 1

    frequencies.append(hist)

  added_cols = {k: [] for k in col_names}
  for hist in frequencies:
    for k in col_names:
      added_cols[k].append(hist[k])

  for k, v in added_cols.items():
    data[k] = v

  return data


def sum_data_column_list(data: pd.DataFrame, col: str, out_col: str = None):
  col_sums = []

  if out_col is None:
    out_col = col + "_summed"

  for row in data[col]:
    if type(row) == float:
      if row == nan:
        col_sums.append(0)
      else:
        col_sums.append(row)
    else:
      elems = eval(str(row))
      try:
        col_sums.append(sum(elems))
      except TypeError:
        col_sums.append(0)

  data[out_col] = col_sums
  return data


def add_binary_feature(data, col_name, feat):
  """
  Given a column from a dataframe, create a binary feature based on whether or not each row in the column is empty.

  data: pandas dataframe, contains column to be analyzed
  col_name: string, name of column in data to be analyzed
  feat: string, name of binary feature to be added to data

  Returns data with feat added as a column. Row values in feat are either 0 or 1 based on if the column col_name is empty or not.
  """

  binaries = []
  empty_status = data[col_name].isnull()
  main_col = data[col_name]

  for idx, val in empty_status.iteritems():
    if val == True:
      binaries.append(0)

    else:
      if main_col[idx] == 0:
        binaries.append(0)

      else:
        binaries.append(1)

  data[feat] = binaries

  return data


def engineer_time_data(data: pd.DataFrame, col: str, cutoffs: Iterable[int],
                       base_time: int) -> pd.DataFrame:
  """

  :param data:
  :param col:
  :param cutoffs:
  :param base_time:
  :return:
  """

  # Sort the year brackets to use
  within = list(sorted(set(cutoffs)))

  incident_time_col = data["Basic Incident Date Time"]

  raise NotImplementedError


def get_only_first_elem(data: pd.DataFrame, col: str,
                        needs_eval=False, default=0) -> pd.DataFrame:
  """
  Replace a list-based DataFrame column with a new column that only contains the
  first element of each list. For non-list columns, the data is left unchanged.
  `needs_eval` should be set if the data was previously exported to a CSV and
  the current column still has all string fields.

  :param data: DataFrame to be updated
  :param col: list-based column to be updated
  :param needs_eval: whether the rows of `col` need to be converted to a Python
    data structure before being processed
  :return: a DataFrame with the updated column
  """

  new_data = []
  for row in data[col]:
    if needs_eval:
      if isinstance(row, str):
        row = eval(row)
    if isinstance(row, list):
      if len(row) == 0 or (isinstance(row[0], str) and row[0].strip() == ""):
        new_data.append(default)
      else:
        new_data.append(row[0])
    else:
      new_data.append(row)

  data[col] = new_data

  return data

def get_only_last_elem(data: pd.DataFrame, column: str):
  """
  Given a column from a DataFrame in which each row is either a list or NaN,
  edit the column so that each row contains either the last entry in the list or NaN.

  :param data: pandas dataframe, contains column to be analyzed
  :param column: string, name of column to be updated

  Returns data with the row values of feature edited to be either the last entry of the list or NaN.
  """

  results = data[column]
  updated_results = []

  for idx, val in results.iteritems():
    if type(val) == float:
      updated_results.append(val)

    else:
      new_res = literal_eval(val)[-1]
      updated_results.append(new_res.replace(' ', ''))

  data[column] = updated_results

  return data

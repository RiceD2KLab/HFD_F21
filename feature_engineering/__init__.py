from ast import literal_eval

import pandas as pd
from collections import defaultdict
from numpy import NaN, nan
from typing import Callable


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
      col_sums.append(sum(elems))

  data[out_col] = col_sums
  return data

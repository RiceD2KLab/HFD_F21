from ast import literal_eval

import pandas as pd
from collections import defaultdict
from numpy import NaN, nan


def frequency_histogram_column(data: pd.DataFrame, column: str,
                        concat_column: str = None):
  """
  Given DataFrame data and a column with categorical data, create a histogram
  of the column's entries.

  :param data:
  :param column:
  :param concat_column: Optional: specifies the column to create with the
    with the histogram.
  :return: A new data frame with an added column including the histogram data.
  """

  if concat_column == None:
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

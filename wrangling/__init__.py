"""
Data wrangling module
"""
import re
import pandas as pd
import glob

from typing import List, Dict


def clean_text_data(raw_data: str, regex_replacements: Dict[str, str] = None,
                    verbatim_replacements: Dict[str, str] = None) -> str:
  """
  Given a raw data string, cleans the data by using the regex and verbatim
  replacements.

  :param raw_data: Data to be cleaned
  :param regex_replacements: Dictionary of regex replacements to make
  :param verbatim_replacements: Dictionary of verbatim replacements to make
  :return: Cleaned data
  """

  if regex_replacements is None:
    regex_replacements = {}

  if verbatim_replacements is None:
    verbatim_replacements = {}

  regexes = {re.compile(k): v for k, v in regex_replacements.items()}

  clean_text = raw_data
  for regex in regexes:
    clean_text = re.sub(regex, '', clean_text)
  for old, new in verbatim_replacements.items():
    clean_text = clean_text.replace(old, new)

  clean_text = clean_text.strip()

  return clean_text


def clean_html(raw_html: str) -> str:
  """
  Given a string of HTML data, cleans the data using pre-defined HTML cleaning
  replacements.
  :param raw_html: Raw HTML string to be cleaned
  :return: Cleaned HTML text
  """

  # Regex removals (HTML tags)
  regex_replacements = {'<.*?>': ""}

  # Raw text removals
  removals = ["&nbsp;", "***", "**", "*", "\r"]
  removals_dict = {removal: "" for removal in removals}
  return clean_text_data(raw_html, regex_replacements=regex_replacements,
                         verbatim_replacements=removals_dict)


def compile_datasets(datasets: List[pd.DataFrame],
                     filter_cols: List[str] = None) -> pd.DataFrame:
  """
  This method takes a number of datasets and a set of columns to delete from
  each data set if present, and combines all specified datasets into a single
  DataFrame.

  :param datasets: A list of datasets to merge.
  :param filter_cols: Columns to remove when filtering the data.
  :return: Compiled data from sources.
  """
  if filter_cols is None:
    filter_cols = []

  for dataset in datasets:
    for drop_col in filter_cols:
      if drop_col in dataset:
        dataset.drop(drop_col, axis=1, inplace=True)

  return pd.concat(datasets)


def stack_datasets(stack_dir: str, extension: str = "*") -> pd.DataFrame:
  """
  Takes a folder directory and extension for desired file type as input and
  outputs a DataFrame with the stacked datasets.

  :param stack_dir: Directory with files to stack
  :param extension: file extension of files to be stacked
  :return: A DataFrame with the stacked datasets
  """
  all_data = [pd.read_csv(filename) for filename in
              glob.iglob(f"{stack_dir}/*.{extension}")]
  return compile_datasets(all_data)


def filter_rows(dataset: pd.DataFrame,
                unwanted_values: Dict) -> pd.DataFrame:
  """
  Given a dataset, drop rows that have unwanted values in specified columns.

  :param dataset: DataFrame from which to filter matching rows
  :param unwanted_values: Columns and corresponding sets of values to ignore
  :return: DataFrame with the unwanted rows filtered out.
  """
  for column, unwanted in unwanted_values.items():
    for item in unwanted:
      dataset = dataset[dataset[column] != item]

  return dataset


def filter_null(dataset: pd.DataFrame, col_names: List[str]) -> pd.DataFrame:
  """
  Given a dataset, drop rows which have NaN or empty entries in any of the
  specified columns.

  :param dataset: Pandas DataFrame
  :param col_names: list, columns corresponding to components of an address
  :return: DataFrame with non-excluded rows.
  """
  null_values = dataset.isnull()
  idxs_to_drop = set([])

  for idx, row in null_values.iterrows():
    for col in col_names:
      if row[col]:
        idxs_to_drop.add(idx)

  return dataset.drop(idxs_to_drop)


def merge_cols_as_str(dataset: pd.DataFrame, to_merge: List[str],
                      merged_col: str,
                      sep: str = " ",
                      inplace: bool = True,
                      ) -> pd.DataFrame:
  """
  Merges a list of columns, `to_merge` into a single column, `merged_col` using
  `sep` as the separator.

  :param dataset: a Pandas DataFrame
  :param to_merge: a list of columns to merge
  :param merged_col: the name of the column that will hold the merged result
  :param sep: separator between two fields of the merged column
  :param inplace: whether to merge the data in place or not
  :return: a DataFrame the list of columns to merge being replaced with a single
    column of merged data
  """

  for col in to_merge:
    dataset[col] = dataset[col].astype(str)
  dataset[merged_col] = dataset[to_merge].agg(sep.join, axis=1)
  dataset.drop(to_merge, axis=1, inplace=inplace)

  return dataset


def trim_string_fields(dataset: pd.DataFrame) -> pd.DataFrame:
  """
  Trims whitespace off the beginning and end of any string fields in a DataFrame.

  :param dataset: DataFrame to be trimmed
  :return: the DataFrame updated with trimmed fields
  """
  return dataset.applymap(lambda x: (x.strip() if isinstance(x, str) else x))


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
  :param default: the default replacement value if the data is an empty list
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

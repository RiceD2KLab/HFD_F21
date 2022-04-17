"""
Data wrangling module
"""
import os.path
import re
from enum import Enum
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
  Given a string of HTML data, cleans the data using pre-defined HTML wrangling
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
  :return: A DataFrame with the unwanted rows filtered out.
  """
  for column, unwanted in unwanted_values.items():
    for item in unwanted:
      dataset = dataset[dataset[column] != item]

  return dataset


def filter_null(dataset: pd.DataFrame, col_names: List[str]) -> pd.DataFrame:
  """
  Given a dataset, drop rows which have NaN or empty entries in any of the
  specified columns.

  dataset: string, path or name of csv dataset
  col_names: list, columns corresponding to components of an address

  Returns DataFrame with non-excluded rows.
  """
  null_values = dataset.isnull()
  idxs_to_drop = set([])

  for idx, row in null_values.iterrows():
    for col in col_names:
      if row[col]:
        idxs_to_drop.add(idx)

  return dataset.drop(idxs_to_drop)


def trim_string_fields(dataset: pd.DataFrame) -> pd.DataFrame:
  """
  Trims whitespace off the beginning and end of any string fields in a DataFrame.
  Args:
    dataset: DataFrame to be trimmed

  Returns:
    the trimmed DataFrame
  """
  return dataset.applymap(lambda x: (x.strip() if isinstance(x, str) else x))


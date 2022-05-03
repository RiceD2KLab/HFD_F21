import glob
import os
from typing import List

import pandas as pd

ORIG_DIR = "Original Datasets"
INTER_DIR = "Intermediate Datasets"
CLEAN_DIR = "Cleaned Datasets"


def output_to_excel(dataframe: pd.DataFrame, filename: str,
                    keep_index=True) -> None:
  """
  Converts a Pandas DataFrame into an Excel spreadsheet.

  :param dataframe: DataFrame to be converted
  :param filename: name of file to save, without extension
  :param keep_index: whether to keep the index column
  """
  base, extension = os.path.splitext(filename)
  if extension != ".xlsx":
    filename = base + ".xlsx"
  dataframe.to_excel(filename, encoding="utf-8", index=keep_index)


def output_to_csv(dataframe: pd.DataFrame, filename: str,
                  keep_index=True) -> None:
  """
  Converts a Pandas DataFrame into a CSV file.

  :param dataframe: DataFrame to be converted
  :param filename: name of file to save, without an extension
  :param keep_index: whether to keep the index column
  """
  base, extension = os.path.splitext(filename)
  if extension != ".csv":
    filename = base + ".csv"

  dataframe.to_csv(filename, encoding="utf-8", index=keep_index)


def output_to_pkl(dataframe: pd.DataFrame, filename: str,
                  keep_index=True) -> None:
  """
  Exports a Pandas DataFrame into a Pickle file.

  :param dataframe: DataFrame to be converted
  :param filename: name of the output file, without an extension
  :param keep_index: whether to keep the index column
  """
  base, extension = os.path.splitext(filename)
  if extension != ".pkl":
    filename = base + ".pkl"

  dataframe.to_pickle(filename, encoding="utf-8", index=keep_index)


def evaluate_col(dataframe: pd.DataFrame, col: str) -> pd.DataFrame:
  pass


def read_all_dir_entries_csv(
    directory: str, extension: str = "*") -> List[pd.DataFrame]:
  """
  Given a directory and (optionally) a file extension, reads in all CSV files in
  the directory with the matching extension.
  :param directory: name of the directory from which to read the files
  :param extension: file extension
  :return: A list of DataFrames that were read in.
  """
  return [pd.read_csv(filename) for filename in
          glob.iglob(f"{directory}/*.{extension}")]

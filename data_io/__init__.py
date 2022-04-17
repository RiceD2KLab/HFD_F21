import os
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
  :return: None
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
  :return: None
  """
  base, extension = os.path.splitext(filename)
  if extension != ".csv":
    filename = base + ".csv"

  dataframe.to_csv(filename, encoding="utf-8", index=keep_index)


def output_to_pkl(dataframe: pd.DataFrame, filename: str,
                  keep_index=True) -> None:
  """
  Exports a Pandas DataFrame into a Pickle file.
  Args:
    dataframe: DataFrame to be converted
    filename: name of the output file, without an extension
  """
  base, extension = os.path.splitext(filename)
  if extension != ".pkl":
    filename = base + ".pkl"

  dataframe.to_pickle(filename, encoding="utf-8", index=keep_index)


def evaluate_col(dataframe: pd.DataFrame, col: str) -> pd.DataFrame:
  pass

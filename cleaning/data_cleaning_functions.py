import os.path
import re
from enum import Enum
import pandas as pd
import glob


class FileType(Enum):
  EXCEL = 1
  CSV = 2


def clean_text_data(raw_data: str, regex_replacements: dict[str, str],
                    verbatim_replacements: dict[str, str]) -> str:
  """
  Given a raw data string, cleans the data by using the regex and verbatim
  replacements.
  :param raw_data: Data to be cleaned
  :param regex_replacements: Dictionary of regex replacements to make
  :param verbatim_replacements: Dictionary of verbatim replacements to make
  :return: Cleaned data
  """
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


def compile_datasets(datasets: list[pd.DataFrame],
                     filter_cols: list[str]) -> pd.DataFrame:
  """
  This method takes a number of datasets and a set of columns to delete from
  each data set if present, and combines all specified datasets into a single
  dataframe.
  :param datasets: A list of datasets to merge.
  :param filter_cols: Columns to remove when filtering the data.
  :return: Compiled data from sources.
  """
  
  for violation in datasets:
    for drop_col in filter_cols:
      if drop_col in violation:
        violation.drop(drop_col, axis=1, inplace=True)
  
  return pd.concat(datasets)


def output_to_excel(dataframe: pd.DataFrame, filename: str) -> None:
  base, extension = os.path.splitext(filename)
  if extension != ".xlsx":
    filename = base + ".xlsx"
  dataframe.to_excel(filename, encoding="utf-8")


def output_to_csv(dataframe: pd.DataFrame, filename: str) -> None:
  base, extension = os.path.splitext(filename)
  if extension != ".csv":
    filename = base + ".csv"
  
  dataframe.to_csv(filename, encoding="utf-8")

def stack_datasets(folder_directory,extension):
    """
    Takes a folder directory and extension for desired file type as input and 
    outputs a concatenated file of all of the files in the given folder. 
    """
    all_data = []
    for file in glob.iglob(f'{directory}/*.{extension}'):
        all_data.append(pd.read_csv(file))

    df = pd.concat(all_data, ignore_index=True)
    df.to_csv(f'{directory}/ConcatenatedData.{extension}', index = False)
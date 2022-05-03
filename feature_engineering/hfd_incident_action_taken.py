import argparse
from collections import defaultdict

import pandas as pd

import os
import matplotlib.pyplot as plt

from feature_engineering import frequency_histogram_column_split, \
  frequency_histogram_column
from data_io import output_to_csv

groupings = {"N": "None", "0": "Other", "1": "FireControl",
             "2": "Search & Rescue", "3": "EMS and Transport",
             "4": "Hazardous Condition", "5": "Fire Rescues",
             "6": "Services", "7": "Assistance", "8": "Investigation",
             "9": "Fill-in, Standby"}


def action_taken_binary_plot(data: pd.DataFrame, hist_col_name: str):
  total_hist = defaultdict(int)
  for row in data[hist_col_name]:
    for k, v in row[0].items():
      total_hist[k.split()[0] == "NNN"] += v

  action_taken_mapping = {True: "None", False: "Action\nTaken"}
  hist_keys = [k for k in total_hist.keys()]
  hist_plot_keys = [action_taken_mapping[k] for k in hist_keys]
  hist_vals = [total_hist[k] for k in hist_keys]

  plt.bar(hist_plot_keys, hist_vals)

  for i, val in enumerate(hist_vals):
    plt.text(i - 0.02 * len(str(val)), val + 300, str(val), fontweight="bold")

  plt.show()


def total_actions_taken_plot(data: pd.DataFrame,
                             hist_col_name: str):
  """

  :param data:
  :param hist_col_name:
  :return:
  """

  total_hist = defaultdict(int)
  for row in data[hist_col_name]:
    for k, v in row[0].items():
      total_hist[k.split()[0][0]] += v

  plot_groupings = {"N": "None", "0": "Other", "1": "Fire\nControl",
                    "2": "Search &\n Rescue", "3": "EMS and\nTransport",
                    "4": "Hazardous\nCondition", "5": "Fire\nRescues",
                    "6": "Services", "7": "Assistance", "8": "Investigation",
                    "9": "Fill-in,\nStandby"}
  hist_keys = list(
    filter(lambda x: x[0] != "N", [k for k in total_hist.keys()]))
  hist_plot_keys = [plot_groupings[k] for k in hist_keys]
  hist_vals = [total_hist[k] for k in hist_keys]

  plt.bar(hist_plot_keys, hist_vals)

  for i, val in enumerate(hist_vals):
    plt.text(i - 0.05 * len(str(val)), val + 300, str(val), fontweight="bold")

  plt.title("HFD Actions Taken Category Totals")
  plt.show()


def get_actions_taken_group(value: str) -> str:
  """
  Given an actions taken code for incident data, returns the category to which
  the code corresponds.

  :param value: Actions taken code and/or description
  :return: Group name
  """
  col_name = "Action Taken: "
  if value[0] not in groupings.keys():
    group = groupings["N"]
  else:
    group = groupings[value[0]]

  return col_name + group


if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    description="HFD Action Taken Codes Feature Engineering")
  parser.add_argument("--output_csv", action="store_true")
  parser.add_argument("--no-output_csv", action="store_false")
  parser.add_argument("--output_pkl", action="store_true")
  parser.add_argument("--aggregate_vis", action="store_true")
  parser.add_argument("--binary_vis", action="store_true")
  parser.set_defaults(output_csv=True, output_pkl=False, aggregate_vis=False,
                      binary_vis=False)

  args = parser.parse_args()

  data_file = os.path.join(os.path.normpath(r"Data/Merged Data"),
                           "Full_Merged_Data_AC_Houston.csv")

  col_name = "Basic Primary Action Taken Code And Description (FD1.48)"
  hist_col_name = "Actions Taken Frequencies"

  data = pd.read_csv(data_file)
  data = frequency_histogram_column_split(data, col_name,
                                          get_actions_taken_group)

  if args.output_pkl:
    data.to_pickle("Engineered_Feature.pkl")

  if args.output_csv:
    output_to_csv(data, "Full_Merged_Data_JW_Houston")

  if args.aggregate_vis:
    frequency_histogram_column(data, col_name, hist_col_name)
    total_actions_taken_plot(data, hist_col_name)
  if args.binary_vis:
    frequency_histogram_column(data, col_name, hist_col_name)
    action_taken_binary_plot(data, hist_col_name)

import codecs, data_io
import os
from json.encoder import py_encode_basestring_ascii
from typing import List, Iterable

import pandas as pd
from pandas import Timestamp, NaT

from ast import literal_eval
import numpy as np
from numpy import NaN, nan
import re
from statistics import mode, mean
import math

import feature_engineering as fe
from feature_engineering import hfd_incident_action_taken
from wrangling import full_merge

JAN_01_00 = 946684800


def feat_building_code(data: pd.DataFrame, column: str) -> pd.DataFrame:
  """
  Given a merged property dataset and a specified column with property use code
  data, counts the gives a categorical name to element in the specified column.

  :param data: merged property dataset
  :param column: column with property use data
  :return: dataset with new categorical column of the INFOR building category
    for each property (row) based on the property use code column.
  """
  property_col = data.loc[:, column]

  code_list = []
  for row in property_col:
    property_codes = []
    if type(row) != float:
      for item in literal_eval(row):
        if len(re.findall("\d+", item)) != 0:
          code = int(re.findall("\d+", item)[0])
          property_codes.append(code)
      if len(property_codes) != 0:
        code = mode(property_codes)
      else:
        code = 0
    else:
      code = 0
    code_list.append(code)

  building_category = []
  for code in code_list:
    first_digit = int(str(code)[0])
    if first_digit == 0:
      building_category.append("Unknown")
    elif first_digit == 1:
      building_category.append("Assembly")
    elif first_digit == 2:
      building_category.append("Educational")
    elif first_digit == 3:
      building_category.append("Health Care, Detention, and Correction")
    elif first_digit == 4:
      building_category.append("Residential")
    elif first_digit == 5:
      building_category.append("Mercantile, Business")
    elif first_digit == 6:
      building_category.append(
        "Industrial, Utility, Defense, Agriculture, Mining")
    elif first_digit == 7:
      building_category.append("Manufacturing, Processing")
    elif first_digit == 8:
      building_category.append("Storage")
    elif first_digit == 9:
      building_category.append("Outside or Special Property")

  data['Property_Code'] = building_category
  return data


def add_true_incident(data: pd.DataFrame, column: str) -> pd.DataFrame:
  """
  Given a DataFrame with aggregated incident data and a feature name, add a new
  column to the DataFrame that counts the number of "true" incidents that a
  given row contains.

  :param data: the name of the fulled merged dataset
  :param column: the name of the column to check
  :return: data with the new feature engineering output.
  """

  col = data[column]
  newcol = []
  for i in range(len(col)):
    count = 0
    if not pd.isnull(col[i]):
      val = col[i][1:-1]
      val = val.split('\'')
      for j in val:
        if not j.startswith('7') and not j.startswith(
            ',') and j != '' and not j.startswith('NNN'):
          count += 1
    newcol.append(count)
  data['True_Incident'] = newcol
  return data


def fire_spread_property_lost(df: pd.DataFrame) -> pd.DataFrame:
  """
  Adds a "Binary_Property_Lost" column to the input DataFrame encoding whether
  property lost has ever been recorded for a given property. Also adds a
  "Fire_Spread_Mean" column that encodes the degree of fire spread with on a
  scale from 1 to 5.

  :param df: DataFrame including structure fire data from columns named
    "fire_spread" and "totalSaved"
  :return: updated DataFrame with property damage and fire spread data
  """
  df['Fire_Spread_Mean'] = nan
  df['Binary_Property_Lost'] = nan
  for i, row in df.iterrows():
    if type(row["fire_spread"]) != float:
      fire_spread = eval(row["fire_spread"])
      filtered_fire_spread = [eval(item[0]) for item in fire_spread if
                              type(item) != float]
      if len(filtered_fire_spread) != 0:
        df.iat[i, df.columns.get_loc('Fire_Spread_Mean')] = mean(
          filtered_fire_spread)
    if type(row["totalSaved"]) != float:
      total_saved = eval(row["totalSaved"])
      filtered_saved = [item for item in total_saved if not math.isnan(item)]
      if len(filtered_saved) != 0:
        binary = 0
        for elem in filtered_saved:
          if elem < 0:
            binary = 1
            break
        df.iat[i, df.columns.get_loc('Binary_Property_Lost')] = binary
  return df


def add_incident_inspection_time(data: pd.DataFrame) -> pd.DataFrame:
  """
  Given a DataFrame that includes time-based columns "Basic Incident Date Time"
  and "Processed / Last Inspected", adds new columns to the DataFrame showing
  binary variables for whether a certain property was inspected or had an
  incident in the last 1, 2, 3, and 4 years.

  :param data: DataFrame with time-based data for incidents and inspections
  :return: updated DataFrame with time-based engineered features
  """
  incidentTime_col = data.loc[:, 'Basic Incident Date Time']
  incidentTime_1yr = []
  incidentTime_2yr = []
  incidentTime_3yr = []
  incidentTime_4yr = []
  for row in incidentTime_col:
    if type(row) != float:
      dummyValue1 = pd.to_datetime(JAN_01_00, unit='s')
      dummyValue2 = pd.to_datetime(JAN_01_00, unit='s')
      dummyValue3 = pd.to_datetime(JAN_01_00, unit='s')
      dummyValue4 = pd.to_datetime(JAN_01_00, unit='s')
      for item in eval(row):
        if len(item.split("/")[2].split(" ")[0]) == 2:
          item_time = pd.to_datetime(item, format='%m/%d/%y %H:%M')
        if len(item.split("/")[2].split(" ")[0]) == 4:
          item_time = pd.to_datetime(item, format='%m/%d/%Y %H:%M')
        if item_time >= dummyValue1:
          dummyValue1 = item_time
        if item_time >= dummyValue2 and item_time <= pd.to_datetime(1609480800,
                                                                    unit='s'):
          dummyValue2 = item_time
        if item_time >= dummyValue3 and item_time <= pd.to_datetime(1577858400,
                                                                    unit='s'):
          dummyValue3 = item_time
        if item_time >= dummyValue4 and item_time <= pd.to_datetime(1546322400,
                                                                    unit='s'):
          dummyValue4 = item_time
      if dummyValue1 > pd.to_datetime(1609480800, unit='s'):
        code_1yr = 1
      else:
        code_1yr = 0
      if dummyValue2 > pd.to_datetime(1577858400, unit='s'):
        code_2yr = 1
      else:
        code_2yr = 0
      if dummyValue3 > pd.to_datetime(1546322400, unit='s'):
        code_3yr = 1
      else:
        code_3yr = 0
      if dummyValue4 > pd.to_datetime(1514786400, unit='s'):
        code_4yr = 1
      else:
        code_4yr = 0
    else:
      code_1yr = 0
      code_2yr = 0
      code_3yr = 0
      code_4yr = 0
    incidentTime_1yr.append(code_1yr)
    incidentTime_2yr.append(code_2yr)
    incidentTime_3yr.append(code_3yr)
    incidentTime_4yr.append(code_4yr)
  data["incidentTime_1yr"] = incidentTime_1yr
  data["incidentTime_2yr"] = incidentTime_2yr
  data["incidentTime_3yr"] = incidentTime_3yr
  data["incidentTime_4yr"] = incidentTime_4yr

  # Adding inspection features
  inspectTime_col = data.loc[:, 'Processed / Last Inspected']
  inspectTime_1yr = []
  inspectTime_2yr = []
  inspectTime_3yr = []
  inspectTime_4yr = []
  inspectTime_5yr = []
  for row in inspectTime_col:
    if type(row) != float:
      dummyValue1 = pd.to_datetime(946684800, unit='s')
      dummyValue2 = pd.to_datetime(946684800, unit='s')
      dummyValue3 = pd.to_datetime(946684800, unit='s')
      dummyValue4 = pd.to_datetime(946684800, unit='s')
      dummyValue5 = pd.to_datetime(946684800, unit='s')
      for item in eval(row):
        if isinstance(item, float):
          if np.isnan(item):
            item_time = pd.to_datetime(0, unit='s')
        elif len(item.split("/")[2].split(" ")[0]) == 2:
          item_time = pd.to_datetime(item, format='%m/%d/%y %H:%M')
        elif len(item.split("/")[2].split(" ")[0]) == 4:
          item_time = pd.to_datetime(item, format='%m/%d/%Y %H:%M')
        if item_time >= dummyValue1:
          dummyValue1 = item_time
        if item_time >= dummyValue2 and item_time <= pd.to_datetime(1609480800,
                                                                    unit='s'):
          dummyValue2 = item_time
        if item_time >= dummyValue3 and item_time <= pd.to_datetime(1577858400,
                                                                    unit='s'):
          dummyValue3 = item_time
        if item_time >= dummyValue4 and item_time <= pd.to_datetime(1546322400,
                                                                    unit='s'):
          dummyValue4 = item_time
        if item_time >= dummyValue5 and item_time <= pd.to_datetime(1514786400,
                                                                    unit='s'):
          dummyValue5 = item_time
      if dummyValue1 > pd.to_datetime(1609480800, unit='s'):
        code_1yr = 1
      else:
        code_1yr = 0
      if dummyValue2 > pd.to_datetime(1577858400, unit='s'):
        code_2yr = 1
      else:
        code_2yr = 0
      if dummyValue3 > pd.to_datetime(1546322400, unit='s'):
        code_3yr = 1
      else:
        code_3yr = 0
      if dummyValue4 > pd.to_datetime(1514786400, unit='s'):
        code_4yr = 1
      else:
        code_4yr = 0
      if dummyValue5 > pd.to_datetime(1483250400, unit='s'):
        code_5yr = 1
      else:
        code_5yr = 0
    else:
      code_1yr = 0
      code_2yr = 0
      code_3yr = 0
      code_4yr = 0
      code_5yr = 0
    inspectTime_1yr.append(code_1yr)
    inspectTime_2yr.append(code_2yr)
    inspectTime_3yr.append(code_3yr)
    inspectTime_4yr.append(code_4yr)
    inspectTime_5yr.append(code_5yr)
  data["inspectTime_1yr"] = inspectTime_1yr
  data["inspectTime_2yr"] = inspectTime_2yr
  data["inspectTime_3yr"] = inspectTime_3yr
  data["inspectTime_4yr"] = inspectTime_4yr
  data["inspectTime_5yr"] = inspectTime_5yr

  return data


if __name__ == "__main__":
  full_data = pd.read_csv(
    os.path.join(full_merge.MERGED_DIR, 'Full Merged Data.csv'))

  # Inspection Status
  full_data = fe.add_binary_feature(full_data, 'INSPTYPE', 'InspectionStatus')

  # Total Inspections
  full_data['Total_Inspections'] = full_data['INSPTYPE'].apply(
    lambda x: len(literal_eval(x)) if type(x) != float else 0)

  # Total Incidents
  full_data['Total_Incidents'] = full_data['Basic Incident Date Time'].apply(
    lambda x: len(literal_eval(x)) if type(x) != float else 0)

  # Total Violations
  full_data['Total_Violations'] = full_data['VIOLATIONCode'].apply(
    lambda x: sum(
      1 for list_item in eval(x) if type(list_item) != float) if type(
      x) != float else 0)

  # Result Variable
  full_data = fe.get_only_last_elem(full_data, 'Result')

  # Building Codes
  property_use_col = 'Basic Property Use Code And Description (FD1.46)'
  feat_building_code(full_data, property_use_col)

  # Time Variables
  full_data = add_incident_inspection_time(full_data)

  # Fire Spread Variables
  full_data = fire_spread_property_lost(full_data)

  # True Incident Status
  full_data = add_true_incident(
    full_data,
    'Basic Incident Type Code And Description (FD1.21)')

  # Incident Status
  full_data = fe.add_binary_feature(full_data, 'True_Incident',
                                    'IncidentStatus')

  # Actions taken
  actions_taken_col = "Basic Primary Action Taken Code And Description (FD1.48)"
  full_data = fe.frequency_histogram_column_split(
    full_data, actions_taken_col,
    hfd_incident_action_taken.get_actions_taken_group)

  # Final output
  data_io.output_to_csv(full_data, os.path.join(full_merge.MERGED_DIR,
                                                "HFD Engineered Data"),
                        keep_index=False)

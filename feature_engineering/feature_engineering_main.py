import codecs
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
from cleaning.data_wrangling import output_to_csv
from feature_engineering import hfd_incident_action_taken

JAN_01_00 = 946684800


# TOTAL COUNT COLUMNS

# Create Column of Total Number of Inspections

# full_data['Total_Inspections'] = full_data['INSPTYPE'].apply(lambda x: len(literal_eval(x)) if type(x)!=float else 0)

# Create Column of Total Number of Incidents

# full_data['Total_Incidents'] = full_data['Basic Incident Number (FD1)'].apply(lambda x: len(literal_eval(x)) if type(x)!=float else 0)

# Create Column of Total Number of Violations

# full_data['Total_Violations'] = full_data['VIOLATIONCode'].apply(lambda x: sum(1 for list_item in eval(x) if type(list_item)!=float) if type(x)!=float else 0)

# RESULT VARIABLE

def feat_recent(data, feature):
  """
  Given a column from a dataframe in which each row is either a list or NaN,
  edit the column so that each row contains either the last entry in the list or NaN.

  data: pandas dataframe, contains column to be analyzed
  feature: string, name of feature to be edited

  Returns data with the row values of feature edited to be either the last entry of the list or NaN.
  """

  results = data[feature]
  updated_results = []

  for idx, val in results.iteritems():
    if type(val) == float:
      updated_results.append(val)

    else:
      new_res = literal_eval(val)[-1]
      updated_results.append(new_res.replace(' ', ''))

  data[feature] = updated_results

  return data


# BUILDING CODE VARIABLE

def feat_building_code(data):
  """
  Input: Merged Property Dataset
  Output: Merged Property Dataset with new categorical column of the INFOR building category for each
  property (row) based on the Basic Property Use Code And Description (FD1.46) column.
  """
  property_col = data.loc[:, 'Basic Property Use Code And Description (FD1.46)']

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


# YUXIN: TRUE INSPECTION VARIABLE

def add_true_incident(data, feature):
  """
  Given a file name and a feature name, add a new column showing the result of feature engineering.

  file: the name of the fulled merged dataset
  feature: the name of the feature being engineered

  Return data with the new feature engineering output.
  """
  col = data[feature]
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


# JOSH: PRIMARY ACTION TAKEN
# Methods in freature_engineeering/hfd_incident_action_taken.py

# ANNITA: STRUCTURE FIRE VARIABLES
def fire_spread_property_lost(df):
  """
  Adds a "Binary_Property_Lost" column to the input dataframe encoding whether property lost has ever been recorded for a given property. Adds a "Fire_Spread_Mean" column to the input dataframe encoding the degree of fire spread with a scale of 1 to 5.
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


# JARRETT: TIME VARIABLES
def add_incident_inspection_time(data):
  """
  Given a file name and a feature name, add new columns showing the result of feature engineering.

  file: the name of the fulled merged dataset
  feature: the name of the feature being engineered

  Return data with the new feature engineering output, which has a binary column to indicate if a property
  has had an inspection in the last year, 2 years, and 5 years, and if a property has had an incident in the
  past year, 2 years, or 5 years.
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
  full_data = pd.read_csv('full_merge_no_duplicates.csv')

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
  full_data = feat_recent(full_data, 'Result')

  # Building Codes
  feat_building_code(full_data)

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
  output_to_csv(full_data, "Full_Merged_Data", keep_index=False)

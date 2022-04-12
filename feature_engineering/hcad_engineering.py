from ast import literal_eval
from typing import Dict

import numpy as np
import pandas as pd
from numpy import NaN, nan
import re
from statistics import mode, mean
import math

from cleaning.data_wrangling import output_to_csv
from feature_engineering import add_binary_feature, sum_data_column_list

hcad_property_dict = {
  "Assembly": [610, 611, 620, 630, 680, 685, 690, 8173, 8175, 8176, 8302,
               8303, 8306, 8308, 8309, 8310, 8311, 8314, 8327, 8337, 8355,
               8379, 8380, 8405, 8416, 8417, 8418, 8422, 8432, 8481, 8482,
               8483, 8485, 8486, 8491, 8514, 8515, 8516, 8517, 8530, 8571,
               8573, 8574, 8575, 8576, 8718, 9302, 9311, 9403, 9432, 9483,
               9575],
  "Educational": [612, 613, 8156, 8158, 8356, 8355, 8356, 8357, 8358, 8359,
                  8360, 8361, 8362, 8363, 8364, 8365, 8366, 8367, 8368, 8369,
                  8370, 8371, 8372, 8373, 8374, 8375, 8376, 8377, 8426, 8484,
                  8487, 8488, 8598],
  "Health Care, Detention, and Correction": [640, 8313, 8331, 8335, 8341,
                                             8381, 8431, 8444, 8489, 9381],
  "Residential": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 125, 126,
                  8150, 8151, 8152, 8153, 8154, 8177, 8178, 8179, 8300, 8321,
                  8323, 8324, 8330, 8332, 8338, 8343, 8348, 8351, 8352, 8354,
                  8393, 8394, 8401, 8424, 8445, 8451, 8493, 8537, 8538, 8539,
                  8540, 8541, 8542, 8543, 8544, 8545, 8546, 8547, 8548, 8549,
                  8550, 8551, 8587, 8588, 8589, 8590, 8591, 8592, 8593, 8594,
                  8595, 8596, 8710, 8774, 8775, 8984, 8985, 8986, 8987, 8988,
                  8989, 9150, 9343, 9351],
  "Mercantile, Business": [614, 8185, 8304, 8318, 8319, 8320, 8336, 8340,
                           8342, 8344, 8346, 8349, 8350, 8353, 8384, 8408,
                           8410, 8412, 8413, 8414, 8419, 8434, 8435, 8436,
                           8441, 8442, 8443, 8446, 8455, 8458, 8459, 8460,
                           8461, 8462, 8465, 8470, 8490, 8492, 8499, 8508,
                           8511, 8512, 8513, 8526, 8527, 8528, 8529, 8531,
                           8532, 8533, 8534, 8554, 8578, 8581, 8582, 8586,
                           8597, 8599, 8600, 8700, 8719, 8720, 8990, 8991,
                           8992, 8993, 9185, 9344, 9350, 9353, 9410, 9412,
                           9492, 9528, 9993],
  "Industrial, Utility, Defense, Agriculture, Mining": [8134, 8135, 8136,
                                                        8137, 8138, 8139,
                                                        8140, 8141, 8142,
                                                        8160, 8170, 8171,
                                                        8301, 8334, 8392,
                                                        8440, 8454, 8496,
                                                        8497, 8498, 8518,
                                                        8519, 8520, 8521,
                                                        8522, 8564, 8994,
                                                        9392, 9430, 9454,
                                                        9496, 9497, 9498],
  "Manufacturing, Processing": [8315, 8316, 8317, 8450, 8494, 8495, 9494,
                                9495],
  "Storage": [660, 8100, 8101, 8102, 8103, 8104, 8105, 8106, 8107, 8108, 8109,
              8110, 8111, 8112, 8113, 8114, 8115, 8116, 8117, 8118, 8119,
              8120, 8121, 8122, 8123, 8124, 8125, 8126, 8127, 8128, 8129,
              8130, 8131, 8132, 8133, 8157, 8180, 8181, 8182, 8183, 8184,
              8305, 8322, 8325, 8326, 8328, 8329, 8339, 8347, 8378, 8383,
              8386, 8387, 8388, 8390, 8391, 8395, 8396, 8397, 8398, 8399,
              8400, 8403, 8404, 8406, 8407, 8409, 8420, 8421, 8423, 8427,
              8429, 84230, 8447, 8448, 8453, 8456, 8466, 8467, 8468, 8469,
              8471, 8472, 8473, 8474, 8475, 8477, 8478, 8479, 8480, 8523,
              8524, 8525, 8555, 8556, 8557, 8558, 8559, 8560, 8561, 8562,
              8563, 8565, 8567, 8658, 8569, 8570, 8577, 8585, 9103, 9104,
              9157, 9305, 9345, 9387, 9391, 9406, 9407, 9447, 9453, 9470,
              9471, 9472, 9520, 9584],
  "Outside or Special Property": [8155, 8161, 8162, 8163, 8174, 8345, 8428,
                                  8552, 8566, 8580, 9174],
  "Unknown": [9781, 9782, 9783, 9784, 8415]}


def update_property_code(data: pd.DataFrame, codes: Dict[int, str]):
  """
  Using hcad_property_dict, this function will take in a dataframe with the property_code column
  and update the unknown values within the column to reflect the corresponding HCAD building clodes,
  classified as INFOR buidling categories.
  """
  for index, _ in enumerate(data['impr_mdl_cd']):
    if type(data.iloc[index, 0]) != float:
      data.iloc[index, 0] = str(mode(literal_eval(data.iloc[index, 0])))
      building_type = codes[data.iloc[index, 0]][0]
      data.iloc[index, 0] = building_type

  for index, row in enumerate(data["Property_Code"]):
    if row == "Unknown":
      hcad_code = data.iloc[index, 0]
      data.iloc[index, 15] = hcad_code


if __name__ == "__main__":
  merged_data = pd.read_csv('Full_Merged_Data.csv')

  # Filter irrelevant rows
  merged_data = merged_data[
    ['bld_num', 'impr_mdl_cd', 'dscr', 'date_erected', 'yr_remodel', 'act_ar',
     'tot_inc', 'tot_appr_val', 'bld_ar', 'land_ar',
     'STADDRESS_x', 'PlaceKey ID', 'Result', 'InspectionStatus',
     'Total_Inspections', 'Total_Incidents', 'Total_Violations',
     'Property_Code',
     'incidentTime_1yr', 'incidentTime_2yr', 'incidentTime_5yr',
     'inspectTime_1yr', 'inspectTime_2yr', 'inspectTime_5yr',
     'Fire_Spread_Mean',
     'Binary_Property_Lost', 'True_Incident', 'IncidentStatus',
     'Action Taken: Hazardous Condition', 'Action Taken: Investigation',
     'Action Taken: EMS and Transport',
     'Action Taken: Assistance', 'Action Taken: FireControl',
     'Action Taken: Search & Rescue', 'Action Taken: Fire Rescues',
     'Action Taken: Fill-in, Standby',
     'Action Taken: None', 'Action Taken: Services']]

  # Building Quantity feature engineering
  buildings = merged_data['bld_num']
  buildings_exist = buildings.isnull()
  build_count = []

  for idx, val in buildings.iteritems():
    # Unknown buildings
    if buildings_exist[idx]:
      build_count.append(0)

    # Known buildings
    elif not buildings_exist[idx]:
      num_buildings = len(literal_eval(val))
      if num_buildings <= 1:
        build_count.append(1)
      else:
        build_count.append(2)

  merged_data['BuildingQuantity'] = build_count
  merged_data = merged_data.drop(['bld_num'], axis=1)

  # Building Remodel feature engineering
  remodel = merged_data['yr_remodel']
  remodel_exist = remodel.isnull()
  remodeled = []

  for idx, val in remodel.iteritems():
    # Unknown remodeling
    if remodel_exist[idx]:
      remodeled.append(0)
    else:
      # Remodeled
      if len(literal_eval(val)) > 1:
        remodeled.append(2)

      elif len(literal_eval(val)) == 1:
        # Not remodeled
        if int(literal_eval(val)[0]) <= 0:
          remodeled.append(1)
        # Remodeled
        elif int(literal_eval(val)[0]) > 0:
          remodeled.append(2)
      else:
        remodeled.append(0)

  merged_data['RemodelStatus'] = remodeled
  merged_data = merged_data.drop(['yr_remodel'], axis=1)

  # Update property code
  hcad_property_dict_inv = {}
  for category, code_list in hcad_property_dict.items():
    for x in code_list:
      hcad_property_dict_inv.setdefault(str(x), []).append(category)
  update_property_code(merged_data)

  # buildingCondition Variable
  # Transforming dscr variable with a numerical description of building quality
  # Numbers were assigned as follows: Very Low = 1, Low = 2, Average = 3, Good = 4, Excellent = 5
  # For properties with multiple descriptors, the lowest/worst descriptor was used
  # For properties with no descriptors, they were assigned Average = 3
  dscr_col = merged_data.loc[:, 'dscr']
  buildingCondition = []
  for row in dscr_col:
    if type(row) == float:
      dscr_val = 3
    elif row.find('Very Low') >= 0:
      dscr_val = 1
    elif row.find('Low') >= 0:
      dscr_val = 2
    elif row.find('Average') >= 0:
      dscr_val = 3
    elif row.find('Good') >= 0:
      dscr_val = 4
    elif row.find('Excellent') >= 0:
      dscr_val = 5
    else:
      dscr_val = 3
    buildingCondition.append(dscr_val)
  merged_data["buildingCondition"] = buildingCondition

  # Building area summing
  bld_ar = "act_ar"
  tot_bld_ar = "tot_act_ar"
  merged_data = sum_data_column_list(merged_data, bld_ar, tot_bld_ar)

  output_to_csv(merged_data, "hcad_engineered_data", keep_index=False)

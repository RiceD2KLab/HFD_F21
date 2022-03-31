
from ast import literal_eval
import numpy as np
import pandas as pd
from numpy import NaN, nan
import re
from statistics import mode, mean
import math

from feature_engineering.feature_engineering_main import add_binary_feature

data = pd.read_csv('Full_Merged_Data.csv')

new_data = data[['bld_num', 'impr_mdl_cd', 'dscr', 'date_erected', 'yr_remodel', 'act_ar', 'tot_inc', 'tot_appr_val', 'bld_ar', 'land_ar', 
'STADDRESS_x', 'PlaceKey ID', 'Result', 'InspectionStatus', 'Total_Inspections', 'Total_Incidents', 'Total_Violations', 'Property_Code', 
'incidentTime_1yr', 'incidentTime_2yr', 'incidentTime_5yr', 'inspectTime_1yr', 'inspectTime_2yr', 'inspectTime_5yr', 'Fire_Spread_Mean',
'Binary_Property_Lost', 'True_Incident', 'IncidentStatus', 'Action Taken: Hazardous Condition', 'Action Taken: Investigation', 'Action Taken: EMS and Transport',
'Action Taken: Assistance', 'Action Taken: FireControl', 'Action Taken: Search & Rescue', 'Action Taken: Fire Rescues', 'Action Taken: Fill-in, Standby',
'Action Taken: None', 'Action Taken: Services']]

#Building Quantity Variable

buildings = new_data['bld_num']
buildings_exist = buildings.isnull()
build_count = []

for idx, val in buildings.iteritems():
    #Unknown buildings
    if buildings_exist[idx] == True:
        build_count.append(0)
    
    #Known buildings
    elif buildings_exist[idx] == False:
        blds = len(literal_eval(val))
         #Single-building property
        if blds <= 1:
            build_count.append(1)
        #Multi-builidng property
        elif blds > 1:
            build_count.append(2)
   
new_data['BuildingQuantity'] = build_count
new_data = new_data.drop(['bld_num'], axis=1)

#Building Remodel Variable

remodel = new_data['yr_remodel']
remodel_exist = remodel.isnull()
remodeled = []

for idx, val in remodel.iteritems():
    #Unknown remodeling
    if remodel_exist[idx] == True:
        remodeled.append(0)
    
    elif remodel_exist[idx] == False:
        #Remodeled
        if len(literal_eval(val)) > 1:
            remodeled.append(2)
        
        elif len(literal_eval(val)) == 1:
            #Not remodeled
            if int(literal_eval(val)[0]) == 0:
                remodeled.append(1)
            #Remodeled
            elif int(literal_eval(val)[0]) > 0:
                remodeled.append(2)

new_data['RemodelStatus'] = remodeled
new_data = new_data.drop(['yr_remodel'], axis=1)

#new_data.to_csv('Working_Data_033022.csv', index=0)






















import pandas as pd
from sklearn.metrics import balanced_accuracy_score

from feature_engineering.hcad_engineering import date_erected

data = pd.read_csv('Working_Data_040422.csv')

#Drop old columns
data = data.drop(['dscr', 'act_ar'], axis=1)

#date_erected to integer
date_erected = data['date_erected']
de_null = date_erected.isnull()
new_de = []

for idx, val in date_erected.iteritems():
    if de_null[idx] == False:
        new_de.append(int(val))
    
    elif de_null[idx] == True:
        new_de.append(val)

data['date_erected'] = new_de

#Subset data for non-null HCAD
hcad_data = data[['impr_mdl_cd', 'date_erected', 'tot_inc', 'bld_ar', 'land_ar', 'STADDRESS_x', 'tot_act_ar']]
hcad_null = hcad_data.isnull()
rows_to_drop = []

for idx, row in hcad_null.iterrows():
   if list(row) == [True, True, True, True, True, True, True]:
       rows_to_drop.append(idx)

model_data = data.drop(rows_to_drop, axis=0)

#Drop remaining features with 10,000< unpopulated rows
model_data = model_data.drop(['Result', 'Fire_Spread_Mean', 'Binary_Property_Lost'], axis=1)

#Export
model_data.to_csv('Modeling_Data_04052022.csv', index=0)
#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


#import both the 2020 and 2021 datasets into dataframes
data2020 = pd.read_csv(r"Address_&_Violation_Records_data 2020.csv")
data2021 = pd.read_csv(r"Address_&_Violation_Records_data 2021.csv")

#drop the column STARTDTTM in 2021 as it is unavailable in 2020 dataset; 2020 - 65k records 2021 -16k records
data2021.drop('STARTDTTM', axis=1, inplace=True)

#combine both the years data 
Violation_data = data2020.append(data2021, ignore_index = True)

Violation_data.head()


# In[2]:


#Check the counts for the unique values in the column Remove Duplication 
Violation_data['Remove Duplication'].value_counts()
# all 81561 rows have the same value; Hence this will not be useful

#drop the Remove Duplication column as it is not useful
Violation_data.drop('Remove Duplication', axis=1, inplace=True)


# In[3]:


#Check the counts for the unique values in the column Code
Violation_data['Code'].value_counts(dropna = False)


# In[4]:


#To avoid the NaN replace the instances with NoData
Violation_data['Code'] = Violation_data['Code'].fillna("NoData")
Violation_data['Code'].value_counts()


# In[5]:


#Check the counts for the unique values in the column DESCRIPT
Violation_data['DESCRIPT'].value_counts(dropna=False)


# In[6]:


#confirming there are no NaN values
Violation_data['DESCRIPT'].isna().sum()


# In[7]:


#Violation_data['FULLNAME'].isna().sum() # -> 2890rows

##Check the counts for the unique values in the column FULLNAME
Violation_data['FULLNAME'].value_counts(dropna=False)

Violation_data['FULLNAME'].nunique() #140 unique FULLNAME 's are present

#Replace the NaN with noData
Violation_data['FULLNAME'] = Violation_data['FULLNAME'].fillna('NoData')


# In[8]:


#Check the number of NaN 's in GPSX
Violation_data['GPSX'].isna().sum() #122 -> Instances

#Replace the Instances with 0.0
Violation_data['GPSX'] = Violation_data['GPSX'].fillna(0.0)

#Change the type from float to int
Violation_data['GPSX'] = Violation_data['GPSX'].astype(int)

#Check the datatype
Violation_data['GPSX'].dtype


# In[10]:


unique_GPSX_Values = Violation_data['GPSX'].value_counts()

# Create a dataframe that can be used to plot the variation between x coordinates
df_unique_GPSX_Values = pd.DataFrame(unique_GPSX_Values)
df_unique_GPSX_Values_reset = df_unique_GPSX_Values.reset_index()
df_unique_GPSX_Values_reset.columns = ['unique_GPSX_Values', 'count']
df_unique_GPSX_Values_reset

import matplotlib.pyplot as plt

#plot a bar graph
plt.bar(df_unique_GPSX_Values_reset['unique_GPSX_Values'], df_unique_GPSX_Values_reset['count'], color = 'red',width=200)
plt.ylim([0,25])
plt.xlim([2500000, 3400000])
plt.locator_params(axis='x', nbins=5)
plt.show()


# In[11]:


#Check the number of NaN 's in GPSX
Violation_data['GPSY'].isna().sum()

#Replace the Instances with 0.0
Violation_data['GPSY'] = Violation_data['GPSY'].fillna(0.0)

#Change the type from float to int
Violation_data['GPSY'] = Violation_data['GPSY'].astype(int)

#Check the datatype
Violation_data['GPSY'].dtype


# In[12]:


unique_GPSY_Values = Violation_data['GPSY'].value_counts()

# Create a dataframe that can be used to plot the variation between y coordinates
df_unique_GPSY_Values = pd.DataFrame(unique_GPSY_Values)
df_unique_GPSY_Values_reset = df_unique_GPSY_Values.reset_index()
df_unique_GPSY_Values_reset.columns = ['unique_GPSY_Values', 'count']
df_unique_GPSY_Values_reset

import matplotlib.pyplot as plt

#plot a bar graph
plt.bar(df_unique_GPSY_Values_reset['unique_GPSY_Values'], df_unique_GPSY_Values_reset['count'], color = 'red',width=2000)
plt.ylim([0,25])
plt.xlim([13000000 , 14000000])
plt.locator_params(axis='x', nbins=5)
plt.show()


# In[13]:


#Drop the rows where violation data is 0,1  in both GPSX and GPSY


Violation_data_drop_GPS = Violation_data

#drop rows where GPSX value is 0
Violation_data_drop_GPS.drop(Violation_data_drop_GPS.loc[Violation_data_drop_GPS['GPSX']==0].index, inplace=True)
#drop rows where GPSX value is 1
Violation_data_drop_GPS.drop(Violation_data_drop_GPS.loc[Violation_data_drop_GPS['GPSX']==1].index, inplace=True)
#drop rows where GPSY value is 0
Violation_data_drop_GPS.drop(Violation_data_drop_GPS.loc[Violation_data_drop_GPS['GPSY']==0].index, inplace=True)
#drop rows where GPSY value is 1
Violation_data_drop_GPS.drop(Violation_data_drop_GPS.loc[Violation_data_drop_GPS['GPSY']==1].index, inplace=True)


# In[14]:


# Cleaning GPSZ

Violation_data_drop_GPS['GPSZ'].isna().sum()

Violation_data_drop_GPS['GPSZ'].value_counts()

# as the places where GPSZ is 1 GPSX and GPSY correspondingly are 1 aswell hence we can drop this column
Violation_data_drop_GPS.drop('GPSZ', axis=1, inplace=True)


# In[15]:


#Handing back the GPS changes back to Violation Data
Violation_data = Violation_data_drop_GPS


# In[16]:


#Clean INSPTYPECAT data
Violation_data['INSPTYPECAT'].value_counts(dropna = False)

#Fill the empty INSPTYPECAT with NoData
Violation_data['INSPTYPECAT'] = Violation_data['INSPTYPECAT'].fillna('NoData')

Violation_data['INSPTYPECAT'].isna().sum()


# In[17]:


##Check the counts for the unique values in the column INSPTYPE
Violation_data['INSPTYPE'].value_counts(dropna = False)
Violation_data['INSPTYPE'].value_counts(dropna = False).sum()

#As there are no empty values no changes need to be made for INSPTYPE


# In[18]:


Violation_data['LOC'] = Violation_data['LOC'].fillna('NoData')
Violation_data['LOC'].value_counts(dropna = False)
#Violation_data['LOC'].value_counts(dropna = False).sum()


# In[19]:


Violation_data['Location'] = Violation_data['Location'].fillna('NoData')

Violation_data['Location'].value_counts(dropna = False)

Violation_data[['LOC','Location']]
# need to merge LOC and Location


# In[20]:


filter_NoData_in_LOC = Violation_data["LOC"]!="NoData"
filter_NoData_in_Location = Violation_data['Location']!="NoData"
  
# filtering data
merge_LOC_data = Violation_data.where(filter_NoData_in_LOC | filter_NoData_in_Location)


# In[21]:


# move the data for LOC and Location to a different dataframe
merge_LOC_data2 = merge_LOC_data[['LOC','Location']]

merge_LOC_data2 = merge_LOC_data2.dropna()
merge_LOC_data2


# In[22]:


'''
function to return value from LOC or Location depending on if data is present in the counterpart; If not return appended
'''

def location_value(row):
    if row['LOC'] != 'NoData' and row['Location'] != 'NoData':
        return row['LOC'] + row['Location']
    elif row['Location'] != 'NoData' :
        return row['Location']
    elif row['LOC'] != 'NoData' :
        return row['LOC'] 
    
merge_LOC_data2['LOC_Location_Combi'] = merge_LOC_data2.apply( lambda row : location_value(row), axis = 1)


# In[23]:




merge_LOC_data2 = pd.DataFrame(merge_LOC_data2, columns=['LOC_Location_Combi'])
merge_LOC_data2

#merge back the combined roe for LOC and Location as LOC_Location_Combi column
Violation_data = Violation_data.merge(merge_LOC_data2, how='outer', left_index=True, right_index=True)


Violation_data['LOC_Location_Combi'] = Violation_data['LOC_Location_Combi'].fillna('NoData')

#Violation_data.to_excel('ViolationCleaned2020and2021.xlsx', encoding='utf-8-sig')


# In[24]:


data2021.drop('LOC', axis=1, inplace=True)
data2021.drop('Location', axis=1, inplace=True)
Violation_data.to_excel('ViolationCleaned2020and2021.xlsx', encoding='utf-8-sig')


# In[29]:


# drop LOC and Location as we have a combined column
Violation_data.drop('LOC', axis=1, inplace=True)
Violation_data.drop('Location', axis=1, inplace=True)
Violation_data['LOC_Location_Combi'].value_counts()


# In[34]:


#Drop Number of Records Column as this has only 1 type of value in all the rows
Violation_data['Number of Records'].value_counts(dropna = False)
#Violation_data_drop_GPS.drop(Violation_data_drop_GPS['Number of Records'])
Violation_data.drop('Number of Records', axis=1, inplace=True)


# In[36]:


#Fill occupancy type with NoData if NaN is present
Violation_data['OCCUPANCYTYPE'] = Violation_data['OCCUPANCYTYPE'].fillna('NoData')
Violation_data['OCCUPANCYTYPE'].value_counts(dropna = False)


# In[37]:


Violation_data['PREDIR'] = Violation_data['PREDIR'].fillna('NoData')
Violation_data['PREDIR'].value_counts(dropna = False)


# In[38]:


Violation_data.to_excel('Clean_data_till_PREDIR.xlsx', encoding='utf-8')


# In[39]:


Violation_data.head()







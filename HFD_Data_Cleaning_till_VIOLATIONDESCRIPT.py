#!/usr/bin/env python
# coding: utf-8

# In[7]:


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


# In[8]:


Violation_data.shape
# dataset has 81561 rows


# In[9]:


#Check the counts for the unique values in the column Remove Duplication 
Violation_data['Remove Duplication'].value_counts()
# all 81561 rows have the same value; Hence this will not be useful

#drop the Remove Duplication column as it is not useful
Violation_data.drop('Remove Duplication', axis=1, inplace=True)


# In[10]:


#Check the counts for the unique values in the column Code
Violation_data['Code'].value_counts(dropna = False)


# In[11]:


#To avoid the NaN replace the instances with NoData
Violation_data['Code'] = Violation_data['Code'].fillna("NoData")

#create a bar graph based on the occurences of each code of violation
Violation_data['Code'].value_counts().plot(kind='barh')


# In[12]:


#create a bar graph based on the occurences of top 6 codes of violation
import matplotlib.pyplot as plt
import seaborn as sns
Violation_code  = Violation_data['Code'].value_counts()
Violation_code = Violation_code[:6,]
plt.figure(figsize=(10,5))
sns.barplot(Violation_code.index, Violation_code.values, alpha=0.8)
plt.title("Distribution of the 6 most occuring Violation Code's in the data")
plt.ylabel('Number of Occurrences', fontsize=12)
plt.xlabel('Violation Code', fontsize=12)
plt.show()


# In[13]:


#Check the counts for the unique values in the column DESCRIPT
Violation_data['DESCRIPT'].value_counts(dropna=False)


# In[14]:


Violation_data['DESCRIPT'].value_counts(dropna=False).sum() # 81561 rows

Violation_data.shape


# In[94]:


#create a bar graph based on the inspection decriptions of all the violation data
Violation_descript  = Violation_data['DESCRIPT'].value_counts()
Violation_descript = Violation_descript[:9,]
plt.figure(figsize=(20,5))
sns.barplot(Violation_descript.index, Violation_descript.values, alpha=0.8)
plt.title("Distribution of the 9 most occuring Inspection Description's in the data")
plt.ylabel('Number of Occurrences', fontsize=12)
plt.xlabel('Inspection Description', fontsize=12)
plt.show()


# In[16]:


#confirming there are no NaN values
Violation_data['DESCRIPT'].isna().sum()


# In[17]:


#Violation_data['FULLNAME'].isna().sum() # -> 2890rows

##Check the counts for the unique values in the column FULLNAME
Violation_data['FULLNAME'].value_counts(dropna=False)

Violation_data['FULLNAME'].nunique() #140 unique FULLNAME 's are present

#Replace the NaN with noData
Violation_data['FULLNAME'] = Violation_data['FULLNAME'].fillna('NoData')


# In[18]:


#Check the number of NaN 's in GPSX
Violation_data['GPSX'].isna().sum() #122 -> Instances

#Replace the Instances with 0.0
Violation_data['GPSX'] = Violation_data['GPSX'].fillna(0.0)

#Change the type from float to int
Violation_data['GPSX'] = Violation_data['GPSX'].astype(int)

#Check the datatype
Violation_data['GPSX'].dtype


# In[25]:


#Check the number of NaN 's in GPSX
Violation_data['GPSY'].isna().sum()

#Replace the Instances with 0.0
Violation_data['GPSY'] = Violation_data['GPSY'].fillna(0.0)

#Change the type from float to int
Violation_data['GPSY'] = Violation_data['GPSY'].astype(int)

#Check the datatype
Violation_data['GPSY'].dtype


# In[27]:


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


# In[37]:


unique_GPSX_Values = Violation_data_drop_GPS['GPSX'].value_counts()

# Create a dataframe that can be used to plot the variation between x coordinates
df_unique_GPSX_Values = pd.DataFrame(unique_GPSX_Values)
df_unique_GPSX_Values_reset = df_unique_GPSX_Values.reset_index()
df_unique_GPSX_Values_reset.columns = ['unique_GPSX_Values', 'count']
df_unique_GPSX_Values_reset

#plot a bar graph
plt.bar(df_unique_GPSX_Values_reset['unique_GPSX_Values'], df_unique_GPSX_Values_reset['count'], color = 'red',width=2000)
plt.ylim([df_unique_GPSX_Values_reset['count'].min(),df_unique_GPSX_Values_reset['count'].max()])
plt.xlabel('GPSX value')
plt.ylabel('counts')
plt.locator_params(axis='x', nbins=5)
plt.show()


# In[39]:


unique_GPSY_Values = Violation_data_drop_GPS['GPSY'].value_counts()

# Create a dataframe that can be used to plot the variation between y coordinates
df_unique_GPSY_Values = pd.DataFrame(unique_GPSY_Values)
df_unique_GPSY_Values_reset = df_unique_GPSY_Values.reset_index()
df_unique_GPSY_Values_reset.columns = ['unique_GPSY_Values', 'count']
df_unique_GPSY_Values_reset

#plot a bar graph
plt.bar(df_unique_GPSY_Values_reset['unique_GPSY_Values'], df_unique_GPSY_Values_reset['count'], color = 'red',width=2000)
plt.ylim([df_unique_GPSY_Values_reset['count'].min(),df_unique_GPSY_Values_reset['count'].max()])
plt.xlabel('GPSY value')
plt.ylabel('counts')
plt.locator_params(axis='x', nbins=5)
plt.show()


# In[40]:


# Cleaning GPSZ

Violation_data_drop_GPS['GPSZ'].isna().sum()

Violation_data_drop_GPS['GPSZ'].value_counts()

# as the places where GPSZ is 1 GPSX and GPSY correspondingly are 1 aswell hence we can drop this column
Violation_data_drop_GPS.drop('GPSZ', axis=1, inplace=True)


# In[41]:


#Handing back the GPS changes back to Violation Data
Violation_data = Violation_data_drop_GPS


# In[42]:


#Clean INSPTYPECAT data
Violation_data['INSPTYPECAT'].value_counts(dropna = False)

#Fill the empty INSPTYPECAT with NoData
Violation_data['INSPTYPECAT'] = Violation_data['INSPTYPECAT'].fillna('NoData')

Violation_data['INSPTYPECAT'].isna().sum()


# In[43]:


Violation_data['INSPTYPECAT'].value_counts(dropna = False)

#Create a bar graph for the Inspection type categories in the data
Violation_INSPTYPECAT  = Violation_data['INSPTYPECAT'].value_counts()
Violation_INSPTYPECAT = Violation_INSPTYPECAT[:7,]
plt.figure(figsize=(17,5))
sns.barplot(Violation_INSPTYPECAT.index, Violation_INSPTYPECAT.values, alpha=0.8)
plt.title("Distribution of the 7 most occuring Violation Inspection Type Category")
plt.ylabel('Number of Occurrences', fontsize=12)
plt.xlabel("Violation inspection Type categories")
plt.show()


# In[44]:


#Check the counts for the unique values in the column INSPTYPE
Violation_data['INSPTYPE'].value_counts(dropna = False)
#Violation_data['INSPTYPE'].value_counts(dropna = False).sum()

#As there are no empty values no changes need to be made for INSPTYPE
Violation_INSPTYPE  = Violation_data['INSPTYPE'].value_counts()
Violation_INSPTYPE = Violation_INSPTYPE[:10,]
plt.figure(figsize=(17,5))
sns.barplot(Violation_INSPTYPE.index, Violation_INSPTYPE.values, alpha=0.8)
plt.title("Distribution of the 8 Violation Inspection Type's")
plt.ylabel('Number of Occurrences', fontsize=12)
plt.xlabel("Violation inspection Type's from the column 'INSPTYPE'")
plt.show()


# In[45]:


#Distribution of Inspection Type amongst the data
Violation_data['INSPTYPE'].value_counts(dropna = False)


# In[46]:


Violation_data['LOC'] = Violation_data['LOC'].fillna('NoData')
Violation_data['LOC'].value_counts(dropna = False)
#Violation_data['LOC'].value_counts(dropna = False).sum()


# In[47]:


Violation_data['Location'] = Violation_data['Location'].fillna('NoData')

Violation_data['Location'].value_counts(dropna = False)

Violation_data[['LOC','Location']]
# need to merge LOC and Location


# In[48]:


filter_NoData_in_LOC = Violation_data["LOC"]!="NoData"
filter_NoData_in_Location = Violation_data['Location']!="NoData"
  
# filtering data
merge_LOC_data = Violation_data.where(filter_NoData_in_LOC | filter_NoData_in_Location)


# In[49]:


# move the data for LOC and Location to a different dataframe
merge_LOC_data2 = merge_LOC_data[['LOC','Location']]

merge_LOC_data2 = merge_LOC_data2.dropna()
merge_LOC_data2


# In[50]:


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


# In[51]:




merge_LOC_data2 = pd.DataFrame(merge_LOC_data2, columns=['LOC_Location_Combi'])
merge_LOC_data2

#merge back the combined roe for LOC and Location as LOC_Location_Combi column
Violation_data = Violation_data.merge(merge_LOC_data2, how='outer', left_index=True, right_index=True)


Violation_data['LOC_Location_Combi'] = Violation_data['LOC_Location_Combi'].fillna('NoData')

#Violation_data.to_excel('ViolationCleaned2020and2021.xlsx', encoding='utf-8-sig')


# In[52]:


data2021.drop('LOC', axis=1, inplace=True)
data2021.drop('Location', axis=1, inplace=True)
Violation_data.to_excel('ViolationCleaned2020and2021.xlsx', encoding='utf-8-sig')


# In[53]:


# drop LOC and Location as we have a combined column
Violation_data.drop('LOC', axis=1, inplace=True)
Violation_data.drop('Location', axis=1, inplace=True)
Violation_data['LOC_Location_Combi'].value_counts()


# In[54]:


#Drop Number of Records Column as this has only 1 type of value in all the rows
Violation_data['Number of Records'].value_counts(dropna = False)
#Violation_data_drop_GPS.drop(Violation_data_drop_GPS['Number of Records'])
Violation_data.drop('Number of Records', axis=1, inplace=True)


# In[55]:


#Fill occupancy type with NoData if NaN is present
Violation_data['OCCUPANCYTYPE'] = Violation_data['OCCUPANCYTYPE'].fillna('NoData')
Violation_data['OCCUPANCYTYPE'].value_counts(dropna = False)


# In[56]:


Violation_data['PREDIR'] = Violation_data['PREDIR'].fillna('NoData')
Violation_data['PREDIR'].value_counts(dropna = False)


# In[29]:


Violation_data.to_excel('Clean_data_till_PREDIR.xlsx', encoding='utf-8')


# In[87]:


Violation_data.head()


# In[57]:


Violation_data['RESULTBY'].value_counts(dropna = False)
Violation_data['RESULTBY'].nunique()
Violation_data['RESULTBY'] = Violation_data['RESULTBY'].fillna('NoData')
#Violation_data_drop_GPS['RESULTBY'].unique()


# In[58]:



#Violation_data['SUPERVISOR'].nunique()
Violation_data['SUPERVISOR'] = Violation_data['SUPERVISOR'].fillna('NoData')
Violation_data['SUPERVISOR'].value_counts(dropna = False)


# In[62]:


Violation_data['TEAMCODE'].value_counts(dropna = False)
Violation_data['TEAMCODE'] = Violation_data['TEAMCODE'].fillna('NoData')
Violation_data['TEAMCODE'].value_counts(dropna = False)
#Violation_data['TEAMDESCRIPTION'].value_counts(dropna = False)


# In[66]:


#Bar chart for the number of cases performed by each type of team
Violation_TEAMCODE  = Violation_data['TEAMCODE'].value_counts()
Violation_TEAMCODE = Violation_TEAMCODE[:11,]
plt.figure(figsize=(17,5))
sns.barplot(Violation_TEAMCODE.index, Violation_TEAMCODE.values, alpha=0.8)
plt.title("Distribution of case's for each Team")
plt.ylabel('Number of Cases', fontsize=12)
plt.xlabel("Name of each Team")
plt.show()


# In[67]:



Violation_data['TEAMDESCRIPTION'] = Violation_data['TEAMDESCRIPTION'].fillna('NoData')

Violation_data['TEAMDESCRIPTION'].value_counts(dropna = False)


# In[68]:


Violation_TEAMDESCRIPTION  = Violation_data['TEAMDESCRIPTION'].value_counts()
Violation_TEAMDESCRIPTION = Violation_TEAMDESCRIPTION[:11,]
plt.figure(figsize=(17,5))
sns.barplot(Violation_TEAMDESCRIPTION.index, Violation_TEAMDESCRIPTION.values, alpha=0.8)
plt.title("Distribution of case's for each Team")
plt.ylabel('Number of Occurrences', fontsize=12)
plt.xlabel("Cases for each Team Code")
plt.show()


# In[69]:


#Creating the maping for each acronym for Team
Violation_TEAMDESCRIPTION.index
Violation_TEAMCODE.index

list1 = []
list2 = []
for i in Violation_TEAMDESCRIPTION.index:
    list1.append(i)
for i in Violation_TEAMCODE.index:
    list2.append(i)
    
dictionary = dict(zip(list2, list1))
dictionary


# In[70]:


Emp_Data = Violation_data[['FULLNAME','RESULTBY','SUPERVISOR','TEAMDESCRIPTION']]
unique_Emp_Data = []
#unique_Name


#unique_Emp_Data
Emp_Data = pd.DataFrame(Emp_Data)
for row in Emp_Data.iterrows():

    check = row[1].tolist()
    #print(check)

    if check not in unique_Emp_Data:
        unique_Emp_Data.append(check)
        
unique_Emp_Data


# In[118]:


unique_Emp_Data = pd.DataFrame(unique_Emp_Data)
unique_Emp_Data.columns=['FULLNAME','EMP_NO','SUPERVISOR','TEAMDESCRIPTION']
unique_Emp_Data.to_csv('unique_Emp_Data_with_team_description.csv')


# In[71]:


#unique_Emp_Data.groupby('')
team_distribution = pd.read_csv('unique_Emp_Data_with_team_description.csv')
team_distribution  = team_distribution.groupby(by = ['TEAMDESCRIPTION']).count()
#team_distribution['index']
team_distribution['FULLNAME']


# In[76]:


#Create a dataframe that groups the data into Teams in first level then groups them based on the supervisor.
team_distribution2 = pd.read_csv('unique_Emp_Data_with_team_description.csv')
team_distribution = team_distribution2.groupby(['TEAMDESCRIPTION','SUPERVISOR'])['FULLNAME'].count()
team_distribution


# In[79]:


#Then write the data to a csv for further exploration using trees
team_distribution = team_distribution2.groupby(['TEAMDESCRIPTION','SUPERVISOR','FULLNAME'])['EMP_NO'].count()
team_distribution.columns=['TEAMDESCRIPTION','SUPERVISOR','FULLNAME']
team_distribution.to_csv('unique_Emp_Data_with_team_description_categorized.csv')


# In[90]:


#read from the csv to plot based onn the team composition
team = pd.read_csv('unique_Emp_Data_with_team_description_categorized.csv')
team_distribution = team['TEAMDESCRIPTION'].value_counts().plot(kind = 'pie')
# pie chart based on the number of team members in each team


# In[93]:


#plot the team distrbution graph based on number of members
team_distribution = team['TEAMDESCRIPTION'].value_counts().plot(kind = 'bar')
plt.xlabel('Team names')
plt.xlabel('Number of members in the team')
plt.show()


# In[100]:


#Clean the Violation Status column
Violation_data['ViolationStatus'].value_counts(dropna = False)

Violation_data['ViolationStatus'] = Violation_data['ViolationStatus'].fillna('NoData')

Violation_data['ViolationStatus'].value_counts()


# In[118]:


#create a bar graph where the frequency of violation codes are represented
from matplotlib.pyplot import figure

figure(figsize=(8, 6), dpi=80)
Violation_data['VIOLATIONCode - Split 1'].value_counts(dropna = False)
Violation_data['VIOLATIONCode - Split 1'] = Violation_data['VIOLATIONCode - Split 1'].fillna('NoData')
Violation_data['VIOLATIONCode - Split 1'].value_counts().plot(kind='bar')
plt.xlabel('violation code')
plt.ylabel('frequency')


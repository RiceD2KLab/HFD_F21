#!/usr/bin/env python
# coding: utf-8

# In[12]:


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


# In[15]:





# In[16]:


import re
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  cleantext = cleantext.replace('&nbsp;','')
  cleantext = cleantext.replace('***','')
  cleantext = cleantext.replace('**','')
  cleantext = cleantext.replace('*','')
  cleantext = cleantext.replace('\r','')
  return cleantext


# In[22]:


#fill the empty data rows with NoData

Violation_data.ViolationComment = Violation_data.ViolationComment.fillna("NoData")

#apply the above created function to the data inorder to clean the HTML that has permeated through the comments

def apply_complex_function(x): return cleanhtml(x['ViolationComment'])

Violation_data['ViolationComment'] = Violation_data.apply(apply_complex_function, axis=1)

#get the result out in excel 

Violation_data.to_excel('ViolationComment2020and2021new.xlsx', encoding='utf-8-sig')

Violation_data['ViolationComment'].to_excel('ViolationComment2020and2021_onlyComments.xlsx', encoding='utf-8-sig')


# In[18]:





# In[20]:





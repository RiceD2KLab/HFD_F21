#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import re
import csv
from wordcloud import WordCloud

# ==================== VIOLATION COMMENT CLEANING CODE FOR WORDCLOUD =====================

# #import both the 2020 and 2021 datasets into dataframes
# data2020 = pd.read_csv(r"Address_&_Violation_Records_data 2020.csv")
# data2021 = pd.read_csv(r"Address_&_Violation_Records_data 2021.csv")

# #drop the column STARTDTTM in 2021 as it is unavailable in 2020 dataset; 2020 - 65k records 2021 -16k records
# data2021.drop('STARTDTTM', axis=1, inplace=True)

# #combine both the years data 
# Violation_data = data2020.append(data2021, ignore_index = True)

# Violation_data.head()


# def cleanhtml(raw_html):
#   cleanr = re.compile('<.*?>')
#   cleantext = re.sub(cleanr, '', raw_html)
#   cleantext = cleantext.replace('&nbsp;','')
#   cleantext = cleantext.replace('***','')
#   cleantext = cleantext.replace('**','')
#   cleantext = cleantext.replace('*','')
#   cleantext = cleantext.replace('\r','')
#   return cleantext

# # In[22]:

# #fill the empty data rows with NoData

# Violation_data.ViolationComment = Violation_data.ViolationComment.fillna("NoData")

# #apply the above created function to the data inorder to clean the HTML that has permeated through the comments

# def apply_complex_function(x): return cleanhtml(x['ViolationComment'])

# Violation_data['ViolationComment'] = Violation_data.apply(apply_complex_function, axis=1)

# #get the result out in excel 

# Violation_data.to_excel('ViolationComment2020and2021new.xlsx', encoding='utf-8-sig')
# Violation_data_new = Violation_data[['ViolationComment', 'TEAMCODE', 'FULLNAME']]
# Violation_data_by_team = Violation_data_new.groupby(by='TEAMCODE')
# Violation_data_new.to_excel('ViolationComment2020and2021_groupbyTEAMCODE.xlsx', encoding='utf-8-sig')


# ======================================== WORD CLOUD ============================================

#read first column of csv file to string of words seperated
#by tab
# TODO: change csv file name to generate word cloud for violations for each 'TEAMCODE' or building type
# format of csv file is: 'violation_[TEAMCODE]'

# Building Codes:
# violation_HighRise.csv 
# violation_APT_HTL.csv
# violation_blankTeamCode.csv
# violation_GO.csv
# violation_HazMatHiPile.csv 
# violation_PlanCk.csv
# violation_SCH_INS.csv
# violation_SpecialOps.csv
# violation_Weekends.csv

# Inspectors:
# violation_JDennis.csv
your_list = [] 
with open('violation_HighRise.csv', 'r') as f:
    reader = csv.reader(f)
    your_list = '\t'.join([i[1] for i in reader])


# Make all strings lowercase and remove insignificant strings

def remove_substring(s, substr):
    # type: (str, str) -> str
    return re.subn(substr, '', s)[0]


new_list = your_list.lower()

new_list = remove_substring(new_list, 'nodata')
new_list = remove_substring(new_list, 'must')
new_list = remove_substring(new_list, 'need')


# Generate a word cloud image
print("NEW LIST: \n", new_list)
wordcloud = WordCloud().generate(new_list)

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

wordcloud = WordCloud(width=2400, height=1200).generate(new_list)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

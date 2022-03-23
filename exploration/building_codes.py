import pandas as pd
import matplotlib as plt
import plotly.express as px
import seaborn as sns

data = pd.read_csv("Full_Merged_Data_TC_Houston.csv")

#Plot 1

data_grouped = data.groupby('Property_Code').count().reset_index()
data_grouped = data_grouped.sort_values(by='Unnamed: 0',ascending=False)


fig = px.bar(data_grouped, x='Property_Code', y='Unnamed: 0',
title="Number of Properties by INFOR Building Types",
            labels={"Property_Code":"Property Type",
            "Unnamed: 0":"Number of Buildings"})

#fig.show()

#Plot 2 

data_grouped.drop(data_grouped[data_grouped['Property_Code'] == "Unknown"].index, inplace=True)

fig = px.bar(data_grouped, x='Property_Code', y='Unnamed: 0',
title="Number of Properties by INFOR Building Types",
            labels={"Property_Code":"Property Type",
            "Unnamed: 0":"Number of Buildings"})

#fig.show()
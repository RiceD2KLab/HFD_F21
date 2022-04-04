import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

data = pd.read_csv('Working_Data_040322.csv')

#Plot 1

data_grouped = data.groupby('Property_Code',as_index=False).size()
data_grouped = data_grouped.sort_values(by='size',ascending=False)

fig = sns.barplot(y='Property_Code',x='size',data=data_grouped)
fig.set(ylabel="Property Type",
            xlabel='Number of Properties',
            title="Number of Properties by INFOR Building Types")

#Plot 2

data_grouped = data.groupby(['Property_Code','InspectionStatus']).size().reset_index().pivot(columns='InspectionStatus', index='Property_Code', values=0)
print(data_grouped)
data_grouped.plot(kind='bar', stacked=True)
plt.xlabel("Property Type")
plt.ylabel("Number of Properties")
plt.legend(labels=['Inspected Since 2005','Not Inspected Since 2005'])
plt.title("Number of Properties by INFOR Building Types and Inspection Status")
plt.show()
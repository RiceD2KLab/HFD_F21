import pandas as pd

## PART 3: Extract statistics for inspection data

inspection = pd.read_csv("INFOR_2018_2021_pk_2.csv")
inspec_num = len(inspection["Inspection #"].unique())
# print(inspec_num)
inspection.drop_duplicates(inplace=True)
# print(len(inspection.index))
cols = ["Inspection Type", "Application Type", "Result", "Section", "Team"]
dfs = []
for col in cols:
    inspection[col] = inspection[col].str.strip().replace("", "N/A").fillna("N/A")
    dfs.append(inspection[col].value_counts().append(pd.Series([inspec_num], index=[col])))
df = pd.concat(dfs)
df.to_csv("Inspection_features.csv")
import pandas as pd

data = pd.read_csv("/Users/tessacannon/Downloads/Full_Merged_Data_YG_Houston.csv")

inspection_binary = data['InspectionStatus']

sum = inspection_binary.sum()

print(len(inspection_binary)-sum)
print(sum)
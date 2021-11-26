import pandas as pd
data = pd.read_excel(r"ViolationCleaned2020and2021.xlsx")
print(data.head())

violation_Distribution_By_Zip_And_TeamCode = data.groupby(["ZIP","TEAMCODE"])["ZIP"].count()

violation_Distribution_By_Zip_And_TeamCode.to_csv("violationDistributionByZipAndTeamCode.csv")
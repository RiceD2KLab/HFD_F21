# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import os

# mount the drive
from google.colab import drive
drive.mount("/content/drive")

# project path in the google drive
path = "/content/drive/Shared drives/DSCI HFD Team Fall 2021/datasets"

os.chdir(path)
os.listdir(path)

data2020 = pd.read_csv(r"Address_&_Violation_Records_data 2020.csv", keep_default_na=False)
data2020.head()


data2021 = pd.read_csv(r"Address_&_Violation_Records_data 2021.csv", keep_default_na=False)
data2021.head()

# merge the full address and delete the unuseful words
data = data2020["STNO"] + " " + data2020["PREDIR"]+ " " + data2020["STNAME"] + " " + data2020["SUFFIX"]+". "+ data2020["CITY"] +", " + data2020["STATE"] + ", " + data2020["ZIP"]
if "NaN " in data:
  data.replace("NaN ", "")


data2020["Full Address"] = data

# export the datasets with full address
os.chdir("/content/drive/Shared drives/DSCI HFD Team Fall 2021/results")
data2020.to_excel(r'Address_&_Violation_Records_data 2020_add_full_address.xlsx', index=False)
data2020.head()

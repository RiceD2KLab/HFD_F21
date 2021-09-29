# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import os
from google.colab import drive
drive.mount("/content/drive")

path = "/content/drive/Shared drives/DSCI HFD Team Fall 2021/datasets"

os.chdir(path)
os.listdir(path)

data2020 = pd.read_csv(r"Address_&_Violation_Records_data 2020.csv", keep_default_na=False)
data2020.head()


data2021 = pd.read_csv(r"Address_&_Violation_Records_data 2021.csv", keep_default_na=False)
data2021.head()


data = data2020["STNO"] + " " + data2020["PREDIR"]+ " " + data2020["STNAME"] + " " + data2020["SUFFIX"]+". "+ data2020["CITY"] +", " + data2020["STATE"] + ", " + data2020["ZIP"]
if "NaN " in data:
  data.replace("NaN ", "")
data

from google.colab import drive
drive.mount('/content/drive')

data2020["Full Address"] = data

os.chdir("/content/drive/Shared drives/DSCI HFD Team Fall 2021/results")
data2020.to_excel(r'Address_&_Violation_Records_data 2020_add_full_address.xlsx', index=False)
data2020.head()

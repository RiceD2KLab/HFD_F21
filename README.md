# Houston Fire Department - SPRING 2022
#### Members: Annita Chang, Joshua Washington, Jarrett Prchal, Tessa Cannon, Yuxin Gong, Ziyana Samanani.

This is our repository that contains the code for our capstone project: <br /> **Analyzing Fire Inspections for the Houston Fire Department**

DISCLAIMER: The Houston Fire Department data is private and cannot be posted to a public repository. In order to run our files and generate diagrams based on the dataset we were given, please locate and download the files `Address_&_Violation_Records_data 2020.csv`, `Address_&_Violation_Records_data 2021.csv`, `INFOR Data by Months`, `Structure Fires 2005-2021`, and `D2K Incident Data July 2018 to JAug 10 2021_Export.csv` from the Data folder in Team HFD Microsoft Teams. We also used three publicly available dataset `building_other.txt`, `real_acct.txt` and `SVI_Harris.csv` that are available on Teams and online.
Incident: `D2K Incident Data July 2018 to JAug 10 2021_Export.csv` under 
Inspection: `INFOR Data by Months`
Violation: `Address_&_Violation_Records_data 2020.csv`, `Address_&_Violation_Records_data 2021.csv`
Struct Fire (fire only incident): `Structure Fires 2005-2021`
HCAD: `building_other.txt`, `real_acct.txt`
SVI: `SVI_Harris.csv`

## Running the code

1. Clone repository to your local machine
2. Install dependencies with the following commands:

```
pip install pandas
pip install argparse
pip install os
pip install typing
pip install placekey
pip install re
pip install enum
pip install glob
pip install numpy
```
## Guide through different directories
data_io: IO modules for processing and data output
wrangling: codes used in data preprocessing
exploration: codes used in visualization
feature_engineering: codes used for generating binary / numeric / categorical variables on different datasets
modeling: code used in our modeling process
interactive map: code used in generating our interactive map

### Data Preprocessing
#### Clean Data
To clean each of the six datasets, run clean_data_name.py under wrangling.
#### Add placekey
To add placekeys to the datasets, run placekey_tagging.py under wrangling.
#### Filter based on Locations
To filter out houston-only properties, run keep_only_houston.py under wrangling.
#### Merge six datasets
To merge datasets, run full_merge.py under wrangling.

### Visualization and Feature Engineering
#### Building Code visualization
Run building_codes.py under exploration to generate building code bar plot in our report.
Run hfd_incident_action_taken.py under feature_engineering to generate HFD action taken plot in our report.
Interactive map has an independent README.md under Interactive map folder.
#### Feature Engineering
Run feature_engineering_main.py unde feature_engineering to generate variables for all datasets other than HCAD. HCAD has its own indepedent feature engineering script: hcad_engineering.py.

### Modeling
Run predictive_modeling.py under modeling to generate our models built.

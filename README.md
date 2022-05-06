# Houston Fire Department - SPRING 2022
#### Members: Tessa Cannon, Annita Chang, Yuxin Gong, Jarrett Prchal, Ziyana Samanani, Joshua Washington

This is the repository that contains the code for our capstone project: <br /> **Analyzing Fire Inspections for the Houston Fire Department**

DISCLAIMER: The Houston Fire Department data is private and cannot be posted to a public repository. In order to run our files and generate diagrams based on the dataset we were given, please locate and download the files from the Data folder in Team HFD Microsoft Teams General Drive. We also used three publicly available datasets `building_other.txt`, `building_res.txt` `real_acct.txt` and `SVI_Harris.csv` that are available on Teams and the [HCAD website](https://hcad.org/pdata/pdata-property-downloads.html).

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

### Data Directory Format
Before running the code, ensure that the project data is mounted to the repository.
For smooth operation, the data should have the following folder structure:

```
Data/
  Address and Violation Records Data/
    Original Datasets/
    Intermediate Datasets/
    Cleaned Datasets/
  Incident Data/
    Original Datasets/
    Intermediate Datasets/
    Cleaned Datasets/
  INFOR Inspection Data/
    Original Datasets/
    Intermediate Datasets/
    Cleaned Datasets/
   Structure Fire Data/
    Original Datasets/
    Intermediate Datasets/
    Cleaned Datasets/
  Public Data/
    HCAD/
      Original Datasets/
      Intermediate Datasets/
      Cleaned Datasets/
    SVI/
      Original Datasets/
      Intermediate Datasets/
      Cleaned Datasets/
  Merged Data/   
```

### Guide through different directories
```
data_io: IO modules for processing and data output
wrangling: codes used in data preprocessing
exploration: codes used in visualization
feature_engineering: codes used for generating binary / numeric / categorical variables on different datasets
modeling: code used in our modeling process
interactive map: code used in generating our interactive map
```
#### Data Preprocessing
##### Clean Data
To clean each of the six datasets, run `clean_<data_name>.py` under `wrangling`.
##### Merge six datasets
To merge datasets, run `full_merge.py` under `wrangling` after the data cleaning has been completed for all datasets.

#### Visualization and Feature Engineering
##### Building Code visualization
Run `building_codes.py` under exploration to generate building code bar plot in our report.
Run `hfd_incident_action_taken.py` under `feature_engineering` to generate HFD action taken plot in our report.
Interactive map has an independent README.md under Interactive map folder.
##### Feature Engineering
The feature engineering code is split between two files: `hfd_engineering.py` and `hcad_engineering.py` in the `feature_engineering` directory.
`hfd_engineering` performs feature engineering based on HFD data, while `hcad_engineering` performs feature engineering based on HCAD data.
For smooth execution of feature engineering, run `hfd_engineering.py` after the merge, followed by `hcad_engineering.py`.

#### Modeling
Run `predictive_modeling.py` under modeling to generate our modeling dataset. The built models are again split between 
two files. Using the dataset created in `predictive_modeling.py` as the imported dataset, run `inspection_models.py` 
to perform the inspection predictive models and `incident_models.py` to perform the incident specific models. 

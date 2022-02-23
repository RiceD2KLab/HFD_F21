# Houston Fire Department - SPRING 2022
#### Members: Annita Chang, Joshua Washington, Jarrett Prchal, Tessa Cannon, Yuxin Gong, Ziyana Samanni.

This is our repository that contains the code for our capstone project: <br /> **Analyzing Fire Inspections for the Houston Fire Department**

DISCLAIMER: The Houston Fire Department data is private and cannot be posted to a public repository. In order to run our files and generate diagrams based on the dataset we were given, please locate and download the files `Address_&_Violation_Records_data 2020.csv`, `Address_&_Violation_Records_data 2021.csv`, `FF--D2K-2021-data_full year 2021.csv`, and `D2K Incident Data July 2018 to JAug 10 2021_Export.csv` from the Team HFD Microsoft Teams.

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

### Data Preprocessing
#### Stack violation and incident data
To stack and clean violation records and incident data, you may run `clean_addressviolation_incident.py` Be sure that the following files can be found in `data/sp22data`:
* `Address_&_Violation_Records_data 2020.csv`
* `Address_&_Violation_Records_data 2021.csv`
* `FF--D2K-2021-data_full year 2021.csv`
* `D2K Incident Data July 2018 to JAug 10 2021_Export.csv`

Running this file will result in the creation of the following cleaned files:
* `Non-Residential Incident Data 2018_2021.csv`
* `Cleaned Addresss and Violation Data 2020_2021.csv`

#### Voilation data comment cleaning
To preprocess the address and violation comments, run `violation_comment_cleanning.py`. Pass in any number of CSV files with comments data to stack and process comments. By default, the cleaned comments data will be output to two separate files:
* `ViolationDataCleanedComments.csv` contains all of the original data with the cleaned comments
* `ViolationDataCleanedComments_comments.csv` contains only cleaned comments data, without the other columns

#### Add Placekey to data rows with address fields
To add Placekeys for locations in the Address and Violation data, run `hfd_data_placekey_tagging.py`. Be sure that `Cleaned Address and Violation Data 2020_2021.csv` is in your working directory. This file will output two separate CSV files:
* `Cleaned Address and Violation Data 2020_2021 Placekey.csv` contains rows with Placekey data
* `Cleaned Address and Violation Data 2020_2021 No Placekey.csv` contains rows for which no Placekeys were obtained

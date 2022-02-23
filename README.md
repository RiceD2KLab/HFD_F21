# Houston Fire Department - SPRING 2022
#### Members: Annita Chang, Joshua Washington, Jarrett Prchal, Tessa Cannon, Yuxin Gong, Ziyana Samanni.

This is our repository that contains the code for our capstone project: <br /> **Analyzing Fire Inspections for the Houston Fire Department**

DISCLAIMER: The Houston Fire Department data is private and cannot be posted to a public repository. In order to run our files and generate diagrams based on the dataset we were given, please locate and download the files `Address_&_Violation_Records_data 2020.csv` and `Address_&_Violation_Records_data 2021.csv` from Microsoft Team HFD.

## Steps to Run our Python Code

1. Clone repository to your local machine
2. Install dependencies with the following commands:

```
pip install pandas
pip install argparse
pip install os
pip install typing
pip install placekey.api
pip install re
pip install enum
pip install glob
pip install numpy
```

### For the data preprocessing
1. Stack and clean the address and violation record data (2020 and 2021), you may  open `clean_addressviolation_incident.py` in an IDE such as Visual Studio Code and run the code.

2. Preprocess the address and violation comment by running `address_processing.py` and `violation_comment_cleanning.py`.

3. Add placekey tagging rows to incident/address_violation/INFOR data that have addresses with place key by running `placekey_tagging.py` and add "main" section to placekey tagging `hfd_data_placekey_tagging.py`.




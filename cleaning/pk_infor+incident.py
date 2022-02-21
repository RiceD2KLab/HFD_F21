import placekey as pk
from placekey.api import PlacekeyAPI
import pandas as pd

"""
Takes as input the incident dataset, column name of the address column, output names and splits it into two datasets:
1. Valid_incident_2018_2021.csv: rows that can be added a placekey.
2. Invalid_incident_2018_2021.csv: rows that do not have a valid field in the column "Basic Incident Full Address".
"""
def filter_invalid(data, col_name, csv1, csv2):
    incident = pd.read_csv(data)
    entries = []
    for i, row in incident.iterrows():
        address = row[col_name]
        if type(address) is str:
            address = address.split(" ")
            #drop incomplete address row
            if len(address) <= 3:
                entries.append(i)
        #drop invalid row (most likely NaN)
        else:
            entries.append(i)
    #export each datasets
    df = incident.filter(items = entries, axis=0)
    df.to_csv(csv1, index=False)
    incident.drop(entries, inplace=True)
    incident.to_csv(csv2, index=False)
# filter_invalid("../../datasets/Incident Data 2018_2021.csv", "Basic Incident Full Address", "Invalid_incident_2018_2021.csv", "Valid_incident_2018_2021.csv")
# filter_invalid("../../datasets/Concatenated_Dataset_INFOR.csv", "Address", "Invalid_INFOR_2018_2021.csv", "Valid_INFOR_2018_2021.csv")

"""
Takes as input the valid incident dataset and adds placekey IDs for each row.
If a placekey cannot be generated, 0 is added as a place filler.
Exports the dataset with placekeys.
"""
def gen_placekey(valid, col_name):
    incident = pd.read_csv(valid)
    places = []
    for i, row in incident.iterrows():
        address = row[col_name]
        address = address.split(" ")
        # fills in the dictionary with corresponding street, city, region, zip, country
        # we are assuming the street address has the format: [STREET] [CITY] [STATE] [ZIP]
        places.append({"query_id":str(i), "street_address": ' '.join(address[:-3]), "city": address[-3], "region": address[-2], 
    "postal_code": address[-1], "iso_country_code": "US"})
    print("START LOOKUPS")
    #performs lookup by batch
    placekey_api_key = 'INSERT PLACEKEY API KEY HERE'
    pk_api = PlacekeyAPI(placekey_api_key)
    placekeys = pk_api.lookup_placekeys(places)
    placekey_col = []
    for pk_dict in placekeys:
        #if the address has a valid placekey, the dict would store placekey: [ID].
        #otherwise, the dict would store error: Invalid address.
        key = pk_dict.get('placekey', 0)
        #if there is a valid placekey, we append it
        #otherwise, we append a 0 as placeholder
        placekey_col.append(key)
    #adds the new column into the dataframe
    incident['PlaceKey ID'] = placekey_col
    #exports
    incident.to_csv(valid, index=False)
# gen_placekey("Valid_incident_2018_2021.csv", "Basic Incident Full Address")
# gen_placekey("Valid_INFOR_2018_2021.csv", "Address")

def filter_placekey(valid, csv1, csv2):
    incident = pd.read_csv(valid)
    df1 = incident[incident['PlaceKey ID'] != '0']
    df2 = incident[incident['PlaceKey ID'] == '0']
    df1.to_csv(csv1, index=False)
    df2.to_csv(csv2, index=False)
# filter_placekey("Valid_incident_2018_2021.csv", "Valid_incident_2018_2021_1.csv", "Valid_incident_2018_2021_2.csv")
# filter_placekey("Valid_INFOR_2018_2021.csv", "Valid_INFOR_2018_2021.csv_1.csv", "Valid_INFOR_2018_2021.csv_2.csv")






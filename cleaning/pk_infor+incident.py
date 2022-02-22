from placekey.api import PlacekeyAPI
import pandas as pd

def split_address(data: str, col_name: str, valid_output_name: str, invalid_output_name: str):
    """
    Splits the input dataset based on whether the address column is complete. We assume the address
    column to take the format [STREET] [CITY] [STATE] [ZIP] and is separated by space. If the address
    is not of this format, we categorize the row as invalid. Exports the two dataframe to two .csv files.
    Input:
    data - a file path to the dataset
    col_name - column name of the address column
    valid_output_name - the name of the file with rows with valid addresses
    invalid_output_name - the name of the file with rows with invalid addresses
    Return:
    None. Exports two dataframes as two csv files.
    """
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
    df.to_csv(invalid_output_name, index=False)
    incident.drop(entries, inplace=True)
    incident.to_csv(valid_output_name, index=False)

def gen_placekey(data:str, col_name:str):
    """
    Tags each row with a placekey that serves as an unique identifier for each address.
    If the Placekey API is unable to generate a valid placekey, we put 0 as a placeholder.
    Input:
    data - a file path to the dataset
    col_name - column name of the address column
    Return:
    None. Directly modifies the input csv file.
    """
    incident = pd.read_csv(data, index_col=0)
    places = []
    for i, row in incident.iterrows():
        address = row[col_name]
        address = address.split(" ")
        # fills in the dictionary with corresponding street, city, region, zip, country
        # we are assuming the street address has the format: [STREET] [CITY] [STATE] [ZIP]
        places.append({"query_id":str(i), "street_address": ' '.join(address[:-3]), "city": address[-3], "region": address[-2], 
    "postal_code": address[-1], "iso_country_code": "US"})
    print("Start lookup")
    #performs lookup by batch
    placekey_api_key = 'INSERT PLACEKEY API KEY HERE' #placekey is a free API and you can get an API key by registering on the website
    pk_api = PlacekeyAPI(placekey_api_key)
    placekeys = pk_api.lookup_placekeys(places)
    ('finish lookup')
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
    incident.to_csv(data, index=False)

def split_placekey(data:str, valid_output_name:str, invalid_output_name:str):
    """
    Splits the input dataset based on whether the placekey column has a valid placekey.
    Exports the two dataframe to two .csv files.
    Input:
    data - a file path to the dataset
    valid_output_name - the name of the file with rows with valid placekey
    invalid_output_name - the name of the file with rows with invalid placekey
    Return:
    None. Exports two dataframes as two csv files.
    """
    incident = pd.read_csv(data)
    #df1:valid placekey
    df1 = incident[incident['PlaceKey ID'] != '0']
    #df2:invalid placekey
    df2 = incident[incident['PlaceKey ID'] == '0']
    #exports
    df1.to_csv(valid_output_name, index=False)
    df2.to_csv(invalid_output_name, index=False)

def preprocess_add_violations(input_name:str, output_name:str):
    """
    Concatenates the address columns into one column 'STADDRESS' with space between each column entry.
    Input:
    input_name: a file path to the dataset
    output_name: a string representing the name of the output file 
    """
    add_vio_data = pd.read_csv(input_name, index_col=0)
    #zipcode column has type float, and has trailing .0, convert it to string
    add_vio_data['ZIP'] = add_vio_data['ZIP'].astype(int).astype(str)
    #replace empty fields with empty string
    values = {"SUFFIX": "", "ZIP": "", "STATE": "", "CITY": ""} 
    add_vio_data.fillna(value=values, inplace=True)
    #concatenate in the order of street number, name, suffix
    add_vio_data['STADDRESS'] = add_vio_data[['STNO', 'STNAME', 'SUFFIX', "CITY", "STATE", "ZIP"]].agg(' '.join, axis=1)
    #drop the individual columns
    add_vio_data.drop(['STNO', 'STNAME', 'SUFFIX', "CITY", "STATE", "ZIP"], axis=1, inplace=True)
    #export
    add_vio_data.to_csv(output_name, index=False)

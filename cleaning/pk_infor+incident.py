from placekey.api import PlacekeyAPI
import pandas as pd

def split_address(data: pd.DataFrame, col_name: str) -> pd.DataFrame:
    """
    Splits the input dataset based on whether the address column is complete. We assume the address column to take the format [STREET] [CITY] [STATE] [ZIP] and is separated by space. If the address is not of this format, we categorize the row as invalid. 
    Input:
    data - a dataframe representin the input dataset
    col_name - column name of the address column
    Return:
    data - a dataframe containing rows with valid addresses
    invalid_df - a dataframe containing rows with invalid addresses
    """
    entries = []
    for i, row in data.iterrows():
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
    invalid_df = data.filter(items = entries, axis=0)
    data.drop(entries, inplace=True)
    return data, invalid_df

def gen_placekey(data:pd.DataFrame, col_name:str) -> pd.DataFrame:
    """
    Tags each row with a placekey that serves as an unique identifier for each address. If the Placekey API is unable to generate a valid placekey, we put 0 as a placeholder.
    Input:
    data - a dataframe representing the input dataset
    col_name - column name of the address column
    Return:
    data - the same dataframe with an additional placekey column
    """
    places = []
    for i, row in data.iterrows():
        address = row[col_name]
        address = address.split(" ")
        # fills in the dictionary with corresponding street, city, region, zip, country
        # we are assuming the street address has the format: [STREET] [CITY] [STATE] [ZIP]
        places.append({"query_id":str(i), "street_address": ' '.join(address[:-3]), "city": address[-3], "region": address[-2], 
    "postal_code": address[-1], "iso_country_code": "US"})
    #performs lookup by batch
    placekey_api_key = 'INSERT PLACEKEY API KEY HERE' #placekey is a free API and you can get an API key by registering on the website
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
    data['PlaceKey ID'] = placekey_col
    return data

def split_placekey(data:pd.DataFrame) -> pd.DataFrame:
    """
    Splits the input dataset based on whether the placekey column has a valid placekey. 
    Input:
    data - a dataframe representing the input dataset
    Return:
    pk_valid - a dataframe containing rows with valid placekey
    pk_invalid - a dataframe containing rows with invalid placekey
    """
    #df1:valid placekey
    pk_valid = data[data['PlaceKey ID'] != '0']
    #df2:invalid placekey
    pk_invalid = data[data['PlaceKey ID'] == '0']
    return pk_valid, pk_invalid

def preprocess_add_violations(data:pd.DataFrame) -> pd.DataFrame:
    """
    Concatenates the address columns into one column 'STADDRESS' with space between each column entry.
    Input:
    data: a dataframe representing the input dataset
    Return:
    concat_data: the same dataframe with a concatenated address column
    """
    add_vio_data = pd.read_csv(data, index_col=0)
    #zipcode column has type float, and has trailing .0, convert it to string
    add_vio_data['ZIP'] = add_vio_data['ZIP'].astype(int).astype(str)
    #replace empty fields with empty string
    values = {"SUFFIX": "", "ZIP": "", "STATE": "", "CITY": ""} 
    add_vio_data.fillna(value=values, inplace=True)
    #concatenate in the order of street number, name, suffix
    add_vio_data['STADDRESS'] = add_vio_data[['STNO', 'STNAME', 'SUFFIX', "CITY", "STATE", "ZIP"]].agg(' '.join, axis=1)
    #drop the individual columns
    add_vio_data.drop(['STNO', 'STNAME', 'SUFFIX', "CITY", "STATE", "ZIP"], axis=1, inplace=True)
    return add_vio_data


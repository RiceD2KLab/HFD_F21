# use placekey API addresses with uniquely identifying placekeys
import pandas as pd
from placekey.api import PlacekeyAPI

# NOTE: Please do not commit code to the repository with the API key in it
placekey_api_key = "API_KEY_HERE"
pk_api = PlacekeyAPI(placekey_api_key)

# aggregate STNO and STNAME columns in address and violation data to create
# appropriate input for street_address argument placekey lookup function
add_vio_data = pd.read_csv('Cleaned Address and Violation Data 2020_2021.csv')
add_vio_data['STADDRESS'] = add_vio_data[['STNO', 'STNAME']].agg(' '.join,
                                                                 axis=1)
add_vio_data.head()

# assign a unique placekey to each unique address
placekeys = []

for idx, row in add_vio_data.iterrows():
  place = {"street_address": row['STADDRESS'], "city": row['CITY'],
           "region": row["STATE"],
           "postal_code": str(row["ZIP"]), "iso_country_code": "US"}
  pk_dict = pk_api.lookup_placekey(**place, strict_address_match=False)
  placekey = pk_dict['placekey']
  placekeys.append(placekey)

add_vio_data['PLACEKEY'] = placekeys

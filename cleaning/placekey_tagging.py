# use placekey API addresses with uniquely identifying placekeys
import pandas as pd
from placekey.api import PlacekeyAPI

placekey_api_key = "API_KEY_HERE"
pk_api = PlacekeyAPI(placekey_api_key)

# aggregate STNO and STNAME columns in address and violation data to create
# appropriate input for street_address argument placekey lookup function
add_vio_data = pd.read_csv('Cleaned Address and Violation Data 2020_2021.csv')
add_vio_data['STADDRESS'] = add_vio_data[['STNO', 'STNAME']].agg(' '.join,
                                                                 axis=1)

# assign a unique placekey to each unique address
places = []
for idx, row in add_vio_data.iterrows():
  place = {"query_id": str(idx), "street_address": row['STADDRESS'], "city": row['CITY'],
           "region": row["STATE"],
           "postal_code": str(row["ZIP"]), "iso_country_code": "US"}
  places.append(place)

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
    add_vio_data['PlACEKEY'] = placekey_col

add_vio_data.head()
add_vio_data.to_csv('Cleaned Address and Violation Data 2020_2021.csv', index=False)



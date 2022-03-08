'''
This file is used to merge five of our datasets: the HCAD data for nonresidential properties,
address and violation data, structure fire incident data, INFOR inspection data, and overall
incident data.

The merged dataset is then outputted to be observed and viewed.
'''


# Import libraries
import pandas as pd


# Download placekey-tagged and cleaned datasets
hcad_df = pd.read_csv('HCAD_pk.csv')
hcad_df = hcad_df.drop_duplicates(subset=["PlaceKey ID"])
addvio_df = pd.read_csv('Address and Violation Data by Property.csv')
structfire_df = pd.read_csv('Structure Fires 2005-2021 Aggregated with PK.csv')
infor_df = pd.read_csv('AggregatedINFOR.csv')
incident_df = pd.read_csv('Cleaned_incident_data.csv')



# Merge the five datasets by PlaceKeyID
merge_result1 = pd.merge(hcad_df, addvio_df, how="outer", on=["PlaceKey ID", "PlaceKey ID"])
merge_result2 = pd.merge(merge_result1, structfire_df, how="outer", on=["PlaceKey ID", "PlaceKey ID"])
merge_result3 = pd.merge(merge_result2, infor_df, how="outer", on=["PlaceKey ID", "PlaceKey ID"])
merge_result4 = pd.merge(merge_result3, incident_df, how="outer", on=["PlaceKey ID", "PlaceKey ID"])


# Check for any duplicate rows
merge_result4 = merge_result4.drop_duplicates()


# Export merged dataset
merge_result4.to_csv(r'full_merge.csv')

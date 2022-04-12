'''
This file is used to merge five of our datasets: the HCAD data for nonresidential properties,
address and violation data, structure fire incident data, INFOR inspection data, and overall
incident data.

The merged dataset is then outputted to be observed and viewed.
'''

import os
import pandas as pd

if __name__ == "__main__":
  # Download placekey-tagged and cleaned datasets
  data_source = os.path.normpath("Data/Merged Data/Sources")
  hcad_df = pd.read_csv(os.path.join(data_source, "HCAD_pk_post.csv"),
                        index_col=0)
  hcad_df = hcad_df.drop_duplicates(subset=["PlaceKey ID"])
  addvio_df = pd.read_csv(
    os.path.join(data_source, "Address and Violation Data by Property.csv"))
  structfire_df = pd.read_csv(os.path.join(data_source,
                                           "Structure Fires 2005-2021 Aggregated with PK.csv"))
  infor_df = pd.read_csv(os.path.join(data_source, "AggregatedINFOR.csv"))
  incident_df = pd.read_csv(
    os.path.join(data_source, "cleaned_incident_data.csv"))

  # Merge the five datasets by PlaceKeyID
  merge_result1 = pd.merge(hcad_df, addvio_df, how="outer",
                           on=["PlaceKey ID", "PlaceKey ID"])
  merge_result2 = pd.merge(merge_result1, structfire_df, how="outer",
                           on=["PlaceKey ID", "PlaceKey ID"])
  merge_result3 = pd.merge(merge_result2, infor_df, how="outer",
                           on=["PlaceKey ID", "PlaceKey ID"])
  merge_result4 = pd.merge(merge_result3, incident_df, how="outer",
                           on=["PlaceKey ID", "PlaceKey ID"])

  # Check for any duplicate rows
  merge_result4 = merge_result4.drop_duplicates()

  # Drop Unnecessary Columns
  merge_result4 = merge_result4.drop(
    columns=['acct', 'STADDRESS_y', 'county_lookup', 'ViolationComment',
             'dispatched_on_local_date', 'complete_address', 'Address',
             'Basic Incident Full Address'])

  # Export merged dataset
  merge_result4.to_csv('full_merge_no_duplicates.csv', index=False)

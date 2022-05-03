"""
This file is used to merge five of our datasets: the HCAD data for
non-residential and large-scale residential properties, address and violation
data, structure fire incident data, INFOR inspection data, and overall incident
data. The merge is executed using successive left outer joins with the HCAD
data as a base, matching on the PlaceKey field in each dataset.

The merged dataset is then output to be observed and viewed.
"""

import os
import pandas as pd
import placekey_tagging as pk
from wrangling import clean_hcad, clean_infor, clean_incident, \
  clean_structure_fire, clean_address_violation

MERGED_DIR = "Merged Data"

if __name__ == "__main__":
  # Download placekey-tagged and cleaned datasets
  hcad_df = pd.read_csv(
    os.path.join(clean_hcad.HCAD_CLEAN_DIR, "HCAD Data Aggregated with PK.csv"),
    index_col=0)
  hcad_df = hcad_df.drop_duplicates(subset=["PlaceKey ID"])
  addvio_df = pd.read_csv(
    os.path.join(clean_address_violation.AV_CLEAN_DIR,
                 "Address and Violation Data Aggregated with PK.csv"))
  structfire_df = pd.read_csv(os.path.join(clean_structure_fire.FIRE_CLEAN_DIR,
                                           "Structure Fire Data Aggregated with PK.csv"))
  infor_df = pd.read_csv(os.path.join(clean_infor.INFOR_CLEAN_DIR,
                                      "INFOR Data Aggregated with PK.csv"))
  incident_df = pd.read_csv(
    os.path.join(clean_incident.INCIDENT_CLEAN_DIR,
                 "Incident Data Aggregated with PK.csv"))

  # Merge the five datasets by PlaceKeyID
  merge_result1 = pd.merge(hcad_df, addvio_df, how="outer",
                           on=[pk.PLACEKEY_FIELD_NAME, pk.PLACEKEY_FIELD_NAME])
  merge_result2 = pd.merge(merge_result1, structfire_df, how="outer",
                           on=[pk.PLACEKEY_FIELD_NAME, pk.PLACEKEY_FIELD_NAME])
  merge_result3 = pd.merge(merge_result2, infor_df, how="outer",
                           on=[pk.PLACEKEY_FIELD_NAME, pk.PLACEKEY_FIELD_NAME])
  merge_result4 = pd.merge(merge_result3, incident_df, how="outer",
                           on=[pk.PLACEKEY_FIELD_NAME, pk.PLACEKEY_FIELD_NAME])

  # Check for any duplicate rows
  merge_result4 = merge_result4.drop_duplicates()

  # Drop Unnecessary Columns
  merge_result4 = merge_result4.drop(
    columns=['acct', 'STADDRESS_y', 'county_lookup', 'dispatched_on_local_date',
             'complete_address', 'Address', 'Basic Incident Full Address'])

  # Export merged dataset
  merge_result4.to_csv(os.path.join(MERGED_DIR, 'Full Merged Data.csv'),
                       index=False)

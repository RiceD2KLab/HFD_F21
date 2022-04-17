import pandas as pd

#drop duplicates from structure fire data
sfs = pd.read_csv('Structure Fires 2005-2021 Aggregated with PK.csv')
sfs = sfs.drop_duplicates()

#drop duplicates from infor data
infor = pd.read_csv('INFOR_2018_2021_pk.csv')
infor = infor.drop_duplicates()

#infor.to_csv('INFOR_2018_2021_pk.csv')

#drop duplicates from a&v data
advio = pd.read_csv('Address and Violation Data 2020_2021_pk.csv')
advio = advio.drop_duplicates()

#drop duplicates from hcad data
hcad = pd.read_csv('HCAD_pk.csv')
hcad = hcad.drop_duplicates()

#drop duplicates from incident data
incident = pd.read_csv('Non-Residential_Incident_2018_2021_pk.csv')
incident = incident.drop_duplicates()


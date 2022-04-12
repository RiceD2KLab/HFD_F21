import os

import pandas as pd

from cleaning.data_wrangling import filter_null


if __name__ == "__main__":
  violations_dir = os.path.normpath(
    "Data/Address and Violation Records Data/Original Datasets")
  av2020 = pd.read_csv(
    os.path.join(violations_dir, 'Address_&_Violation_Records_data 2020.csv'))
  av2021 = pd.read_csv(
    os.path.join(violations_dir, 'Address_&_Violation_Records_data 2021.csv'))

  av2021 = av2021.drop('STARTDTTM', axis=1)

  # stacked address & violation data
  address_violation_full = pd.concat([av2020, av2021]).drop_duplicates()

  # remove rows with empty address component fields from Address and Violation Data
  cleaned_address_violation = filter_null(
    address_violation_full,
    ['STATE', 'STNO', 'CITY', 'STNAME', 'ZIP'])
  cleaned_address_violation.to_csv(
    'Cleaned Address and Violation Data 2020_2021.csv')

  # drop irrelevant columns from placekey tagged Address and Violation Data

  advio_pk = pd.read_csv(os.path.join(os.path.normpath(
    "Data/Address and Violation Records Data/Intermediate Datasets/"),
                                      'Address and Violation Data 2020_2021_pk.csv'))

  advio_pk = advio_pk.drop(
    labels=['APNO', 'APUSEINSPKEY', 'COMPDTTM', 'DESCRIPT', 'Remove Duplication',
            'Code', 'FULLNAME',
            'GPSX', 'GPSY', 'GPSZ', 'INSPTYPECAT', 'LOC', 'Location',
            'Number of Records', 'OCCUPANCYTYPE', 'PREDIR', 'RESULTBY',
            'RESULTDTTM',
            'RESULT', 'SCHEDDTTM', 'SUBDIVDESC', 'SUPERVISOR', 'TEAMDESCRIPTION',
            'ViolationStatus', 'WORKTYPE'], axis=1)

  # Aggregrate Address & Violation data by PlaceKey ID and compile categorical features into lists.
  advio_pk = advio_pk.groupby('PlaceKey ID').agg(lambda x: list(x))

  # Update STADDRESS to only have a single copy of the address corresponding to the PlaceKey ID
  single_address = []

  for idx, row in advio_pk.iterrows():
    single_address.append(row['STADDRESS'][0])

  # Update STADDRESS column
  advio_pk['STADDRESS'] = single_address

  # Export aggregated A&V data
  advio_pk.to_csv('Address and Violation Data by Property.csv')

import pandas as pd

#compile address & violation record data for 2020 & 2021

av2020 = pd.read_csv('data/sp22data/Address_&_Violation_Records_data 2020.csv')
av2021 = pd.read_csv('data/sp22data/Address_&_Violation_Records_data 2021.csv')

av2020.columns
av2021.columns

av2021 = av2021.drop('STARTDTTM', axis=1)
av2021.head()

#compile incident data
inc_full2021 = pd.read_csv('data/sp22data/FF--D2K-2021-data_full year 2021.csv')
inc_2018_2021 = pd.read_csv('data/sp22data/D2K Incident Data July 2018 to JAug 10 2021_Export.csv')

inc_full2021.count()
inc_2018_2021.count()

inc_2018_2021 = inc_2018_2021.rename({'Apparatus Resource Primary Action Taken Code And Description (FD18.9)':'Basic Primary Action Taken Code And Description (FD1.48)'})

#stacked address & violation data
advio_full = pd.concat([av2020, av2021])
advio_full.head()
advio_full.count()
av2020.count()

#clean stacked address & violation data
advio_full = advio_full.drop_duplicates()
advio_full.count()

#stacked incident data
inc_full = pd.concat([inc_full2021, inc_2018_2021])
inc_full.count()

#clean stacked incident data
inc_full = inc_full.drop_duplicates()
inc_full.count()

#export cleaned data
advio_full.to_csv('Address and Violation Data 2020_2021')
inc_full.to_csv('Incident Data 2018_2021')
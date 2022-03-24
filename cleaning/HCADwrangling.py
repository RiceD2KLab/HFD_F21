import pandas as pd

#import HCAD data - "buildings" (non-residential properties) and "all_properties"
buildings = pd.read_csv('building_other.txt', delimiter="\t",encoding= 'unicode_escape')
all_properties = pd.read_csv('real_acct.txt', delimiter="\t",encoding= 'unicode_escape')

#Inner join datasets on "acct" feature (unique identifier for each building) to eliminate residential properties

joined_data = buildings.set_index('acct').join(all_properties.set_index('acct'))

#Select relevant columns and export data
non_residential_properties = joined_data[['site_addr_1', 'site_addr_2','site_addr_3','impr_tp']]
non_residential_properties.to_csv('Non-Residential_Properties.csv')
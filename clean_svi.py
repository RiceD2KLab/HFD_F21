import pandas as pd

svi = pd.read_csv("/Users/tessacannon/Downloads/Texas.csv")

svi_harris = svi.loc[svi['COUNTY']=='Harris']

svi_harris_cleaned = svi_harris[['FIPS','AREA_SQMI','E_TOTPOP','E_HU','E_POV',
'E_UNEMP','E_PCI','E_NOHSDP','E_AGE65','E_AGE17','E_DISABL','E_SNGPNT','E_MINRTY',
'E_LIMENG','E_MUNIT','E_MOBILE','E_CROWD','E_NOVEH','E_GROUPQ','RPL_THEME1','RPL_THEME2',
'RPL_THEME3','RPL_THEME4','RPL_THEMES']]

svi_harris_cleaned.to_csv("/Users/tessacannon/Downloads/Cleaned_SVI_Harris.csv")
import os

import pandas as pd

import data_io as io

SVI_DIR = os.path.normpath("Data/Public Data/SVI")
SVI_ORIG_DIR = os.path.join(SVI_DIR, io.ORIG_DIR)
SVI_INTER_DIR = os.path.join(SVI_DIR, io.INTER_DIR)
SVI_CLEAN_DIR = os.path.join(SVI_DIR, io.CLEAN_DIR)


def clean_svi(svi_data: pd.DataFrame) -> pd.DataFrame:
  """

  :param svi_data:
  :return:
  """
  # Keep only Harris county, filter columns
  svi_harris = svi_data.loc[svi['COUNTY'] == 'Harris']
  return svi_harris[
    ['FIPS', 'AREA_SQMI', 'E_TOTPOP', 'E_HU', 'E_POV',
     'E_UNEMP', 'E_PCI', 'E_NOHSDP', 'E_AGE65', 'E_AGE17', 'E_DISABL',
     'E_SNGPNT', 'E_MINRTY',
     'E_LIMENG', 'E_MUNIT', 'E_MOBILE', 'E_CROWD', 'E_NOVEH', 'E_GROUPQ',
     'RPL_THEME1', 'RPL_THEME2',
     'RPL_THEME3', 'RPL_THEME4', 'RPL_THEMES']]


if __name__ == "__main__":
  svi = pd.read_csv(os.path.join(SVI_ORIG_DIR, "Texas.csv"))

  # Output. No aggregate, so we need to exclude default Pandas index
  io.output_to_csv(clean_svi(svi),
                   os.path.join(SVI_CLEAN_DIR, "Cleaned_SVI_Harris"),
                   keep_index=False)

import geopandas as gpd
from numpy import vectorize
import pandas as pd
import pyproj


#Enter the name of the teeam for which the interactive map needs to be generated from the list :- ['APT/HTL' 'GO' 'HazMatHiPi' 'HighRise' 'PlanCk' 'SCH/INS' 'SpecialOps','Weekends']
What_Team_Type_Is_Needed = 'HazMatHiPi'
#shapefile = gpd.read_file("zipcode/ZIPCODE.shp")

# Read the shape file
shapefile = gpd.read_file("shapefile_houston.shp")
shapefile.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)

#Read the csv which holds the count for the acses handled by each team grouped by zipcode
ZIPCODE_Count_Data = pd.read_csv("violationDistributionByZipAndTeamCode.csv")
#rename the columns
ZIPCODE_Count_Data.rename(columns={"ZIPCODE":"ZIPCODE","ZIP":"COUNT"},inplace=True)



#Since the ZIPCODE in the read file is float we convert the type to int
ZIPCODE_Count_Data = ZIPCODE_Count_Data.astype({'ZIPCODE': int})

ZIPCODE_Count_Data = ZIPCODE_Count_Data.loc[ZIPCODE_Count_Data['TEAMCODE'] == What_Team_Type_Is_Needed]


#Set ZIPCODE as the index
ZIPCODE_Count_Data.set_index("ZIPCODE")

import plotly.express as px
import geopandas as gpd

comb_shape = shapefile.merge(ZIPCODE_Count_Data,on="ZIPCODE").set_index("ZIPCODE")




title_Text = "Number of Violations Reported by ZIP for "+What_Team_Type_Is_Needed

fig = px.choropleth_mapbox(comb_shape,
                   geojson=comb_shape.geometry,
                   locations=comb_shape.index,
                   color="COUNT",  
                   #projection="mercator" ,
                   center={"lat": 29.7604, "lon": -95.3698},
                    mapbox_style="open-street-map",
                   color_continuous_scale="Oranges",
                   zoom=9,
                   #width=1920,
                   width=1280,
                   #height=1080,
                   height=720,
                   title=title_Text,
                   opacity=0.7
                   )

#Change the characteristics of the interactive pointer
fig.update_layout(
    hoverlabel=dict(
        bgcolor="black",
        font_size=34,
        font_family="Rockwell"
    )
)


fig.update_geos(fitbounds="locations", visible=False) 


# Checks to handle / as this casues issues to the output path
if What_Team_Type_Is_Needed.__contains__("/"):
    WhatTeamTypeIsNeeded=What_Team_Type_Is_Needed.replace("/","-")
    print(What_Team_Type_Is_Needed)
fig.write_html(What_Team_Type_Is_Needed+".html")

fig.show()

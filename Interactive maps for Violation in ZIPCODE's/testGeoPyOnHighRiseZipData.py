import geopandas as gpd
from numpy import vectorize
import pandas as pd
import pyproj

'''
def callTheTeam(team):
    var28_df = var28_df.loc[var28_df['TEAMCODE'] == WhatTeamTypeIsNeeded]
    return var28_df
'''
WhatTeamTypeIsNeeded = 'Weekends'
#shapefile = gpd.read_file("zipcode/ZIPCODE.shp")
shapefile = gpd.read_file("shapefile_houston.shp")
shapefile.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)

#print(shapefile)

var28_df = pd.read_csv("violationDistributionByZipAndTeamCode.csv")
var28_df.rename(columns={"ZIPCODE":"ZIPCODE","ZIP":"COUNT"},inplace=True)
#var28_df = var28_df[ZIPCODE].astype('int64')
#var28_df = var28_df[COUNT].astype('int64')
#print(list(var28_df.columns))

var28_df = var28_df.astype({'ZIPCODE': int})
#var28_df= callTheTeam(WhatTeamTypeIsNeeded)
var28_df = var28_df.loc[var28_df['TEAMCODE'] == WhatTeamTypeIsNeeded]
#print(var28_df)


#print(var28_df)
var28_df.set_index("ZIPCODE")

import plotly.express as px
import geopandas as gpd

comb_shape = shapefile.merge(var28_df,on="ZIPCODE").set_index("ZIPCODE")




titleText = "Number of Violations Reported by ZIP for "+WhatTeamTypeIsNeeded
fig = px.choropleth_mapbox(comb_shape,
                   geojson=comb_shape.geometry,
                   locations=comb_shape.index,
                   color="COUNT",  
                   #projection="mercator" ,
                   center={"lat": 29.7604, "lon": -95.3698},
                    mapbox_style="open-street-map",
                   color_continuous_scale="Oranges",
                   zoom=9,
                   width=1920,
                   height=1080,
                   title=titleText,
                   opacity=0.7
                   )
fig.update_layout(
    updatemenus=[
        dict(
            buttons=list([
                dict(
                    args=[WhatTeamTypeIsNeeded, "surface"],
                    label="APT/HTLS",
                    method="update"
                ),
                dict(
                    args=[WhatTeamTypeIsNeeded, "heatmap"],
                    label="GO",
                    method="update"
                )
            ]),
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.1,
            yanchor="top"
        ),
    ]
)
fig.update_layout(
    hoverlabel=dict(
        bgcolor="black",
        font_size=34,
        font_family="Rockwell"
    )
)

fig.update_geos(fitbounds="locations", visible=False) 
fig.show()

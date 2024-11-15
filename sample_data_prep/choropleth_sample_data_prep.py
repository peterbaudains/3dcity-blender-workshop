import geopandas as gpd
import pandas as pd
from pathlib import Path


# 2021 Census data, contains Crown Copyright Data used under OGL v3: 
# https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/
df = pd.read_csv(str(Path.home()) + '\\Downloads\\1035608137486784.csv', skiprows=9, header=None, skipfooter=8)
df = df.loc[:, 1:2]
df.columns = ['OAcode', 'popden']
df['popden'] = pd.to_numeric(df['popden'])

# Output areas geopackage downloaded from Open Geography Portal, used under OGL v3: 
# https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/
gdf = gpd.read_file(str(Path.home()) + '\\Downloads\\Output_Areas_2021_EW_BFC_V8_-1910516784426669580.gpkg')

# Merge the two dataframes
gdf = pd.merge(left=df, right=gdf, left_on='OAcode', right_on='OA21CD')

# Re-convert to geodataframe
gdf = gpd.GeoDataFrame(gdf[['OA21CD', 'popden']], 
                       geometry=gdf['geometry'],
                       crs=27700)

# Save as gpkg
gdf.to_file('sample_data\\CityOfLondon_Southwark_2021PopDen.gpkg')

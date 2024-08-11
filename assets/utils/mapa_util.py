import geopandas as gpd
from shapely import wkt

class MapaUtil:
    
    def convert_gfd(self, dataframe):
        dataframe['geometry'] = dataframe['geometry'].apply(wkt.loads)
        gdf = gpd.GeoDataFrame(dataframe, geometry='geometry')
        gdf.set_crs(epsg=4326, inplace=True)
        return gdf
import fiona
from polygeohasher import polygeohasher
import geopandas as gpd


f = fiona.open('Province/省级行政区.shp')
gdf = gpd.read_file(f) # read your geometry file here

primary_df = polygeohasher.create_geohash_list(gdf, 5,inner=False) # returns a dataframe with list of geohashes for each geometry

secondary_df = polygeohasher.geohash_optimizer(primary_df, 2, 1, 5) # returns optimized list of geohash

polygeohasher.optimization_summary(primary_df, secondary_df) #creates a summary of first and second output

'''
--------------------------------------------------
            OPTIMIZATION SUMMARY
--------------------------------------------------
Total Counts of Initial Geohashes :  2597
Total Counts of Final Geohashes   :  837
Percent of optimization           :  67.77 %
--------------------------------------------------
'''

geo_df = polygeohasher.geohashes_to_geometry(secondary_df,"geohash_column_name") # return geometry for a DataFrame with a column - `opitimized_geohash_list` (output from above)

geo_df.to_file("your write path.format",driver = "GeoJSON") #write file in your favorite spatial file format

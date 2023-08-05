'''
Geoprocessing tools for analysing remote sensing data
using in Open Data Cube 
It's consists of:
- convert_geojson_crs
- convert_shp_crs
- merge
- intersect
- union
- erase
- clip
- convert_geojson_to_shp
- convert_shp_to_geojson
'''

import json
import geojson
import pandas as pd
import geopandas as gpd
from shapely.geometry import shape 


        
# function to convert CRS of GeoJson 
def convert_geojson_CRS(input_path, output_path, crs):
    # Read in the GeoJSON file using geopandas
    gdf = gpd.read_file(input_path)

    # Convert the geometry to the desired CRS
    gdf = gdf.to_crs(crs)

    # Write out the GeoDataFrame to a SHP file with the specified CRS and encoding
    gdf.to_file(output_path, driver='GeoJSON', crs=crs, encoding='utf-8')
    
# function to convert CRS of shp 
def convert_shp_CRS(input_path, output_path, crs):
    # Read in the GeoJSON file using geopandas
    gdf = gpd.read_file(input_path)

    # Convert the geometry to the desired CRS
    gdf = gdf.to_crs(crs)

    # Write out the GeoDataFrame to a SHP file with the specified CRS and encoding
    gdf.to_file(output_path, driver='ESRI Shapefile', crs=crs, encoding='utf-8')

# the merge tool combines datasets that are the same datatype into one   
def merge(files, output_file):
    # Initialize an empty list of features
    features = []

    # Loop through all the input files and add their features to the list
    for file in files:
        with open(file) as f:
            data = json.load(f)
            features += data['features']

    # Create a new GeoJSON object
    new_data = {
        "type": "FeatureCollection",
        "features": features
    }

    # Write the new GeoJSON file
    with open(output_file, 'w') as f:
        geojson.dump(new_data, f)
        
        
# function for intersect
def intersect(file_paths, output_file):
    
    # Read each GeoJSON file and create a GeoDataFrame
    gdfs = [gpd.read_file(fp) for fp in file_paths]
    
    # perform intersect on each pair of geodataframe
    result = gdfs[0]
    for gdf in gdfs[1:]:
        result = result.intersection(gdf)
        
    #save result to output file
    result.to_file(output_file)
    
    
# function for union
def union(file_paths, output_file):
    
    # read each files and create a geodataframe
    gdfs = [gpd.read_file(fp) for fp in file_paths]
    
    # perfrom Union on each pair of Geodataframe
    result = gdfs[0]
    for gdf in gdfs[1:]:
        result = result.union(gdf)
    # save to output file
    result.to_file(output_file)
    
    
# func for Erase/Difference    
def erase(file, erase_file, output_file):
    
    # read input and erase file
    gdf = gpd.read_file(file)
    gdfe = gpd.read_file(erase_file)
    
    # perform func
    result = gdf.overlay(gdfe, how = 'difference')
    
    # savs to output
    result.to_file(output_file)
    

#func for clip
def clip(file, clip_file, output_file):
    
    # read input and erase file
    gdf = gpd.read_file(file)
    gdfc = gpd.read_file(clip_file)
    
    # perform func
    result = gpd.clip(gdf, gdfc)
    
    # savs to output
    result.to_file(output_file)
    
#func for Symmetrical difference
def smc_difference(file, diff_file, output_file):
    
    # read input and erase file
    gdf = gpd.read_file(file)
    gdfd = gpd.read_file(diff_file)
    
    # perform function
    result = gdf.overlay(gdfd, how = 'symmetric_difference')
    
    #save to output
    result.to_file(output_file)
    

# func for dissolve    
def dissolve(file, output, dissolve_by):
    
    # read input and erase file
    gdf = gpd.read_file(file)
    
    # perform func
    result = gdf.dissolve(by=dissolve_by)
       
    #save to output
    result.to_file(output)
    
    
# func for buffer ie. buffer = 0.005 (500 meter)
def buffer(file, output, buffer_num):
    
    # read input and erase file
    gdf = gpd.read_file(file)
       
    # perform func
    result = gdf.buffer(buffer_num)
            
    #save to output
    result.to_file(output)

# function to convert GeoJson to Shp
def convert_geojson_to_shp(input_path, output_path, crs):
    # Read in the GeoJSON file using geopandas
    gdf = gpd.read_file(input_path)

    # Convert the geometry to the desired CRS
    gdf = gdf.to_crs(crs)

    # Write out the GeoDataFrame to a SHP file with the specified CRS and encoding
    gdf.to_file(output_path, driver='ESRI Shapefile', crs=crs, encoding='utf-8')
    
# function to convert shp to GeoJSON
def convert_shp_to_geojson(input_path, output_path, crs):
    # Read in the GeoJSON file using geopandas
    gdf = gpd.read_file(input_path)

    # Convert the geometry to the desired CRS
    gdf = gdf.to_crs(crs)

    # Write out the GeoDataFrame to a SHP file with the specified CRS and encoding
    gdf.to_file(output_path, driver='GeoJSON', crs=crs, encoding='utf-8')

    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
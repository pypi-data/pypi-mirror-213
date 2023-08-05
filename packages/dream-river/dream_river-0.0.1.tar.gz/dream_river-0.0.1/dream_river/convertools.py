import datacube
import matplotlib.pyplot as plt
import numpy as np
import scipy
import os
import xarray as xr
import geopandas as gpd
from osgeo import gdal
from osgeo import osr
from osgeo import ogr
from datacube.utils.cog import write_cog
from skimage.segmentation import felzenszwalb
from flusstools.geotools import raster2array, open_raster
from flusstools.geotools import create_raster, get_srs, float2int

# function to convert raster image to polygon 
# by using image segmentation(felzenszwalb)
def vectorize(ds, outname_raster, outname_vector):
    
    # calculate Index to catagorize the value to polygon
    band_diff = 100*((ds.nir - ds.red) /(ds.nir + ds.red))
    
    # select first time step
    time_step = 0
    VI = band_diff.isel(time = time_step)
    
    
    
    # Convert our mean index xarray into a numpy array, we need
    # to be explicit about the datatype to satisfy felzenszwalb
    input_array = VI.values.astype(np.float64)
    
    # Calculate the segments (image segmentation)
    segments = felzenszwalb(input_array, 
                             scale=1, 
                             sigma=0.5, 
                             min_size=90, 
                             channel_axis=-1)
    
    # Calculate the zonal mean index across the segments
    segments_zonal_mean_qs = scipy.ndimage.mean(input=input_array,
                                                labels=segments,
                                                index=segments)
    

    # Convert numpy array to xarray.DataArray
    segments_zonal_mean_qs = xr.DataArray(segments_zonal_mean_qs, 
                                           coords=VI.coords, 
                                           dims=['y', 'x'], 
                                           attrs=VI.attrs)
    
    # Write array to GeoTIFF
    write_cog(geo_im=segments_zonal_mean_qs,
              fname=outname_raster, # .tif
              overwrite=True);
    
    # convert raster to polygon
    raster2polygon(outname_raster , outname_vector) #(.tif,.shp)
    
    #convert CRS
    gdf = gpd.read_file(outname_vector)
    gdf= gdf.to_crs(32647)
    # gdf[gdf.columns[0]] /= 100
    gdf.to_file(outname_vector, driver='ESRI Shapefile', crs=32647, encoding='utf-8')
    
    
    
# func to convert raster image to polygon
def raster2polygon(file_name, out_shp_fn, band_number=1, field_name="values"):
    """
    Convert a raster to polygon
    :param file_name: STR of target file name, including directory; must end on ".tif"
    :param out_shp_fn: STR of a shapefile name (with directory e.g., "C:/temp/poly.shp")
    :param band_number: INT of the raster band number to open (default: 1)
    :param field_name: STR of the field where raster pixel values will be stored (default: "values")
    :return: None
    """
    # if len(out_shp_fn) < 13:
    #     pass
    # else:
    #     raise ValueError('Shapefile name may not have more than 13 characters')
        
    # ensure that the input raster contains integer values only and open the input raster
    file_name = float2int(file_name)
    raster, raster_band = open_raster(file_name, band_number=band_number)

    # create new shapefile with the create_shp function
    new_shp = create_shp(out_shp_fn, layer_name="raster_data", layer_type="polygon")
    dst_layer = new_shp.GetLayer()

    # create new field to define values
    new_field = ogr.FieldDefn(field_name, ogr.OFTInteger)
    dst_layer.CreateField(new_field)

    # Polygonize(band, hMaskBand[optional]=None, destination lyr, field ID, papszOptions=[], callback=None)
    gdal.Polygonize(raster_band, None, dst_layer, 0, [], callback=None)

    # create projection file
    srs = get_srs(raster)
    make_prj(out_shp_fn, int(srs.GetAuthorityCode(None)))
    print("Success: Wrote %s" % str(out_shp_fn)) 
    
 
 # function extension for converting raster image to polygon   
def create_shp(shp_file_dir, overwrite=True, *args, **kwargs):
    """
    :param shp_file_dir: STR of the (relative shapefile directory (ends on ".shp")
    :param overwrite: [optional] BOOL - if True, existing files are overwritten
    :kwarg layer_name: [optional] STR of the layer_name - if None: no layer will be created (max. 13 chars)
    :kwarg layer_type: [optional] STR ("point, "line", or "polygon") of the layer_name - if None: no layer will be created
    :output: returns an ogr shapefile layer
    """
    shp_driver = ogr.GetDriverByName("ESRI Shapefile")

    # check if output file exists if yes delete it
    if os.path.exists(shp_file_dir) and overwrite:
        shp_driver.DeleteDataSource(shp_file_dir)

    # create and return new shapefile object
    new_shp = shp_driver.CreateDataSource(shp_file_dir)

    # create layer if layer_name and layer_type are provided
    if kwargs.get("layer_name") and kwargs.get("layer_type"):
        # create dictionary of ogr.SHP-TYPES
        geometry_dict = {"point": ogr.wkbPoint,
                         "line": ogr.wkbMultiLineString,
                         "polygon": ogr.wkbMultiPolygon}
        # create layer
        try:
            new_shp.CreateLayer(str(kwargs.get("layer_name")),
                                geom_type=geometry_dict[str(kwargs.get("layer_type").lower())])
        except KeyError:
            print("Error: Invalid layer_type provided (must be 'point', 'line', or 'polygon').")
        except TypeError:
            print("Error: layer_name and layer_type must be string.")
        except AttributeError:
            print("Error: Cannot access layer - opened in other program?")
    return new_shp
    
# function to create projection file of a shapfile
def make_prj(shp_file_name, epsg):
    """
    Returns:
        None: Creates a projection file (``.prj``) in the same directory and
        with the same name of ``shp_file_name``.
    """
    shp_dir = shp_file_name.split(shp_file_name.split("/")[-1].split("\\")[-1])
    shp_name = shp_file_name.split(".shp")[0].split("/")[-1].split("\\")[-1]
    with open(shp_dir[0] + shp_name + ".prj", "w+") as prj:
        prj.write(get_wkt(epsg))
        
        
        
def get_wkt(epsg, wkt_format="esriwkt"):
    """Gets WKT-formatted projection information for an epsg code using the ``osr`` library.

    Args:
        epsg (int): epsg Authority code
        wkt_format (str): of wkt format (default is esriwkt for shapefile projections)

    Returns:
        str: WKT (if error: returns default corresponding to ``epsg=4326``).
    """
    default = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295],UNIT["Meter",1]]'
    spatial_ref = osr.SpatialReference()
    try:
        spatial_ref.ImportFromEPSG(epsg)
    except TypeError:
        logging.error(
            "epsg must be integer. Returning default WKT(epsg=4326).")
        return default
    except Exception:
        logging.error(
            "epsg number does not exist. Returning default WKT(epsg=4326).")
        return default
    if wkt_format == "esriwkt":
        spatial_ref.MorphToESRI()
    return spatial_ref.ExportToPrettyWkt()

  
    
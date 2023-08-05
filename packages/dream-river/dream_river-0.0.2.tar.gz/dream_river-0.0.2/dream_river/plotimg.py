'''
ploting tools for creating the interactive map
for Open Data Cube 

The some function reference from dea_tools library(https://www.dea.ga.gov.au/)

'''

# Import required packages
import math
import folium
import numpy as np
import geopandas as gpd
import json
import os
import datacube 
import xarray as xr
import matplotlib.pyplot as plt 
import odc.ui


from pyproj import Transformer
from odc.ui import image_aspect
from folium.plugins import Draw, Geocoder, Fullscreen, LocateControl
from datacube.utils.cog import write_cog 

# This function is used to plot rgb image from dataset
def rgb(ds,
        bands=['red', 'green', 'blue'],
        index=None,
        index_dim='time',
        robust=True,
        percentile_stretch=None,
        col_wrap=4,
        size=6,
        aspect=None,
        savefig_path=None,
        savefig_kwargs={},
        **kwargs):
    
    # checks bands in dataset or not?
    ds_bands = list(ds.data_vars)
    if set(bands).issubset(ds_bands) == False:
       
        raise ValueError(
            'The bands of your dataset not match with rgb function'
            ' Please check the default is [red, green, blue]') 
    
    #get name of x,y dimension

    try: y_dim, x_dim = ds.geobox.dimension
    except AttributeError: 
        from datacube.utils import spatial_dims
        y_dim, x_dim = spatial_dims(ds)

    #create aspect size kwarg. it will be passed to imshow
    if 'ax' in kwargs:
        aspect_size_kwarg = {}
    else: 
        if not aspect:
            aspact = image_aspect(ds)
            
        aspect_size_kwarg = {'aspect': aspect, 'size': size}

    # <'index' is not provide value>
    #the index defult is none 
    #thus, plot using defult value and arguments passed via `**kwargs`
    if index is None:
        da = ds[bands].to_array()

        if percentile_stretch:
            value_min, valuse_max = da.compute().quantile(
                percentile_stretch).valuse
            
            kwargs.update({'vmin': value_min, 'vmax': valuse_max})

        #if it has more than 3 dims and index_dim = 1
        # squeeze this dimension out to remove it
        if ((len(index)>2) and ('col' not in kwargs) and
            (len(da[index_dim]) == 1)):
            da = da.squeeze(dim = index_dim)

        #if it has more than 3 dims and index_dim > 1
        elif ((len(ds.dims) > 2) and ('col' not in kwargs) and
              (len(da[index_dim]) > 1)):

            raise Exception(
                f'The input dataset `ds` has more than two dimensions: '
                f'{list(ds.dims.keys())}. Please select a single observation '
                'using e.g. `index=0`, or enable faceted plotting by adding '
                'the arguments e.g. `col="time", col_wrap=4` to the function '
                'call')
        da = da.compute()
        img = da.plot.imshow(robust=robust, 
                             col_wrap=col_wrap,
                             **aspect_size_kwarg,
                             **kwargs)
        
    #<If 'index' provide index value >
    else:
        
        # if 'index' give foat num, raise exception to change to int
        if isinstance(index, float):
            raise Exception(
                f'please provide index value as the integer or list of integer'
            )
        
        # if it provide 'col' too! raise exception
        if 'col' in kwargs:
            raise Exception(
                'Cannot provide both \'index\' and \'col\' '
                "Please remove one of it and try again"
            )
        
        # colect index into list to be computed
        index = index if isinstance(index, list) else [index]

        # select band and observations and convert to data array
        da = ds[bands].isel(**{index_dim:index}).to_array().compute()

        if percentile_stretch:
            value_min, valuse_max = da.compute().quantile(
                percentile_stretch).valuse
            
            kwargs.update({'vmin': value_min, 'vmax': valuse_max})
        
        # if multiple index
        if len(index)>1:
            img = da.plot.imshow(x=x_dim,
                                 y=y_dim,
                                 robust=robust,
                                 col=index_dim,
                                 col_wrap=col_wrap,
                                 **aspect_size_kwarg,
                                 **kwargs)

        # If only one index is supplied, squeeze out index_dim and plot as a single panel
        else:

            img = da.squeeze(dim=index_dim).plot.imshow(
                robust=robust, **aspect_size_kwarg, **kwargs)
            

    # If an export path is provided, save image to file. Individual and
    # faceted plots have a different API (figure vs fig) so we get around this
    # using a try statement:
    if savefig_path:

        print(f'Exporting image to {savefig_path}')

        try:
            img.fig.savefig(savefig_path, **savefig_kwargs)
        except:
            img.figure.savefig(savefig_path, **savefig_kwargs)       


def _degree_to_zoom_level(l1, l2, margin = 0.0):

    #Helper function to set zoom level for 'display_map'

    degree = abs(l1 - l2) * (1 + margin)
    zoom_level_int = 0
    if degree != 0:
        zoom_level_float = math.log(360/degree)/math.log(2)
        zoom_level_int = int(zoom_level_float)
    else:
        zoom_level_int = 18
    return zoom_level_int


def display_map(x, y, crs='EPSG:4326'):
    '''
    Generates a Folium map with a latlon bounded rectangle drawn on it.
    Parameters

    '''
    try:
        assert x is not None
        assert y is not None
    except AssertionError as error:
        print(error)
    
    # Convert each corner coordinates to lat-lon
    x_corner = (x[0], x[1], x[0], x[1])
    y_corner = (y[0], y[0], y[1], y[1])
    transformer = Transformer.from_crs(crs,"EPSG:4326")
    lon, lat = transformer.transform(x_corner, y_corner)

    # Calculate zoom level based on coordinates
    margin=-0.5 
    zoom_bias=0
    lat_zoom_level = _degree_to_zoom_level( min(lat), max(lat), margin=margin ) + zoom_bias
    lon_zoom_level = _degree_to_zoom_level(min(lon),max(lon), margin=margin ) + zoom_bias
    zoom_level = min(lat_zoom_level, lon_zoom_level)

    # Identify centre point for plotting
    center = [np.mean(lat), np.mean(lon)]

    # Create map
    Hybrid_map = folium.Map(
        location=center,
        zoom_start=zoom_level,
        tiles="http://mt1.google.com/vt/lyrs=y&z={z}&x={x}&y={y}",
        attr="Google")

    # Create bounding box coordinates to overlay on map
    line_segments = [(lat[0], lon[0]),
                     (lat[1], lon[1]),
                     (lat[3], lon[3]),
                     (lat[2], lon[2]),
                     (lat[0], lon[0])]

    # Add bounding box as an overlay
    Hybrid_map.add_child(folium.features.PolyLine(locations=line_segments,
                                                  color='orange',
                                                  opacity=0.8))

    # Add clickable lat-lon popup box
    Hybrid_map.add_child(folium.features.LatLngPopup())

    return Hybrid_map

# create map from lat/lon
def show_map(lat=None, lon=None, with_draw_tools=True,zoom=None):
    """Create a map using Folium."""
    
    # Set default latitude and longitude values
    if lat is None:
        lat = 13.726  # Bangkok latitude
    if lon is None:
        lon = 100.514  # Bangkok longitude
    
     # set default zoom level
    if zoom is None:
        zoom = 10
             
    # Create a map using Folium
    m = folium.Map(location=[lat, lon], zoom_start=zoom, tiles = None)
    
    # add geocoder plugin
    geocoder = Geocoder(position='topleft', collapsed=True, show=True)
    geocoder.add_to(m)
    
    # add LocateControl plugin
    Lo = LocateControl()
    Lo.add_to(m)
    
    # add fullscreen plugin
    Fullscreen().add_to(m) 
    
    # add masker location
    folium.Marker([lat, lon],
                  icon=folium.Icon(color="red", icon="flag")).add_to(m)
    
    # add WMTS
    # folium.WmsTileLayer('https://basemap.nationalmap.gov/arcgis/services/USGSTopo/MapServer/WMSServer?', 
    #                     layers='0', name = 'Topography', attr='USGS', format= 'image/png', transparent = True).add_to(m)
    
  
    # add tile layer map
    folium.TileLayer('https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', name='Google Satellite', attr='Google').add_to(m)
    folium.TileLayer('https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}', name='Terrain', attr='Google').add_to(m)
    folium.TileLayer('https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', name='Hybrid', attr='Google').add_to(m)
    folium.TileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', name='OpenStreetMap', attr='OpenStreetMap').add_to(m)
    folium.TileLayer('https://basemap.sphere.gistda.or.th/tiles/sphere_hybrid/EPSG3857/{z}/{x}/{y}.jpeg?key=42B90819583344A789DA424BE70CDB61', name='Gistda Hybrid', attr='sphere.gistda').add_to(m)
    folium.TileLayer('https://basemap.sphere.gistda.or.th/tiles/thailand_images/EPSG3857/{z}/{x}/{y}.jpeg?key=test2022', name='Gistda Satellite', attr='sphere.gistda').add_to(m)

    # Add layer control to the map
    folium.LayerControl().add_to(m)

    # Add drawing tools to create the polygon
    if with_draw_tools:
        
        draw = Draw(
            export=True,
            filename='drawn_polygons.geojson',
            draw_options={
                'polygon': {'allowIntersection': True},
                'rectangle': True,
                'circle':  True,
                'marker':  True,
                'polyline':  True,
            },
            edit_options={
                'featureGroup': None,
            },
        )

        draw.add_to(m)

    return m

# the function to display the polygons on the display map
def show_vector(file_paths):
     
    # Create a Folium map centered on the first polygon of the first file
    polygons = gpd.read_file(file_paths[0])
    center_lon, center_lat = polygons['geometry'][0].centroid.coords[0]
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13,  tiles = None)
    
    # Define a list of colors to use for each file
    colors = ['lime','blue', 'red', 'yellow','#40E0D0', 'orange', 'CA33FF','Aqua','Fuchsia',
             'lime','blue', 'red', 'yellow','#40E0D0', 'orange', 'CA33FF','Aqua','Fuchsia']
   
    # Read each GeoJSON file and create a GeoDataFrame
    gdfs = [gpd.read_file(file) for file in file_paths]
    
    # Add each GeoDataFrame as a separate layer with a different color
    for i, gdf in enumerate(gdfs):
        filename = os.path.splitext(os.path.basename(file_paths[i]))[0]
        folium.GeoJson(gdf,
                name=  filename,
                style_function=lambda x, color=colors[i]: {'color': color, 'fillOpacity': 0.2},
                tooltip=gdf.columns.tolist()).add_to(m)

                       
    # Add tile map
    folium.TileLayer('https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', name='Google Satellite', attr='Google').add_to(m)
    folium.TileLayer('https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}', name='Terrain', attr='Google').add_to(m)
    folium.TileLayer('https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', name='Hybrid', attr='Google').add_to(m)
    folium.TileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', name='OpenStreetMap', attr='OpenStreetMap').add_to(m)
    folium.TileLayer('https://basemap.sphere.gistda.or.th/tiles/sphere_hybrid/EPSG3857/{z}/{x}/{y}.jpeg?key=42B90819583344A789DA424BE70CDB61', name='Gistda Hybrid', attr='sphere.gistda').add_to(m)
    folium.TileLayer('https://basemap.sphere.gistda.or.th/tiles/thailand_images/EPSG3857/{z}/{x}/{y}.jpeg?key=42B90819583344A789DA424BE70CDB61', name='Gistda Satellite', attr='sphere.gistda').add_to(m)
    
    # Add layer control to the map
    folium.LayerControl().add_to(m)

    # Show the map
    return m

# the function to create new column in geojson file
# to add classtye table for training data
def geojson_add_Newcol(geojson_file_path):
    with open(geojson_file_path, 'r') as f:
        geojson_data = json.load(f)

    # Count the number of rows in the GeoJSON data
    
    num_rows = len(geojson_data['features'])
    print('num of rows: ',num_rows)
  
    # Prompt the user for the new column name and value
    new_column_name = input("Enter the name of the new column: ")
    # new_column_value = int(input("Enter the value for the new column: "))
    
    # Try to get an integer input for the new column value
    while True:
        new_column_value = input("Enter the value for the new column: ")
        try:
            new_column_value = int(new_column_value)
            break
        except ValueError:
            print("Invalid input: Please enter an integer value.")
    
    # Add the new column to each feature in the GeoJSON data
    for feature in geojson_data['features']:
        feature['properties'][new_column_name] = new_column_value

    # Write the updated GeoJSON data back to the file
    with open(geojson_file_path, 'w') as f:
        json.dump(geojson_data, f)

    # Return the number of rows in the GeoJSON data before the new column was added
    return num_rows


#load dataset from DC /plot color image from bands/export to GeoTiff
def get_img(query, filename):
   
    # connect to datacube
    dc = datacube.Datacube()
    
    # load dataset from query
    ds = dc.load(**query)
    print (ds)
    print('-'*50)
    a = list(ds.data_vars)[0]
    
    # preview img dataset
    img =ds[a].plot(col="time", robust=True)
    plt.show(img)
    
    # count num of timestep
    dss=len(ds.time)
    
    print ('-'*50)
    print ('There are:_ ' + str(dss) + '_timesteps')
    
    # get timestep from user
    time_step = int(input("Choose the timestep that you want like: [0,1,2,...] "))
    
    if len(query['measurements']) >= 3:
        #plot image selected
        rgb(ds, bands=query["measurements"][:3], index=time_step) 

    else: 
        pass

    
    # combine RGB bands into a single xarray DataArray
    rgb_array = xr.concat([ds[band].isel(time=time_step) for band in query['measurements']], dim='band')
    
    # export selected image to GeoTiff
    write_cog(geo_im=rgb_array, fname=filename, overwrite=True)
        
    # # export selected image to GeoTiff
    # write_cog(geo_im=ds[query['measurements'][0]].isel(time=time_step), fname=filename, overwrite=True)
     
    
    # Format the time stamp for use as the plot title
    time_string = str(ds.time.isel(time=time_step).values).split('.')[0]  

    # Set the title and axis labels
    ax = plt.gca()
    ax.set_title(f"Timestep {time_string}", fontweight='bold', fontsize=16)
    ax.set_xlabel('Easting (m)', fontweight='bold')
    ax.set_ylabel('Northing (m)', fontweight='bold')

    # Display the plot
    plt.show()
    
    
def find_centroid(file, output):
    
    # read input and erase file
    gdf = gpd.read_file(file)
    
    # perform func
    result = gdf.centroid
    
        #save to output
    result.to_file(output)
    
    

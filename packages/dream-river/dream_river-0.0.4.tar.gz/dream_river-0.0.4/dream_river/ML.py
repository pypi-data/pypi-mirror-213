import shapely
import xarray as xr
import datacube
import matplotlib
import pydotplus
import numpy as np
import subprocess as sp
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from io import StringIO
from odc.io.cgroups import get_cpu_quota
from sklearn.ensemble import RandomForestClassifier
from sklearn import model_selection
from sklearn.metrics import accuracy_score
from datacube.utils import geometry
from datacube.utils.cog import write_cog
from dea_tools.classification import collect_training_data, predict_xr

from convertools import vectorize
import warnings
warnings.filterwarnings("ignore")

def custom_loadband(query):

    # Initialise datacube
    dc = datacube.Datacube(app='extract_VI')

    # Load data using query
    dd = dc.load(**query)
    
    # band index
    dd['NDVI']=(dd.nir - dd.red)/(dd.nir + dd.red)
    dd['GNDVI']=(dd.nir - dd.green)/(dd.nir + dd.green)
    dd['EVI']=((2.5 * (dd.nir - dd.red))/(dd.nir + 6 * dd.red -7.5 * dd.blue + 1))
    dd['SAVI']=((1.5 * (dd.nir - dd.red))/(dd.nir + dd.red + 0.5))
    dd['NDWI']=(dd.green - dd.nir)/(dd.green + dd.nir)

    return dd

def custom_function(product, query):

    # Initialise datacube
    dc = datacube.Datacube(app='custom_feature_layers')

    # Load data using query
    ds = dc.load(product,**query)
    
    # band index
    ds['NDVI']=(ds.nir - ds.red)/(ds.nir + ds.red)
    ds['GNDVI']=(ds.nir - ds.green)/(ds.nir + ds.green)
    ds['EVI']=((2.5 * (ds.nir - ds.red))/(ds.nir + 6 * ds.red -7.5 * ds.blue + 1))
    ds['SAVI']=((1.5 * (ds.nir - ds.red))/(ds.nir + ds.red + 0.5))
    ds['NDWI']=(ds.green - ds.nir)/(ds.green + ds.nir)
    
    return ds

def rice_detect(ds, product, outname_raster, outname_vector, query, field):
    
    ######### Part create Training data ############################################## 
    
    # create polygon 
    vectorize(ds, outname_raster, outname_vector )

    # auto detect the num of CPUs 
    ncpus=round(get_cpu_quota())
       
    # load training data 
    input_data = gpd.read_file(outname_vector) #.shp or geojson
    
    # Extract data using shapfile(polygon)
    column_names, model_input = collect_training_data(gdf=input_data,
                                                      dc_query=query,
                                                      ncpus=ncpus,
                                                      feature_func=custom_loadband,
                                                      field=field,
                                                      zonal_stats='mean')
    
    ########### preprocessing training data ##########################################
    print(column_names)
   
    # Create a DataFrame from model_input
    df = pd.DataFrame(model_input, columns=column_names)

    # Create a GeoDataFrame from the DataFrame
    gdf = gpd.GeoDataFrame(df)
    
    # Define the query conditions
    ndvi_condition = (df['NDVI'].between(0.4, 0.65))
    gndvi_condition = (df['GNDVI'].between(0.4, 0.8))
    savi_condition = (df['SAVI'].between(0.4, 0.6))
    evi_condition = (df['EVI'].between(0.2, 0.8))
    ndwi_condition = (df['NDWI'].between(-0.5, -0.26))
 


    # Modify the input training data for single class labels
    model_input[:, 0] = np.where((ndvi_condition & (savi_condition|evi_condition|gndvi_condition)), 1, 0)
    
    

    # to check parameter as input
    A = gdf.describe()
    print(A)

    
    # Split into training and testing data (trai80/test20)
    model_train, model_test = model_selection.train_test_split(model_input, 
                                                               stratify=model_input[:, 0], 
                                                               train_size=0.7, 
                                                               random_state=0)
    print('#'*40)
    print("Train shape(70%):", model_train.shape)
    print("Test shape(30%):", model_test.shape)
    print('#'*40)
    
    
    # Convert model_train to a NumPy array
    model_train_array = model_train
    model_test_array = model_test
    ############## Model preparation #################################################

    # Select the variables we want to use to train our model
    model_variables = [col for col in column_names if col not in ["values"]]
    
    print('The variables for Training Model :', model_variables)
    
    # Extract relevant indices from the processed shapefile
    model_col_indices = [column_names.index(var_name) for var_name in model_variables]
    
    # Initialise model
    model = RandomForestClassifier(n_estimators=50)
    
    print("Initial call RF ML")
    ####################### Train Model/ predict #############################################
    
    # Train model
    model.fit(model_train_array[:, model_col_indices], model_train_array[:, column_names.index('values')])
    
    # Predict data
    predictions = model.predict( model_test_array[:, model_col_indices])
    
    print('Training Model!!!')
    
    # show the accuracy of prediction
    acc = accuracy_score(predictions,  model_test_array[:, 0])
    print('The accuracy of model is :',acc)
    
    # This shows the feature importance of the input features for predicting the class labels provided
    plt.bar(x=model_variables, height=model.feature_importances_)
    plt.gca().set_ylabel('Importance', labelpad=10)
    plt.gca().set_xlabel('Variable', labelpad=10);
    
    
    shape = input_data
    
    # Compute the bounding box of the union of all geometries in shp
    xmin, ymin, xmax, ymax = shape.unary_union.bounds
    
    # Convert bounding box coordinates to decimal degrees
    gdf_crs_decimal_degrees = shape.to_crs("EPSG:4326")
    xmin, ymin = gdf_crs_decimal_degrees.total_bounds[:2]
    xmax, ymax = gdf_crs_decimal_degrees.total_bounds[2:]

    print('x axis :',xmin, xmax)
    print('y axis :',ymin, ymax)
    
    # Set up the query parameters
    query2 = {
        # 'product': product, 
        'measurements': query['measurements'],
        'time': query['time'],
        'x': (xmin, xmax),
        'y': (ymin, ymax),
        'resolution': query['resolution'], 
        'output_crs': query['output_crs'],
        'group_by': 'solar_day'  }
    
    
    
    # Use custom function to generate input data
    input_data = custom_function(product,query=query2)
    
    
    # Predict landcover using the trained model
    predicted = predict_xr(model, input_data, clean=True)
    
    print('predicted!!!')

    
#################################### Plot output ############################################## 
 
    # Set up plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Plot classified image
    predicted.Predictions.plot(ax=axes[0], 
                   cmap='Greens', 
                   add_labels=False, 
                   add_colorbar=False)

    # Plot true colour image
    (input_data[['red', 'green', 'blue']]
     .squeeze('time')
     .to_array()
     .plot.imshow(ax=axes[1], robust=True, add_labels=False))

    # Remove axis on right plot
    axes[1].get_yaxis().set_visible(False)

    # Add plot titles
    axes[0].set_title('Classified data')
    axes[1].set_title('True colour image');
    
    print('plot image')
    
########################## Export output ###################################

    # Write the predicted data out to a GeoTIFF
    write_cog(predicted.Predictions,
             'predicted.tif',
              overwrite=True)
    print('Export predicted image')
################################################################################    
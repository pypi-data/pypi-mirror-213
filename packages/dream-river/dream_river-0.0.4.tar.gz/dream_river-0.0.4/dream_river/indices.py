import warnings
import numpy as np

def cal_index(ds,
              index=None,
              collection=None,
              custom_varname=None,
              normalise=True,
              drop=False,
              inplace=False):
    
    # Set ds equal to a copy of itself in order to prevent the function 
    # from editing the input dataset. This can prevent unexpected
    # behaviour though it uses twice as much memory. 
    if not inplace:
        ds = ds.copy(deep=True)
    
    # Capture input band names in order to drop these if drop=True
    if drop:
        bands_to_drop=list(ds.data_vars)
        print(f'Dropping bands {bands_to_drop}')

    # Dictionary containing remote sensing index band recipes
    index_dict = {
                  # Normalised Difference Vegation Index, Rouse 1973
                  'NDVI': lambda ds: (ds.nir - ds.red) /
                                     (ds.nir + ds.red),
        
                # Normalised Difference Vegation Index, Rouse 1973
                  'GNDVI': lambda ds: (ds.nir - ds.green) /
                                     (ds.nir + ds.green),

                  # Leaf Area Index, Boegh 2002
                  'LAI': lambda ds: (3.618 * ((2.5 * (ds.nir - ds.red)) /
                                     (ds.nir + 6 * ds.red -
                                      7.5 * ds.blue + 1)) - 0.118), 
        
                  # Ratio vegetation Index, Boegh 2002
                  'RVI': lambda ds: (ds.nir) /
                                     (ds.red), 
        
                  # Simple Ratio (SR) 
                  'SR': lambda ds: ds.nir/ds.red, 
        
                  # Soil Adjusted Vegetation Index, Huete 1988
                  'SAVI': lambda ds: ((1.5 * (ds.nir - ds.red)) /
                                      (ds.nir + ds.red + 0.5)),
        
                  # Modified Soil Adjusted Vegetation Index, Qi et al. 1994
                  'MSAVI': lambda ds: ((2 * ds.nir + 1 - 
                                      ((2 * ds.nir + 1)**2 - 
                                       8 * (ds.nir - ds.red))**0.5) / 2), 
        
                  # Normalised Difference Water Index, McFeeters 1996
                  'NDWI': lambda ds: (ds.green - ds.nir) /
                                     (ds.green + ds.nir),
        
                  # Water Index, Fisher 2016
                  'WI': lambda ds: (1.7204 + 171 * ds.green + 3 * ds.red -
                                    70 * ds.nir - 45 * ds.swir1 -
                                    71 * ds.swir2),
                  # Difference vegetation index (DVI) 
                  'DVI': lambda ds: (ds.nir - ds.red), 
        
                  # Enhanced Vegetation Index, Huete 2002
                  'EVI': lambda ds: ((2.5 * (ds.nir - ds.red)) /
                                     (ds.nir + 6 * ds.red -7.5 * ds.blue + 1)),
        
                  # Burn Area Index, Martin 1998
                  'BAI': lambda ds: (1.0 / ((0.10 - ds.red) ** 2 +
                                            (0.06 - ds.nir) ** 2)) }
    
    
    

    # If index supplied is not a list, convert to list. This allows us to
    # iterate through either multiple or single indices in the loop below
    indices = index if isinstance(index, list) else [index]
    
    #calculate for each index in the list of indices supplied (indexes)
    for index in indices:

        # Select an index function from the dictionary
        index_func = index_dict.get(str(index))

        # If no index is provided or if no function is returned due to an 
        # invalid option being provided, raise an exception informing user to 
        # choose from the list of valid options
        if index is None:

            raise ValueError(f"No remote sensing `index` was provided. Please "
                              "refer to the function \ndocumentation for a full "
                              "list of valid options for `index` (e.g. 'NDVI')")

        elif (index in ['WI','EVI', 'LAI', 'SAVI', 'MSAVI'] 
              and not normalise):

            warnings.warn(f"\nA coefficient-based index ('{index}') normally "
                           "applied to surface reflectance values in the \n"
                           "0.0-1.0 range was applied to values in the 0-10000 "
                           "range. This can produce unexpected results; \nif "
                           "required, resolve this by setting `normalise=True`")

        elif index_func is None:

            raise ValueError(f"The selected index '{index}' is not one of the "
                              "valid remote sensing index options. \nPlease "
                              "refer to the function documentation for a full "
                              "list of valid options for `index`")

        # Rename bands to a consistent format if depending on what collection
        # is specified in `collection`. This allows the same index calculations
        # to be applied to all collections. If no collection was provided, 
        # raise an exception.
        
        dataset = ['ls8_collections_sr_scene']
        if collection is None:

            raise ValueError("'No `collection` was provided. Please specify "
                             "either 'ls8_collections_sr_scene'"
                             "to ensure the function calculates indices using the "
                             "correct spectral bands")

        elif collection in dataset:

            # Dictionary mapping full data names to simpler 'red' alias names
            bandnames_dict = {
                'nir': 'nir',
                'red': 'red',
                'green': 'green',
                'blue': 'blue',
                'swir_1': 'swir1',
                'swir_2': 'swir2',
                'aerosol_qa	': 'aerosol_qa',
                'radsat_qa': 'radsat_qa',
                'pixel_qa': 'pixel_qa'
            }

            # Rename bands in dataset to use simple names (e.g. 'red')
            bands_to_rename = {
                a: b for a, b in bandnames_dict.items() if a in ds.variables
            }


        # Raise error if no valid collection name is provided:
        else:
            raise ValueError(f"'{collection}' is not a valid option for "
                              "`collection`. Please specify either \n"
                              "'ls8_collections_sr_scene'")

        # Apply index function 
        try:
            # If normalised=True, divide data by 10,000 before applying func
            mult = 10000.0 if normalise else 1.0
            index_array = index_func(ds.rename(bands_to_rename) / mult)
        except AttributeError:
            raise ValueError(f'Please verify that all bands required to '
                             f'compute {index} are present in `ds`. \n'
                             f'These bands may vary depending on the `collection` '
                             f'(e.g. the Landsat `nir` band \n'
                             f'is equivelent to `nir_1` for Sentinel 2)')

        # Add as a new variable in dataset
        output_band_name = custom_varname if custom_varname else index
        ds[output_band_name] = index_array
    
    # Once all indexes are calculated, drop input bands if inplace=False
    if drop and not inplace:
        ds = ds.drop(bands_to_drop)

    # If inplace == True, delete bands in-place instead of using drop
    if drop and inplace:
        for band_to_drop in bands_to_drop:
            del ds[band_to_drop]

    # Return input dataset with added water index variable
    return ds


        
                                    
        
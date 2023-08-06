#!/usr/bin/env python3
'''
|
|------------------------------------------------------------------------------------------
|
|  PARSE_VECTOR.PY
|
|  UPDATED:    2023-02-14
|  AUTHOR:     kent campbell
|  CONTACT:    campbellkb@ornl.gov
|
|  DESCRIPTION
|
|     This module provides functions for processing VECTOR granules such as kml, kmz & shp.
|
|------------------------------------------------------------------------------------------
|
'''
# | Python 3 standard library |
from os.path import sep, splitext, split as fsplit

# | Third party packages |
from osgeo import gdal, gdalconst, ogr

# | Local packages |
try:
    from utilities import datetime_override, file_checksum, get_file_size, spatial_coordinates, osr_spatial_reference_metadata
except:
    from scripts.utilities import datetime_override, file_checksum, get_file_size, spatial_coordinates, osr_spatial_reference_metadata

# |----------------------------------------------------------------------------
# | GDAL/OGR configuration.
# |----------------------------------------------------------------------------
# | Relevant links:
# |   https://gdal.org/api/index.html#python-api
# |----------------------------------------------------------------------------
# Register all known configured GDAL drivers.
gdal.AllRegister()

# Make lists of the current system's configured GDAL and OGR drivers.
gdal_drivers, ogr_drivers = [], []

# Loop over the GDAL driver count and append to list.
for i in range(gdal.GetDriverCount()):
    gdal_drivers.append(gdal.GetDriver(i).GetDescription())

# Loop over the OGR driver count and append to list.
for i in range(ogr.GetDriverCount()):
    ogr_drivers.append(ogr.GetDriver(i).GetDescription())

# Push exceptions to GDAL's built in error handler.
gdal.PushErrorHandler('CPLQuietErrorHandler')

# |----------------------------------------------------------------------------
# | VECTOR file functions
# |----------------------------------------------------------------------------
def vector_metadata(input_file: str, cfg_dict: dict = None):
    ''' Get metadata from a VECTOR granule
    
    Args:
        input_file (str): The path to a VECTOR granule.
        cfg_dict (dict): A dictionary of key/value pairs that represent configuration options.

    Returns:
        record (dict): Dictionary of metadata for the granule.
    '''
    try:
        metadata = {'filename': fsplit(input_file)[1],
                    'subdir': fsplit(input_file)[0].lstrip(sep)}

        # Add to metadata dictionary in stages
        metadata['attributes'] = vector_attributes(input_file)
        metadata['coordinates'] = vector_coordinates(input_file, cfg_dict)

        if not cfg_dict['no_stats']:
            metadata['statistics'] = vector_statistics(input_file)
        else:
            metadata['statistics'] = None

        metadata['variables'] = vector_variables(input_file)

        properties = vector_properties(input_file, cfg_dict)

        record = {'metadata': metadata,
                  'properties': properties
        }
    
        return record
    except:
        return None

def vector_attributes(input_file: str):
    '''Process a VECTOR granule's attributes.

    Args:
        input_file (str): The path to a VECTOR granule.
    
    Returns:
        dictionary of items for the attributes portion of the metadata
    '''
    try:
        # Try OGR drivers until one is successful, then break.
        for driver_name in ogr_drivers:
            try:
                # Get the driver object for the current driver long name.
                driver = ogr.GetDriverByName(driver_name)

                # Open in read only mode. OGR datasets CANNOT leave this context.
                dataset = driver.Open(input_file, gdalconst.GA_ReadOnly)
            except:
                pass
            else:
                if dataset:
                    break
        try:
            name = dataset.GetName()
            description = dataset.GetDescription()
            n_layers = dataset.GetLayerCount()
            n_spatial_ref = dataset.GetRefCount()
        except:
            name = None
            description = None
            n_layers = None
            n_spatial_ref = None

        try:
            for layer_number in range(0, dataset.GetLayerCount()):
                layer = dataset.GetLayerByIndex(layer_number)
                spatial_ref = osr_spatial_reference_metadata(layer)
        except:
            layer = None
            spatial_ref = None

        try:
            attributes = dataset.GetMetadata_Dict()
            style_table = dataset.GetStyleTable()
        except:
            attributes = None
            style_table = None

        dataset = None

        attributes = {
            # Get the dataset name, description, and driver description.
            'name': name,
            'description': description,
            'driver': driver_name,

            # Get the layer count.
            'n_layers': n_layers,
            
            # Get the spatial reference count.
            'n_spatial_reference': n_spatial_ref,
            
            # Get the spatial reference for the layer.
            'spatial_reference': spatial_ref,
            
            # Get the vector dataset's metadata attributes as a dictionary.
            'attributes': attributes,
            
            # Get the embedded style table, if it exists.
            'style_table': style_table,
        }

        return attributes
    except:
        return None

def vector_coordinates(input_file: str, cfg_dict: dict = None):
    '''Process a VECTOR granule's coordinates.

    Args:
        input_file (str): The path to a VECTOR granule.
        cfg_dict (dict): A dictionary of key/value pairs that represent configuration options.

    Returns:
        dictionary of items for the coordinates portion of the metadata
    '''
    try:
        # Try OGR drivers until one is successful, then break.
        for driver_name in ogr_drivers:
            try:
                # Get the driver object for the current driver long name.
                driver = ogr.GetDriverByName(driver_name)

                # Open in read only mode. OGR datasets CANNOT leave this context.
                dataset = driver.Open(input_file, gdalconst.GA_ReadOnly)
            except:
                pass
            else:
                if dataset:
                    break

        # Make a Record for each layer features and add to dict.
        for layer_number in range(0, dataset.GetLayerCount()):
            layer = dataset.GetLayerByIndex(layer_number)

            coordinates = spatial_coordinates(layer)

        temporal = vector_temporal(cfg_dict)
        coordinates['time'] = {'min': temporal['start_time'], 'max': temporal['end_time']}

        return coordinates
    except:
        return None

def vector_temporal(cfg_dict: dict = None):
    '''Process a VECTOR granule's temporal extents.

    Args:
        cfg_dict (dict): A dictionary of key/value pairs that represent configuration options.
    
    Returns:
        dictionary of items for the temporal extents of the metadata
    '''
    start_time, end_time = datetime_override(None, None, cfg_dict)

    temporal = {
        'start_time': start_time,
        'end_time': end_time,
    }

    return temporal

def vector_statistics(input_file: str):
    '''Process a VECTOR granule's statistics.

    Args:
        input_file (str): The path to a VECTOR granule.
    
    Returns:
        dictionary of items for the statistics portion of the metadata
    '''
    return None

def vector_variables(input_file: str):
    '''Process a VECTOR granule's variable list.

    Args:
        input_file (str): The path to a VECTOR granule.
    
    Returns:
        dictionary of items for the variables portion of the metadata
    '''
    try:
        # Try OGR drivers until one is successful, then break.
        for driver_name in ogr_drivers:
            try:
                # Get the driver object for the current driver long name.
                driver = ogr.GetDriverByName(driver_name)

                # Open in read only mode. OGR datasets CANNOT leave this context.
                dataset = driver.Open(input_file, gdalconst.GA_ReadOnly)
            except:
                pass
            else:
                if dataset:
                    break

        # Make a Record for each layer features and add to dict.
        for layer_number in range(0, dataset.GetLayerCount()):
            # Get layer (layer CAN leave this context; i.e. pass to/from functions).
            layer = dataset.GetLayerByIndex(layer_number)

            # Get the layer definition.
            # layer_defn = layer.GetLayerDefn()

            # A dictionary to store the layer schema.
            layer_schema = {}

            # NOTE: CODE BELOW GRABS VARIABLE NAMES FROM LAYERS WITHIN THE GRANULE, 
            # THAT BEHAVIOR IS NOT CONSISTENT WITH V2 (WHICH IS WHY IT IS COMMENTED OUT).

            # # Loop over the field indices and populate the schema dictionary.
            # for i in range(layer_defn.GetFieldCount()):
            #     # Get the definition for the current field.
            #     field_defn = layer_defn.GetFieldDefn(i)
                
            #     # Get the field name.
            #     field_name = field_defn.GetName()

            #     # Set the field schema by name.
            #     layer_schema[field_name] = {
            #         'index': i,
            #         'name': field_name,
            #         'type': field_defn.GetTypeName(),
            #         #'typeid': field_defn.GetType(),
            #         'precision': field_defn.GetPrecision(),
            #         'default': field_defn.GetDefault(),
            #         'nullable': False if field_defn.IsNullable() == 0 else True,
            #         'ignored': False if field_defn.IsIgnored() == 0 else True,
            #         'characters': field_defn.GetWidth(),
            #         'justify': field_defn.GetJustify(),
            #     }

            # NOTE: CODE BELOW GRABS VARIABLE NAMES FROM LAYERS WITHIN THE GRANULE, 
            # THAT BEHAVIOR IS NOT CONSISTENT WITH V3 (WHICH IS WHY IT IS COMMENTED OUT).

        variables = {
            'n_variables': len(list(layer_schema)),
            'variables': list(layer_schema),
            'variables_units': '',
            'variables_desc': '',
        }

        return variables
    except:
        return None

def vector_properties(input_file: str, cfg_dict: dict = None):
    '''Process a VECTOR granule's properties.

    Args:
        input_file (str): The path to a VECTOR granule.
    
    Returns:
        dictionary of items for the properties portion of the metadata
    '''
    if not cfg_dict['no_checksum']:
        checksum = file_checksum(input_file)
    else:
        checksum = None

    properties = {
        'format': 'vector',
        'size': get_file_size(input_file),
        'checksum': file_checksum(input_file),
    }

    return properties

def is_vector_granule(input_file: str, GMFT_dict: dict = None):
    '''Determine if granule is a VECTOR granule.

    Args:
        input_file (str): The path to a granule.
        GMFT_dict (dict): A dictionary of GranuleMeta Format Types.
    
    Returns:
        boolean indicating if it is a VECTOR granule.
    '''
    fext = splitext(input_file)[1]

    try:
        return ((fext in ['.kml', '.kmz', '.shp']) or
                (GMFT_dict[gdal.IdentifyDriver(input_file).ShortName] == 'vector'))
    except:
        return fext in ['.kml', '.kmz', '.shp']
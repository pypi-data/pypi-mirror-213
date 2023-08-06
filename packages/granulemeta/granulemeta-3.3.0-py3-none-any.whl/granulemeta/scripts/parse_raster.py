#!/usr/bin/env python3
'''
|
|------------------------------------------------------------------------------------------
|
|  PARSE_RASTER.PY
|
|  UPDATED:    2023-02-14
|  AUTHOR:     kent campbell
|  CONTACT:    campbellkb@ornl.gov
|
|  DESCRIPTION
|
|     This module provides functions for processing RASTER granules such as geoTIFFs
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
    from validate_cloud_optimized_geotiff import validate
except:
    from scripts.utilities import datetime_override, file_checksum, get_file_size, spatial_coordinates, osr_spatial_reference_metadata
    from scripts.validate_cloud_optimized_geotiff import validate

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
# | RASTER file functions
# |----------------------------------------------------------------------------
def raster_metadata(input_file: str, cfg_dict: dict = None):
    ''' Get metadata from a RASTER granule
    
    Args:
        input_file (str): The path to a RASTER granule.
        cfg_dict (dict): A dictionary of key/value pairs that represent configuration options.

    Returns:
        record (dict): Dictionary of metadata for the granule.
    '''
    try:
        metadata = {'filename': fsplit(input_file)[1],
                    'subdir': fsplit(input_file)[0].lstrip(sep)}

        dataset = gdal.Open(input_file, gdalconst.GA_ReadOnly)

        # Add to metadata dictionary in stages
        try:
            attr, stats = raster_attributes_and_statistics(dataset)
            metadata['attributes'] = attr
            if (metadata['attributes']['driver'] == 'GTiff'):
                if (is_COG(input_file)):
                    metadata['attributes']['driver'] = 'COG'
                else:
                    metadata['attributes']['driver'] = 'GeoTIFF'

            metadata['statistics'] = stats
        except:
            pass

        try:
            metadata['coordinates'] = raster_coordinates(dataset, cfg_dict)
        except:
            pass

        try:
            metadata['variables'] = raster_variables(input_file)
        except:
            pass

        properties = raster_properties(input_file, cfg_dict)

        record = {'metadata': metadata,
                  'properties': properties
        }
    
        return record
    except:
        return None
    finally:
        dataset = None

def raster_attributes_and_statistics(dataset):
    '''Process a RASTER granule's attributes.

    Args:
        dataset: a gdal.Dataset object
    
    Returns:
        dictionary of items for the attributes portion of the metadata
    '''
    try:
        # Collect statistics for each band (as a tuple) and add to dict.
        for band_number in range(1, dataset.RasterCount + 1):
            # Get the current band by its number.
            band = dataset.GetRasterBand(band_number)
            band_stats = raster_band_metadata(band)

        try:
            driver = dataset.GetDriver().GetDescription()
            description = dataset.GetDescription()
            n_cols = dataset.RasterXSize
            n_rows = dataset.RasterYSize
            n_bands = dataset.RasterCount
        except:
            driver = None
            description = None
            n_cols = None
            n_rows = None
            n_bands = None

        attributes = {
            # Get some basic metadata about the raster dataset.
            'driver': driver,
            'description': description,
            'n_cols': n_cols,
            'n_rows': n_rows,
            'n_bands': n_bands,
            
            # Get the embedded style table, if it exists.
            'style_table': dataset.GetStyleTable(),
            
            # Get the raster GeoTransform.
            'transform': dataset.GetGeoTransform(),
            
            # Get the raster's metadata attributes as a dictionary.
            'attributes': dataset.GetMetadata_Dict(),

            # Get the spatial reference for the raster dataset.
            'spatial_reference': osr_spatial_reference_metadata(dataset),

            # Get attributes pulled from band data.
            'scale': band_stats['attributes']['scale'],
            'offset': band_stats['attributes']['offset'],
        }

        statistics = {
            'min': band_stats['statistics']['min'],
            'max': band_stats['statistics']['max'],
            'mean': band_stats['statistics']['mean'],
            'std': band_stats['statistics']['std'],
            'data_type': band_stats['statistics']['data_type'],
            'missing_value': band_stats['statistics']['missing_value'],
        }

        return attributes, statistics
    except:
        return None

def raster_coordinates(dataset, cfg_dict: dict = None):
    '''Process a RASTER granule's coordinates.

    Args:
        dataset: a gdal.Dataset object
        cfg_dict (dict, optional): a dictionary of configuration key/value pairs.
    
    Returns:
        dictionary of items for the coordinates portion of the metadata
    '''
    try:
        coordinates = spatial_coordinates(dataset, swap_LL = True)

        temporal = raster_temporal(cfg_dict)

        coordinates['time'] = {'min': temporal['start_time'], 'max': temporal['end_time']}

        return coordinates
    except:    
        return None

def raster_temporal(cfg_dict: dict = None):
    '''Process a RASTER granule's temporal extents.

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
 
def raster_variables(input_file: str):
    '''Process a RASTER granule's variable list.

    Args:
        input_file (str): The path to a RASTER granule.
    
    Returns:
        dictionary of items for the variables portion of the metadata
    '''
    return None

def raster_properties(input_file: str, cfg_dict: dict = None):
    '''Process a RASTER granule's properties.

    Args:
        input_file (str): The path to a RASTER granule.
        cfg_dict (dict): A dictionary of key/value pairs that represent configuration options.
    
    Returns:
        dictionary of items for the properties portion of the metadata
    '''
    if not cfg_dict['no_checksum']:
        checksum = file_checksum(input_file)
    else:
        checksum = None

    properties = {
        'format': 'raster',
        'size': get_file_size(input_file),
        'checksum': checksum,
    }

    return properties

def raster_band_metadata(band):
    '''Get metadata for a single band within a RASTER granule.
    
    Args:
        band (osgeo.gdal.Band): An osgeo.gdal.Band.

    Returns:
        dict: A dictionary of metadata about a raster band.
    '''
    # Lightweight statistics calculation (uses GDAL C API).
    min_, max_, mean_, stdev_ = band.GetStatistics(
        0,  # 'approx_ok' (required): Do not compute stats from OVERVIEWS.
        1   # 'force' (required): Not sure...
    )

    # Return the band metadata in a dictionary.
    return {
        # Get all the band attributes available via Python accesss to GDAL API.
        'attributes': {
            'number': band.GetBand(),
            'description': band.GetDescription(),
            'n_overviews': band.GetOverviewCount(),
            'scale': band.GetScale(),
            'offset': band.GetOffset(),
            'categories': band.GetCategoryNames(),
            'checksum': band.Checksum(),
            'block_size': band.GetBlockSize(),
            'data_type_id': band.DataType,
            'data_type': gdal.GetDataTypeName(band.DataType),
            'unit_type': band.GetUnitType(),
            'mask_flags': band.GetMaskFlags(),
            'color_interp_id': band.GetColorInterpretation(),
            'color_interp': gdal.GetColorInterpretationName(band.GetColorInterpretation()),

            # Collect and unpack the band attributes, set all to lowercase.
            **{ k.lower(): v for k,v in band.GetMetadata_Dict().items() }
        },

        # Collect some band statistics in a dictionary.
        'statistics': {
            'data_type': gdal.GetDataTypeName(band.DataType),
            'missing_value': band.GetNoDataValue(),
            'default_histogram': band.GetDefaultHistogram(),
            'min': min_,
            'max': max_,
            'mean': mean_,
            'std': stdev_,
        }
    }

def is_raster_granule(input_file: str, GMFT_dict: dict = None):
    '''Determine if granule is a RASTER granule.

    Args:
        input_file (str): The path to a granule.
        GMFT_dict (dict): A dictionary of GranuleMeta Format Types.
    
    Returns:
        boolean indicating if it is a RASTER granule.
    '''
    fext = splitext(input_file)[1]

    try:
        return ((fext in ['.tif']) or
                (GMFT_dict[gdal.IdentifyDriver(input_file).ShortName] == 'raster'))
    except:
        return fext in ['.tif']

def is_COG(input_file: str):
    '''Determine if granule is a Cloud-Optimized GeoTIFF granule.

    Args:
        input_file (str): The path to a granule.
    
    Returns:
        boolean indicating if it is a Cloud-Optimized GeoTIFF granule.
    '''
    try:
        _, errors, _ = validate(input_file)
        is_cog_file = not errors
    except:
        is_cog_file = False

    return is_cog_file
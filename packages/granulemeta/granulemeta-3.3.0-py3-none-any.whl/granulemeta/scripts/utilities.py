#!/usr/bin/env python3
'''
|
|------------------------------------------------------------------------------
|
|  UTILITIES.PY
|
|  UPDATED:    2023-05-22
|  AUTHOR:     kent campbell
|  CONTACT:    campbellkb@ornl.gov
|
|  DESCRIPTION
|
|     This module provides general utility functions for granulemeta-v3
|
|------------------------------------------------------------------------------
|
'''
# | Python 3 standard library |
import re

from calendar import timegm
from hashlib import md5
from os import remove, sep, stat, walk
from os.path import isdir, isfile, normpath, sep, splitext
from subprocess import getoutput
from time import gmtime, strftime, strptime

# | Third party packages |
import numpy as np

from osgeo import osr, __version__ as osgeo_ver

# |----------------------------------------------------------------------------
# | sorting function(s)
# |----------------------------------------------------------------------------
def natural_key(string_):
    '''Allows application of "Natural Sorting" algorithm'''
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]

# |----------------------------------------------------------------------------
# | conversion function(s)
# |----------------------------------------------------------------------------
def dms2dd(dms):
    '''Converts degrees/minutes/seconds/direction to decimal degrees.
    
    Args:
        dms (str):  a lat or lon string in degrees/minutes/seconds/direction.

    Returns:
        dd (float): a lat or lon floating point number in decimal degrees.
    '''
    degrees, dms = dms.split('d', 1)
    minutes,dms = dms.split('\'', 1)
    seconds, direction = dms.split('"', 1)
    
    dd = float(degrees) + float(minutes) / 60 + float(seconds) / (60 * 60);
    
    if direction == 'W' or direction == 'S':
        dd *= -1
    
    return dd

# |----------------------------------------------------------------------------
# | file system utility functions
# |----------------------------------------------------------------------------
def get_directories(path):
    '''Retrieves a sorted list of subdirectories under the provided path. 

    Args:
        path (str): path to walk through in search of subdirectories
    
    Returns:
        sorted_directories (list): a sorted list of subdirectories
    '''
    directories = []

    for directory,_,_ in walk(path):
        if directory not in directories:
            directories.append(normpath(directory) + sep)

    sorted_directories = []

    for directory in sorted(directories, key = natural_key):
        sorted_directories.append(directory)

    return sorted_directories

def get_files(path):
    '''Retrieves a sorted list of files found within the provided path and its subdirectories 

    Args:
        path (str): path to recursively walk through in search of files
    
    Returns:
        sorted_filenames (list): a sorted list of files contained in the 
                                 directory searched and all its subdirectories
    '''
    filenames = []

    for d, _, f in walk(path):
        for fn in f:
            filename = normpath(d) + sep + fn

            if filename not in filenames:
                filenames.append(filename)
    
    sorted_filenames = []

    for fn in sorted(filenames, key = natural_key):
        sorted_filenames.append(fn)

    return sorted_filenames

def get_fileset(path):
    '''Retrieves a sorted list of files found within the provided path and its subdirectories 

    Args:
        path (list): a list containing one of the following:
                     1. a glob style list of files handled the command line and argparse
                     2. a singular file name (incl. path) without any wildcards
                     3. a single directory/path without any wildcards
    
    Returns:
        path (list): a sorted list of files to process for metadata
    '''
    if isinstance(path, list) and len(path) > 1:
        # glob style list of files handled by the command line and argparse
        return path
    elif isinstance(path, list) and isfile(path[0]):
        # singular file without wildcards
        return path
    elif isinstance(path, list) and isdir(path[0]):
        # directory without wildcards
        return get_files(path[0])

def file_checksum(path):
    '''Retrieves the MD5 checksum of a file.

    Args:
        filename (str): name of file (including path).
    
    Returns:
        checksum (str): MD5 checksum
    '''
    # Initiate the hash.
    hash_md5 = md5()

    # Open the file, loop over the chunks, and build hash.
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)

    checksum = hash_md5.hexdigest()

    return checksum

def get_file_size(input_file: str):
    '''Retrieves the size of a file in megabytes.

    Args:
        filename (str): name of file (including path).
    
    Returns:
        size (float):   size of file in megabytes.
    '''
    # Get the file size
    return stat(input_file).st_size * 0.000001

def is_extensionless(input_file: str):
    '''Determine if the file has a file extension

    Args:
        input_file (str): The path to a file

    Returns:
        boolean indicating if it lacks a file extension
    '''

    return splitext(input_file)[1] == ''

def remove_aux_xml_files(paths: list):
    '''Removes aux.xml files from a list of directories and/or paths.

    Args:
        paths (list): a list of directories and/or paths.
    
    Returns:
        N/A
    '''
    for path in paths:
        if isdir(path):
            for d, _, f in walk(path):
                for fn in f:
                    if fn[-8:] == '.aux.xml':
                        aux_xml = d.rstrip(sep) + sep + fn

                        try:
                            remove(aux_xml)
                            print('Removing: %s' %aux_xml)
                        except:
                            pass
                        
        elif isfile(path + '.aux.xml'):
            aux_xml = path + '.aux.xml'

            try:
                remove(aux_xml)
                print('Removing: %s' %aux_xml)
            except:
                pass

# |----------------------------------------------------------------------------
# | ascii function(s)
# |----------------------------------------------------------------------------
def read_ascii(filename):
    '''Reads the contents of an ASCII file

    Args:
        filename (str): name of file (including path) to read.

    Returns:
        lines (list):   a list of lines contained in the file.
    '''
    rfile = open(filename, 'r')
    lines = rfile.readlines()
    rfile.close()
    return lines

def write_line(filename, line, mode = 'a+'):
    '''Write a single line of text out to file

    Args:
        filename (str): name of file (including path) to write to.
        line (str):     the string to be written to file.
        mode (str):     writing mode ('a+' for append, 'w+' for write).
    
    Returns:
        N/A
    '''
    if isinstance(filename, str):
        wfile = open(filename, mode)
        wfile.write(line.rstrip() + '\n')
        wfile.close()
    else:
        filename.write(line + '\n')

def write_lines(filename, lines, mode = 'w+'):
    '''Write multiple lines to file

    Args:
        filename (str): name of file (including path) to write to.
        line (list):    a list of strings to be written to file.
        mode (str):     writing mode ('a+' for append, 'w+' for write).
    
    Returns:
        N/A
    '''
    if isinstance(filename, str):
        wfile = open(filename, mode)

        for line in lines:
            wfile.write(line.rstrip() + '\n')

        wfile.close()
    else:
        for line in lines:
            wfile.write(line.rstrip())

# |----------------------------------------------------------------------------
# | casting function(s)
# |----------------------------------------------------------------------------
def to_bool(val):
    if isinstance(val, str):
        if val.upper() == 'FALSE':
            return False
        elif val.upper() == 'TRUE':
            return True
        else:
            try:
                int_val = int(val)
                if int_val == 0:
                    return False
                elif int_val == 1:
                    return True
            except:
                return val
    elif isinstance(val, int):
        if val == 0:
            return False
        elif val == 1:
            return True
        else:
            return val
    else:
        return val

# |----------------------------------------------------------------------------
# | config/cmd line arg processing function(s)
# |----------------------------------------------------------------------------
def set_cfg_bool(arg, cfg_dict, val):
    if val in cfg_dict.keys():
        cfg_dict[val] = to_bool(cfg_dict[val])

    if arg is True or val not in cfg_dict.keys():
        cfg_dict[val] = arg
    
    return cfg_dict

def set_cfg_int(arg, cfg_dict, val):
    if arg != -1 or val not in cfg_dict.keys():
        cfg_dict[val] = int(arg)

    cfg_dict[val] = int(cfg_dict[val])

    return cfg_dict

def set_cfg_str(arg, cfg_dict, val):
    if arg is not None or val not in cfg_dict.keys():
        cfg_dict[val] = arg
    
    return cfg_dict

# |----------------------------------------------------------------------------
# | formatting function(s)
# |----------------------------------------------------------------------------
def format_num(num, handle_none = True):
    '''Format a string/number/None to a formatted numeric string (does not restrict number of decimal places)

    Args:
        num (str/float/int/None): "number" to convert/format
        handle_none (bool): handle "None" value if encountered
    
    Returns:
        num (str): a number formatted and converted to a string (usually for output to file)
    '''
    if num == '':
        return ''
    elif handle_none == True and (num is None):
        return ''
    else:
        if (round(num, 6) - int(num)) == 0.0:
            num = '%i' %num
        else:
            num = '%f' %num

    return num

def format_float(num, digits, return_zero = True):
    '''Format a string/number/None to a formatted numeric string

    Args:
        num (str/float/int/None): "number" to convert/format
        digits (int): number of decimal places to format the number to (if necessary)
        return_zero (bool): flag to toggle whether to return a zero or empty string for N/A values
    
    Returns:
        num (str): a number formatted and converted to a string (usually for output to file)
    '''
    if num is None or num == '':
        if return_zero == True:
            return '0'
        else:
            return ''

    num = float(num)
    if (num == float(int(num))):
        return '%i' %(int(num))
    else:    
        return '%.{0}f'.format(digits) %(num)

# |----------------------------------------------------------------------------
# | override start/end time (using config) function
# |----------------------------------------------------------------------------
def datetime_override(start_time_in = None, end_time_in = None, cfg_dict: dict = None):
    '''Overrides the start and/or end datetime(s) with those specified in the config file (if present).

    Args:
        start_time_in (str): start datetime as parsed from a granule
        end_time_in (str): end datetime as parsed from a granule
        cfg_dict (dict): A dictionary of key/value pairs that represent configuration options.
    
    Returns:
        start_time (str): The start datetime as it is supposed to appear in the output.
        end_time (str): The end datetime as it is supposed to appear in the output.
    '''
    if (cfg_dict is not None):
        try:
            # Handle possibility that start_date and start_time were provided separately
            if (('start_date' in cfg_dict.keys()) and 
                ('start_time' in cfg_dict.keys())):
                start_time = (cfg_dict['start_date'] + ' ' + cfg_dict['start_time'])
            # Handle possibility that start_date contains entire starting datetime value
            elif (('start_date' in cfg_dict.keys()) and 
                ('start_time' not in cfg_dict.keys())):
                start_time = cfg_dict['start_date']
            # Handle possibility that start_time contains entire starting datetime value
            elif (('start_date' not in cfg_dict.keys()) and 
                ('start_time' in cfg_dict.keys())):
                start_time = cfg_dict['start_time']
            else:
                start_time = start_time_in    
        except:
            start_time = start_time_in

        try:
            # Handle possibility that end_date and end_time were provided separately
            if (('end_date' in cfg_dict.keys()) and 
                ('end_time' in cfg_dict.keys())):
                end_time = (cfg_dict['end_date'] + ' ' + cfg_dict['end_time'])
            # Handle possibility that end_date contains entire ending datetime value
            elif (('end_date' in cfg_dict.keys()) and 
                ('end_time' not in cfg_dict.keys())):
                end_time = cfg_dict['end_date']
            # Handle possibility that end_time contains entire starting datetime value
            elif (('end_date' not in cfg_dict.keys()) and 
                ('end_time' in cfg_dict.keys())):
                end_time = cfg_dict['end_time']
            else:
                end_time = end_time_in
        except:
            end_time = end_time_in
    else:
        start_time = start_time_in
        end_time = end_time_in

    # If time is 00:00:00, roll back end time by one second, 
    # to prevent confusion regarding the timespan the granule covers.
    if end_time is not None:
        if ((cfg_dict['no_adjust_midnight_endtime'] is False) and (end_time[-8:] == '00:00:00')):
            try:
                end_time = strptime(end_time, '%Y-%m-%d %H:%M:%S')
                end_time = gmtime(timegm(end_time) - 1)
                end_time = strftime('%Y-%m-%d %H:%M:%S', end_time)
            except:
                # Cover cases where there's a 3 digit year
                tm = strptime(end_time[-14:], '%m-%d %H:%M:%S')
                tm = gmtime(timegm(tm) - 1)
                tm = strftime('%m-%d %H:%M:%S', tm)
                end_time = end_time[:-14] + tm
            
            print('NOTE: The \'end_time\' was decremented by 1 second to 23:59:59 of prior day.')
    return start_time, end_time

# |----------------------------------------------------------------------------
# | metadata helper function(s)
# |----------------------------------------------------------------------------
def get_subdataset_str(input_file: str):
    ''' Get the first subdataset that isn't for time or coordinates.
    
    Args:
        input_file (str): The path to a granule.
    
    Returns:
        subdataset_str (str): a string to use as part of a call to gdalinfo that 
                              will specify which subdataset to run gdalinfo upon
    '''
    # Determine if the input file has subdatasets
    output = getoutput('gdalinfo %s' %(input_file))

    # If there are subdatasets, use one of the correct ones
    sd_idx = 0
    for i,line in enumerate(output.split('\n')):
        if ('SUBDATASET_' in line and '_NAME=' in line and input_file in line and
            line.rsplit(':', 1)[-1] not in ['lat', 'lon', 'time', 'time_bnds']):
            sd_idx = int(line.split('_')[1])

    # Construct appropriate subdataset_str
    if (sd_idx > 0):
        subdataset_str = ' -sd %i' %(sd_idx)
    else:
        subdataset_str = ''

    return subdataset_str

def nc_dump_var(input_file: str, varname: str):
    ''' Grab data from a netCDF file for a given variable.
    
    Args:
        input_file (str): The path to a granule.
        varname (str): Variable name to dump from the granule.
    
    Returns:
        output (list): The text output from ncdump split on spaces and put into a list.
    '''
    try:
        output = getoutput('ncdump %s -v %s' %(input_file, varname))
        output = output.split('data:')[1].split(' ')
    except:
        output = getoutput('ncdump %s -v %s' %(input_file, varname.capitalize()))
        output = output.split('data:')[1].split(' ')

    return output

def nc_dump_var_dict(input_file: str):
    ''' Get a dict of variables and their attributes for a given netCDF file
    
    Args:
        input_file (str): The path to a granule.

    Returns:
        variables (dict): A dictionary of the variable names contained in 'input_file'
                          and attributes as available for each variable.
    '''
    try:
        output = getoutput('ncdump -h %s' %input_file)
    except:
        return None
    else:
        output = output.split('variables:')[1].split('// global attributes:')[0]
        output = output.split('\n')

        variables = {}
        for i, line in enumerate(output):
            if (len(line) > 0 and line[:2] != '\t\t'):
                # Get variable name
                line = line.strip().strip(';')
                var = line.split(' ')[1].split('(')[0].strip()

                variables[var] = {}

                # Get variable attributes
                for line in output[i+1:]:
                    if (var in line):
                        line = line.split(':', 1)[1]
                        line = line.strip(';').strip()
                        key, value = line.split('=', 1)

                        key = key.strip()
                        value = value.strip()

                        variables[var][key] = value
                    else:
                        break

        return variables

def access_keys(record: dict, keys: list):
    '''Access a value from a 'granulemeta.Record' metadata construct.
    
    Args:
		keys (list): an ordered list of keys to access a metadata field's value.
  
	Returns:
		any type: The value of the metadata field.
    '''
    try:
        # Iterate over the input keys and select the items sequentially.
        for k in keys:
            record = record[k]
    except TypeError:
        # This prevents errors when no data is found for given key.
        return ''
    except KeyError:
        return ''
    else:
        # Return the value at the terminal depth.
        if record is None:
            return ''
        else:
            return record

def access_list(record: dict, keys: list, varname: str, cfg_dict: dict):
    '''Access a value from a 'granulemeta.Record' metadata construct.
    
    Args:
        record (dict):  a dict of metadata for a single granule.
		keys (list):    an ordered list of keys to access a metadata field's value.
        varname (str):  a string indicating the name of the variable to set.
        cfg_dict (dict): A dictionary of key/value pairs that represent configuration options.
  
	Returns:
		any type: The value of the metadata field 
                  or the value overriding it from the config file.
    '''
    if (varname in cfg_dict.keys()):
        return cfg_dict[varname].split(',')
    else:
        return access_keys(record, keys)

def access_str(record: dict, keys: list, varname: str, cfg_dict: dict):
    '''Access a value from a 'granulemeta.Record' metadata construct.
    
    Args:
        record (dict):  a dict of metadata for a single granule.
		keys (list):    an ordered list of keys to access a metadata field's value.
        varname (str):  a string indicating the name of the variable to set.
        cfg_dict (dict): A dictionary of key/value pairs that represent configuration options.
  
	Returns:
		any type: The value of the metadata field 
                  or the value overriding it from the config file.
    '''
    if (varname in cfg_dict.keys()):
        return cfg_dict[varname]
    else:
        return access_keys(record, keys)

def access_int(record: dict, keys: list, varname: str, cfg_dict: dict):
    '''Access a value from a 'granulemeta.Record' metadata construct.
    
    Args:
        record (dict):  a dict of metadata for a single granule.
		keys (list):    an ordered list of keys to access a metadata field's value.
        varname (str):  a string indicating the name of the variable to set.
        cfg_dict (dict): A dictionary of key/value pairs that represent configuration options.
  
	Returns:
		any type: The value of the metadata field 
                  or the value overriding it from the config file.
    '''
    if (varname in cfg_dict.keys()):
        return int(cfg_dict[varname])
    else:
        try:
            return int(access_keys(record, keys))
        except:
            return access_keys(record, keys)

def access_flt(record: dict, keys: list, varname: str, cfg_dict: dict):
    '''Access a value from a 'granulemeta.Record' metadata construct.
    
    Args:
        record (dict):  a dict of metadata for a single granule.
		keys (list):    an ordered list of keys to access a metadata field's value.
        varname (str):  a string indicating the name of the variable to set.
        cfg_dict (dict): A dictionary of key/value pairs that represent configuration options.
  
	Returns:
		any type: The value of the metadata field 
                  or the value overriding it from the config file.
    '''
    if (varname in cfg_dict.keys()):
        flt = cfg_dict[varname]
    else:
        flt = access_keys(record, keys)

    try:
        if float(flt) == float(int(flt)):
            return int(flt)
        else:
            return float(flt)
    except:
        return(flt)

# |----------------------------------------------------------------------------
# | gdal spatial function(s)
# |----------------------------------------------------------------------------
def spatial_coordinates(layer, swap_LL = False):
    '''Returns a dictionary of coordinate mins and maxs for rasters and vectors.

    Args:
        layer (osgeo.gdal.Dataset, osgeo.ogr.Dataset): A GDAL/OGR dataset.

    Returns:
        dict: A dictionary in standard 'Record.metadata['coordinates']' format.
    '''
    proj_extent = spatial_extent(layer)
    geog_extent = proj_extent

    srs = osr_spatial_reference(layer)
    if srs is not None:
        if  srs.IsProjected() == 1:
            try:
                # If the layer is projected, try to transform. Ignore failures.
                geog_extent = spatial_extent_geographic(layer)
            except:
                pass
    
    x_res, y_res = spatial_coordinates_resolution(layer)

    if y_res is not None:
        y_res = abs(y_res)

    # Account for differences in versions of osgeo library
    if (swap_LL == True and osgeo_ver < '3.0.0'):
        geog_extent = geog_extent[2:4] + geog_extent[0:2]

    # Unpack the extents into a dictionary and return it.
    return {
        'x': {
            'min': proj_extent[0], 
            'max': proj_extent[1],
            'res': x_res,
        },
        'y': {
            'min': proj_extent[2], 
            'max': proj_extent[3],
            'res': y_res,
        },
        'lon': {
            'min': geog_extent[0], 
            'max': geog_extent[1],
            'res': x_res,
        },
        'lat': {
            'min': geog_extent[2], 
            'max': geog_extent[3],
            'res': y_res,
        },
    }

def spatial_extent(dataset):
    '''Returns the extent of input GDAL/OGR dataset in its native SRS.

    Args:
        dataset (osgeo.gdal.Dataset OR osgeo.ogr.Dataset): A GDAL/OGR dataset.

    Returns:
        tuple: A tuple of floats like: ``(x_min, x_max, y_min, y_max)``.
    '''
    
    # Try to get the extent (vectors & NOT-PROJECTED rasters).
    try:
        return dataset.GetExtent()
    
    # Else this must be a PROJECTED raster, calculate from GeoTransform. 
    except:
        # Get the raster's GeoTransform as its component parts.
        x_min, x_res, x_skew, y_max, y_skew, y_res = dataset.GetGeoTransform()
        
        # Get the opposite extremes of the 'x_min' and 'y_max'.
        x_max = x_min + (dataset.RasterXSize * x_res)
        y_min = y_max + (dataset.RasterYSize * y_res)
        
        # Return the extent.
        return(x_min, x_max, y_min, y_max)

def spatial_extent_geographic(dataset):
    '''Returns geographic extent (lat, lon) of input GDAL/OGR dataset layer.

    Args:
        dataset (osgeo.gdal.Dataset OR osgeo.ogr.Dataset): A GDAL/OGR dataset.

    Returns:
        tuple: A tuple of floats like: (lon_min, lon_max, lat_min, lat_max).
    '''

    # Get the extent in the native projection.
    xmin, xmax, ymin, ymax = spatial_extent(dataset)
    
    # Generate edge arrays to bound the dataset extent.
    x = np.linspace(xmin, xmax, num = 10)
    y = np.linspace(ymin, ymax, num = 10)
    edges = ([(xmin, iy) for iy in y] + 
             [(xmax, iy) for iy in y] +
             [(ix, ymin) for ix in x] + 
             [(ix, ymax) for ix in x])
    
    # Get the spatial reference of the dataset.
    srs = osr_spatial_reference(dataset)
    
    # Get a mew (empty) osr.SpatialReference instance.
    geographic = osr.SpatialReference()
    
    # Import WGS84.
    geographic.ImportFromEPSG(4326)
    
    # Transform the coordinates on the edge of the dataset to WGS84.
    t_points = np.apply_along_axis(spatial_transform, 1, edges, 
                                   from_srs = srs, to_srs = geographic)
    
    # Select the rectangular bounding extent by min, max of the 2d array.
    north, east = t_points.max(0)
    south, west = t_points.min(0)

    # Return the bounds.
    return(west, east, south, north)

def spatial_transform(xy: tuple, from_srs, to_srs):
    '''Transforms a point from one srs to another.

    Args:
        xy (tuple): an x and y pair as a tuple (float, float).
        from_srs (osr.SpatialReference): The source SRS.
        to_srs (osr.SpatialReference): The target SRS.

    Returns:
        tuple: Transformed point as a tuple (float, float).
    '''
    # Get the transform for the 'from_srs', 'to_srs' pair.
    coord_transform = osr.CoordinateTransformation(from_srs, to_srs)
    
    # Round the input x and y to 8 digits (matching standard gdal output).
    x_round, y_round = round(xy[0], 8), round(xy[1], 8)
    
    # Transform the points using the to-from coordinate transform.
    results = coord_transform.TransformPoint(x_round, y_round)
    
    # Return x and y.
    return(results[0], results[1])

def spatial_coordinates_resolution(layer):
    '''Returns a tuple (2) of x and y resolution for the input layer, or Nones.
    
    Args:
        layer (osgeo.gdal.Dataset, osgeo.ogr.Dataset): A GDAL/OGR dataset.
        
    Returns:
        tuple: (x_res, y_res) for rasters OR (None, None) for vectors.
    '''
    
    # If the parent submodule is OGR, return Nones.
    if layer.__module__ == 'osgeo.ogr':
        return (None, None)
    elif layer.__module__ == 'osgeo.gdal':
        # If it's GDAL, return the first and fifth elements.
        gt = layer.GetGeoTransform()
        
        return (gt[1], gt[5])
    else:
        # Else, this function received an unexpected input, return Nones.
        return (None, None)

def osr_spatial_reference(layer):
    '''Returns an osr.SpatialReference object for the input GDAL/OGR dataset.

    Args:
        layer (osgeo.gdal.Dataset OR osgeo.ogr.Layer): The input layer.

    Returns:
        osr.SpatialReference: An osr.SpatialReference object.
    '''
    # Try to get the osr.SpatialReference object directly
    try:
        srs = layer.GetSpatialRef()
    except:
        srs = None
    else:
        # If 'srs' is an instance of osr.SpatialReference, return it.
        return srs
    
    try:
        srs = osr.SpatialReference(wkt=layer.GetProjectionRef())
    except:
        pass
    else:
        # If 'srs' is an instance of osr.SpatialReference, return it.
        return srs
    
    # Try 'GetProjection' and return 'None' on failure
    try:
        return osr.SpatialReference(wkt=layer.GetProjection())
    except:
        return None

def osr_spatial_reference_metadata(layer = None):
    '''Construct the spatial_reference metadata dictionary for an input layer.

    Args:
        layer (osgeo.gdal.Dataset/osgeo.ogr.Layer, optional): A GDAL/OGR data layer.

    Returns:
        dict: Spatial reference system metadata following the standard for the
              'Record.metadata['attributes']['spatial_reference'] slot.
    '''
    # If layer is not None, get osr.SpatialReference object for vector layer.
    if layer is not None:
        srs = osr_spatial_reference(layer)
    
    if srs is None:
        # Initialize a new SRS object and import WGS84.
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(4326)

    if srs.IsGeographic():
        map_units = srs.GetAngularUnitsName()
    else:
        map_units = srs.GetLinearUnitsName()

    # Get the spatial reference for the layer.
    return {
        # A couple flags indicating whether or not SRS is projected.
        'geographic': srs.IsGeographic() == 1,
        'projected': srs.IsProjected() == 1,
        
        # Two representations of the SRS.
        'proj4': srs.ExportToProj4(),
        'well_known_text': srs.ExportToWkt(),
        'parameters':{'map_units': map_units},
    }

# |----------------------------------------------------------------------------
# | Value identification/matching functions used across data formats.
# |----------------------------------------------------------------------------
def string_select(strings: list, regex: str, common: list):
    '''Search a list (or dict) of fields for matches to an input regex.
    
    Args:
        strings (list) : A list or dict of fields to try to match.
        regex (str): A regular expression to match.
        common (list): A list of common abbreviations.
    
    Returns:
        The best match among matches to regex, or None.
    '''

    # Try to find all of the regex matches from input header row fields.
    result = list(filter(regex.match, [s.lower() for s in strings]))
    
    # Check to see if there is a 100% common match.
    for s in strings:
        if s in common:
            return s

    if len(result) == 0:
        # Return None if no matches.
        return None
    elif len(result) == 1:
        # If result length is 1, select matching input and return.
        return [s for s in strings if s.lower() == result[0]][0]
    elif len([r for r in result if r.lower().strip() in common]) > 0:
        # Else (if a common match exists) try to match results to one of these common abbreviations.
        result = [r for r in result if r.lower().strip() in common]
        
        # Return according to the same conditions as before.
        if len(result) == 0:
            return None
        elif len(result) == 1:
            return [s for s in strings if s.lower() == result[0]][0]
        else:
            # If there are still more than one, just guess the first one.
            return [s for s in strings if s.lower() == result[0]][0]
    else:
        # Just gimme the first one
        return [s for s in strings if s.lower() == result[0]][0]

def detect_nan(values: list, common_nans: list, drop_nan: bool = False):
    '''Identify the NaN value in an input value list and optionally drop it.

    Conditional logic informed by the configured ``common_nans`` values to 
    identify and optional drop NaNs from an input values list if the boolean
    keyword argument ``drop_nan`` is True (default: False).

    Args:
        values (list): The list of values to search for NaN.
        common_nans (list): A list of common NaN values for comparison.
        drop_nan (bool, optional): Set to True to drop the most likely NaN value 
                                   from the values list, returning both the NaN 
                                   and the values. Defaults to False.

    Returns:
        str:  The value identified as NaN, or None if no NaN was detected.
        list: The value list with NaN dropped if the ``drop_nan`` argument 
              was set to True (default: False).
    '''

    # NOTE: Add support for detecting multiple NaN values.
    
    # Set missing value to None by default.
    missing_value = None
    
    # Loop over the values.
    for val in values:
        # Check for the value in the common_nans list by its default type.
        if val in common_nans:
            # If value is in the common missing value list, break the loop.
            missing_value = val
            break

        # If the default type is not a match, try to match it as a numeric.
        else: 
            try:
                # Try to convert the value to an int and a float.
                i_val, f_val = int(val), float(val)
            except:
                # If it couldn't be converted, go to the next value.
                pass
            else:
                # If it could be converted, check if either is a common_nan.
                if i_val in common_nans or f_val in common_nans:
                    # If either form is in the list, break the loop.
                    missing_value = val
                    break
    
    # If drop_nan boolean argument is True, drop all NaN values from the list.
    if drop_nan:
        values = [v for v in values if v != missing_value]
        
    # Return the values and the NaN, if it was detected. Else it'll be None.
    return(values, missing_value)
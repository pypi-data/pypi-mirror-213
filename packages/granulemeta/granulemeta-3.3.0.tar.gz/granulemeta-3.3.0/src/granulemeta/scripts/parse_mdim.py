#!/usr/bin/env python3
'''
|
|------------------------------------------------------------------------------------------
|
|  PARSE_MDIM.PY
|
|  UPDATED:    2022-05-22
|  AUTHOR:     kent campbell
|  CONTACT:    campbellkb@ornl.gov
|
|  DESCRIPTION
|
|     This module provides functions for processing MDIM granules such as netCDFs & hdfs.
|
|------------------------------------------------------------------------------------------
|
'''
# | Python 3 standard library |
from os.path import sep, splitext, split as fsplit
from re import compile as re_compile
from subprocess import getoutput

# | Third-party packages |
from osgeo import gdal, gdalconst, osr
import netCDF4 as nc4

# | Local packages |
try:
    from utilities import datetime_override, dms2dd, file_checksum, get_file_size, get_subdataset_str, nc_dump_var, nc_dump_var_dict, string_select
except:
    from scripts.utilities import datetime_override, dms2dd, file_checksum, get_file_size, get_subdataset_str, nc_dump_var, nc_dump_var_dict, string_select
    
# |----------------------------------------------------------------------------
# | MDIM file functions
# |----------------------------------------------------------------------------
def mdim_metadata(input_file: str, cfg_dict: dict = None):
    ''' Get metadata from a MDIM granule
    
    Args:
        input_file (str): The path to a MDIM granule.
        cfg_dict (dict): A dictionary of key/value pairs that represent configuration options.

    Returns:
        record (dict): Dictionary of metadata for the granule.
    '''
    try:
        metadata = {'filename': fsplit(input_file)[1],
                    'subdir': fsplit(input_file)[0].lstrip(sep)
        }

        # Add to metadata dictionary in stages
        metadata['attributes'] = mdim_attributes(input_file)
        metadata['coordinates'] = mdim_coordinates(input_file, cfg_dict)

        if not cfg_dict['no_stats']:
            metadata['statistics'] = mdim_statistics(input_file)
        else:
            metadata['statistics'] = None

        metadata['variables'] = mdim_variables(input_file)

        properties = mdim_properties(input_file, cfg_dict)
        properties['format'] = metadata['attributes']['spatial_reference']['ftype']

        record = {
            'metadata': metadata,
            'properties': properties
        }

        return record
    except:
        return None

def mdim_attributes(input_file: str):
    '''Process a MDIM granule's attributes.

    Args:
        input_file (str): The path to a MDIM granule.
    
    Returns:
        dictionary of items for the attributes portion of the metadata
    '''
    try:
        # Check version of GDAL
        output = getoutput('gdalinfo --version')
        gdal_version = int(output.split('.')[0].upper().strip('GDAL'))

        # Set some variables depending on version of GDAL
        if gdal_version < 3:
            flags = ' -proj4'
            wkt_end_str = 'PROJ.4 string is:'
        else:
            flags = ' -proj4 -wkt_format WKT1'
            wkt_end_str = 'Data axis to CRS axis mapping:'

        # Use 'gdalinfo' terminal command and process values from returned output
        subdataset_str = get_subdataset_str(input_file)
        output = getoutput('gdalinfo %s%s%s' %(input_file, subdataset_str, flags))
        output = output.split('\n')

        # Check for a failure to open with gdalinfo
        if output[0][:7] == 'ERROR 4':
            # Process as VECTOR
            attributes = mdim_vector(input_file)
        else:
            # Process as RASTER
            attributes = mdim_raster(input_file, output, wkt_end_str)

        return attributes
    except:
        return None

def mdim_vector(input_file: str):
    '''Process a MDIM vector granule's attributes.

    Args:
        input_file (str): The path to a MDIM vector granule.
    
    Returns:
        dictionary of items for the attributes portion of the metadata
    '''
    try:
        with nc4.Dataset(input_file, 'r') as dataset:
            # If this is a trajectory netCDF, get only a spatial reference.
            if 'featureType' in dataset.__dict__.keys():
                # Initialize a new SRS object and import WGS84.
                srs = osr.SpatialReference()
                srs.ImportFromEPSG(4326)

                if srs.IsGeographic():
                    map_units = srs.GetAngularUnitsName()
                else:
                    map_units = srs.GetLinearUnitsName()

                if dataset.__dict__['featureType'] == 'trajectory':
                    file_type = 'trajectory'
                    geometry_type = 'LN'
                else:
                    file_type = 'vector'
                    geometry_type = 'BR'

                spatial_ref = {
                    'geographic': srs.IsGeographic(),
                    'projected': srs.IsProjected(),
                    'proj4': srs.ExportToProj4(),
                    'well_known_text': srs.ExportToWkt(),
                    'parameters': {'map_units':map_units},
                    'ftype': file_type,
                    'geom_type': geometry_type,
                }
            else:
                # Use gdal to open file.
                dataset = gdal.Open(input_file, gdalconst.GA_ReadOnly)

                if dataset is None:
                    spatial_ref = {
                        'ftype': 'vector',
                        'geom_type': 'BR'
                    }
                else:
                    # First, try to get the osr.SpatialReference object directly --------------
                    try:
                        srs = dataset.GetSpatialRef()
                    except:
                        srs = None
                    
                    if srs is None:
                        # Second, try to get it by conerting WKT string via 'GetProjectionRef' ----
                        try:
                            srs = osr.SpatialReference(wkt = dataset.GetProjectionRef())
                        except:
                            pass
                        
                    if srs is None:
                        # Third, try 'GetProjection' and return 'None' on failure -----------------
                        try:
                            srs = osr.SpatialReference(wkt = dataset.GetProjection())
                        except:
                            pass

                    # If srs is still None, initialize an SRS for WGS84
                    if srs is None:
                        srs = osr.SpatialReference()
                        srs.ImportFromEPSG(4326)

                    # Set values in spatial_ref dictionary.
                    spatial_ref = {
                            'geographic': srs.IsGeographic(),
                            'projected': srs.IsProjected(),
                            'proj4': srs.ExportToProj4(),
                            'well_known_text': srs.ExportToWkt(),
                            'parameters': {'map_units':map_units},
                            'ftype': 'vector',
                            'geom_type': 'BR',
                    }
    except:
        spatial_ref = {}
    finally:
        dataset = None

    attributes = {
        # Get some basic metadata about the MDIM vector dataset.
        'driver': gdal.IdentifyDriver(input_file).ShortName,
        # 'n_cols': n_cols,
        # 'n_rows': n_rows,
        # 'n_bands': n_bands,
        # **dataset.__dict__,
        'scale': {'1':1},
        'offset': {'1':0},

        # Get the spatial reference for the MDIM vector dataset.
        'spatial_reference': spatial_ref,
    }

    # for k,v in attributes.items():
    #     print(k,v)

    return attributes

def mdim_raster(input_file: str, output: list, wkt_end_str: str):
    '''Process a MDIM raster granule's attributes.

    Args:
        input_file (str): The path to a MDIM raster granule.
        output (list): List of lines returned from running gdalinfo commmand.
        wkt_end_str (str): String that signifies the end of the wkt string in output.
    
    Returns:
        dictionary of items for the attributes portion of the metadata
    '''
    proj4_idx = None
    wkt_idx_start = None
    wkt_idx_end = None

    transform = [None,None,None,None]
    n_cols, n_rows = None, None
    file_type = 'raster'
    geometry_type = 'BR'

    for i, line in enumerate(output):
        if ('PROJ.4 string is:' in line):
            proj4_idx = i + 1

        if ('Coordinate System is:' in line):
            wkt_idx_start = i+1
        
        if (wkt_end_str in line):
            wkt_idx_end = i

        # Get transform
        if ('Origin = (' in line):
            origin_x, origin_y = map(float, line.strip().split('Origin = (', 1)[1].strip(')').split(','))
            transform[0] = origin_x
            transform[2] = origin_y

        if ('Pixel Size = (' in line):
            pxl_sz_x, pxl_sz_y = map(float, line.strip().split('Pixel Size = (', 1)[1].strip(')').split(','))
            transform[1] = pxl_sz_x
            transform[3] = pxl_sz_y

        if ('featureType=trajectory' in line):
            file_type = 'trajectory'
            geometry_type = 'LN'

        # Get n_cols, n_rows and n_bands
        if ('Size is' in line) and ((n_cols is None) or (n_rows is None)):
            n_cols, n_rows = map(int, line.split('Size is ')[1].split(','))
        elif ('Block=' in line) and ((n_cols is None) or (n_rows is None)):
            n_bands, cr = line.rsplit('Block=', 1)
            n_bands = int(n_bands.strip().split(None,1)[-1])
            n_cols, n_rows = map(int, cr.split()[0].split('x'))

    n_bands = 1 # Hardcoding it just like Granulemeta-V1.

    # Get proj4 string
    native_crs_proj4 = ''
    if proj4_idx is not None:
        native_crs_proj4 = output[proj4_idx]

    # Get wkt string
    wkt = ''
    if (wkt_idx_start is not None and wkt_idx_end is not None):
        for i in output[wkt_idx_start:wkt_idx_end]:
            wkt += i.strip()

    # Peek into the mdim file (without too much cost, hopefully)
    map_units = None

    try:
        dataset = gdal.Open(input_file)
        prj = dataset.GetProjection()
        srs = osr.SpatialReference(wkt = prj)

        # Get map_units string
        if srs.IsGeographic():
            map_units = srs.GetAngularUnitsName()
        else:
            map_units = srs.GetLinearUnitsName()
    except:
        pass
    finally: 
        # Free up memory
        srs = None
        prj = None
        dataset = None

    spatial_ref = {
        'proj4':native_crs_proj4.strip("'"),
        'well_known_text': wkt,
        'parameters':{'map_units':map_units},
        'ftype': file_type,
        'geom_type': geometry_type,
    }

    attributes = {
        # Get some basic metadata about the MDIM raster dataset.
        'driver': gdal.IdentifyDriver(input_file).ShortName,
        'n_cols': n_cols,
        'n_rows': n_rows,
        'n_bands': n_bands,
        'scale': {'1':1},
        'offset': {'1':0},

        # Get the spatial reference for the MDIM raster dataset.
        'spatial_reference': spatial_ref,
    }  

    return attributes

def mdim_coordinates(input_file: str, cfg_dict: dict = None):
    '''Process a MDIM granule's coordinates.

    Args:
        input_file (str): The path to a MDIM granule.
    
    Returns:
        dictionary of items for the coordinates portion of the metadata
    '''
    try:
         # Use 'gdalinfo' terminal command and process values from returned output
        subdataset_str = get_subdataset_str(input_file)
        flags = ' -nogcp -norat -noct -nofl'
        output = getoutput('gdalinfo %s%s%s' %(input_file, subdataset_str, flags))

        if ('Pixel Size = ' in output):
            res_x, res_y = map(abs, map(float, output.split('Pixel Size = (')[1].split(')', 1)[0].split(',', 1)))
        else:
            res_x, res_y = None, None

        lons = []
        lats = []

        if ('Lower Left' in output):
            min_x, min_y = map(float, output.split('Lower Left  (', 1)[1].split(')', 1)[0].split(',', 1))
            lon, lat = output.split('Lower Left  (', 1)[-1].split(') (', 1)[-1].split(')', 1)[0].split(',', 1)

            if ('lat_LL' in output):
                lat = float(output.split('lat_LL=', 1)[1].split('\n', 1)[0])
            
            if ('lon_LL' in output):
                lon = float(output.split('lon_LL=', 1)[1].split('\n', 1)[0])

            lons.append(lon)
            lats.append(lat)
        else:
            min_x, min_y = None, None

        if ('Upper Right' in output):
            max_x, max_y = map(float, output.split('Upper Right (', 1)[1].split(')', 1)[0].split(',', 1))
            lon, lat = output.split('Upper Right (')[-1].split(') (', 1)[-1].split(')', 1)[0].split(',', 1)

            if ('lat_UR' in output):
                lat = float(output.split('lat_UR=', 1)[1].split('\n', 1)[0])
            
            if ('lon_UR' in output):
                lon = float(output.split('lon_UR=', 1)[1].split('\n', 1)[0])
                
            lons.append(lon)
            lats.append(lat)
        else:
            max_x, max_y = None, None
    
        if ('Lower Right' in output):
            lon, lat = output.split('Lower Right (')[-1].split(') (', 1)[-1].split(')', 1)[0].split(',', 1)

            if ('lat_LR' in output):
                lat = float(output.split('lat_LR=', 1)[1].split('\n', 1)[0])

            if ('lon_LR' in output):
                lon = float(output.split('lon_LR=', 1)[1].split('\n', 1)[0])
                
            lons.append(lon)
            lats.append(lat)

        if ('Upper Left' in output):
            lon, lat = output.split('Upper Left  (')[-1].split(') (', 1)[-1].split(')', 1)[0].split(',', 1)

            if ('lat_UL' in output):
                lat = float(output.split('lat_UL=', 1)[1].split('\n', 1)[0])
                
            if ('lon_UL' in output):
                lon = float(output.split('lon_UL=', 1)[1].split('\n', 1)[0])

            lons.append(lon)
            lats.append(lat)

        # Convert lons from DMS to decimal degrees and find the mins and maxes.
        if (len(lons) == 0):
            min_lon = None
            max_lon = None
        else:
            # Assume format of values is something like 74d12'45"N for coordinates
            try:
                # if so, convert to decimal degrees
                min_lon = min(map(dms2dd, lons))
                max_lon = max(map(dms2dd, lons))
            except (AttributeError, ValueError):
                # If conversion fails, assume already in decimal degrees
                min_lon = min(map(float, lons))
                max_lon = max(map(float, lons))

        # Convert lats from DMS to decimal degrees and find the mins and maxes.
        if (len(lats) == 0):
            min_lat = None
            max_lat = None
        else:
            # Assume format of values is something like 72d49'16.15"W for coordinates, convert to decimal degrees
            try:
                # If so, convert to decimal degrees
                min_lat = min(map(dms2dd, lats))
                max_lat = max(map(dms2dd, lats))
            except (AttributeError, ValueError):
                # If conversion fails, assume already in decimal degrees
                min_lat = min(map(float, lats))
                max_lat = max(map(float, lats))

        if ((None in [min_lat, max_lat, min_lon, max_lon]) or
            (min_lat < -90 or min_lat > 90) or (max_lat < -90 or max_lat > 90) or
            (min_lon < -180 or min_lon > 180) or (max_lon < -180 or max_lon > 180)):
            common_lats = ["y", "lt", "lat", "latitude",]
            if 'lat_name' in cfg_dict.keys():
                common_lats = [cfg_dict['lat_name']] + common_lats
            
            common_lons = ["x", "ln", "lng", "lon", "long", "longitude",]
            if 'lon_name' in cfg_dict.keys():
                common_lons = [cfg_dict['lon_name']] + common_lons
            
            # Values aren't correct, try getting them from netCDF variables
            variable_config = {
                'lat': {
                    'regex': re_compile('.*lat.*'),
                    'common': common_lats,
                },
                'lon': {
                    'regex': re_compile('.*lon.*'),
                    'common': common_lons,
                },
            }

            var_list = list(nc_dump_var_dict(input_file).keys())

            variables_output = {}
            for variable_name, variable_selectors in variable_config.items():
                try:
                    # Try to match to the list of columns.
                    match = string_select(strings = var_list,
                                          regex = variable_selectors['regex'], 
                                          common = variable_selectors['common'])
                except Exception as e:
                    # Ignore exceptions
                    pass
                else:
                    # If the match is not None, dump the variable values.
                    if match is not None:
                        try:
                            output = nc_dump_var(input_file, match)

                            values = []
                            for val in output:
                                val = val.strip()
                                val = val.strip(',')
                                val = val.strip('}')

                                try:
                                    val = float(val)
                                except:
                                    pass
                                else:
                                    values.append(float(val))
                        except:
                            continue
                        else:
                            if len(values) > 0:
                                variables_output[variable_name] = values

            # Get the min and max values from the dumped lat and lon values.
            try:
                min_lat = min(variables_output['lat'])
                max_lat = max(variables_output['lat'])
                min_lon = min(variables_output['lon'])
                max_lon = max(variables_output['lon'])
            except:
                min_lat = None
                max_lat = None
                min_lon = None
                max_lon = None

        temporal = mdim_temporal(input_file, cfg_dict)

        coordinates = {
            'x': {'res': res_x, 'min': min_x, 'max': max_x},
            'y': {'res': res_y, 'min': min_y, 'max': max_y},
            'z': {'res': 0, 'min': 0, 'max': 0},
            'lat': {'min': min_lat, 'max': max_lat},
            'lon': {'min': min_lon, 'max': max_lon},
            'time': {'min': temporal['start_time'], 'max': temporal['end_time']},
        }

        return coordinates
    except:
        return None

def mdim_temporal(input_file: str, cfg_dict: dict = None):
    '''Process a MDIM granule's temporal extents.

    Args:
        input_file (str): The path to a MDIM granule.
        cfg_dict (dict): A dictionary of key/value pairs that represent configuration options.
    
    Returns:
        dictionary of items for the temporal extents of the metadata
    '''
    try:
        dataset = nc4.Dataset(input_file, 'r')
        variables = list(dataset.variables)

        # If neither 'time' nor 'time_bnds' are in the dataset, return Nones.
        time_var = 'time'
        skip_time_section = False

        if 'time' not in variables and 'time_bnds' not in variables:
            common_dates = ['date', 'datetime', 'timestamp',]
            if 'date_name' in cfg_dict.keys():
                common_dates = [cfg_dict['date_name']] + common_dates

            common_times = ['time', 'datetime', 'timestamp',]
            if 'time_name' in cfg_dict.keys():
                common_times = [cfg_dict['time_name']] + common_times

            # Try finding the time values in variables instead of dimensions
            variable_config = {
                'date': {
                    'regex': re_compile('.*date.*'),
                    'common': common_dates,
                },
                'time': {
                    'regex': re_compile('.*time.*'),
                    'common': common_times,
                },
            }

            var_list = list(nc_dump_var_dict(input_file).keys())

            for _, variable_selectors in variable_config.items():
                try:
                    # Try to match to the list of columns.
                    match = string_select(strings = var_list,
                                          regex = variable_selectors['regex'], 
                                          common = variable_selectors['common'])
                except:
                    pass
                else:
                    if match is not None:
                        time_var = match
                        skip_time_section = False
                    else:
                        skip_time_section = True

        if skip_time_section == False:
            try:
                nctime = dataset.variables['time_bnds'][:]
                s_time = nctime.min()
                e_time = nctime.max()
            except:
                nctime = dataset.variables[time_var][:]
                time_array = nctime.__array__().flatten()
                size = len(time_array)
                res = (time_array.max() - time_array.min()) / size
                s_time = time_array.min() - res / 2
                e_time = time_array.max() + res / 2

            # Get time units.
            try:
                t_unit = nctime.units
            except AttributeError:
                t_unit = dataset.variables[time_var].units

            # And try to get the calendar, falling back on 'gregorian'.
            try:
                t_cal = nctime.calendar
            except AttributeError:
                t_cal = u'gregorian'

            # Get start time and put it in the DAAC time format.
            try:
                start_time = nc4.num2date(s_time, units = t_unit, calendar = t_cal)
                start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
            except:
                start_time = None

            # Get end time and put it in the DAAC time format.
            try:
                end_time = nc4.num2date(e_time, units = t_unit, calendar = t_cal)
                end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
            except:
                end_time = None
        else:
            start_time = None
            end_time = None
    except:
        start_time = None
        end_time = None
    finally:
        # Free up memory
        nctime = None
        dataset = None

    try:
        start_time, end_time = datetime_override(start_time, end_time, cfg_dict)
        # NOTE: The call to datetime_override() handles the 1 second rollback functionality.
        #       It could be repeated below "to make sure", but it's not necessary, thus not done.
    except:
        pass

    temporal = {
        'start_time': start_time,
        'end_time': end_time,
    }

    return temporal

def mdim_statistics(input_file: str):
    '''Process a MDIM granule's statistics.

    Args:
        input_file (str): The path to a MDIM granule.
    
    Returns:
        dictionary of items for the statistics portion of the metadata
    '''
    try:
        # Use 'gdalinfo' terminal command and process values from returned output
        subdataset_str = get_subdataset_str(input_file)
        flags = ' -stats'
        output = getoutput('gdalinfo %s%s%s' %(input_file, subdataset_str, flags))

        if (' Type=' in output):
            native_datatype = output.split(' Type=')[1].split(',')[0]
        else:
            native_datatype = None

        if ('_FillValue=' in output):
            nodata_val = float(output.split('_FillValue=', 1)[1].split('\n', 1)[0])
        elif ('NoData Value=' in output):
            nodata_val = float(output.split('NoData Value=', 1)[1].split('\n', 1)[0])
        else:
            nodata_val = None

        min_val = None
        max_val = None
        mean_val = None
        stdev_val = None

        mean_ct = 0
        stdev_ct = 0

        for line in output.split('\n'):
            if ('STATISTICS_MINIMUM' in line):
                val = float(output.split('STATISTICS_MINIMUM=', 1)[1].split('\n', 1)[0])

                if (min_val is None or val < min_val):
                    min_val = val
            elif('STATISTICS_MAXIMUM' in line):
                val = float(output.split('STATISTICS_MAXIMUM=', 1)[1].split('\n', 1)[0])

                if (max_val is None or val > max_val):
                    max_val = val
            elif('STATISTICS_MEAN' in line):
                val = float(output.split('STATISTICS_MEAN=', 1)[1].split('\n', 1)[0])

                if (mean_val is None):
                    mean_val = val
                else:
                    mean_val += val

                mean_ct += 1
            elif('STATISTICS_STDDEV' in line):
                val = float(output.split('STATISTICS_STDDEV=', 1)[1].split('\n', 1)[0])

                if (stdev_val is None):
                    stdev_val = val
                else:
                    stdev_val += val

                stdev_ct += 1

        if mean_val is None:
            mean_val = 0
        else:
            mean_val = mean_val / mean_ct

        if stdev_val is None:
            stdev_val = 0
        else:
            stdev_val = stdev_val / stdev_ct
        
        statistics = {
            'data_type': native_datatype,
            'missing_value': nodata_val,
            'min': min_val,
            'max': max_val,
            'mean': mean_val,
            'std': stdev_val,
        }

        return statistics
    except:
        return None

def mdim_variables(input_file: str):
    '''Process a MDIM granule's variable list.

    Args:
        input_file (str): The path to a MDIM granule.
    
    Returns:
        dictionary of items for the variables portion of the metadata
    '''
    try:
        var_dict = nc_dump_var_dict(input_file)

        variables = []
        units = []
        desc = []
        for k in var_dict.keys():
            variables.append(k)

            try:
                units.append(var_dict[k]['units'])
            except:
                units.append('')

            try:
                desc.append(var_dict[k]['long_name'])
            except:
                desc.append('')

        variables_units = ''
        for var in units:
            if variables_units == '':
                variables_units = var.strip()
            else:
                variables_units += '; %s' %var

        variables_desc = ''
        for var in desc:
            if variables_desc == '':
                variables_desc = var.strip()
            else:
                variables_desc += '; %s' %var

        variables_units = '"' + variables_units.rstrip(';').replace('"', '') + '"'
        variables_desc = '"' + variables_desc.rstrip(';').replace('"', '') + '"'

        variables = {
            'n_variables': len(variables),
            'variables': variables,
            'variables_units': variables_units,
            'variables_desc': variables_desc,
        } 

        return variables    
    except:
        return None

def mdim_properties(input_file: str, cfg_dict: dict = None):
    '''Process a MDIM granule's properties.

    Args:
        input_file (str): The path to a MDIM granule.
    
    Returns:
        dictionary of items for the properties portion of the metadata
    '''
    if not cfg_dict['no_checksum']:
        checksum = file_checksum(input_file)
    else:
        checksum = None

    properties = {
        'size': get_file_size(input_file),
        'checksum': checksum,
    }

    return properties

def is_mdim_granule(input_file: str):
    '''Determine if granule is a MDIM granule.

    Args:
        input_file (str): The path to a granule.
    
    Returns:
        boolean indicating if it is a MDIM granule.
    '''
    fext = splitext(input_file)[1]
    return fext in ['.nc', '.nc4', '.h5', '.hdf5', '.hdf']
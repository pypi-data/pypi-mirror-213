#!/usr/bin/env python3
'''
|
|------------------------------------------------------------------------------
|
|  PARSE_ENVI.PY
|
|  UPDATED:    2023-02-14
|  AUTHOR:     kent campbell
|  CONTACT:    campbellkb@ornl.gov
|
|  DESCRIPTION
|
|     This module provides functions for processing ENVI granules
|
|------------------------------------------------------------------------------
|
'''
# | Python 3 standard library |
from os.path import isfile, sep, splitext, split as fsplit
from subprocess import getoutput

# | Local packages |
try:
    from utilities import datetime_override, dms2dd, file_checksum, get_file_size, get_subdataset_str, is_extensionless
except:
    from scripts.utilities import datetime_override, dms2dd, file_checksum, get_file_size, get_subdataset_str, is_extensionless
    
# |----------------------------------------------------------------------------
# | ENVI granule functions
# |----------------------------------------------------------------------------
def envi_metadata(input_file: str, cfg_dict: dict = None):
    ''' Get metadata from an ENVI granule
    
    Args:
        input_file (str): The path to an ENVI granule.
        cfg_dict (dict): A dictionary of key/value pairs that represent configuration options.

    Returns:
        record (dict): Dictionary of metadata for the granule.
    '''
    try:
        metadata = {'filename': fsplit(input_file)[1],
                    'subdir': fsplit(input_file)[0].lstrip(sep)}

        # Add to metadata dictionary in stages
        metadata['attributes'] = envi_attributes(input_file)
        metadata['coordinates'] = envi_coordinates(input_file, cfg_dict)

        if not cfg_dict['no_stats']:
            metadata['statistics'] = envi_statistics(input_file)
        else:
            metadata['statistics'] = None

        metadata['variables'] = envi_variables(input_file)

        properties = envi_properties(input_file, cfg_dict)

        record = {'metadata': metadata,
                  'properties': properties
        }

        return record
    except:
        return None

def envi_attributes(input_file: str):
    '''Process an ENVI granule's attributes.

    Args:
        input_file (str): The path to an ENVI granule.
    
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

        proj4_idx = None
        wkt_idx_start = None
        wkt_idx_end = None

        transform = [None,None,None,None]
        n_cols, n_rows = None, None
        for i,line in enumerate(output):
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

            # Get n_cols, n_rows and n_bands
            if ('Size is' in line) and ((n_cols is None) or (n_rows is None)):
                n_cols, n_rows = map(int, line.split('Size is ')[1].split(','))
            elif ('Block=' in line) and ((n_cols is None) or (n_rows is None)):
                n_bands, cr = line.rsplit('Block=', 1)
                n_bands = int(n_bands.strip().split(None,1)[-1])
                n_cols, n_rows = map(int, cr.split()[0].split('x'))

        n_bands = 1 # Hardcoding it just like Granulemeta-V1.

        # get proj4 string
        native_crs_proj4 = ''
        if proj4_idx is not None:
            native_crs_proj4 = output[proj4_idx]

        # get wkt string
        wkt = ''
        if (wkt_idx_start is not None and wkt_idx_end is not None):
            for i in output[wkt_idx_start:wkt_idx_end]:
                wkt += i.strip()

        # get map_units string
        try:
            if isfile(input_file + '.hdr'):
                rfile = open(input_file + '.hdr', 'r')
            else:
                rfile = open(splitext(input_file)[0] + '.hdr', 'r')
                
            text = rfile.read()
            rfile.close()

            map_units = text.split('units=', 1)[1].split('\n', 1)[0]
        except:
            map_units = ''

        spatial_ref = {'proj4':native_crs_proj4.strip("'"),
                       'well_known_text': wkt,
                       'parameters':{'map_units':map_units}
        }

        attributes = {
            # Get some basic metadata about the ENVI dataset.
            'driver': 'ENVI',

            'n_cols': n_cols,
            'n_rows': n_rows,
            'n_bands': n_bands,
            'scale': {'1':1},
            'offset': {'1':0},

            # Get the spatial reference for the ENVI dataset.
            'spatial_reference': spatial_ref,
        }

        return attributes
    except:
        return None

def envi_coordinates(input_file: str, cfg_dict: dict = None):
    '''Process an ENVI granule's coordinates.

    Args:
        input_file (str): The path to an ENVI granule.
    
    Returns:
        dictionary of items for the coordinates portion of the metadata
    '''
    try:
         # Use 'gdalinfo' terminal command and process values from returned output
        subdataset_str = get_subdataset_str(input_file)
        flags = ' -nogcp -nomd -norat -noct -nofl'
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
            lons.append(lon)
            lats.append(lat)
        else:
            min_x, min_y = None, None
        
        if ('Upper Right' in output):
            max_x, max_y = map(float, output.split('Upper Right (', 1)[1].split(')', 1)[0].split(',', 1))
            lon, lat = output.split('Upper Right (')[-1].split(') (', 1)[-1].split(')', 1)[0].split(',', 1)
            lons.append(lon)
            lats.append(lat)
        else:
            max_x, max_y = None, None

        if ('Lower Right' in output):
            lon, lat = output.split('Lower Right (')[-1].split(') (', 1)[-1].split(')', 1)[0].split(',', 1)
            lons.append(lon)
            lats.append(lat)

        if ('Upper Left' in output):
            lon, lat = output.split('Upper Left  (')[-1].split(') (', 1)[-1].split(')', 1)[0].split(',', 1)
            lons.append(lon)
            lats.append(lat)

        # Convert lats & lons from DMS to decimal degrees and find the mins and maxes for both sets.
        if (len(lons) == 0):
            min_lon = None
            max_lon = None
        else:
            # assume format of values is something like 74d12'45"N for coordinates
            try:
                # if so, convert to decimal degrees
                min_lon = min(map(dms2dd, lons))
                max_lon = max(map(dms2dd, lons))
            except ValueError:
                # if conversion fails, assume already in decimal degrees
                min_lon = min(map(float, lons))
                max_lon = max(map(float, lons))

        if (len(lats) == 0):
            min_lat = None
            max_lat = None
        else:
            # assume format of values is something like 72d49'16.15"W for coordinates, convert to decimal degrees
            try:
                # if so, convert to decimal degrees
                min_lat = min(map(dms2dd, lats))
                max_lat = max(map(dms2dd, lats))
            except ValueError:
            # if conversion fails, assume already in decimal degrees
                min_lat = min(map(float, lats))
                max_lat = max(map(float, lats))

        temporal = envi_temporal(input_file, cfg_dict)

        coordinates = {
            'x': {'res': res_x, 'min': min_x, 'max': max_x},
            'y': {'res': res_y, 'min': min_y, 'max': max_y},
            'z': {'res': 0, 'min': 0, 'max': 0},
            'lat': {'min': min_lat, 'max': max_lat},
            'lon': {'min': min_lon, 'max': max_lon},
            'time': {'min': temporal['start_time'], 'max': temporal['end_time']},
        }

        return(coordinates)
    except:
        return None

def envi_temporal(input_file: str, cfg_dict: dict = None):
    '''Process an ENVI granule's temporal extents.

    Args:
        input_file (str): The path to an ENVI granule.
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

def envi_statistics(input_file: str):
    '''Process an ENVI granule's statistics.

    Args:
        input_file (str): The path to an ENVI granule.
    
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

        if ('STATISTICS_MAXIMUM' in output):
            max_val = float(output.split('STATISTICS_MAXIMUM=', 1)[1].split('\n', 1)[0])
        else:
            max_val = None

        if ('STATISTICS_MEAN' in output):
            mean_val = float(output.split('STATISTICS_MEAN=', 1)[1].split('\n', 1)[0])
        else:
            mean_val = 0

        if ('STATISTICS_MINIMUM' in output):
            min_val = float(output.split('STATISTICS_MINIMUM=', 1)[1].split('\n', 1)[0])
        else:
            min_val = None

        if ('STATISTICS_STDDEV' in output):
            stdev_val = float(output.split('STATISTICS_STDDEV=', 1)[1].split('\n', 1)[0])
        else:
            stdev_val = 0
        
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

def envi_variables(input_file: str):
    '''Process an ENVI granule's variable list.

    Args:
        input_file (str): The path to an ENVI granule.
    
    Returns:
        dictionary of items for the variables portion of the metadata
    '''
    try:
        # Use 'gdalinfo' terminal command and process values from returned output
        output = getoutput('gdalinfo %s' %(input_file))

        var_list = []
        lines = output.split('\n')
        for line in lines:
            line = line.strip()

            if ((line[:11] == 'SUBDATASET_') and 
                (line.split('=', 1)[0][-5:] == '_DESC')):
                var_list.append(line.rsplit(']', 1)[1].split(' (', 1)[0])

        variables = {
            'n_variables': len(var_list),
            'variables': var_list,
            'variables_units': '',
            'variables_desc': '',
        }

        return variables
    except:
        return None

def envi_properties(input_file: str, cfg_dict: dict = None):
    '''Process an ENVI granule's properties.

    Args:
        input_file (str): The path to an ENVI granule.
    
    Returns:
        dictionary of items for the properties portion of the metadata
    '''
    if not cfg_dict['no_checksum']:
        checksum = file_checksum(input_file)
    else:
        checksum = None

    properties = {
        'format': 'envi',
        'size': get_file_size(input_file),
        'checksum': checksum,
    }

    return properties

def is_envi_header(input_file: str):
    '''Determine if granule is actually an ENVI header file.

    Args:
        input_file (str): The path to a granule.
    
    Returns:
        boolean indicating if it is an ENVI header file.
    '''
    try:
        with open(input_file) as hdr:
            first_line = hdr.readline().strip().upper()

        if first_line == 'ENVI':
            return True
        else:
            return False
    except:
        return False

def is_envi_granule(input_file: str, suppress_print = False):
    '''Determine if granule is an ENVI granule based on if it has a
       corresponding header (.hdr) file and if that header file's 
       first line only contains the word 'ENVI'.

    Args:
        input_file (str): The path to a granule.
    
    Returns:
        boolean indicating if it is an ENVI granule.
    '''
    if isfile(input_file + '.hdr'):
        if is_extensionless(input_file) and not suppress_print:
            # Warn the user that 'input_file' has no file extension
            print(' WARNING: %s does not have a file extension.' %input_file)
        
        return is_envi_header(input_file + '.hdr')
    elif input_file == splitext(input_file)[0] + '.hdr':
        return False
    elif isfile(splitext(input_file)[0] + '.hdr'):
        return is_envi_header(splitext(input_file)[0] + '.hdr')
    else:
        return False
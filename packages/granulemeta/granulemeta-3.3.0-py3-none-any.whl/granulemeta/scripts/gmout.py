#!/usr/bin/env python3
'''
|
|------------------------------------------------------------------------------
|
|  GMOUT.PY
|
|  UPDATED:    2023-01-12
|  AUTHOR:     kent campbell
|  CONTACT:    campbellkb@ornl.gov
|
|  DESCRIPTION
|
|     This module provides functions for writing to a gmout file.
|
|------------------------------------------------------------------------------
|
'''
# | Python 3 standard library |
from os.path import basename, splitext

# | Local packages |
try:
    from utilities import *
    from process_daymet import process_Daymet_LL
except:
    from scripts.utilities import *
    from scripts.process_daymet import process_Daymet_LL

# |----------------------------------------------------------------------------
# | GMOUT wwarning functions
# |----------------------------------------------------------------------------
def check_missing(var):
    ''' Returns True when a "missing" value found

    Args:
        val (any): value to be compared to common missing values.

    Returns:
        result (bool): True if missing, False otherwise
    '''
    if (var is None or var in ['', '""', 0]):
        return True
    else:
        return False

def check_negative(val):
    ''' Returns True when a negative numeric values is found

    Args:
        val (any): value to be cast to float and checked with respect to zero.

    Returns:
        result (bool): True if negative, False otherwise
    '''
    try:
        if float(val) < 0:
            return True
        else:
            False
    except:
        return False

# |----------------------------------------------------------------------------
# | GMOUT writing functions
# |----------------------------------------------------------------------------
def write_gmout_header(outfile):
    header = ('ds_id,granule_id,gr_id,subdir,filename,title,start_time,' +
              'end_time,max_lat,min_lat,max_lon,min_lon,file_type,file_format,' + 
              'geometry_type,day_night,file_size_mb,checksum_md5,n_variables,' +
              'variables,variables_units,variables_desc,calendar,native_datatype,' +
              'offered_resampling,native_crs,native_crs_wkt,native_crs_proj4,' +
              'offered_crs,res_x,res_y,res_z,min_x,min_y,min_z,max_x,max_y,max_z,' +
              'map_units,z_units,n_cols,n_rows,n_bands,scaling,offset,time_series,' +
              'min_val,max_val,mean_val,stddev_val,nodata_val,break_method,' +
              'num_of_classes,color_scheme,b_reverse_color,b_use_parent_color_scheme,' +
              'b_enhance,lut,feature_notes,additional_information')

    # Write gmout header to file, overwriting an existing file if necessary.
    write_line(outfile, header, 'w')

def gmout_writer(outfile, granule, cfg: dict = {}):
    if ('ds_id' in cfg.keys()):
        ds_id = cfg['ds_id']
    else:
        ds_id = '0000'

    if ('granule_id_prefix' in cfg.keys()):
        granule_id_prefix = cfg['granule_id_prefix']
    else:
        granule_id_prefix = ds_id

    if ('granule_id' in cfg.keys()):
        granule_id = '%04i_%i' %(int(granule_id_prefix), int(cfg['granule_id']))
    else:
        granule_id = '%04i_%i' %(int(granule_id_prefix), granule['granule_id'])
    
    if ('gr_id' in cfg.keys()):
        gr_id = cfg['gr_id']
    else:
        gr_id = ''

    if ('subdir' in cfg.keys()):
        subdir = cfg['subdir']
    else:
        subdir = granule['metadata']['subdir']
    
    if ('filename' in cfg.keys()):
        filename = cfg['filename']
    else:
        filename = basename(granule['metadata']['filename'])
    
    if ('title' in cfg.keys()):
        title = cfg['title']
    else:
        title = splitext(granule['metadata']['filename'])[0]

    start_time = access_str(granule, ['metadata', 'coordinates', 'time', 'min'], 'start_time', cfg)
    end_time = access_str(granule, ['metadata', 'coordinates', 'time', 'max'], 'end_time', cfg)

    if ('' in [start_time, end_time] and cfg['force_blanks'] == False):
        # Bail out after informing the user if time extents were not provided on a granule.
        # NOTE: This can cause complications on some file types. This may need to be removed.
        print('Time extents not found in %s. Please define start & end datetimes in configuration file.' %filename)
        exit(1)

    max_lat = format_float(access_flt(granule, ['metadata', 'coordinates', 'lat', 'max'], 'max_lat', cfg), 5, False)
    min_lat = format_float(access_flt(granule, ['metadata', 'coordinates', 'lat', 'min'], 'min_lat', cfg), 5, False)
    
    max_lon = format_float(access_flt(granule, ['metadata', 'coordinates', 'lon', 'max'], 'max_lon', cfg), 5, False)
    min_lon = format_float(access_flt(granule, ['metadata', 'coordinates', 'lon', 'min'], 'min_lon', cfg), 5, False)
    
    if ('' in [max_lat, min_lat, max_lon, min_lon] and cfg['force_blanks'] == False):
        # Bail out after informing the user if a bounding box was not provided on a granule.
        print('No spatial information detected. Please define a bounding box in a configuration file.')
        exit(1)

    file_type = access_str(granule, ['properties', 'format'], 'file_type', cfg)
    file_format = access_str(granule, ['metadata', 'attributes', 'driver'], 'file_format', cfg)

    try:
        geometry_type = access_str(granule, ['metadata', 'attributes', 'spatial_reference', 'geom_type'], 'geometry_type', cfg)

        if geometry_type == '':
            geometry_type = 'BR'
    except:
        geometry_type = 'BR'
    
    if ('day_night' in cfg.keys()):
        day_night = cfg['day_night']
    else:
        day_night = 'B'

    file_size_mb = format_float(access_flt(granule, ['properties', 'size'], 'file_size_mb', cfg), 4)
    checksum_md5 = access_str(granule, ['properties', 'checksum'], 'checksum_md5', cfg)

    n_variables = format_num(access_int(granule, ['metadata', 'variables', 'n_variables'], 'n_variables', cfg))
    if n_variables == '':
        n_variables = '0'

    variables = ''
    for var in access_list(granule, ['metadata', 'variables', 'variables'], 'variables', cfg):
        if variables == '':
            variables = var
        else:
            variables += '; %s' %var

    variables = '"%s"' %variables

    variables_units = access_str(granule, ['metadata', 'variables', 'variables_units'], 'variables_units', cfg)
    variables_desc = access_str(granule, ['metadata', 'variables', 'variables_desc'], 'variables_desc', cfg)
    
    if ('calendar' in cfg.keys()):
        calendar = cfg['calendar']
    else:
        calendar = ''

    native_datatype = access_str(granule, ['metadata', 'statistics', 'data_type'], 'native_datatype', cfg)

    if ('offered_resampling' in cfg.keys()):
        offered_resampling = cfg['offered_resampling']
    else:
        offered_resampling = '"NEAREST,AVERAGE,BILINEAR"'
    
    if (granule['metadata']['coordinates'] is None):
        # Handle possibility that the granule isn't georeferenced
        native_crs = ''
        native_crs_wkt = ''
        native_crs_proj4 = ''
        offered_crs = ''

        map_units = access_str(granule, ['metadata', 'attributes', 'spatial_reference', 'parameters', 'map_units'], 'map_units', cfg)
        map_units = map_units.replace('metre', 'meter').lower()
    else:
        # Granule must have georeference data, handle it
        if ('native_crs' in cfg.keys()):
            native_crs = cfg['native_crs']
        else:
            native_crs = ''

        wkt = access_str(granule, ['metadata', 'attributes', 'spatial_reference', 'well_known_text'], 'native_crs_wkt', cfg).replace('"', "'")
        map_units = access_str(granule, ['metadata', 'attributes', 'spatial_reference', 'parameters', 'map_units'], 'map_units', cfg)
        map_units = map_units.replace('metre', 'meter').lower()
        
        if len(wkt) == 0:
            native_crs = '4326'
            wkt = "GEOGCS['WGS 84',DATUM['WGS_1984',SPHEROID['WGS 84',6378137,298.257223563,AUTHORITY['EPSG','7030']],AUTHORITY['EPSG','6326']],PRIMEM['Greenwich',0,AUTHORITY['EPSG','8901']],UNIT['degree',0.01745329251994328,AUTHORITY['EPSG','9122']],AUTHORITY['EPSG','4326']]"
            map_units = 'degrees'

        native_crs_wkt = '"' + wkt + '"'

        proj4 = access_str(granule, ['metadata', 'attributes', 'spatial_reference', 'proj4'], 'native_crs_proj4', cfg).replace('=', '= ')
        if len(proj4) == 0:
            native_crs_proj4 = '" "'
        else:
            native_crs_proj4 = ' ' + proj4
        
        if ('offered_crs' in cfg.keys()):
            offered_crs = cfg['offered_crs']
        else:
            offered_crs = '"4326,900913"'

    res_x = format_float(access_flt(granule, ['metadata', 'coordinates', 'x', 'res'], 'res_x', cfg), 6)
    res_y = format_float(access_flt(granule, ['metadata', 'coordinates', 'y', 'res'], 'res_y', cfg), 6)
    res_z = format_float(access_flt(granule, ['metadata', 'coordinates', 'z', 'res'], 'res_z', cfg), 6)

    min_x = format_float(access_flt(granule, ['metadata', 'coordinates', 'x', 'min'], 'min_x', cfg), 4)
    min_y = format_float(access_flt(granule, ['metadata', 'coordinates', 'y', 'min'], 'min_y', cfg), 4)
    min_z = format_float(access_flt(granule, ['metadata', 'coordinates', 'z', 'min'], 'min_z', cfg), 4)

    max_x = format_float(access_flt(granule, ['metadata', 'coordinates', 'x', 'max'], 'max_x', cfg), 4)
    max_y = format_float(access_flt(granule, ['metadata', 'coordinates', 'y', 'max'], 'max_y', cfg), 4)
    max_z = format_float(access_flt(granule, ['metadata', 'coordinates', 'z', 'max'], 'max_z', cfg), 4)
    
    # NOTE: map_units are set with the 'native_crs_wkt' value

    if ('z_units' in cfg.keys()):
        z_units = int(cfg['z_units'])
    else:
        z_units = 0

    n_cols = format_num(access_int(granule, ['metadata', 'attributes', 'n_cols'], 'n_cols', cfg))
    n_rows = format_num(access_int(granule, ['metadata', 'attributes', 'n_rows'], 'n_rows', cfg))
    n_bands = format_num(access_int(granule, ['metadata', 'attributes', 'n_bands'], 'n_bands', cfg))
    scaling = format_num(access_int(granule, ['metadata', 'attributes', 'scale', '1'], 'scale', cfg))
    offset = format_num(access_int(granule, ['metadata', 'attributes', 'offset', '1'], 'offset', cfg))

    if ('time_series' in cfg.keys()):
        time_series = cfg['time_series']
    else:
        time_series = '""'

    min_val = str(access_flt(granule, ['metadata', 'statistics', 'min'], 'min_val', cfg))
    max_val = str(access_flt(granule, ['metadata', 'statistics', 'max'], 'max_val', cfg))
    mean_val = str(access_flt(granule, ['metadata', 'statistics', 'mean'], 'mean_val', cfg))
    stddev_val = str(access_flt(granule, ['metadata', 'statistics', 'std'], 'stddev_val', cfg))
    nodata_val = str(access_flt(granule, ['metadata', 'statistics', 'missing_value'], 'nodata_val', cfg))

    if ('break_method' in cfg.keys()):
        break_method = int(cfg['break_method'])
    else:
        break_method = 1
    
    if ('num_of_classes' in cfg.keys()):
        num_of_classes = int(cfg['num_of_classes'])
    else:
        num_of_classes = 1
    
    if ('color_scheme' in cfg.keys()):
        color_scheme = cfg['color_scheme']
    else:
        color_scheme = 'rainbow'
    
    if ('b_reverse_color' in cfg.keys()):
        b_reverse_color = int(cfg['b_reverse_color'])
    else:
        b_reverse_color = 0
    
    if ('b_use_parent_color_scheme' in cfg.keys()):
        b_use_parent_color_scheme = int(cfg['b_use_parent_color_scheme'])
    else:
        b_use_parent_color_scheme = 0
    
    if ('b_enhance' in cfg.keys()):
        b_enhance = int(cfg['b_enhance'])
    else:
        b_enhance = 0
    
    if ('lut' in cfg.keys()):
        lut = cfg['lut']
    else:
        lut = ''
    
    if ('feature_notes' in cfg.keys()):
        feature_notes = cfg['feature_notes']
    else:
        feature_notes = '""'
    
    if ('additional_information' in cfg.keys()):
        additional_information = cfg['additional_information']
    else:
        additional_information = '""'
    
    # Check for non-COG GeoTIFF, warn if found
    if (file_format == 'GeoTIFF'):
        print(' WARNING: %s is not in cloud-optimized format' %filename)
    elif ((splitext(filename)[1] == '.tif') and 
          (file_format not in ['GeoTIFF', 'COG'])):
        print(' WARNING: %s is not in cloud-optimized format' %filename)

    # Check for missing values, warn if found
    if check_missing(start_time):
        print(' WARNING: Missing field [ start_time ]')
    if check_missing(end_time):
        print(' WARNING: Missing field [ end_time ]')
    if check_missing(variables_units):
        print(' WARNING: Missing field [ variables_units ]')
    if check_missing(variables_desc):
        print(' WARNING: Missing field [ variables_desc ]')
    if check_missing(res_x):
        print(' WARNING: Missing field [ res_x ]')
    if check_missing(res_y):
        print(' WARNING: Missing field [ res_y ]')
    if check_missing(res_z):
        print(' WARNING: Missing field [ res_z ]')
    if check_missing(min_x):
        print(' WARNING: Missing field [ min_x ]')
    if check_missing(min_y):
        print(' WARNING: Missing field [ min_y ]')
    if check_missing(min_z):
        print(' WARNING: Missing field [ min_z ]')
    if check_missing(max_x):
        print(' WARNING: Missing field [ max_x ]')
    if check_missing(max_y):
        print(' WARNING: Missing field [ max_y ]')   
    if check_missing(max_z):
        print(' WARNING: Missing field [ max_z ]')
    
    # Check for negative values, warn if found
    if check_negative(file_size_mb):
        print(' WARNING: Questionable negative value for field [ file_size_mb ]')
    if check_negative(n_variables):
        print(' WARNING: Questionable negative value for field [ n_variables ]')
    if check_negative(res_x):
        print(' WARNING: Questionable negative value for field [ res_x ]')
    if check_negative(res_y):
        print(' WARNING: Questionable negative value for field [ res_y ]')
    if check_negative(res_z):
        print(' WARNING: Questionable negative value for field [ res_z ]')
    if check_negative(n_cols):
        print(' WARNING: Questionable negative value for field [ n_cols ]')
    if check_negative(n_rows):
        print(' WARNING: Questionable negative value for field [ n_rows ]')
    if check_negative(n_bands):
        print(' WARNING: Questionable negative value for field [ n_bands ]')
    if check_negative(stddev_val):
        print(' WARNING: Questionable negative value for field [ stddev_val ]')

    # Construct line that will be written to the output file
    output_vars = [ds_id, granule_id, gr_id, subdir, filename, title,
                   start_time, end_time, max_lat, min_lat, max_lon, min_lon,
                   file_type, file_format, geometry_type, day_night, file_size_mb,
                   checksum_md5, n_variables, variables, variables_units, 
                   variables_desc, calendar, native_datatype, offered_resampling, 
                   native_crs, native_crs_wkt, native_crs_proj4, offered_crs,
                   res_x, res_y, res_z, min_x, min_y, min_z, max_x, max_y, max_z,
                   map_units, '%i' %z_units, n_cols, n_rows, n_bands, scaling,
                   offset, time_series, min_val, max_val, mean_val, stddev_val,
                   nodata_val, '%i' %break_method, '%i' %num_of_classes,
                   color_scheme, '%i' %b_reverse_color, '%i' %b_use_parent_color_scheme,
                   '%i' %b_enhance, lut, feature_notes, additional_information]

    # Post-processing fixes for Daymet Lower Latency Granules
    if (cfg['daymet'] is True):
        process_Daymet_LL(output_vars)

    # Join output variables into single (comma-separated) line of text               
    output_line = ','.join(output_vars)

    write_line(outfile, output_line)
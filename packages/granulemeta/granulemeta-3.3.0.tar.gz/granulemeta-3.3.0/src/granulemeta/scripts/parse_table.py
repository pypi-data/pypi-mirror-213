#!/usr/bin/env python3
'''
|
|------------------------------------------------------------------------------
|
|  PARSE_TABLE.PY
|
|  UPDATED:    2023-05-22
|  AUTHOR:     kent campbell
|  CONTACT:    campbellkb@ornl.gov
|
|  DESCRIPTION
|
|     This module provides functions for processing TABLE granules
|
|------------------------------------------------------------------------------
|
'''
# | Python 3 standard library |
from io import StringIO
from numpy import nan as np_nan
from os.path import sep, splitext, split as fsplit
from re import compile as re_compile

# | Third-party packages |
from osgeo import gdal

import dateutil.parser as dtparser
import pandas as pd

# | Local packages |
try:
    from utilities import datetime_override, detect_nan, file_checksum, get_file_size, string_select
except:
    from scripts.utilities import datetime_override, detect_nan, file_checksum, get_file_size, string_select

# |----------------------------------------------------------------------------
# | TABLE granule functions
# |----------------------------------------------------------------------------
def table_metadata(input_file: str, cfg_dict: dict = None, GMFT_dict: dict = None):
    ''' Get metadata from a TABLE granule
    
    Args:
        input_file (str): The path to a TABLE granule.
        cfg_dict (dict): A dictionary of key/value pairs that represent configuration options.
        GMFT_dict (dict): A dictionary of GranuleMeta Format Types.

    Returns:
        record (dict): Dictionary of metadata for the granule.
    '''
    try:
        metadata = {'filename': fsplit(input_file)[1],
                    'subdir': fsplit(input_file)[0].lstrip(sep)}

        fext = splitext(input_file)[1]

        # Identify the driver type needed for the granule
        try:
            file_format = gdal.IdentifyDriver(input_file).ShortName
        except:
            file_format = None

        if is_icartt_granule(fext):
            header_row = pd.read_csv(input_file, header=None, nrows=1).values[0][0]
            
            if file_format is None:
                file_format = 'text/icartt'
        else:
            # Determine length of granule
            with open(input_file) as f:
                nlines = len(f.readlines())

            # Grab tail end of granule, so that number of columns can be determined
            idx = int(nlines * .75)
            tail_ncols = len(pd.read_csv(input_file, skiprows = idx, nrows = 1).columns)

            # Choose a reasonable length of the granule's lines to iterate over (backwards)
            # until a line containing the wrong number of columns is found. This will tell
            # the script where the header line is and which lines to skip.
            idx = int(nlines * .25)
            if idx < 10:
                idx = nlines
            elif idx > 1000:
                idx = 1000 

            with open(input_file) as f:
                lines = []
                for _ in range(idx):
                    line = f.readline()
                    if line == '':
                        break
                    else:
                        lines.append(line.strip())

            header_row = 0
            for i, line in enumerate(lines[::-1]):
                ncols, nnans, _ = table_line_summary(line)
                if ncols != tail_ncols:
                    # Return previous index as header line if colcount for this line == file's tail column count.
                    header_row = idx - i
                elif int(tail_ncols/2) < nnans:
                    # Return previous index as header line if nan count is more than half the column count
                    header_row = idx - i
        
        try:
            # Read the data into a pandas DataFrame           
            df = pd.read_csv(input_file, skiprows = header_row, low_memory = False)
        except pd.errors.ParserError:
            # Parsing was unsuccessful
            return metadata
        
        # Add to metadata dictionary in stages
        nvars = len(list(df))
        variables = list(df)
        
        metadata['attributes'] = {
            'n_lines': len(df),
            'h_index': header_row,
            'h_size': header_row,
            'n_rows': df.shape[0],
            'n_cols': df.shape[1],
            'n_vars': nvars,
            'driver': file_format,
        }

        # Free up some memory
        df = None

        metadata['coordinates'] = table_coordinates(input_file, header_row, cfg_dict)

        if not cfg_dict['no_stats']:
            metadata['statistics'] = table_statistics(input_file, header_row)
        else:
            metadata['statistics'] = None

        metadata['variables'] = {
            'n_variables': nvars,
            'variables': variables,
            'variables_units': '',
            'variables_desc': '',
        }

        properties = table_properties(input_file, cfg_dict, GMFT_dict)

        record = {'metadata': metadata,
                  'properties': properties
        }

        return record
    except:
        return None

def table_coordinates(input_file: str, header_row: int, cfg_dict: dict = None):
    '''Process a TABLE granule's coordinates.

    Args:
        df (pd.DataFrame): The DataFrame containing the data from the TABLE granule.
        cfg_dict (dict): A dictionary of key/value pairs that represent configuration options.
    
    Returns:
        dictionary of items for the coordinates portion of the metadata
    '''
    try:
        try:
            # Read the data into a pandas DataFrame    
            df = pd.read_csv(input_file, skiprows = header_row, low_memory = False)
        except pd.errors.ParserError:
            # Parsing was unsuccessful
            return None

        common_lats = ["y", "lt", "lat", "latitude", ]
        if 'lat_name' in cfg_dict.keys():
            common_lats = [cfg_dict['lat_name']] + common_lats

        common_lons = ["x", "ln", "lng", "lon", "long", "longitude", ]
        if 'lon_name' in cfg_dict.keys():
            common_lons = [cfg_dict['lon_name']] + common_lons

        common_dates = ['date', 'datetime', 'timestamp', ]
        if 'date_name' in cfg_dict.keys():
            common_dates = [cfg_dict['date_name']] + common_dates

        common_times = ['time', 'datetime', 'timestamp', ]
        if 'time_name' in cfg_dict.keys():
            common_times = [cfg_dict['time_name']] + common_times

        variable_config = {
            'lat': {
                'regex': re_compile('.*lat.*'),
                'common': common_lats,
            },
            'lon': {
                'regex': re_compile('.*lon.*'),
                'common': common_lons,
            },
            'date': {
                'regex': re_compile('.*date.*'),
                'common': common_dates,
            },
            'time': {
                'regex': re_compile('.*time.*'),
                'common': common_times,
            },
        }

        variables_output = {}
        variable_ts_ = None
        for variable_name, variable_selectors in variable_config.items():
            try:
                # Try to match to the list of columns.
                match = string_select(
                    strings = list(df),
                    regex = variable_selectors['regex'],
                    common = variable_selectors['common'],
                )
            except Exception as e:
                # Ignore exceptions (for now).
                pass # raise e
            else:
                # If the match is not None, grab the variable from the data frame.
                if match is not None:
                    variable = df[match]

                    # If match contains the substrings 'date' or 'time', 
                    if 'date' in match.lower() or 'time' in match.lower():
                        # Try to intelligently convert to dates or times.
                        try:
                            variable_ts_ = variable.apply(lambda x: dtparser.parse(x))

                            if 'date' in match.lower():
                                variable = pd.Series([t.date() for t in variable_ts_])
                            if 'time' in match.lower():
                                variable = pd.Series([t.time() for t in variable_ts_])
                        except:
                            pass
                    elif variable_name in ['date', 'time']:
                        try:
                            variable_ts_ = variable.apply(lambda x: dtparser.parse(x))

                            if variable_name == 'date':
                                variable = pd.Series([t.date() for t in variable_ts_])
                            if variable_name == 'time':
                                variable = pd.Series([t.time() for t in variable_ts_])
                        except:
                            pass

                    # Summarize variable statistics; set to the output dictionary.
                    variables_output[variable_name] = table_column_summary(variable)

        # Free up some memory
        df = None

        if variable_ts_ is not None:
            start_time = str(variable_ts_.min())
            end_time = str(variable_ts_.max())
        else:
            start_time = None
            end_time = None

        temporal = table_temporal(start_time, end_time, cfg_dict)

        try:
            min_lat = variables_output['lat']['min']
        except:
            min_lat = None
        
        try:
            max_lat = variables_output['lat']['max']
        except:
            max_lat = None
        
        try:
            min_lon = variables_output['lon']['min']
        except:
            min_lon = None
        
        try:
            max_lon = variables_output['lon']['max']
        except:
            max_lon = None

        coordinates = {
            'lat': {'min': min_lat, 'max': max_lat},
            'lon': {'min': min_lon, 'max': max_lon},
            'time': {'min': temporal['start_time'], 'max': temporal['end_time']},
        }

        return coordinates
    except Exception as e:
        return None

def table_temporal(start_time, end_time, cfg_dict: dict = None):
    '''Process a TABLE granule's temporal extents.

    Args:
        cfg_dict (dict): A dictionary of key/value pairs that represent configuration options.
    
    Returns:
        dictionary of items for the temporal extents of the metadata
    '''
    start_time, end_time = datetime_override(start_time, end_time, cfg_dict)

    temporal = {
        'start_time': start_time,
        'end_time': end_time,
    }

    return temporal

def table_statistics(input_file: str, header_row: int):
    '''Process a TABLE granule's statistics.

    Args:
        df (pd.DataFrame): The DataFrame containing the data from the TABLE granule.
    
    Returns:
        dictionary of items for the statistics portion of the metadata
    '''
    try:
        try:
            # Read the data into a pandas DataFrame    
            df = pd.read_csv(input_file, skiprows = header_row, low_memory = False)
        except pd.errors.ParserError:
            # Parsing was unsuccessful
            return None

        # NOTE: The stats calculated below won't propagate to a gmout file. 
        #       Too many possible variables to have statistics for...
        stats = df.describe().to_dict()

        # Free up some memory
        df = None

        return stats
    except:
        return None

def table_properties(input_file: str, cfg_dict: dict = None, GMFT_dict: dict = None):
    '''Process a TABLE granule's properties.

    Args:
        input_file (str): The path to an TABLE granule.
        cfg_dict (dict): A dictionary of key/value pairs that represent configuration options.
        GMFT_dict (dict): A dictionary of GranuleMeta Format Types.
    
    Returns:
        dictionary of items for the properties portion of the metadata
    '''
    try:
        file_type = GMFT_dict[gdal.IdentifyDriver(input_file).ShortName]
    except:
        file_type = 'table'

    if not cfg_dict['no_checksum']:
        checksum = file_checksum(input_file)
    else:
        checksum = None

    properties = {
        'format': file_type,
        'size': get_file_size(input_file),
        'checksum': checksum,
    }

    return properties

def is_table_granule(input_file: str):
    '''Determine if granule is a TABLE granule.

    Args:
        input_file (str): The path to a granule.
    
    Returns:
        boolean indicating if it is a TABLE granule.
    '''
    fext = splitext(input_file)[1]
    return(is_text_granule(fext) or is_icartt_granule(fext))

def is_icartt_granule(fext: str):
    '''Determine if granule is an ICARTT granule.

    Args:
        fext (str): The file extension for a granule.
    
    Returns:
        boolean indicating if it is an ICARTT granule.
    '''
    return fext in ['.ict', '.icartt']

def is_text_granule(fext: str):
    '''Determine if granule is a TEXT granule.

    Args:
        fext (str): The file extension for a granule.
    
    Returns:
        boolean indicating if it is a TEXT granule.
    '''
    return fext in ['.csv', '.tsv', '.txt', '.dat']
        
# |----------------------------------------------------------------------------
# | table specific utility function(s)
# |----------------------------------------------------------------------------
def table_find_header(input_lines: list):
    '''Custom logic predicts the header index from a list of lines (strings).
    
    Args:
        input_lines (list): ...
    
    Returns:
        index (int): position of the header line within a list of lines.
    '''
    # Drop all trailing empty lines from the list in a reversed loop.
    for i in range(len(input_lines)-1, -1, -1):
        # If indexed line is not empty, drop trailing lines and break the loop.
        if input_lines[i].strip() != '':
            input_lines = input_lines[:i]
            break

    # Get the number of remaining lines.
    line_count = len(input_lines)

    # Get the 1/4 tail of the file and make pseudo file.
    tail_length = int(line_count / 4)

    # Adust tail size where necessary
    if tail_length < 1000:
        tail_length = line_count
    elif tail_length > 1000:
        tail_length = 1000
    
    tail_io = StringIO('\n'.join(input_lines[-1 * tail_length:]))

    try:
        # Try to read the tail with pandas.
        tail_df = pd.read_csv(tail_io, engine = 'python')
    except pd.errors.EmptyDataError as _:
        # Return None in the event of failure.
        return None

    # Get the tail column count and tail column dtypes.
    tail_ncols = len(list(tail_df))

    for i, ln in enumerate(input_lines[::-1]):
        ncols, nnans, _ = table_line_summary(ln)

        if ncols != tail_ncols:
            # Return previous index as header line if colcount for this line == file's tail column count.
            return len(input_lines) - i
        
        elif int(tail_ncols/2) < nnans:
            # Return previous index as header line if nan count is more than half the column count
            return len(input_lines) - i

    return 0

def table_line_summary(input_line: str):
    '''Takes an input line (a text string) and returns details about it.
    
    Args:
        input_line (str): a string that represents a line from a text file.
        
    Returns:
        line_ncols (int): number of columns in the line
        line_nnans (int): number of nans in the line 
        line_dtypes (list): list of datatypes contained in the line
    '''
    # Get the line as stringio pseudo file object.
    line_sio = StringIO(input_line)

    # Read the individual line into a pandas.DataFrame with one row.
    try:
        line_row = pd.read_csv(line_sio, engine = 'python', header = None)
    except pd.errors.ParserError:
        return 0, 0, None

    # Get the number of columns sniffed by pandas for this line.
    line_ncols = len(list(line_row))

    # Find out how many of the sniffed columns contain nans/nulls.
    line_nnans = line_row.isnull().sum(axis = 1).values[0]

    # Get the sniffed type of each column.
    line_dtypes = [line_row[col].dtype for col in list(line_row)]
    
    return line_ncols, line_nnans, line_dtypes

def table_column_summary(variable):
    '''Takes a column of data and returns statistics about it.
    
    Args:
        variable (pd.DataFrame): a DataFrame that represents a column from a text file.
        
    Returns:
        stats (dict): statistics for a given column of data.
    '''
    common_nans = [
        -9999., -999. -99., -0.9, -0.99, -0.999, -0.9999,
        -1, 0,
        'NA', 'NaN',
    ]

    # Detect the missing value. No need to drop it.
    _, missing_value = detect_nan(values = variable.unique().tolist(), 
                                  common_nans = common_nans,)
    
    # Replace the missing value with np_nan in the series if one was detected.
    if missing_value is not None:
        variable = variable.replace(missing_value, np_nan)
    
    # Calculate stats of the (possibly sanitized) variable Series.
    stats = variable.describe().to_dict()
    
    # Replace 'first', 'last' with 'min', 'max' if exist (dates and times).
    if 'first' in list(stats):
        stats['min'] = stats.pop('first')
    if 'last' in list(stats):
        stats['max'] = stats.pop('last')

    # Add the missing value to the stats.
    stats['missing_value'] = missing_value
    
    # Return the stats.
    return stats
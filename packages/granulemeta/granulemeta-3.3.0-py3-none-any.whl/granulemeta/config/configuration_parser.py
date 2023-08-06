#!/usr/bin/env python3
'''
|
|------------------------------------------------------------------------------
|
|  CONFIGURATION_PARSER
|
|  AUTHOR:  kent campbell
|  CONTACT: campbellkb@ornl.gov
|
|  DESCRIPTION
|
|     Script reads configuration files and returns a dictionary of 
|     configuration values.
|
|------------------------------------------------------------------------------
|
'''
# | Python 3 standard library |
from re import match
from time import strftime, strptime
from os.path import exists, split as splitfile

# | Start of code |
def read_ascii(filename: str):
    rfile = open(filename, 'r')
    lines = rfile.readlines()
    rfile.close()
    return lines

def write_ascii(filename, lines):
    wfile = open(filename, 'w+')

    for line in lines:
        wfile.write(line.rstrip() + '\n')

    wfile.close()

def read_config(filename: str, kv_dict: dict = {}):
    '''Read the configuration file and return a dictionary of key/value pairs.

    Args:
        filename: A string containing the path & filename of the config file.
        kv_dict (optional): A previously populated configuration dictionary of
                            key/value pairs. Where the key is the same as an 
                            existing item, it will be overwritten.

    Returns:
        kv_dict: A dictionary of key/value pairs pulled from the config file.
    '''
    if exists(filename):
        lines = read_ascii(filename)
    else:
        print(filename)
        raise Exception('Invalid argument: Configuration file does not exist')

    for i, line in enumerate(lines):
        if ((line[0] != '#') and
            ('=' in line) and
            (len(line.split('=', 1)) == 2)):
            key, value = line.split('=', 1)

            key = key.strip()
            value = value.strip()

            if ((key.strip().replace(' ', '') == '') or
                (value.strip().replace(' ', '') == '')):
                error_msg = ('Invalid key/value pair on line %i. ' +
                             'Must be KEY = VALUE.') %(i + 1)
                raise Exception(error_msg)
            else:
                if (value.strip().replace(' ', '') == 'None'):
                    value = None
                kv_dict[key] = value
        elif ((line[0] != '#') and
              ('=' not in line) and
              (len(line.strip()) > 0)):
            error_msg = ('Invalid key/value pair on line %i. ' +
                         'Must be KEY = VALUE.') %(i + 1)
            raise Exception(error_msg)

    return kv_dict

def parse_filename(datafilename: str, kv_dict: dict):
    '''Parse metadata from filename and add all metadata items to a copy of
       the configuration dictionary passed in.

    Args:
        datafilename: A datafilename that contains metadata within the 
                      filename that needs to be extracted.
        kv_dict: A dictionary of key/value pairs pulled from a config file.
                 Most likely the return value from read_config().

    Returns:
        kv_dict: The same kv_dict passed into parse_filename(), but with any
                 metadata extracted from the filename added to it.
    '''

    # Ensure the desired key is present in the config dict
    if ('filename_regex' in kv_dict.keys()):
        pattern = kv_dict['filename_regex']

        if (pattern is not None):
            match_dict = match(pattern, splitfile(datafilename)[1])

            if (match_dict is not None):
                group_dict = match_dict.groupdict()

                for key, value in group_dict.items():
                    if 'date' in key:
                        # Parse and format a date value from the filename
                        dt = strptime(value, kv_dict['file_date_in_format'])
                        dt = strftime(kv_dict['file_date_out_format'], dt)
                        kv_dict[key] = dt
                    elif 'time' in key and key != 'time_series':
                        # Parse and format a time value from the filename
                        tm = strptime(value, kv_dict['file_time_in_format'])
                        tm = strftime(kv_dict['file_time_out_format'], tm)
                        kv_dict[key] = tm
                    else:
                        # Parse a key/value pair from the filename without formatting it.
                        kv_dict[key] = value

    return kv_dict

if __name__ == '__main__':
    cfg_file = './default.cfg'
    data_file = '190821_113533_190921_125931_LS_ADAPD.tdms'

    # EXAMPLE 1: Parsing out dates and times separately
    #filename_regex = (?P<start_date>\d+)_(?P<start_time>\d+)_(?P<end_date>\d+)_(?P<end_time>\d+)_(?P<project_name>\S+)\.(?P<file_ext>\S+)
    #file_date_in_format = %y%m%d
    #file_date_out_format = %Y/%m/%d
    #file_time_in_format = %H%M%S
    #file_time_out_format = %H:%M:%S

    # EXAMPLE 2: Parsing out dates and times together
    #filename_regex = (?P<start_date>\d+_\d+)_(?P<end_date>\d+_\d+)_(?P<project_name>\S+)\.(?P<file_ext>\S+)
    #file_date_in_format = %y%m%d_%H%M%S
    #file_date_out_format = %Y/%m/%d %H:%M:%S

    cfg_dict = read_config(cfg_file)
    cfg_dict = parse_filename(data_file, cfg_dict)

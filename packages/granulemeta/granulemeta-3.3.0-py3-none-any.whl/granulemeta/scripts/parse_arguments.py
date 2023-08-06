#!/usr/bin/env python3
'''
|
|------------------------------------------------------------------------------
|
|  PARSE_ARGUMENTS.PY
|
|  UPDATED:    2023-05-22
|  AUTHOR:     kent campbell
|  CONTACT:    campbellkb@ornl.gov
|
|  DESCRIPTION
|
|     This module provides functions for processing command line arguments
|
|------------------------------------------------------------------------------
|
'''
# | Python 3 standard library |
import argparse

from os.path import isdir, isfile
from sys import stdout

# | Global Variable(s) |
__version__ = '3.3.0'

# |----------------------------------------------------------------------------
# | command line argument handling functions
# |----------------------------------------------------------------------------
def argument_handler():
    '''Primary argument handler.'''

    # Parser object.
    p = argparse.ArgumentParser(description = '----- Granulemeta v' + __version__ + ' -----')

    # Determine where to send output. Defaults to stdout.
    p.add_argument('-o', '--outfile', default = stdout, type = str,
                   help = 'the path to an output file (with ext)')
    
    # Specify a configuration file at the command line
    p.add_argument('-c', '--config', default = None, type = _file_and_dir_validator,
                   help = 'a configuration file')

    # Exclude all other types but: 'raster', 'vector', 'mdim', 'table', ...
    p.add_argument('-t', '--type', type = _type_validator,
                   help = "input data type: [raster, vector, mdim, table, audio, envi, archive]")

    # Only process a certain number of granules before stopping execution
    p.add_argument('-n', '--nfiles', default = -1, type = int,
                   help = 'number of granules to process before stopping execution (defaults to -1 for all files).')

    # Determine where to send output. Defaults to stdout.
    p.add_argument('--outtype', default = 'gmout', type = str,
                   help = 'type of output file to produce')

    # If the output file already exists, overwrite its contents instead of appending new content only.
    p.add_argument('--overwrite', default = False, action = 'store_true',
                   help = 'a flag for enabling the overwriting of an existing output file')

    # Opt to format output for Daymet Lower Latency granules.
    p.add_argument('--daymet', default = False, action = 'store_true',
                   help = 'a flag indicating format for daymet')

    # Opt to keep endtime as is instead of adjusting ones that are at midnight.
    p.add_argument('--no-adjust-midnight-endtime', default = False, action = 'store_true',
                   help = 'a flag for disabling the auto-adjustment of the endtime')

    # Opt to remove aux.xml files from the input directory.
    p.add_argument('--keep_aux_xml', default = False, action = 'store_true',
                   help = 'a flag to disable the automatic deletion of aux.xml files')

    # Opt to leave bounding box and time extents blank when not found.
    p.add_argument('--force_blanks', default = False, action = 'store_true',
                   help = 'a flag to leave bounding box and time extents blank when not found instead of exiting with an error message')

    p.add_argument('--no_stats', default = False, action = 'store_true',
                   help = 'a flag to prevent calculating statistics on granules during execution')

    p.add_argument('--no_checksum', default = False, action = 'store_true',
                   help = 'a flag to prevent calculating the md5 checksum on granules during execution')

    p.add_argument('--add_ext', default = False, action = 'store_true',
                   help = 'a flag to add \'.bin\' extensions to extensionless ENVI files')
    
    p.add_argument('--lat_name', default = None, type = str,
                   help = 'a string providing the name of the column (in the granule) from which the script extracts the latitude values.')
    
    p.add_argument('--lon_name', default = None, type = str,
                   help = 'a string providing the name of the column (in the granule) from which the script extracts the longitude values.')
    
    p.add_argument('--date_name', default = None, type = str,
                   help = 'a string providing the name of the column (in the granule) from which the script extracts the date values.')
    
    p.add_argument('--time_name', default = None, type = str,
                   help = 'a string providing the name of the column (in the granule) from which the script extracts the time values.')

    p.add_argument('--version', default = False, action = 'store_true',
                   help = 'a flag to allow for the version number of granulemeta to be printed')

    # Positional argument 1: Input directory or file.
    p.add_argument('path', type = _file_and_dir_validator, nargs = '+',
                   help = 'an input directory (OR file OR sequence of files OR glob pattern(s)) to traverse for metadata')

    # Return parsed arguments.
    return p.parse_args()

def _type_validator(input_type: str):
    '''An input 'type' validator.'''
    
    # Valid inputs:
    v = ['raster', 'vector', 'mdim', 'table', 'audio', 'envi', 'archive']
    
    # Bad input message:
    e = "Input data type ('-t', '--type') must be from: {}.".format(v)
    
    # If the input data type is not valid, raise ValueError. Else return it.
    if input_type not in v:
        raise ValueError(e)
    else:
        return input_type

def _file_and_dir_validator(input_path: str):
    '''A file or directory path validator.'''
    if isinstance(input_path, str):
        if not any([isfile(input_path), isdir(input_path)]):
            print('No file(s) found corresponding to supplied PATH argument')
            exit(1)
        else:
            return input_path
    elif isinstance(input_path, list):
        for x in input_path:
            if not any([isfile(x), isdir(x)]):
                print('No file(s) found corresponding to supplied PATH argument')
                exit(1)
        return(input_path)
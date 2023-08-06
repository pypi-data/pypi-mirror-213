#!/usr/bin/env python3
'''
|
|------------------------------------------------------------------------------
|
|  PARSE_ARCHIVE.PY
|
|  UPDATED:    2022-10-21
|  AUTHOR:     kent campbell
|  CONTACT:    campbellkb@ornl.gov
|
|  DESCRIPTION
|
|     This module provides functions for processing ARCHIVE granules
|
|------------------------------------------------------------------------------
|
'''
# | Python 3 standard library |
from mimetypes import guess_type
from os.path import sep, split as fsplit

# | Local packages |
try:
    from utilities import datetime_override, file_checksum, get_file_size
except:
    from scripts.utilities import datetime_override, file_checksum, get_file_size

# |----------------------------------------------------------------------------
# | ARCHIVE file functions
# |----------------------------------------------------------------------------
def archive_metadata(input_file: str, metadata:dict, cfg_dict: dict = None):
    ''' Get metadata from an ARCHIVE granule
    
    Args:
        input_file (str): The path to an ARCHIVE granule.
        cfg_dict (dict): A dictionary of key/value pairs that represent configuration options.

    Returns:
        record (dict): Dictionary of metadata for the granule.
    '''

    try:
        metadata = {'filename': fsplit(input_file)[1],
                    'subdir': fsplit(input_file)[0].lstrip(sep)}

        # Add to metadata dictionary in stages
        metadata['coordinates'] = None

        properties = archive_properties(input_file)

        record = {'metadata': metadata,
                  'properties': properties
        }

        return record
    except:
        return None

def archive_temporal(cfg_dict: dict = None):
    '''Process an ARCHIVE granule's temporal extents.

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

def archive_properties(input_file: str):
    '''Process an ARCHIVE granule's properties.

    Args:
        input_file (str): The path to an ARCHIVE granule.
    
    Returns:
        dictionary of items for the properties portion of the metadata
    '''
    if is_zip_file(input_file):
        file_type = 'zip'
    elif is_tar_file:
        file_type = 'targz'
    else:
        file_type = None

    properties = {
        'format': file_type,
        'size': get_file_size(input_file),
        'checksum': file_checksum(input_file),
    }

    return properties

def is_archive_granule(input_file: str):
    '''Determine if granule is an ARCHIVE granule.

    Args:
        input_file (str): The path to a granule.
    
    Returns:
        boolean indicating if it is an ARCHIVE granule.
    '''
    return (is_zip_file(input_file) or 
            is_tar_file(input_file))

def is_zip_file(input_file: str):
    '''Determine if granule is a zip file

    Args:
        input_file (str): The path to a granule.
    
    Returns:
        boolean indicating if it is a zip file.
    '''
    mimetype, _ = guess_type(input_file)
    return mimetype == 'application/zip'

def is_tar_file(input_file: str):
    '''Determine if granule is a tar file

    Args:
        input_file (str): The path to a granule.
    
    Returns:
        boolean indicating if it is a tar file.
    '''
    mimetype, _ = guess_type(input_file)
    return mimetype == 'application/x-tar'
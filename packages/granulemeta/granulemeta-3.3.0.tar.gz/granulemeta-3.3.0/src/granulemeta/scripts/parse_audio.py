#!/usr/bin/env python3
'''
|
|------------------------------------------------------------------------------
|
|  PARSE_AUDIO.PY
|
|  UPDATED:    2022-12-09
|  AUTHOR:     kent campbell
|  CONTACT:    campbellkb@ornl.gov
|
|  DESCRIPTION
|
|     This module provides functions for processing audio (wav, mp3) granules
|
|------------------------------------------------------------------------------
|
'''
# | Python 3 standard library |
from calendar import timegm
from os.path import sep, splitext, split as fsplit
from time import gmtime, strftime, strptime

# | Third party packages |
from tinytag import TinyTag

# | Local packages |
try:
    from utilities import file_checksum, get_file_size
except:
    from scripts.utilities import file_checksum, get_file_size

# |----------------------------------------------------------------------------
# | AUDIO granule functions
# |----------------------------------------------------------------------------
def audio_metadata(input_file: str, cfg_dict: dict = None):
    ''' Get metadata from an AUDIO granule
    
    Args:
        input_file (str): The path to an AUDIO granule.
        cfg_dict (dict): A dictionary of key/value pairs that represent configuration options.

    Returns:
        record (dict): Dictionary of metadata for the granule.
    '''
    try:
        metadata = {'filename': fsplit(input_file)[1],
                    'subdir': fsplit(input_file)[0].lstrip(sep)}

        # Add to metadata dictionary in stages
        metadata['attributes'] = audio_attributes(input_file)
        metadata['coordinates'] = audio_coordinates(input_file, cfg_dict)

        if not cfg_dict['no_stats']:
            metadata['statistics'] = audio_statistics(input_file)
        else:
            metadata['statistics'] = None

        metadata['variables'] = audio_variables(input_file)

        properties = audio_properties(input_file, cfg_dict)

        record = {'metadata': metadata,
                  'properties': properties
        }

        return record
    except:
        return None

def audio_attributes(input_file: str):
    '''Process an AUDIO granule's attributes.

    Args:
        input_file (str): The path to an AUDIO granule.
    
    Returns:
        dictionary of items for the attributes portion of the metadata
    '''
    try:
        dataset = TinyTag.get(input_file)

        attributes = {
            # Get some basic metadata about the audio dataset.
            'bitrate': dataset.bitrate,
            'duration': dataset.duration,
            'filesize': dataset.filesize,  # This is duplicating metadata already included when audio_properties() is run.
            'samplerate': dataset.samplerate
        }

        return attributes
    except:
        return None

def audio_coordinates(input_file: str, cfg_dict: dict = None):
    '''Process an AUDIO granule's coordinates.

    Args:
        input_file (str): The path to an AUDIO granule.
    
    Returns:
        None
    '''
    # This is mostly a function stub. It's here in case there becomes a 
    # way to get spatial data from an AUDIO file in the future. 

    temporal = audio_temporal(cfg_dict)

    coordinates = {
        'time': {'min': temporal['start_time'], 'max': temporal['end_time']},
    }

    return coordinates

def audio_temporal(cfg_dict: dict = None):
    '''Process an AUDIO granule's temporal extents.

    Args:
        input_file (str): The path to an AUDIO granule.
        cfg_dict (dict): A dictionary of key/value pairs that represent configuration options.
    
    Returns:
        dictionary of items for the temporal extents of the metadata
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
        except:
            start_time = None

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

            # If time is 00:00:00, roll back end time by one second, 
            # to prevent confusion regarding the timespan the granule covers.
            if ((cfg_dict['no_adjust_midnight_endtime'] is False) and (end_time[-8:] == '00:00:00')):
                end_time = strptime(end_time, '%Y-%m-%d %H:%M:%S')
                end_time = gmtime(timegm(end_time) - 1)
                end_time = strftime('%Y-%m-%d %H:%M:%S', end_time)
                
                print('NOTE: The \'end_time\' was decremented by 1 second to 23:59:59 of prior day.')
        except:
            end_time = None
    else:
        start_time = None
        end_time = None

    temporal = {
        'start_time': start_time,
        'end_time': end_time,
    }

    return temporal

def audio_statistics(input_file: str):
    '''Process an AUDIO granule's statistics.

    Args:
        input_file (str): The path to an AUDIO granule.
    
    Returns:
        None
    '''
    # This is a function stub. It's here in case there becomes a way
    # to get statistics data from an AUDIO file in the future. 
    return None

def audio_variables(input_file: str):
    '''Process an AUDIO granule's variable list.

    Args:
        input_file (str): The path to an AUDIO granule.
    
    Returns:
        None
    '''
    # This is a function stub. It's here in case there becomes a way 
    # to get information on variables for an AUDIO file in the future. 
    return None

def audio_properties(input_file: str, cfg_dict: dict = None):
    '''Process an AUDIO granule's properties.

    Args:
        input_file (str): The path to an AUDIO granule.
    
    Returns:
        dictionary of items for the properties portion of the metadata
    '''
    if not cfg_dict['no_checksum']:
        checksum = file_checksum(input_file)
    else:
        checksum = None

    properties = {
        'format': 'audio',
        'size': get_file_size(input_file),
        'checksum': checksum,
    }

    return properties

def is_audio_granule(input_file: str):
    '''Determine if granule is an AUDIO granule.

    Args:
        input_file (str): The path to a granule.
    
    Returns:
        boolean indicating if it is an AUDIO granule.
    '''
    fext = splitext(input_file)[1]
    return fext in ['.wav', '.mp3']
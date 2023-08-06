#!/usr/bin/env python3
'''
|
|------------------------------------------------------------------------------
|
|  PROCESS_DAYMET.PY
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

# | Local packages |
try:
    from utilities import format_float
except:
    from scripts.utilities import format_float

# |----------------------------------------------------------------------------
# | DAYMET post-processing function(s)
# |----------------------------------------------------------------------------
def process_Daymet_LL(output_vars):
    # n_variables
    output_vars[18] = '1'

    # variables_units and variables_desc
    variables = output_vars[19].strip('"')
    if variables == 'dayl':
        output_vars[20] = '"s"'
        output_vars[21] = '"daylength"'
    elif variables == 'prcp':
        output_vars[20] = '"mm/day"'
        output_vars[21] = '"daily total precipitation"'
    elif variables == 'srad':
        output_vars[20] = '"W/m2"'
        output_vars[21] = '"daylight average incident shortwave radiation"'
    elif variables == 'swe':
        output_vars[20] = '"kg/m2"'
        output_vars[21] = '"snow water equivalent"'
    elif variables == 'tmax':
        output_vars[20] = '"degrees C"'
        output_vars[21] = '"daily maximum temperature"'
    elif variables == 'tmin':
        output_vars[20] = '"degrees C"'
        output_vars[21] = '"daily minimum temperature"'
    elif variables == 'vp':
        output_vars[20] = '"Pa"'
        output_vars[21] = '"daily average vapor pressure"'

    # max_lat, min_lat, max_lon & min_lon
    if '_na_' in output_vars[4].lower():
        output_vars[8] = format_float(82.9143, 4, False)    # max_lat
        output_vars[9] = format_float(14.0749, 4, False)    # min_lat
        output_vars[10] = format_float(-53.0567, 4, False)  # max_lon
        output_vars[11] = format_float(-178.1333, 4, False) # min_lon

    return output_vars
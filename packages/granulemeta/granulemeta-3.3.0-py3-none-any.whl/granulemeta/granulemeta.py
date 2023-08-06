#!/usr/bin/env python3
'''
|
|------------------------------------------------------------------------------
|
|  GRANULEMETA-V3
|
|  UPDATED:    2023-05-22
|  AUTHOR:     kent campbell
|  CONTACTS:   campbellkb@ornl.gov
|
|  DESCRIPTION
|
|     Script generates low-level metadata and outputs that metadata in the 
|     specified format (i.e. gmout) to a specified output file.
|
|  USAGE
|
|     $  granulemeta.py [-h] [-c CONFIG] [-t TYPE] [-o OUTFILE] [-n NFILES] [--outtype OUTTYPE] [--overwrite] [--daymet]
|                       [--no-adjust-midnight-endtime] [--keep_aux_xml] [--force_blanks] [--no_stats] [--no_checksum] 
|                       [--add_ext] [--version] path [path ...]
|
|        positional arguments:
|           path                            an input directory (OR file OR sequence of files OR glob pattern) to traverse for metadata
|
|        optional arguments:
|           -h, --help                      show this help message and exit
|           -o OUTFILE, --outfile OUTFILE   the path to an output file (with ext)
|           -c CONFIG, --config CONFIG      a configuration file
|           -t TYPE, --type TYPE            input data type: [raster, vector, mdim, table, audio, envi, archive]
|           -n NFILES, --nfiles NFILES      number of files to process before stopping execution (defaults to -1 for all files).
|           --outtype OUTTYPE               type of output file to produce [gmout, ???]
|           --overwrite                     a flag for enabling the overwriting of an existing output file
|           --daymet                        a flag indicating output should be formatted for daymet
|           --no-adjust-midnight-endtime    a flag for disabling the auto-adjustment of the endtime
|           --keep_aux_xml                  a flag to disable the automatic deletion of aux.xml files
|           --force_blanks                  a flag to leave bounding box and time extents blank when not found instead of exiting with an error message
|           --no_stats                      a flag to prevent calculating statistics on granules during execution
|           --no_checksum                   a flag to prevent calculating the md5 checksum on granules during execution
|           --add_ext                       a flag to add '.bin' extensions to extensionless ENVI files
|           --lat_name LAT_NAME             a string providing the name of the column (in the granule) from which the script extracts the latitude values.
|           --lon_name LON_NAME             a string providing the name of the column (in the granule) from which the script extracts the longitude values.
|           --date_name DATE_NAME           a string providing the name of the column (in the granule) from which the script extracts the date values.
|           --time_name TIME_NAME           a string providing the name of the column (in the granule) from which the script extracts the time values.
|           --version                       a flag to allow for the version number of granulemeta to be printed
|
|------------------------------------------------------------------------------
|
'''
# | Python 3 standard library |
from os import remove, rmdir
from os.path import isdir, isfile, realpath, sep, splitext, split as fsplit
from tarfile import open as tar_open
from zipfile import ZipFile as zip_open

# | Local packages |
from config.configuration_parser import parse_filename, read_config
from scripts.utilities import get_fileset, is_extensionless, read_ascii, remove_aux_xml_files
from scripts.utilities import set_cfg_bool, set_cfg_int, set_cfg_str, to_bool
from scripts.gmout import gmout_writer, write_gmout_header
from scripts.parse_arguments import argument_handler, _type_validator, __version__
from scripts.add_ext import add_extensions

from scripts.parse_archive import archive_metadata, is_archive_granule, is_tar_file, is_zip_file
from scripts.parse_audio import audio_metadata, is_audio_granule
from scripts.parse_envi import envi_metadata, is_envi_granule
from scripts.parse_mdim import mdim_metadata, is_mdim_granule
from scripts.parse_raster import raster_metadata, is_raster_granule
from scripts.parse_table import table_metadata, is_table_granule
from scripts.parse_vector import vector_metadata, is_vector_granule

# |----------------------------------------------------------------------------
# | Generate Metadata
# |----------------------------------------------------------------------------
def generate_metadata():
    '''Generate rich metadata outputs in paired JSON and CSV formats.
    
    Call the data traversal function for an input file or directory:
        * the input directory,
        * any found zip archives (zip, tar, gz),
        * any found hierarchival data files (hdf, netcdf). 
    
    Will operate on the file system, archives, or data files, and their 
    sub-constructs.

    Args:
        cfg_dict (dict): A dict of key/value pairs that represent config options.

    Returns:
        ...
    '''
    # Call the argument handler.
    args_ = argument_handler()

    # Get default configuration
    config_dir =  fsplit(realpath(__file__))[0] + sep + 'config'
    default_cfg_file = '%s%s%s' %(config_dir.rstrip(sep), 
                                  sep, 'default.cfg')
    cfg_dict = read_config(default_cfg_file)

    # Get GranuleMetaFormatTypes configuration file
    GMFT_file = '%s%s%s' %(config_dir.rstrip(sep), sep, 
                           'GranuleMetaFormatTypes.cfg')
    GMFT_dict = read_config(GMFT_file)

    # Overrride default with daymet config file if '--daymet' flag was given
    if (args_.daymet is True):
        daymet_cfg_file = '%s%s%s' %(config_dir.rstrip(sep), 
                                     sep, 'daymet.cfg')
        cfg_dict = read_config(daymet_cfg_file, cfg_dict)

    # Override default with command line specified config file 
    if (args_.config is not None):
        cfg_dict = read_config(args_.config, cfg_dict)

    # Add config setting for some flags based on supplied command line args.
    cfg_dict = set_cfg_bool(args_.overwrite, cfg_dict, 'overwrite')
    cfg_dict = set_cfg_bool(args_.daymet, cfg_dict, 'daymet')
    cfg_dict = set_cfg_bool(args_.no_adjust_midnight_endtime, cfg_dict, 'no_adjust_midnight_endtime')
    cfg_dict = set_cfg_bool(args_.keep_aux_xml, cfg_dict, 'keep_aux_xml')
    cfg_dict = set_cfg_bool(args_.force_blanks, cfg_dict, 'force_blanks')
    cfg_dict = set_cfg_bool(args_.no_stats, cfg_dict, 'no_stats')
    cfg_dict = set_cfg_bool(args_.no_checksum, cfg_dict, 'no_checksum')
    cfg_dict = set_cfg_bool(args_.add_ext, cfg_dict, 'add_ext')
    cfg_dict = set_cfg_bool(args_.version, cfg_dict, 'version')

    cfg_dict = set_cfg_int(args_.nfiles, cfg_dict, 'nfiles')
    cfg_dict = set_cfg_str(args_.type, cfg_dict, 'type')

    cfg_dict = set_cfg_str(args_.lat_name, cfg_dict, 'lat_name')
    cfg_dict = set_cfg_str(args_.lon_name, cfg_dict, 'lon_name')
    cfg_dict = set_cfg_str(args_.date_name, cfg_dict, 'date_name')
    cfg_dict = set_cfg_str(args_.time_name, cfg_dict, 'time_name')

    # Make sure 'type' argument is valid
    if cfg_dict['type'] is not None:
        _type_validator(cfg_dict['type'])

    # Handle case where '--version' flag has been supplied
    if (cfg_dict['version'] is True):
        print('\n----- Granulemeta v' + __version__ + ' -----\n')

    # Get the 'path' argument formed into a list of file names
    file_list = get_fileset(args_.path)

    # Rename any extensionless ENVI files to include a '.bin' extension
    # and update the file_list variable to reflect the change
    if (to_bool(cfg_dict['add_ext']) is True):
        file_list = add_extensions(file_list)

    # Check for previously processed granules within specified outfile
    files_processed = []

    # Initialize counter for number of granules processed on this execution
    nfiles_processed = 0

    if (isinstance(args_.outfile, str) and isfile(args_.outfile) and not cfg_dict['overwrite']):
        # If outfile already exists, read its contents
        lines = read_ascii(args_.outfile)

        # and make a list of existing granules the outfile already contains
        if args_.outtype == 'gmout':
            for line in lines[1:]:
                try:
                    fname = line.split(',')[4]
                    files_processed.append(fname)
                except:
                    continue
    else:
        # Outfile doesn't already exist or overwrite flag was set
        write_gmout_header(args_.outfile)

    # Iterate over list of granules to process
    for f in file_list:
        # Bail out if enough granules have been processed this execution
        if nfiles_processed == cfg_dict['nfiles']:
            print('Stopping: %i granules processed.' %nfiles_processed)
            break

        if (f[-8:] == '.aux.xml' and args_.keep_aux_xml == False):
            # Skip aux.xml files if not asked to keep them
            if isfile(f):
                try:
                    remove(f)
                    print('Skipping & Removing: %s' %f)
                except:
                    print('Skipping [Unable to Remove]: %s' %f)
        elif (not is_valid_filetype(f, cfg_dict, GMFT_dict)):
            # Skip invalid file types and ENVI header files
            print('Skipping: %s' %f)
        elif(fsplit(f)[1] in files_processed and not cfg_dict['overwrite']):
            # Skip files already present in outfile
            print('Skipping [Already Processed]: %s' %f)
        else:
            # Process granules based on type
            print('Processing: %s' %f)

            # Parse variable values from filename, if necessary
            if (('filename_regex' in cfg_dict.keys()) and
                (cfg_dict['filename_regex'] is not None)):
                # Parse metadata out of the filename
                cfg_dict = parse_filename(fsplit(f)[1], cfg_dict)

            # Process the granule
            metadata = process_granule(f, cfg_dict, GMFT_dict)

            if not isinstance(metadata, list):
                metadata_list = [metadata]
            else:
                metadata_list = metadata
            
            for metadata in metadata_list:
                # In case something went sideways...
                if metadata is None:
                    # Clean up an .aux.xml files if allowed to, despite no data being found...
                    if args_.keep_aux_xml is False:
                        remove_aux_xml_files([f])

                    print(' WARNING: No metadata produced for %s! Moving on to next granule.' %f)
                    continue

                metadata['granule_id'] = len(files_processed) + nfiles_processed + 1

                # Write Metadata to File
                if args_.outtype == 'gmout':
                    gmout_writer(args_.outfile, metadata, cfg_dict)

                # Increment processed granule counter
                nfiles_processed += 1

                # Clean up an .aux.xml files if allowed to...
                if args_.keep_aux_xml is False:
                    remove_aux_xml_files([f])

    if nfiles_processed != cfg_dict['nfiles']:
        if nfiles_processed == 0:
            print('Finished: No new granules to process.')
        else:
            print('Finished: %i granules processed.' %nfiles_processed)

def process_granule(input_file: str, cfg_dict: dict = None, GMFT_dict: dict = None): 
    if is_archive_granule(input_file):
        granules = []
        path = fsplit(input_file)[0]

        # If 'zip', open with 'zipfile' & get file list.
        if is_zip_file(input_file):
            # Open zip, extract its contents
            with zip_open(input_file, 'r') as z:
                archive_files, _ = z.namelist(), 'zip'
                z.extractall(path)

                # Iterate through extracted contents and process any valid granules.
                for farch in archive_files:
                    # If farch ends with '/', it's a folder. go on to next iteration.
                    if farch.endswith('/'):
                        continue

                    # Attempt to process extracted file.
                    m = process_granule(path + sep + farch, cfg_dict, GMFT_dict)

                    if m is not None:
                        granules.append(m)

        # If 'tar' or 'targz', open with 'tarfile' & get file list.        
        if is_tar_file(input_file):
            # Open tar(gz), extract its contents
            with tar_open(input_file, 'r') as z:
                archive_files, _ = z.getnames(), 'tar'
                z.extractall(path)

                # Iterate through extracted contents and process any valid granules.
                for farch in archive_files:
                    # If farch ends with '/', it's a folder. go on to next iteration.
                    if farch.endswith('/'):
                        continue
                    
                    # Attempt to process extracted file.
                    m = process_granule(path + sep + farch, cfg_dict, GMFT_dict)

                    if m is not None:
                        granules.append(m)

        metadata = archive_metadata(input_file, cfg_dict)

        for granule in granules:
            # If any metadata was retrieved add to metadata dict for its parent zip file.
            try:
                metadata['metadata']['attributes'] = granule['metadata']['attributes']
            except:
                pass

            try:
                metadata['metadata']['coordinates'] = granule['metadata']['coordinates']
            except:
                pass

            try:
                metadata['metadata']['statistics'] = granule['metadata']['statistics']
            except:
                pass
            
            try:
                metadata['metadata']['variables'] = granule['metadata']['variables']
            except:
                pass

        # Delete extracted copies
        for farch in archive_files:
            if isfile(path + sep + farch):
                remove(path + sep + farch)
        
        # Delete empty extracted archive directory
        arch_dir = fsplit(input_file)[0] + sep + fsplit(farch)[0]
        if isdir(arch_dir):
            try:
                rmdir(arch_dir)
            except:
                pass

    elif is_envi_granule(input_file):
        # Process ENVI granules
        metadata = envi_metadata(input_file, cfg_dict)
    elif is_extensionless(input_file):
        print(' ERROR: %s does not have a file extension and not a valid ENVI granule' %input_file)
        exit(1)
    elif is_mdim_granule(input_file):
        # Process MDIM granules (netCDF, HDF4, HDF5)
        metadata = mdim_metadata(input_file, cfg_dict)
    elif is_audio_granule(input_file):
        # Process AUDIO granules (WAV, MP3)
        metadata = audio_metadata(input_file, cfg_dict)
    elif is_vector_granule(input_file, GMFT_dict):
        # Process VECTOR granules (KML, KMZ, SHP)
        metadata = vector_metadata(input_file, cfg_dict)
    elif is_raster_granule(input_file, GMFT_dict):
        # Process RASTER granules (geoTIFF)
        metadata = raster_metadata(input_file, cfg_dict)
    elif is_table_granule(input_file):
        # Process TABLE (TEXT & ICARTT) granules (CSV, TSV, TXT, DAT, ICARTT)
        metadata = table_metadata(input_file, cfg_dict, GMFT_dict)
    else:
        return None

    return metadata

def is_valid_filetype(input_file: str, cfg_dict: dict = None, GMFT_dict: dict = None):
    '''Indicate whether a granule's filetype is valid for processing.
    
    Args:
        input_file (str): The path to a granule.
        cfg_dict (dict):  A dict of key/value pairs that represent config options.
        GMFT_dict (dict): A dictionary of GranuleMeta Format Types.
    
    Returns:
        boolean indicating if granule's filetype is valid for processing.
    '''
    #NOTE: Could easily add functionality for excluding a filetype here. 
    #      just read config file and if the input_file is the "excluded" 
    #      type, return false before checking for any of the usually 
    #      included filetypes.  

    if (is_archive_granule(input_file) and 
        cfg_dict['type'] in ['archive', None]):
        return True
    elif (is_envi_granule(input_file, True) and 
          cfg_dict['type'] in ['envi', None]):
        return True
    elif (is_mdim_granule(input_file) and 
          cfg_dict['type'] in ['mdim', None]):
        return True
    elif (is_audio_granule(input_file) and 
          cfg_dict['type'] in ['audio', None]):
        return True
    elif (is_vector_granule(input_file, GMFT_dict) and 
          cfg_dict['type'] in ['vector', None]):
        return True
    elif (is_raster_granule(input_file, GMFT_dict) and 
          cfg_dict['type'] in ['raster', None]):
        return True
    elif (is_table_granule(input_file) and 
          cfg_dict['type'] in ['table', None]):
        return True
    else:
        return False

# |----------------------------------------------------------------------------
# | __main__
# |----------------------------------------------------------------------------
if __name__ == '__main__':
    generate_metadata()
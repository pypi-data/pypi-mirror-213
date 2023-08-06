#!/usr/bin/env python3

'''
|
|------------------------------------------------------------------------------
|
|  ADD_EXT.PY
|
|  UPDATED:     2023-02-14
|  AUTHOR:      kent campbell
|  CONTACTS:    campbellkb@ornl.gov
|
|  DESCRIPTION
|
|     Script generates adds '.bin' extension to any extensionless file found
|     within the supplied path argument that has a corresponding '.hdr' file.
|
|  USAGE
|
|     $  add_ext.py [-h] path [path ...]
|
|        positional arguments:
|           path        an input directory (OR file OR sequence of files OR glob pattern(s)) to traverse
|
|           optional arguments:
|               -h, --help  show this help message and exit
|
|------------------------------------------------------------------------------
|
'''
# | Python 3 standard library |
import argparse
import re

from os import remove, walk
from os.path import isdir, isfile, normpath, sep, splitext, split as fsplit
from shutil import copy2

# |----------------------------------------------------------------------------
# | command line argument handling functions
# |----------------------------------------------------------------------------
def argument_handler():
    '''Primary argument handler.'''
    
    # Parser object.
    p = argparse.ArgumentParser()

    # Positional argument 1: Input directory or file.
    p.add_argument('path',
                   type = _file_and_dir_validator,
                   nargs = '+',
                   help = 'an input directory (OR file OR sequence of files OR glob pattern(s)) to traverse')

    # Return parsed arguments.
    return p.parse_args()

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

# |----------------------------------------------------------------------------
# | sorting function(s)
# |----------------------------------------------------------------------------
def natural_key(string_):
    '''Allows application of "Natural Sorting" algorithm'''
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]

# |----------------------------------------------------------------------------
# | file system utility functions
# |----------------------------------------------------------------------------
def get_files(path):
    '''Retrieves a sorted list of files found within the provided path and its subdirectories 

    Args:
        path (str): path to recursively walk through in search of files
    
    Returns:
        sorted_filenames (list): a sorted list of files contained in the 
                                 directory searched and all its subdirectories
    '''
    filenames = []

    for d, _, f in walk(path):
        for fn in f:
            filename = normpath(d) + sep + fn

            if filename not in filenames:
                filenames.append(filename)
    
    sorted_filenames = []

    for fn in sorted(filenames, key = natural_key):
        sorted_filenames.append(fn)

    return sorted_filenames

def get_fileset(path):
    '''Retrieves a sorted list of files found within the provided path and its subdirectories 

    Args:
        path (list): a list containing one of the following:
                     1. a glob style list of files handled the command line and argparse
                     2. a singular file name (incl. path) without any wildcards
                     3. a single directory/path without any wildcards
    
    Returns:
        path (list): a sorted list of files to process for metadata
    '''
    if isinstance(path, list) and len(path) > 1:
        # glob style list of files handled by the command line and argparse
        return path
    elif isinstance(path, list) and isfile(path[0]):
        # singular file without wildcards
        return path
    elif isinstance(path, list) and isdir(path[0]):
        # directory without wildcards
        return get_files(path[0])

def is_extensionless(input_file: str):
    '''Determine if the file has a file extension

    Args:
        input_file (str): The path to a file

    Returns:
        boolean indicating if it lacks a file extension
    '''

    return splitext(input_file)[1] == ''

# |----------------------------------------------------------------------------
# | ENVI file detection functions
# |----------------------------------------------------------------------------
def is_envi_header(input_file: str):
    '''Determine if file is actually an ENVI header file

    Args:
        input_file (str): The path to a file
    
    Returns:
        boolean indicating if it is an ENVI header file
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
    
def is_envi_file(input_file: str):
    '''Determine if file is an ENVI file based on if it has a
       corresponding header (.hdr) file and if that header file's 
       first line only contains the word 'ENVI'

    Args:
        input_file (str): The path to a file
    
    Returns:
        boolean indicating if it is an ENVI file
    '''
    if isfile(input_file + '.hdr'):
        return is_envi_header(input_file + '.hdr')
    elif input_file == splitext(input_file)[0] + '.hdr':
        return False
    elif isfile(splitext(input_file)[0] + '.hdr'):
        return is_envi_header(splitext(input_file)[0] + '.hdr')
    else:
        return False

# |----------------------------------------------------------------------------
# | function for adding extensions to extensionless ENVI files
# |----------------------------------------------------------------------------
def add_extensions(file_list: list):
    for i in range(len(file_list)):
        f = file_list[i]

        if is_envi_file(f) and is_extensionless(f):
            fname = fsplit(f)[1]
            print('Renaming %s to %s' %(fname, fname + '.bin'))
            
            # Create copy of file with '.bin' extension, including permissions
            # and all metadata (creation and modification times, etc..)
            copy2(f, f + '.bin')

            # Delete original file
            remove(f)

            file_list[i] = f + '.bin'

    if __name__ != '__main__':
        return(file_list)

# |----------------------------------------------------------------------------
# | __main__
# |----------------------------------------------------------------------------
if __name__ == '__main__':
    # Call the argument handler.
    args_ = argument_handler()
    file_list = get_fileset(args_.path)

    add_extensions(file_list)
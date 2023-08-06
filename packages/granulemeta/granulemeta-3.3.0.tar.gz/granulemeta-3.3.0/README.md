# granulemeta


This code was orginally created as a file-level metadata extraction tool for use by the ORNL DAAC. The update to version 3 represents a complete refactoring in the approach taken by the prior version of ORNL DAAC's file level metadata extraction tool. The refactoring of the code put an emphasis on making the codebase more maintainable and extensible while making the code's execution more consistently stable and yet more flexible in how the code could be utilized by the end-user.  

The default output for granulemeta-v3 is a csv in **gmout** format (as is necessary for ORNL DAAC's ingest process), however the code can easily be extended to accomodate other output formats. 

## install

```
pip install granulemeta
```

## usage

### Run from the command line:

```
granulemeta.py -o [OUTPUT_FILE].csv [PATH: directory or file or glob]
```

### Run from docker container for local development:
```
./run-docker-dev.sh [PATH TO DATA DIRECTORY] [PATH TO GRANULEMETA CODE DIRECTORY]
```

This will give you a command line environment to run granulemeta in. The first path argument provided will be mounted as `/data` and the second path argument as `/code`. Within the dev container, granulemeta can be run using the following syntax:
```
granulemeta -o [OUTPUT_FILE].csv [PATH: directory or file or glob]
```

## requirements
This script was developed on Python 3. It relies on **five** packages not in Python's standard library:

* `numpy`: https://numpy.org/
* `pandas`: https://pandas.pydata.org/
* `netCDF4`: https://unidata.github.io/netcdf4-python/netCDF4/index.html
* `tinytag`: https://pypi.org/project/tinytag/
* `gdal`: https://gdal.org/python/

[`requirements.txt`](requirements.txt) was last generated on 2022-06-09.

## notes
Notable features added since the creation of version 3:
* Lines are written to the output file as it processes each granule instead of waiting until all granules have been processed to write the output file.
* Unless the `--overwrite` option is given, the script will skip granules already present in the output file. This (coupled with the feature directly above) will allow the script to pick up where it left off if it crashes partway through processing a dataset.
* There is a `--nfiles` (or `-n`) option that allows the script to automatically stop execution after processing a specified number of granules.
* [Glob syntax](https://en.wikipedia.org/wiki/Glob_(programming)) can now be used for the input `path` argument to allow a user to restrict the files that a given execution of the script processes (i.e. using `/path/*.nc` as your input path would only process granules with the `.nc` file extension).
* Behind the scenes, the code is better organized to better facilitate redability, maintainability, and extensibility. This has been accomplished by breaking the code up into several modules.

## authorship
The following authors have contributed to the granulemeta development process:

Kent Campbell, Jack McNelis, Vinny Palandro, Yaxing Wei, Tammy Walker, Matt Donovan, Jessica Welch, Daine Wright, Bruce Wilson, Chris Lindsley, Ketan Patel, Scott Pearson, Rupesh Shrestha, Tom Ruggles

## contacts
author: campbellkb@ornl.gov
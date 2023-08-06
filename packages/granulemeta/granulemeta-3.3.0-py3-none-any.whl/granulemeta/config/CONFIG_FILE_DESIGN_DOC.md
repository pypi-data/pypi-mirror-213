# Configuration File Design and Usage Document

## Overall design constraints & philosohpy

1. Comment lines will be on a line of their own. Comment lines are indicated by a `#` at the beginning of the line.

1. Comment lines and blank lines will not be parsed.

1. Configuration files will be human readable/editable. The format for configuration variable syntax is a keyword followed by an equal sign (preferrably with a space on either side of the equal sign, for readability), and then the value for the keyword (this type of line will be referred to as a key/value pair for the remainder of this document).

1. Malformed key/value pairs (i.e. missing the keyword, value or = between them) will throw an error so that the user can rectify the issue.

1. The primary function within the configuration parser will be `read_config()`. It will have one required argument (`filename`), which will be a string argument providing the path and filename of the configuration file to be read. Its return value will be a dictionary of those key/value pairs. It has a second (optional) argument (`kv_dict`) of type dictionary that will allow for a program to use `read_config()` in multiple passes (i.e. first call is to the default config file, second call is for the project specific one that only has key/value pairs for things that deviate from the default). Each "pass" will simply append new key/value pairs or overwrite existing ones to the passed in `kv_dict` with key/value pairs found in the configuration file specified as the `filename` argument.

1. The list of keywords available for use within a configuration file are as follows:
	1. `filename_regex`: Regular expression defining the format of the input file names and serves as a mechanism to split out date(s) and time(s) for further parsing by the next several keywords in this list.

	1. `file_date_in_format`: Format for parsing a date (from the output of the regex defined by the `filename_regex` key/value pair), using the syntax for [strptime](https://docs.python.org/3/library/time.html#time.strptime) in Python's time module to determine the format of the value string.

	1. `file_date_out_format`: Using the syntax for [strftime](https://docs.python.org/3/library/time.html#time.strftime) in Python's time module, this specifies how dates within the filename should be reformatted.

	1. `file_time_in_format`: Format for parsing a time (from the output of the regex defined by the `filename_regex` key/value pair), using the syntax for [strptime](https://docs.python.org/3/library/time.html#time.strptime) in Python's time module to determine the format of the value string.

	1. `file_time_out_format`: Using the syntax for [strftime](https://docs.python.org/3/library/time.html#time.strftime) in Python's time module, this specifies how timestamps within the filename should be reformatted.

	1. Any of the header/column names within the output csv will override what it reads from the metadata within the file (i.e using `gr_id` as a key will replace the `gr_id` value typically generated in the gmout wrapper with the value found in the config file). The header/column names that can be used in a configuration file to override an existing value are:<br> ds_id, granule_id, gr_id, subdir, filename, title, start_time, end_time, max_lat, min_lat, max_lon, min_lon, file_type, file_format, geometry_type, day_night, file_size_mb, checksum_md5, n_variables, variables, variables_units, variables_desc, calendar, native_datatype, offered_resampling, native_crs, native_crs_wkt, native_crs_proj4, offered_crs, res_x, res_y, res_z, min_x, min_y, min_z, max_x, max_y, max_z, map_units, z_units, n_cols, n_rows, n_bands, scaling, offset, time_series, min_val, max_val, mean_val, stddev_val, nodata_val, break_method, num_of_classes, color_scheme, b_reverse_color, b_use_parent_color_scheme, b_enhance, lut, feature_notes, additional_information

1. Notes on specific keywords and their use and/or mechanics of how they will be parsed (some of this will be clearer in example config file):
	1. For the purposes of parsing data from the filename, the keyword will be `filename_regex`, its expected value is a regular expression as expected by Python's [re](https://docs.python.org/3/library/re.html#module-re) module.

	1. Dates will be parsed out of and formatted into a specified format based on format strings as expected by the [strptime](https://docs.python.org/3/library/time.html#time.strptime) and [strftime](https://docs.python.org/3/library/time.html#time.strftime) functions from Python's [time](https://docs.python.org/3/library/time.html) module.

1. A secondary function called `parse_filename()` as a convenience function. It takes a datafile's filename and a configuration dictionary (output from `read_config()`) as its input arguments and parses dates, times, or other values as specified by the appropriate configuration key/value pairs from the filename itself. This function will necessitate certain elements to be present in the regular expression and certain conventions be adhered to. Some of the specific conventions are as follows:
	1. Blocks of text intended to be parsed as a date should be given a symbolic group name that includes the word "date" using the `(?P<name>...)` syntax documented in the documentation for Python's [re](https://docs.python.org/3/library/re.html#module-re) module.

	1. Blocks of text intended to be parsed as a time should be given a symbolic group name that includes the word "time" using the `(?P<name>...)` syntax documented in the documentation for Python's [re](https://docs.python.org/3/library/re.html#module-re) module.

	1. In cases where the symbolic group name contains both the words "date" and "time", the date formatting will be used.

	1. Blocks of text intended to be parsed as an override for a <b><i>non-date/time</i></b> value in the output file should use the same word as the header/column name corresponding to that value (i.e. use `(?P<gr_id>\S+)` to overwrite the extracted/generated value for `gr_id` with whatever is parsed out of the filename). This also means that if the `start_date` value will be parsed from the filename, EITHER symbolic groups for `start_date` and `start_time` both need to be defined in the `filename_regex` key/value pair OR a symbolic group for just `start_date` should exist and the corresponding values for `file_date_in_format` and `file_date_out_format` should handle both date and time formatting.

## Regular expression examples

Using `190821_113533_190921_125931_LS_ADAPD.tdms` as the filename:
1. With a config file that looks like:<br>
	```
	filename_regex = (?P<start_date>\d+)_(?P<start_time>\d+)_(?P<end_date>\d+)_(?P<end_time>\d+)_(?P<project_name>\S+)\.(?P<file_ext>\S+)
	file_date_in_format = %y%m%d
	file_date_out_format = %Y/%m/%d
	file_time_in_format = %H%M%S
	file_time_out_format = %H:%M:%S
	```

	Running `parse_filename()` will add key/value pairs for `start_date`, `start_time`, `end_date` and `end_time` within the configuration dictionary. The granulemeta wrapper will take dates and times and concatenate them to write to the output file in the `start_time` and `end_time` columns, respectively.
	With the example filename and the configuration parameters above, it would produce a `start_time` of "2019/08/21 11:35:33" and an `end_time` of "2019/09/21 12:59:31".
	
1. With a config file that looks like:<br>
	```
	filename_regex = (?P<start_date>\d+_\d+)_(?P<end_date>\d+_\d+)_(?P<project_name>\S+)\.(?P<ext>\S+)
	file_date_in_format = %y%m%d_%H%M%S
	file_date_out_format = %Y/%m/%d %H:%M:%S
	```

	Running `parse_filename()` will add key/value pairs for `start_date`  and `end_date` within the configuration dictionary. The granulemeta wrapper will take the datetimes and write them to the output file in the `start_time` and `end_time` columns, respectively.
	With the example filename and the configuration parameters above, it would produce a `start_time` of "2019/08/21 11:35:33" and an `end_time` of "2019/09/21 12:59:31".

1. With a config file that looks like:<br>
	```
	filename_regex = (?P<start_time>\d+_\d+)_(?P<end_time>\d+_\d+)_(?P<project_name>\S+)\.(?P<ext>\S+)
	file_time_in_format = %y%m%d_%H%M%S
	file_time_out_format = %Y/%m/%d %H:%M:%S
	```

	Running `parse_filename()` will add key/value pairs for `start_time`  and `end_time` within the configuration dictionary. The granulemeta wrapper will take the datetimes and write them to the output file in the `start_time` and `end_time` columns, respectively.
	With the example filename and the configuration parameters above, it would produce a `start_time` of "2019/08/21 11:35:33" and an `end_time` of "2019/09/21 12:59:31".
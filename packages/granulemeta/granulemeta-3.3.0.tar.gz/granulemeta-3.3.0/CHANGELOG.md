# Changelog

All notable changes to this project will be documented in this file.
Changes should be included in merge requests. Then copied here.

## 3.3.0 - 2023-06-14
- [Made granulemeta repo publicly available on github]()
- [Made granulemeta pip installable through PyPI]()

## 3.2.2 - 2023-05-22
- [Fixed newly created bug in midnight endtime adjustment code](0103f55bf2df2374f6aec199c6de7bd3b6832349)
- [Removed unnecessary print statement](03b5be5b1006e7861d443ddad898b8e95535248a)
- [Allow 3 digit years to be handled](87b1e9f8041759d72a863350964fa7e81f329606)
- [14 - Improved processing speed of large CSVs](cda5f6127a2c8a0c2b190eba23518af5734a7f47)
- [13 - Added ability to Latitude, Longitude, Date & Time variable names](33099e2a7699c12223ea89da4c0c2c40b859fc7b)

## 3.2.1 - 2023-02-14
- [Added `--version` flag](b7c79b44f4cb43e1e34f77d3f1a155293e7c7d49)
- [Expanded vector and raster file types that can be processed including image file types (jpg, jpeg, gif, png)](ca9c2ed987d9fa459ef73f450e85d71b0c7bc567)
- [Added a warning and an error for extensionless files](dec6acdc2287a97738f18acaa5dfa27a111bbeaf)
- [Added script (`add_ext.py`) for giving extensionless ENVI files a file extension](7de72c43183e2c3751da856de4c21d12c6a16759)
- [Added `--add_ext` option for using `add_ext.py` during execution of granulemeta](e3774d7ab66ceceadbf5b7075003460fc9de123c)
- [Added ability to use config to toggle command line flags](34ee915d9bfc075eab1b3dff32305004b52b3e9c)
- [Updated `kitchen_sink.cfg` to reflect recent updates](31a4c27f403372cc22b7bc60db1dd04d8c0b5060)
- [Minor formatting/content updates to comment blocks for consistency's sake](e0d9d8defbd18309b11b8ded4a4d2d95b7d78cd4)

## 3.2.0 - 2023-01-12
- [Added version number to help text](6463c75ee8f3ecedc2cd271ccedd0604091cae59)
- [Add --daymet flag and functionality](a901a63c8935b4bfd239d66fe356055078afa1cd)
- [Fixed 2nd transposed lat/lon issue](001268ad7bcccf583da54338b833762761aa8584)

## 3.1.9 - 2023-01-04
- [Fixed issue with Lat/Lon Transposition in GMOUT](97d74358597caeafca74d4b807bc2e6f3ae5c518)
- [Provided option to turn off checksum computations](d802ed078c955cf1910f1984bf144e23cfe1c6a3)

## 3.1.8 - 2022-11-29
- [Added COG/non-COG format differentiation](6739024e21bbd11ccf6c1b1ec7b81e14685b378b)
- [Added a space at the beginning of 'WARNING' messages](71c705b4f036546ca8ade86e46a7fd4544a9af05)

## 3.1.7 - 2022-10-21
- [Fixed auto-cleanup of temporary archive files](eb6d32beb22eee98a38c44dff842d479f6054dfd)
- [Fixed coordinates error with archive granules](39dacc25a171545917deda380fe150c45737fb19)
- [Added `--no_stats` command line flag](724bc52a23dea31a8131fc63ee93e499b49b7e6c)

## 3.1.6 - 2022-08-22
- [Added `--type` option functionality](bd21f9160522b299b5cdb34b7ec4c8e0fa4f84e8)
- [Improved handling of non-georeferenced netCDFs](f92270766eb9bb5052d1ed88f3f270e0f506bd9c)

## 3.1.5 - 2022-07-26
- [Added ability to handle non-georeferenced netCDFs](21f2c1fed87743df48ac1ed9e982cd1e895d477b)

## 3.1.4 - 2022-07-14
- [Added increased functionality for ENVI granule detection](2deec53b4da90f22a584f6161c79f8d4101d64e3)
- [Fixed instability issue in processing vector granules](186b917551cc45b2bb7bcc175d9b572282b2ac36)

## 3.1.3 - 2022-07-08
- [Improved how netCDF variables are extracted as metadata](fda7df924629a67be16ba54b1c3b0b8792f2ea81)
- [Removed unnecessary debug/dev code](5533bf9a80b7055937ce74472ae8d526aba89aa6)

## 3.1.2 - 2022-07-05
- [stability and reliability fixes and minor new features](81642fc67750bc4faedcb1c28d409500f7404764)

## 3.1.1 - 2022-06-09
- [added dev docker container](01efbda7cc3199491f2d2d35abe48e98783f8499)
- [minor code tweak](52fc3dc96ebbdabc07f96f120b129e27375d747c)
- [fixed formatting and documentation](55aa41b15cbe70c4b4e7dd9e871568a1b23f2f91)
- [fixed more formatting and documentation](68891df9b882d71b5c47b5638d45058da16b34e9)
- [added warning for when no metadata produced for a given granule](1f9367eec8f7c2ea97bdee55520057374865a298)
- [added warnings to gmout for some specific missing or negative values](dad83fee55be8581be7c6d1eecada9c573f5689f)
- [fixed some start & end time bugs](4dc200c47bb8d43b65b51966266bc106d1749002)

## 3.1.0 - 2022-06-08
- [major update. (now handles every granule type V2 handles)](6c1970a231d9157325ef796c2c44c88f09fd5e48)

## 3.0.0 - 2022-06-01
- [initial commit (only handles ENVI, netCDF & HDF granules)](63ffba2e85d63260150ba152b8cc131d5033cbc2) 

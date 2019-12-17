# Software for data processing of array spectroradiometer 
[![License: CC BY-SA 4.0](https://licensebuttons.net/l/by-sa/4.0/80x15.png)](https://creativecommons.org/licenses/by-sa/4.0/)

## Description
The repository contains scripts to process the data of array spectroradiometer BTS2048.

The software package 
* reads OR0-Files from UV observations with the array spectroradiometer and 
* is able to visualize the data and
* is able to convert the data to netcdf.

## Requirements
The software is written in [Python](https://www.python.org).
The software requires Python Version ??? TODO.
The software requires following Python packages:
* argparse
* calendar
* datetime
* matplotlib
* NetCDF
* numpy
* os
* pygal



## Usage
```
python ??? -s 20180913 -e 20181231 TODO
```
## Authors
* Rico Hengst
* Nicolas Bayer
* Lionel Doppler

## TODO's
* use json file as metadata lookup table to write static netcdf metadata file 
* improve connfiguration in terms of folder structure (input data)
  * case 1 (default), use branced structure
  * case 2, use flat structure (all files in a single directory)
* improve connfiguration in terms of file name convention (location abbrev in filename as constant part of filename)
  * case 1 (default), use 'MP'
  * case 2, use another name
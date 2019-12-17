# Software for data processing of array spectroradiometer 
[![License: CC BY-SA 4.0](https://licensebuttons.net/l/by-sa/4.0/80x15.png)](https://creativecommons.org/licenses/by-sa/4.0/)

## Description
The repository contains scripts to process the data of array spectroradiometer BTS2048.
The software package 
* reads OR0-Files from UV observations with the array spectroradiometer BTS2048 and 
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
* improve connfiguration in terms of folder structure 
  * case 1 (default), use branced structure
    * `├── 2019
│   ├── 01
│   │   ├── 01
│   │   ├── 02
│   │   ├── 03
│   │   ├── 04
│   │   ├── 05
│   │   ├── 06
│   │   ├── 07`
  * case 2, use flat structure (all files in a single directory)
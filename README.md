# BTS 2048 data post-processing

[![License: CC BY-SA 4.0](https://licensebuttons.net/l/by-sa/4.0/80x15.png)](https://creativecommons.org/licenses/by-sa/4.0/)

The repository contains post-processing scripts to read and visualize solar radiation data exported by the  "Solarscan Software System" (hereinafter referred as Solarscan).


## Description
### General issue
The spectroradiometer BTS2048 is currently operated via a Solarscan. Solarscan is responsible for the a continuous scheduling and the measurement and the radiometric calibration of the BTS2048. Solarscan exports it's data in a specific ASCII-Format, see also [Solarscan User Manual](doc/Solarscan_BTS2048.pdf).

The used file format of the Solarscan export is not well documented. However, the data should be archived in a well documented file format, which will be used of a majority of the Earth science community. The scripts of that repository will take account of this.

### Objectives
The software package is written to post-process observed solar radiation data of the array spectroradiometer BTS2018.
The software package includes
* a module to read OR0-Files from UV observations stred in Solarscan format and
* a module to visualize the numerical data and
* a module to store data as netcdf file(s)
* a module to visualize data gaps.

### Assumption
* the OR0-Files should fits the naming pattern "`&lt;IDYYMMDD&gt;.OR0`", where 
  * **ID** is a character string with a length of two and respresents a identifier of the UV station
  * and **YY** year since 2000, **MM** number of month, **DD** day of the month (all filled with zeros)
* the OR0-Files are in following directory structure "&lt;YYYY/MM/DD/&gt;", where
  * and **YYYY** year, **MM** number of month, **DD** day of the month (all filled with zeros)
### Scheme
![BTS scheme](doc/bts_scheme.png)

## Requirements

* Python version 3.x
* argparse
* calendar
* datetime
* matplotlib
* NetCDF
* numpy
* os
* pygal
* configparser

## Usage
```
python BTS_main_process.py -s 20190101 -e 20190102

```

## License
[CC BY-SA 4.0 ![License: CC BY-SA 4.0](https://licensebuttons.net/l/by-sa/4.0/80x15.png)](https://creativecommons.org/licenses/by-sa/4.0/)

## DISCLAIMER

Please note: all tools/ scripts in this repository are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. We disclaim any and all warranties, either express or implied, including but not limited to any warranty of noninfringement, merchantability, and/ or fitness for a particular purpose. We do not warrant that the technology will meet your requirements, that the operation thereof will be uninterrupted or error-free, or that any errors will be corrected.

Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.

You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.

## Authors
* Rico Hengst
* Lionel Doppler
* Nicolas Bayer

## Cooperation
![Tropos Logo](doc/TROPOS-Logo_ENG.png)
![DWD Logo](doc/Deutscherwetterdienst-logo.png)

## ToDo
* improve script to read, plot auxiliary data

# Data import and processing of SOLARSCAN OR0-files
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

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
* a switch to visualize data gaps (missing files).

### Assumption
**Filename:** the OR0-Files should fits the naming pattern "`<IDYYMMDD>.OR0`", where
  * **ID** is a character string with a length of two and respresents a identifier of the UV station
  * and **YY** year since 2000, **MM** number of month, **DD** day of the month (all filled with zeros)

### Scheme
![BTS scheme](doc/bts_scheme.png)

## Requirements 1

* Python version 3.x
* argparse
* calendar
* configparser
* datetime
* matplotlib
* mpl_toolkits
* netCDF4
* numpy
* os
* pandas
* pytz
* pygal


## Requirements 2 (optional)
To generate plots about the statistics of **missing data** in your archiv you have to implement a further python module [github.com/rico-hengst/tropos.heatmap_missing_files](https://github.com/rico-hengst/tropos.heatmap_missing_files) from as git submodule.
```
# go to root directory of the current main repo

# Already done during implementation of submodule
# Add submodule repository
$ git submodule add <repository> <path>
$ git submodule add https://github.com/rico-hengst/tropos.heatmap_missing_files src/Submodule

# Already done during implementation of submodule
# notice the modification to your main repository
$ git status -s
A  .gitmodules
A  src/Submodule
$ git commit "added submodule"


# Last step is always required to get updates
# Init submodule and get content from the repository
$ git submodule update --init

```
... to embedding external git repositories in the current repository.

* [vogella.com](https://www.vogella.com/tutorials/GitSubmodules/article.html)
* [ralfebert.de](https://www.ralfebert.de/git/submodules/)

 
## Configuration

When using this software code for the first time, we would like to recommend to configure the code in s suggested way. configuration.
The software has two configuration files. Please copy both configuration files to the software root directory and use the extension ```.private```.
```bash
cp src/config.default src/config.private
cp src/uv_js_meta.json.default src/uv_js_meta.json.private
```

* ```uv_js_meta.json.private```: Please edit your contact data at the JSON-file ```uv_js_meta.json.private```, that is used for writing UV measurement data and metadata to a netcdf file. 
* ```config.private```: Please edit also the content of the INI-file ```config.private```. The INI-file contains the configuration about the directory paths of your UV measurements, the directory of the software output (netcdf, quicklooks) and so on.
Please edit also the name of the json_file to ```json_file=uv_js_meta.json.private```.

Now the configuration is done.


## Usage

```
# example to create netCDF files and images
cd src

./BTS_main_process.py -n -i -s 20190101 -e 20190102


optional arguments:
  -h, --help         show this help message and exit
  -s ID              Insert the initial date as 20190107 (YYYYmmdd)
  -e FD              Insert the final date as 20190107 (YYYmmdd)
  -i, --image        create images files
  -n, --netcdf       create netCDF files
  -st, --statistics  create statistics of missing files !! Submodule required, see Requirements 2 !!

``` 


## License
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Logos, icons and the Solarscan User manual are not affected by the license of this repository.


## Authors
* Rico Hengst ![Logo](doc/ORCIDiD_icon16x16.png) [https://orcid.org/0000-0001-8994-5868](https://orcid.org/0000-0001-8994-5868)
* Nicolas Bayer
* Lionel Doppler ![Logo](doc/ORCIDiD_icon16x16.png) [https://orcid.org/0000-0003-3162-8602](https://orcid.org/0000-0003-3162-8602)

## Cooperation
![Tropos Logo](doc/TROPOS-Logo_ENG.png)
![DWD Logo](doc/Deutscherwetterdienst-logo.png)

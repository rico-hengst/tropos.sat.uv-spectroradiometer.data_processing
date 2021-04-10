#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 13:30:44 2019

@author: bayer
"""

from netCDF4 import date2num
import numpy as np
import logging
# Hartwigs sunpos routine
from trosat import sunpos as sp
from trosat import cfconv as cf

""" Create logger, name important """
module_logger = logging.getLogger('uv-processing.BTS2NetCDF')

def netCDF_file(d_bts1day,nc_file, cfjson ):
    """
    Creates netCDEF-File for UV measurements for a specific date. 

    Parameters
    ----------
    d_bts1day : Dictionary
        Contains the data measured by th UV-Spectrometer.
    nc_file : string
        PathFileName of netcdf-File and location where it will be saved in.
    cfjson : Dictionary
        Contains all the meta-data from the json-file.
    """
    
    """ Calculate cosine of zenith, angle and earth-sun-distance """
    szen, sazi = sp.sun_angles(d_bts1day['datetime'],cfjson['variables']['lat']['data'], cfjson['variables']['lon']['data'])
    esd=sp.earth_sun_distance(d_bts1day['datetime'])

    """ Write dict data to numpy array https://www.quora.com/Is-it-possible-to-convert-a-Python-set-and-dictionary-to-a-NumPy-array """
    np_datetime = np.array(list(d_bts1day["datetime"]))
    
    """ Prepare time variable to store seconds since ... in netCDF-File """
    second_since = date2num(np_datetime, cfjson['variables']['time']['attributes']['units'])
    
    """ Create dictionary for mapping the data and concatenate the variables names and location """
    mapping_table={"lon":{"conf":"lon"},
          "lat":{"conf":"lat"},
          "elev":{"conf":"elev"},
          "uva_irrad":{"bts":"uva"},
          "uvb_irrad":{"bts":"uvb"},
          "uv_index":{"bts":"uvind"},
          "spec_irrad":{"bts":"spect"},
          "wvl":{"bts":"wvl"},
          "uv_irrad":{"bts":"uvint"},
          "sazi":{"calculated":sazi},
          "szen":{"calculated":szen},
          "esd":{"calculated":esd},
          "time":{"calculated":second_since}
          }
    
    """ Introduce the size of the dimensions for each case """        
    cfjson.setDim('time', len(d_bts1day['time']))
    cfjson.setDim('wvl', len(d_bts1day['wvl']) )
    
    """ add data to the variables """
    for netcdf_variable , mapping_table_value in mapping_table.items():
        for attribution , local_variable in mapping_table_value.items():
            if attribution == 'bts':
                cfjson.setData(netcdf_variable,d_bts1day[local_variable])
            elif attribution == 'calculated':
                cfjson.setData(netcdf_variable,local_variable)
    
    """ Creating and saving the netCDF-File """
    f = cf.create_file(nc_file, cfdict=cfjson)
    
    f.close()

    module_logger.info( 'Write data to netcdf: ' + nc_file )  




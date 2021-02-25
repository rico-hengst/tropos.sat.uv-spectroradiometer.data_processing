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

# create logger, name important
module_logger = logging.getLogger('uv-processing.BTS2NetCDF')

def netCDF_file(d_bts1day,nc_file, cfjson ):

    # """checking if the file does already exist, and delete if so."""
    # if os.path.isfile(netCDF_path+i8date+'.nc'):
    #     os.remove(netCDF_path+i8date+'.nc')
    
    ## calculate cosine of zenith angle
    szen, sazi = sp.sun_angles(d_bts1day['datetime'],cfjson['variables']['lat']['data'], cfjson['variables']['lon']['data'])
    esd=sp.earth_sun_distance(d_bts1day['datetime'])

    """ write dict data to numpy array https://www.quora.com/Is-it-possible-to-convert-a-Python-set-and-dictionary-to-a-NumPy-array """
    np_datetime = np.array(list(d_bts1day["datetime"]))
    
    """ prepare time variable to store seconds since ... in netcdf file"""
    second_since = date2num(np_datetime, cfjson['variables']['time']['attributes']['units'])
    
    """ Create dictionary for connecting data """
    data={"lon":{"conf":"lon"},
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
    
    """ Introduce the size of the dimensions for each case"""        
    cfjson.setDim('time', len(d_bts1day['time']))
    cfjson.setDim('wvl', len(d_bts1day['wvl']) )
    
    """ add data to the variables """
    for key,value in data.items():
        for origin,name in value.items():
            # if origin=='conf':
            #     f[key][:]=config.get('STATION','station_'+name)
            # if origin=='conf':
                # print(key,cfjson['variables'][key]['data'])
                # f[key][:]=cfjson['variables'][name]['data']
            if origin=='bts':
                cfjson.setData(key,d_bts1day[name])
                # if key=='spec_irrad':
                #     f[key][:,:]=d_bts1day[name]
                #     continue
                # f[key][:]=d_bts1day[name]
            elif origin=='calculated':
                # f[key][:]=name
                cfjson.setData(key,name)
    """creating the netCDF file"""
    f = cf.create_file(nc_file, cfdict=cfjson)
    f.close()

    module_logger.info( 'Write data to netcdf: ' + nc_file )  
 
    
# """read netCDF"""
# nc = nc4.Dataset('/vols/satellite/home/bayer/uv/netCDF/2019/08/bts2048_uv_20190826_mp_l1_c1.nc','r')
# for i in nc.variables:
#     print(i,nc.variables[i] )#, nc.variables[i].units, nc.variables[i].shape)
#     print(nc.variables)
#     i=nc.variables[i][:]
#     #print(i)
# print(nc.history)
# print(nc.variables["uva_irrad"][:])
# print(nc)
    
# d_bts1day=bts.read_oro_bts('/vols/satellite/datasets/surfrad/uv_radiometer/raw/2019/08/26/MP190826.OR0','globals',20190826)
# nc = nc4.Dataset('/vols/satellite/home/bayer/uv/netCDF/2019/08/bts2048_uv_20190826_mp_l1_c1.nc','r')
# with open('/vols/satellite/home/bayer/uv/src/config/templates/uv_js_meta.json') as f:
#     cfjson= json.load(f)

        # # f[x].setncatts(cfjson['variables'][x]['attributes'])
        # if variable=='time':
        #     f[variable][:]= second_since
        # elif cfjson['variables'][variable]['shape']==['time']:
        #     f[variable][:]=d_bts1day[variable]
        # elif len(cfjson['variables'][variable]['shape'])==2:
        #     f[variable][:,:]=d_bts1day[variable]
        # elif cfjson['variables'][variable]['shape']==['wvl']:
        #     f[variable][:]=d_bts1day[variable]
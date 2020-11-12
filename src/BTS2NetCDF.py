#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 13:30:44 2019

@author: bayer
"""
import netCDF4 as nc4
from netCDF4 import date2num,num2date
import numpy as np
from datetime import datetime

def netCDF_file(d_bts1day,nc_file, cfjson ):

    # """checking if the file does already exist, and delete if so."""
    # if os.path.isfile(netCDF_path+i8date+'.nc'):
    #     os.remove(netCDF_path+i8date+'.nc')
    
    
    """ write dict data to numpy array https://www.quora.com/Is-it-possible-to-convert-a-Python-set-and-dictionary-to-a-NumPy-array """
    np_datetime = np.array(list(d_bts1day["datetime"]))
    
    """ prepare time variable to store seconds since ... in netcdf file"""
    second_since = date2num(np_datetime, cfjson['variables']['time']['attributes']['units'])
    
    
    """creating the netCDF file"""    
    f = nc4.Dataset(nc_file,'w', format='NETCDF4') #'w' stands for write 

    """Creating the dimensions in the NetCDF file from the JSON file"""
    for x,y in cfjson['dimensions'].items(): 
        f.createDimension(x,len(d_bts1day[x]))
        # print(f.dimensions)
    """Building variables    time = uv_grp.createVariable('Time', 'i4', 'time')"""
    for x in cfjson['variables']:
        f.createVariable(x,cfjson['variables'][x]['type'],(cfjson['variables'][x]['shape']),zlib=True,least_significant_digit=3)
        """Adding units to the variables"""
        # f[x].setncatts(cfjson['variables'][x]['attributes'])
        f[x].units=cfjson['variables'][x]['attributes']['units']
        if x=='time':
            f[x][:]= second_since
        elif cfjson['variables'][x]['shape']==['time']:
            f[x][:]=d_bts1day[x]
        elif len(cfjson['variables'][x]['shape'])==2:
            f[x][:,:]=d_bts1day[x]
    today = datetime.today()
    f.history = "Created " + today.strftime("%d/%m/%y")

    """adding attributer"""
    for x in cfjson['attributes']:
        setattr(f,x,cfjson['attributes'][x])
    f.close()

    
    print("%-21s: %-60s" %('Write data to netcdf', nc_file))
    
 
    
# """read netCDF"""
# nc = nc4.Dataset('/vols/satellite/home/bayer/uv/netCDF/20190701.nc','r')
# for i in nc.variables:
#     print(i,nc.variables[i] )#, nc.variables[i].units, nc.variables[i].shape)
#     print(nc.variables)
#     i=nc.variables[i][:]
#     #print(i)
# print(nc.history)
# print(nc.variables["uva"][:])
# print(nc)

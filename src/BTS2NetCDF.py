#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 13:30:44 2019

@author: bayer
"""
import netCDF4 as nc4
# import os
from datetime import datetime

def netCDF_file(d_bts1day,nc_file, cfjson ):

    # """checking if the file does already exist, and delete if so."""
    # if os.path.isfile(netCDF_path+i8date+'.nc'):
    #     os.remove(netCDF_path+i8date+'.nc')
    
    """creating the netCDF file"""    
    f = nc4.Dataset(nc_file,'w', format='NETCDF4') #'w' stands for write 

    """Creating the dimensions in the NetCDF file from the JSON file"""
    for x,y in cfjson['dimensions'].items(): 
        if y!=-1:
            f.createDimension(x,1)
        elif y==-1:
            f.createDimension(x,len(d_bts1day[x]))

    """Building variables    time = uv_grp.createVariable('Time', 'i4', 'time')"""
    for x in cfjson['variables']:
        f.createVariable(x,cfjson['variables'][x]['type'],cfjson['variables'][x]['shape'])
        """Adding units to the variables"""
        # f[x].setncatts(cfjson['variables'][x]['attributes'])
        f[x].units=cfjson['variables'][x]['attributes']['units']
        if len(cfjson['variables'][x]['shape'])<=2:
            """In case of "time" add data values from data dictionary"""
            """otherwise use data values from json file"""
            if x=='time':
                f[x][:]= d_bts1day[x]
            else:
                f[x][:]=cfjson['variables'][x]['data']
        elif len(cfjson['variables'][x]['shape'])==3:
            f[x][0,0,:]=d_bts1day[x]
        elif len(cfjson['variables'][x]['shape'])==4:
            f[x][0,0,:,:]=d_bts1day[x]   
    today = datetime.today()
    f.history = "Created " + today.strftime("%d/%m/%y")

    """adding attributer"""
    for x in cfjson['attributes']:
        setattr(f,x,cfjson['attributes'][x])
    f.close()
    
 
    
"""read netCDF"""
# nc = nc4.Dataset('/vols/satellite/home/bayer/uv/netCDF/20190101.nc','r')
# for i in nc.variables:
#     print(i, nc.variables[i].units, nc.variables[i].shape)
#     i=nc.variables[i][:]
#     print(i)
# print(nc.history)
# print(nc.variables)
# print(nc)

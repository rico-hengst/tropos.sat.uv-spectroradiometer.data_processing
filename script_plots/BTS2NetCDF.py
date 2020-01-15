#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 13:30:44 2019

@author: bayer
"""
import netCDF4 as nc4

def netCDF_file(d_bts1day,i8date,netCDF_path, cfjson ):
    
    """define the netCDF path where the file should be generated"""
    netCDF_path = "/vols/satellite/home/bayer/uv/netCDF/"
    file_out=netCDF_path+str(i8date[:]) + '.nc'
    f = nc4.Dataset(file_out,'w', format='NETCDF4') #'w' stands for write 
#    print(cfjson['dimensions'])
#    print(cfjson['dimensions'].values())
    """Creating the dimensions in the NetCDF file from the JSON file"""
    for x,y in cfjson['dimensions'].items(): 
        if y!=-1:
            f.createDimension(x,y)
        elif y==-1:
            f.createDimension(x,d_bts1day[x].size)

    """Building variables    time = uv_grp.createVariable('Time', 'i4', 'time')"""
#    print(cfjson['variables'].items())
    for x in cfjson['variables']:
        x=f.createVariable(x,cfjson['variables'][x]['type'],cfjson['variables'][x]['shape'])
        print(f.variables)
#        f[x].setncatts(cfjson['variables'][x]['attributes'])
#        for y in cfjson['variables'][x]:
        f[x].units=cfjson['variables'][x]['attributes']['units']
##        if hasattr(cfjson['variables'][x],'data'):
        if len(cfjson['variables'][x]['shape'])<=2:
            f[x][:]=cfjson['variables'][x]['data']
        elif len(cfjson['variables'][x]['shape'])==3:
            f[x][0,0,:]=d_bts1day[x]
        elif len(cfjson['variables'][x]['shape'])==4:
            f[x][0,0,:,:]=d_bts1day[x]   
    print(f)        
    exit() 
                
#            if y=='data':
#                x[:]=cfjson['variables'][x]['data']
#                print(cfjson['variabless'][x][y])
#                print(len(cfjson['variables'][x][y]))
#    if vars: 
#        for name,var in cfjson.items():
#            f.createVariable( name, cfjson.type, cfjson.shape)
#            if hasattr(var,'attributes'):
#                f[name].setncatts(cfjson.attributes)
#            if hasattr(var,'data'):
#                f[name][:] = cfjson.data            
#    """Passing data into variables"""
#    for x in cfjson['variables']:
#        for y in cfjson['variables'][x]:
##            if y=='shape':
##                if len(cfjson['variables'][x][y])==3:
##                    vars()[x]=d_bts1day[x]
##                    x.units=cfjson['variables'][x]['attributes']['units']
##                elif len(cfjson['variables'][x][y])==4:
##                    vars()[x]=d_bts1day[x]
##                    x.units=cfjson['variables'][x]['attributes']['units']
#            if y=='data':
#                print(cfjson['variables'][x]['attributes']['units'])
#                print(cfjson['variables'][x][y])
#                z=vars()[x]
#                print(z)
#                z[:]=cfjson['variables'][x][y]
#                z.units=cfjson['variables'][x]['attributes']['units']
##            if y=='attributes':
##                for z in cfjson['variables'][x][y]:
##                    if z=='units':
    
#    
#    for x,y in cfjson['variables'].items():
##        print(x)
##        print(y)
#        for z,a in y.items():
#            if z=='shape':
#                x=f.createVariable(x,'f4',(a))
#                print(f.variables)
#            if z=='data':
#                x[:]=a
#                print(x)
#             
##            print(z)
##            print(a)
##    print(cfjson['variables']['longitude']['type'])
#    exit ()
#    
#    for x in cfjson['variables']:
#        x=f.createVariable(x,cfjson['variables']['type'].values(),cfjson['variables']['shape'])
#        x.data[:]=d_bts1day[x]
#        print(f.variables)
#    f.createVariable('time','longitude','latitude','UVA','UVB','uvind','uvint',
#                          'spectrum','wavelength')    
#    for v in f.variables.keys():
#        if v in cfjson.variables:
#            f[v].setncatts(cfjson.variables[v].attributes)
#            if v in d_bts1day.variables:
#                v[:]=d_bts1day[v]
#            print(f.groups)
#            print(f.dimensions)
#            print(f.time)
    f.close()
    
    ###################This should be read from the json file ################
    """creat a group:
    A netCDF group is basically a directory or folder within the netCDF dataset. 
    This allows you to organize data as you would in a unix file system."""
#    uv_grp = f.createGroup('uv_radiometer_data')  
    
    """create dimensions"""
#    uv_grp.createDimension('lon', 1)
#    uv_grp.createDimension('lat', 1)
#    uv_grp.createDimension('time', d_bts1day["seconds"].size)
#    uv_grp.createDimension('wvl', d_bts1day["wvl"].size)
#            
    """Building variables"""
#    time = uv_grp.createVariable('Time', 'i4', 'time')
#    longitude = uv_grp.createVariable('Longitude', 'f4', 'lon')
#    latitude = uv_grp.createVariable('Latitude', 'f4', 'lat') 
#    UVA=uv_grp.createVariable('UVA','f4',('time', 'lon', 'lat'))
#    UVB=uv_grp.createVariable('UVB','f4',('time', 'lon', 'lat'))
#    uvind=uv_grp.createVariable('uvind','f4',('time', 'lon', 'lat'))
#    uvint=uv_grp.createVariable('uint','f4',('time', 'lon', 'lat'))
#    spectrum=uv_grp.createVariable('spectrum','f4',('wvl','time','lon','lat'))
#    wavelength = uv_grp.createVariable('wvl', 'f4', ('wvl','lon','lat'))
#    print(f)
#    print(uv_grp)
#
    """Passing data into variables"""
#    longitude[:]=12.928 
#    latitude[:]=51.526 
#    UVA[:,0,0]=d_bts1day["uva"]
#    UVB[:,0,0]=d_bts1day["uvb"]
#    uvind[:,0,0]=d_bts1day["uvind"]
#    uvint[:,0,0]=d_bts1day["uvint"]
#    wavelength[:,0,0]=d_bts1day["wvl"]
#    spectrum[:,:,0,0]=d_bts1day["spect"]
#    time[:]=d_bts1day["seconds"]
#    
    """adding comments and units"""
#    f.height='80m above see level'
#    today = datetime.today()
#    f.history = "Created " + today.strftime("%d/%m/%y")
#    time.units = 'in UT seconds from zero hours on day given by DATE'
#    UVA.units = 'mW/m²'
#    UVB.units = 'mW/m²'
#    uvind.warning = 'This index depends only on the wavelength!'
#    ###########################################################################
    


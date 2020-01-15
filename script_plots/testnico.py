#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 11:46:17 2019

@author: bayer
"""
import os
import read_bts2048rh as bts
import calendar
import netCDF4 as nc4
from datetime import datetime
import read_bts2048rh as bts
import BTS2plot
import BTS2NetCDF 
import json
i8date = '20190520'
f8date= '20190520'   
# i8date = 20190623
iyear=i8date[0:4]
iy=int(iyear)
imonth=i8date[4:6]
im=int(imonth)
iday=i8date[6:8]
ida=int(iday)
fyear=f8date[0:4]
fy=int(fyear)
fmonth=f8date[4:6]
fm=int(fmonth)
fday=f8date[6:8]
fda=int(fday)

    
"""Define the main path where the files are in"""   
main_path="/vols/satellite/datasets/surfrad/uv_radiometer/"
    
"""Define the main path where the images should be saved"""
image_path="/vols/satellite/home/bayer/uv/images/"
    
"""Define the main path where the netCDF files should be saved"""
netCDF_path = "/vols/satellite/home/bayer/uv/netCDF/"
    
"""Define the JSON path where the json metadata file should be saved"""
json_file = '/vols/satellite/home/bayer/uv/uv_js_meta.json'    
with open(json_file) as f:
    cfjson= json.load(f)
d={'t':[1,5,9,4], 'var':[85 ,32,98,31]}
print(d['t'])
    
################################################################################ 
    
methodbts = "global" 
main_path="/vols/satellite/datasets/surfrad/uv_radiometer/"    
image_path="/vols/satellite/home/bayer/uv/images/"
for ys in range(iy,fy+1):
    for imonth in range(1,13):
        if ys==iy and imonth<im:
            continue
        elif ys==fy and imonth>fm:
            break
        else:
            numberOfDays = calendar.monthrange(ys, imonth)[1]
            for iday in range(1,numberOfDays+2):
                if iday<ida:
                    iday=iday+1
                elif iday==numberOfDays+1 and imonth<=11:
                    imonth=imonth+1
                    ida=1
                elif iday==numberOfDays+1 and imonth==12:
                    imonth=1
                    ida=1
                    ys=ys+1
                elif imonth==fm and ys==fy and iday>fda:
                    break
                elif iday>=ida and iday<=numberOfDays:
                    path_file=main_path+str(ys)+"/"+str(imonth).zfill(2)+"/"+str(iday).zfill(2)+"/"+"MP"+str(ys-2000).zfill(2)+str(imonth).zfill(2)+str(iday).zfill(2)+".OR0"
                    if os.path.isfile(path_file):
                        if os.stat(path_file).st_size<1:
                            print('file is empty '+path_file)
                            iday=iday+1
                        else:
                            i8date=str(ys)+str(imonth).zfill(2)+str(iday).zfill(2)
                            #Obtanin the directory data from the OR0 files
                            d_bts1day=bts.read_oro_bts(path_file,methodbts,i8date)
                            #Ploting function
                            #plotme.plotme(d_bts1day,i8date,image_path)
                            iday=iday+1
                    else:
                        print(path_file+" does not exist")
                        iday=iday+1
 

"""define the netCDF path where the file should be generated"""
netCDF_path = "/vols/satellite/home/bayer/uv/netCDF/"

"""checking if the file does already exist, and delete if so."""
if os.path.isfile('test5.nc'):
    os.remove('test5.nc')
    
"""creating the netCDF file"""    
f = nc4.Dataset('test5.nc','w', format='NETCDF4') #'w' stands for write 

"""Creating the dimensions in the NetCDF file from the JSON file"""
for x,y in cfjson['dimensions'].items(): 
    if y!=-1:
        f.createDimension(x,1)
    elif y==-1:
        f.createDimension(x,len(d_bts1day[x]))
#print(f.dimensions)

"""Building variables    time = uv_grp.createVariable('Time', 'i4', 'time')"""
for x in cfjson['variables']:
    f.createVariable(x,cfjson['variables'][x]['type'],cfjson['variables'][x]['shape'])
    """Adding units to the variables"""
    # f[x].setncatts(cfjson['variables'][x]['attributes'])
    f[x].units=cfjson['variables'][x]['attributes']['units']
    if len(cfjson['variables'][x]['shape'])<=2:
        f[x][:]=cfjson['variables'][x]['data']
    elif len(cfjson['variables'][x]['shape'])==3:
        f[x][0,0,:]=d_bts1day[x]
    elif len(cfjson['variables'][x]['shape'])==4:
        f[x][0,0,:,:]=d_bts1day[x]   
today = datetime.today()
f.history = "Created " + today.strftime("%d/%m/%y")
print(f['latitude'].attributes)
#    print(cfjson['variables'].items())
#    print(cfjson['variables'][x],cfjson['variables'][x]['shape'])
print(f.variables)
#        for y in cfjson['variables'][x]:
##        if hasattr(cfjson['variables'][x],'data'):
#print(x)
#f.height='80m above see level'
#print(f)   
#print(f.variables)        

f.variables.keys()
lon = f.variables['longitude'][:]
lat = f.variables['latitude'][:]
print(lat[:])
uva= f.variables['uva'][:]
spect=f.variables['spect'][:]

print(spect[0,0,:,500])
exit()     






















                                               
#
#"""define the netCDF path where the file should be generated"""
#netCDF_path = "/home/bayer/uv/netCDF/"
#file_out=netCDF_path+str(i8date[:]) + '.nc'
#f = nc4.Dataset(file_out,'w', format='NETCDF4') #'w' stands for write
#print(f.data_model)    
#
#    
#"""creat a group:
#A netCDF group is basically a directory or folder within the netCDF dataset. 
#This allows you to organize data as you would in a unix file system."""
#uv_grp = f.createGroup('uv_radiometer_data')
#    
#
#"""create dimensions"""
#uv_grp.createDimension('lon', 1)
#uv_grp.createDimension('lat', 1)
#uv_grp.createDimension('time', d_bts1day["seconds"].size)
#
#"""Building variables"""
#time = uv_grp.createVariable('Time', 'i4', 'time')
#longitude = uv_grp.createVariable('Longitude', 'f4', 'lon')
#latitude = uv_grp.createVariable('Latitude', 'f4', 'lat') 
#UVA=uv_grp.createVariable('UVA','f4',('time', 'lon', 'lat'))
#UVB=uv_grp.createVariable('UVB','f4',('time', 'lon', 'lat'))
#uvind=uv_grp.createVariable('uvind','f4',('time', 'lon', 'lat'))
#uvint=uv_grp.createVariable('uint','f4',('time', 'lon', 'lat'))
#
##wvl=uv_grp.createVariable('wvl','f4',('time', 'lon', 'lat'))
#print(f)
#print(uv_grp)
#
#"""Passing data into variables"""
#longitude=12.928 
#latitude=51.526 
#UVA[:,0,0]=d_bts1day["uva"]
#UVB[:,0,0]=d_bts1day["uvb"]
#uvind[:,0,0]=d_bts1day["uvind"]
#uvint[:,0,0]=d_bts1day["uvint"]
#
#f.height='80m above see level'
#today = datetime.today()
#f.history = "Created " + today.strftime("%d/%m/%y")
#time.units = 'in UT seconds from zero hours on day given by DATE'
#UVA.units = 'mW/m²'
#UVB.units = 'mW/m²'
#uvind.warning = 'This index depends only on the wavelength!'
#
#f.close()
#
#"""To Read the netCDF file
#f = nc4.Dataset(file_out,'r') #opens the file for reading
#uv_grp = f.groups['uv_radiometer_data']
#print(uv_grp.variables['uvind']) #print "meta data for uvind variable
#uv_grp.variables.keys()  #prints the variables in the uv_grp group
#wvl = uv_grp.variables['wvl'][:] #saves the data from the file in a new variable UVB
#spectrum = uv_grp.variables['spectrum'][:]
#"""

#file_out = "MP"+str(i8date[2:4]).zfill(2)+str(i8date[4:6]).zfill(2)+str(i8date[6:8]).zfill(2)+".nc"

#uv_grp.createDimension('datetime', d_bts1day["datetime"].size)  
#uv_grp.createDimension('info', d_bts1day["info"].size)
#uv_grp.createDimension('seconds', d_bts1day["seconds"].size)
#uv_grp.createDimension('spect', d_bts1day["spect"].size)
#uv_grp.createDimension('time', d_bts1day["time"].size)
#uv_grp.createDimension('UVA', d_bts1day["uva"].size)
#uv_grp.createDimension('UVB', d_bts1day["uvb"].size)
#uv_grp.createDimension('uvind', d_bts1day["uvind"].size)
#uv_grp.createDimension('uvint', d_bts1day["uvint"].size)
#uv_grp.createDimension('wvl', d_bts1day["wvl"].size)

#datetime=uv_grp.createVariable('datetime','f8','datetime')
#info=uv_grp.createVariable('info','f4','info')
#seconds=uv_grp.createVariable('seconds','f4','seconds')
#spect=uv_grp.createVariable('spect','f4','spect')
#time=uv_grp.createVariable('time','f4','time')
#UVA=uv_grp.createVariable('UVA','f4',('time', 'lon', 'lat'))
#UVB=uv_grp.createVariable('UVB','f4',('time', 'lon', 'lat'))
#uvind=uv_grp.createVariable('uvind','f4','uvind')
#uvint=uv_grp.createVariable('uint','f4','uint')
#wvl=uv_grp.createVariable('wvl','f4','wvl')

#datetime[:]=d_bts1day["datetime"]
#info[:]=d_bts1day["info"]
#seconds[:]= d_bts1day["seconds"]
#time[:]=d_bts1day["time"]
#spect[:]= d_bts1day["spect"]
#wvl[:,0,0]=d_bts1day["wvl"]


#file_out=netCDF_path+str(i8date[0:4])+"/"+str(i8date[4:6]).zfill(2)+"/"+str(i8date[6:8]).zfill(2)+"/"+"MP"+str(i8date[2:4]).zfill(2)+str(i8date[4:6]).zfill(2)+str(i8date[6:8]).zfill(2)+".nc"



#netCDF_path = "/home/bayer/uv/netCDF/"
#file_name=netCDF_path+str(i8date[0:4])+"/"+str(i8date[4:6]).zfill(2)+"/"+str(i8date[6:8]).zfill(2)+"/"+str(i8date[:]) + '.nc'
#
#ds = xr.Dataset({'datetime': (['time','sx', 'sy'],  d_bts1day["datetime"]),
#                     'info': (['time','sx', 'sy'], d_bts1day["info"]),
#                     'seconds': (['time','sx', 'sy'],  d_bts1day["seconds"]),
#                     'spect': (['time','sx', 'sy'], d_bts1day["spect"]),
#                     'time': (['time','sx', 'sy'],  d_bts1day["time"]),
#                     'UVA': (['time','sx', 'sy'], d_bts1day["UVA"]),
#                     'UVB': (['time','sx', 'sy'],  d_bts1day["UVB"]),
#                     'uvind': (['time','sx', 'sy'],  d_bts1day["uvind"]),
#                     'uvint': (['time','sx', 'sy'],  d_bts1day["uvint"]),
#                     'wvl': (['time','sx', 'sy'], d_bts1day["wvl"])})

#ds.to_netcdf(file_name)

#ds.attrs['title'] = "UV radiometer Melpitz messurements."
#ds.attrs['institution'] = "Leibniz Institute for Tropospheric Research"      

#ORIGINAL LOOP
###############
#for ys in range(iy,fy+1):
#    for imonth in range(1,13):
#        if ys==iy and imonth<im:
#            continue
#        elif ys==fy and imonth>fm:
#            break
#        else:
#            numberOfDays = calendar.monthrange(ys, imonth)[1]
#            for iday in range(1,numberOfDays+1):
#                if iday<ida:
#                    continue
#                elif iday>=ida and iday<=numberOfDays:
#                    path_file=main_path+str(ys)+"/"+str(imonth).zfill(2)+"/"+str(iday).zfill(2)+"/"+"MP"+str(ys-2000).zfill(2)+str(imonth).zfill(2)+str(iday).zfill(2)+".OR0"
#                    if os.path.isfile(path_file):
#                        if os.stat(path_file).st_size<1:
#                            print('file is empty '+path_file)
#                            iday=iday+1
#                        else:
#                            i8date=str(ys)+str(imonth).zfill(2)+str(iday).zfill(2)
#                            #Obtanin the directory data from the OR0 files
#                            d_bts1day=bts.read_oro_bts(path_file,methodbts,i8date)
#                            #Ploting function
#                            plotme.plotme(d_bts1day,i8date,image_path)
#                            iday=iday+1
#                    else:
#                        print(path_file+" does not exist")
#                        iday=iday+1
#                elif imonth==im and ys==fy and iday>fda:
#                    break
#                    
#                    
#                    
#                    
#for iy in range(iy,fy+1):
#    if iy!=fy:
#        path = main_path + str(iy) + "/"
#        for im in range(im,14):
#            path1=path+str(im).zfill(2)+"/"
#            if im<=12:   
#                numberOfDays = calendar.monthrange(iy, im)[1]
#                for ida in range(ida,numberOfDays + 2):
#                    if ida<=numberOfDays:
#                        path2 = path1 + str(ida).zfill(2) + "/"
#                        path_file=path2+"MP"+str(iy-2000).zfill(2)+str(im).zfill(2)+str(ida).zfill(2)+".OR0"
#                        if os.path.isfile(path_file):
#                            i8date=str(iy)+str(im).zfill(2)+str(ida).zfill(2)
#                            d_bts1day=bts.read_oro_bts(path_file,methodbts,i8date)
#                            plotme.plotme(d_bts1day,i8date,image_path)
#                            ida=ida+1
#                        else:
#                            ida=ida+1
#                            print(path_file+" does not exist")
#                    elif ida==numberOfDays + 1:   
#                        ida=1   
#                        im=im+1
#                        path1 = path + str(im).zfill(2) + "/"
#            elif im==13:
#                im=1
#                iy=iy+1 
#                path = main_path + str(iy) + "/"
#    elif iy==fy:
#        path = main_path + str(iy) + "/"
#        for im in range(im,fm+1):
#            path1 = path + str(im).zfill(2) + "/"
#            if im<fm:
#                numberOfDays = calendar.monthrange(iy, im)[1]
#                for ida in range(ida,numberOfDays + 2):
#                    path2=path1+str(ida).zfill(2)+"/"
#                    if ida<=numberOfDays:
#                        path_file=path2+"MP"+str(iy-2000).zfill(2)+str(im).zfill(2)+str(ida).zfill(2)+".OR0"
#                        if os.path.isfile(path_file):
#                            i8date=str(iy)+str(im).zfill(2)+str(ida).zfill(2)
#                            d_bts1day=bts.read_oro_bts(path_file,methodbts,i8date)
#                            plotme.plotme(d_bts1day,i8date,image_path)
#                            ida=ida+1
#                        else:
#                            ida=ida+1
#                            print(path_file+" does not exist")
#                    elif ida==numberOfDays + 1:   
#                        ida=1   
#                        im=im+1
#                        path1 = path + str(im).zfill(2) + "/"    
#            elif im==fm:
#                path1 = path + str(im).zfill(2) + "/"
#                for ida in range(ida,fda+1):
#                    path2= path1 + str(ida).zfill(2) + "/"
#                    path_file=path2+"MP"+str(iy-2000).zfill(2)+str(im).zfill(2)+str(ida).zfill(2)+".OR0"
#                    if os.path.isfile(path_file):
#                        i8date=str(iy)+str(im).zfill(2)+str(ida).zfill(2)
#                        d_bts1day=bts.read_oro_bts(path_file,methodbts,i8date)
#                        plotme.plotme(d_bts1day,i8date,image_path)
#                        ida=ida+1
#                    else:
#                        ida=ida+1 
#                        print(path_file+" does not exist")                     
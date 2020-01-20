#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 12:59:26 2019

@author: bayer

__author__ = "Nicolas Bayer"
__maintainer__ = "Nicolas Bayer"
__email__ = "bayer@tropos.de"
__status__ = "Production"
"""
import os
import read_bts2048rh as bts
import BTS2plot
import calendar
import BTS2NetCDF 
import argparse
import json
import configparser

"""Insert de initial and final dates as strings as 20190107(year:2019/month:01/day:07)"""

"""for calling the function from the terminal"""
parser = argparse.ArgumentParser(description='Process UVradiometer Messurments in Melpitz.') 
parser.add_argument('-s', type=str, dest='id', # la variable se guarda en args.id como string
                    help='Insert the initial date as 20190107(y:2019 m:01 d:07)')
parser.add_argument('-e', type=str, dest='fd',
                    help='Insert the final date as 20190107(y:2019 m:01 d:07)')
args = parser.parse_args()

"""Break in case the dates weren't correct"""
if len(args.id)!=8 or len(args.fd)!=8:
    print('Error: Wrong date introduced, please try again')
    exit()
if int(args.id)>int(args.fd):
    print('Error: Wrong dates were chosen/ pay attention to the order, please try again.')
    exit()

def statistic(i8date,f8date):
    methodbts = "global" 
    iy=int(i8date[0:4])
    im=int(i8date[4:6])
    ida=int(i8date[6:8])
    fy=int(f8date[0:4])
    fm=int(f8date[4:6])
    fda=int(f8date[6:8])
    
    
    """Read config file"""
    config = configparser.ConfigParser()
    config.read('config.private')
    
    
    """Check if directories etc exists"""
    if not os.path.isdir( config.get('DEFAULT','main_path') ):
        print('Path main_path not exists '+ config.get('DEFAULT','main_path'))
        quit()
        
    if not os.path.isdir( config.get('DEFAULT','image_path') ):
        print('Path image_path not exists '+ config.get('DEFAULT','image_path'))
        quit()
        
    if not os.path.isdir( config.get('DEFAULT','netCDF_path') ):
        print('Path netcdf_path not exists '+ config.get('DEFAULT','netCDF_path'))
        quit()
        
    if not os.path.isfile( config.get('DEFAULT','json_file') ):
        print('File json not exists '+ config.get('DEFAULT','json_file'))
        quit()
    
    #quit()
    
    '''
    """Define the main path where the files are in"""
    main_path="/vols/satellite/datasets/surfrad/uv_radiometer/"
    
    """Define the main path where the images should be saved"""
    image_path="/vols/satellite/home/hengst/BT/images/"
    
    """Define the main path where the netCDF files should be saved"""
    netCDF_path = "/vols/satellite/home/hengst/BT/netcdf/"
    
    """Define the JSON path where the json metadata are located"""
    json_file = '/vols/satellite/home/hengst/scripte/python/sat-uv-spectroradiometer.data_processing/uv_js_meta.json'
    '''
    
    
    """Load content of json_file to python variable cfjson"""
    cfjson={}
    with open( config.get('DEFAULT','json_file') ) as f:
            cfjson= json.load(f)
        
    """Start the loop"""
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
                        """Compose PathFileName of OR0-File"""
                        path_file = config.get('DEFAULT','main_path') + \
                            str(ys) + "/" + str(imonth).zfill(2) + "/" + str(iday).zfill(2) + "/" + \
                            "MP" +str(ys-2000).zfill(2) + str(imonth).zfill(2) + str(iday).zfill(2) + ".OR0"
                        if os.path.isfile(path_file):  # see if the .OR0 file exist
                            if os.stat(path_file).st_size<1:  # controls if the file is not empty
                                print('file is empty '+path_file)
                                iday=iday+1
                            else:
                                i8date=str(ys)+str(imonth).zfill(2)+str(iday).zfill(2)
                                """Obtanin the directory data from the OR0 files"""
                                d_bts1day=bts.read_oro_bts(path_file,methodbts,i8date)
                                """Ploting function"""
                                BTS2plot.plotme(d_bts1day,i8date,config.get('DEFAULT','image_path'))
                                """checking if the file does already exist, and delete if so."""
                                nc_file = config.get('DEFAULT','netCDF_path') + str(i8date[:]) + '.nc'
                                if os.path.isfile(nc_file):
                                    os.remove(nc_file)
                                    BTS2NetCDF.netCDF_file(d_bts1day,nc_file,cfjson) 
                                else:
                                    """Save the data processed by the bts function in a netCDF file"""
                                    BTS2NetCDF.netCDF_file(d_bts1day,nc_file,cfjson) 
                                iday=iday+1
                        else:
                            print(path_file+" does not exist")
                            iday=iday+1
    
#####################################################################################                                                            
statistic(args.id,args.fd)

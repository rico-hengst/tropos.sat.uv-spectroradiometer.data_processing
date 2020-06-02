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
#import Submodule/PlotHeatmap as plthtmp
from Submodule import PlotHeatmap as plthtmp
import BTS2NetCDF 
import argparse
import json
import configparser
import platform
import pandas as pd
"""Insert de initial and final dates as strings as 20190107(year:2019/month:01/day:07)"""

"""for calling the function from the terminal"""
parser = argparse.ArgumentParser(description='Process UVradiometer Messurments in Melpitz.') 
parser.add_argument('-s', type=str, dest='id', # la variable se guarda en args.id como string
                    help='Insert the initial date as 20190107(y:2019 m:01 d:07)')
parser.add_argument('-e', type=str, dest='fd',
                    help='Insert the final date as 20190107(y:2019 m:01 d:07)')
parser.add_argument('-i', '--image', action='store_true', 
                    help="create images files")
parser.add_argument('-n', '--netcdf', action='store_true', 
                    help="create netCDF files")
parser.add_argument('-st', '--statistics', action='store_true', 
                    help="create statistics of missing files")
args = parser.parse_args()


"""Break in case the dates weren't correct"""
if len(args.id)!=8 or len(args.fd)!=8:
    print('Error: Wrong date introduced, please try again')
    exit()
if int(args.id)>int(args.fd):
    print('Error: Wrong dates were chosen/ pay attention to the order, please try again.')
    exit()
    
"""Check python version"""
python_version = platform.python_version().split(".")
if int(python_version[0]) < 3:
  print("Your python version is: " + platform.python_version() )
  print("Script will be terminated cause python version < 3 is required !")
  exit()

def statistic(i8date,f8date):
    methodbts = "global" 
   
    """Read config file"""
    config = configparser.ConfigParser()
    
    config.read('config.private')
    
    """Read private config file"""
    if not os.path.isfile( 'config.private' ):
        print('File config.private not exists, use DEFAULT config instead!')
    else:
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


#    print(config.get('DEFAULT', 'station_prefix')+'test')
#    if config.get('DEFAULT','station_prefix') is None:
#       print('Station prefix not exists ')
#        quit()

#    if not os.path.exists( config.get('DEFAULT','station_prefix') ):
#        print('Station prefix not exists '+ config.get('DEFAULT','station_prefix'))
#        quit()
        
    """Load content of json_file to python variable cfjson"""
    cfjson={}
    with open( config.get('DEFAULT','json_file') ) as f:
            cfjson= json.load(f)
    
    
    # a lookup value dict for missing files
    dict_lookup_missing_value = {
        "file_not_exists": 1,
        "file_empty": 0.8,
        "file_less_than_1mb": 0.3,
        "file_size_ok" : 0
    }
    
    
    # add dataframe to plot missing files
    df = pd.DataFrame({'date' : [], 'missing file' : [] })
    
    """pandas time counter vector instead of loop"""
    dates=pd.date_range(args.id, args.fd,freq='1D', name=str, normalize=False) 
    # pd.to_numeric(dates.str.replace('-',''))
    for day in dates:
        """Compose PathFileName of OR0-File"""
        path_file = config.get('DEFAULT','main_path') + day.strftime('%Y')+ "/" +day.strftime('%m')+ \
                        "/" +day.strftime('%d')+ "/" + config.get('STATION','station_prefix') + \
                        day.strftime('%y').zfill(2)+day.strftime('%m')+ day.strftime('%d')+".OR0"
        if os.path.isfile(path_file):  # see if the .OR0 file exist
            if os.stat(path_file).st_size<1:  # controls if the file is not empty
                print('file is empty '+path_file)
                if args.statistics:
                    df = df.append({'date': day.date(), 'missing file' : dict_lookup_missing_value["file_empty"]}, ignore_index=True)
            else:
                if args.statistics:
                    if os.stat(path_file).st_size<1048576:  # controls if the file is less than 1mb
                        df = df.append({'date': day.date(), 'missing file' : dict_lookup_missing_value["file_less_than_1mb"]}, ignore_index=True)
                    else:
                        df = df.append({'date': day.date(), 'missing file' : dict_lookup_missing_value["file_size_ok"]}, ignore_index=True)
                """Obtanin the directory data from the OR0 files"""
                if args.image or args.netcdf:
                    d_bts1day=bts.read_oro_bts(path_file,methodbts,day.strftime('%Y%m%d'))
                    if args.image:
                        """Ploting function"""
                        BTS2plot.plotme(d_bts1day,day.strftime('%Y%m%d'),config.get('DEFAULT','image_path'))
                    if args.netcdf:
                        """checking if the file does already exist, and delete if so."""
                        nc_file = config.get('DEFAULT','netCDF_path') + day.strftime('%Y%m%d') + '.nc'
                        if os.path.isfile(nc_file):
                            os.remove(nc_file)
                            BTS2NetCDF.netCDF_file(d_bts1day,nc_file,cfjson) 
                        else:
                            """Save the data processed by the bts function in a netCDF file"""
                            BTS2NetCDF.netCDF_file(d_bts1day,nc_file,cfjson) 
        else:
            print("file not exist "+path_file)
            if args.statistics:
                df = df.append({'date': day.date(), 'missing file' : dict_lookup_missing_value["file_not_exists"]}, ignore_index=True)
        # plot statistics
        if (args.statistics):
            # generate filename
            picture_filename = \
                config.get('DEFAULT','image_path') + 'MissingFiles_' + \
                str( df['date'][0].strftime('%Y-%m-%d') ) + \
                '_' + \
                str(df['date'][len(df.index)-1].strftime('%Y-%m-%d') )
                
            # plot first or second half of year
            if (day.strftime('%m%d')=='0630' or day.strftime('%-m%d')=='1231'):
                print('Plot ' + picture_filename )
                
                # transform column date to datetime
                df['date'] =  pd.to_datetime(df['date'])
                
                plthtmp.main(
                    {
                    'data_import_type' : 'DataFrame',
                    'picture_filename' : picture_filename,
                    'DataFrame' : df
                    }
                )
                
                # init new dataframe
                df = pd.DataFrame({'date' : [], 'missing file' : [] })
                
            # plot period after the last half year
            elif (day.strftime('%Y%m%d') == f8date):
                print('Plot short period: ' + picture_filename )
                    
                # transform column date to datetime
                df['date'] =  pd.to_datetime(df['date'])
                
                plthtmp.main(
                    {
                    'data_import_type' : 'DataFrame',
                    'picture_filename' : picture_filename,
                    'DataFrame' : df
                    }
                )

#####################################################################################                                                            
statistic(args.id,args.fd)




















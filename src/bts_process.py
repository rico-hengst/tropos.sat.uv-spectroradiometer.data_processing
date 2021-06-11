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
import sys
import argparse
import configparser
import platform
import pandas as pd
import xarray as xr
import logging
from copy import deepcopy
from trosat import cfconv as cf

try:
    from tropos_uv import read_bts2048rh as bts_read
except:
    print("imoprt local read_bts2048rh") 
    import read_bts2048rh as bts_read

    
try: 
    from tropos_uv import bts2plot
except:
    print("import local bts2plot")
    import bts2plot
    

try: 
    
    from tropos_uv import bts2netCDF
except:
    print("import local bts2netCDF")
    import bts2netCDF
    

try: 
    from tropos_uv import get_config
except:
    print("import local get_config")
    import get_config
    

    





    

def loop(args, config, logger):
    methodbts = "global" 


    """Check if directories etc exists"""
    if not os.path.isdir( config.get('PATHFILE','main_path') ):
        logger.error('Path main_path not exists '+ config.get('PATHFILE','main_path'))
        quit()
        
    if not os.path.isdir( config.get('PATHFILE','image_path') ):
        logger.error('Path image_path not exists '+ config.get('PATHFILE','image_path'))
        quit()
        
    if not os.path.isdir( config.get('PATHFILE','netCDF_path') ):
        logger.error('Path netcdf_path not exists '+ config.get('PATHFILE','netCDF_path'))
        quit()


    """Check if directories are writable"""
    if args.netcdf:
        if not os.access(config.get('PATHFILE','netCDF_path'), os.W_OK):
            logger.error('Path netCDF_path not writable '+ config.get('PATHFILE','netCDF_path'))
            quit()
    
    if args.netcdf or args.image:
        if not os.access(config.get('PATHFILE','image_path'), os.W_OK):
            logger.error('Path image_path not writable '+ config.get('PATHFILE','image_path'))
            quit()    
        
   
    """Load content of json_file to python variable cfjson"""
    cfjson=cf.read_cfjson(args.jsonfile)
    # {}
    # with open( json_file ) as f:
    #         cfjson= json.load(f)
    
    
    """ a lookup value dict for missing files"""
    dict_lookup_missing_value = {
        "file_not_exists": 1,
        "file_empty": 0.8,
        "file_less_than_1mb": 0.3,
        "file_size_ok" : 0
    }
    
    
    """add dataframe to plot missing files"""
    missing_files_key_name = "missing data"
    df = pd.DataFrame({'date' : [], missing_files_key_name : [] })
    
    """pandas time counter vector instead of loop"""    
    dates=pd.date_range(args.id, args.fd,freq='1D', name=str, normalize=False) 

    # pd.to_numeric(dates.str.replace('-',''))
    for date in dates:
        
        """Compose PathFileName of or0-File"""
        or0_file = config.get('STATION','station_prefix') + \
                        date.strftime('%y').zfill(2)+date.strftime('%m')+ date.strftime('%d')+".OR0"
        path_file = ""
        
        
        """path_file is dependent on the main_path_tree"""
        if (config.get('PATHFILE','main_path_tree') == 'flat') :
            path_file = config.get('PATHFILE','main_path') + or0_file
        elif (config.get('PATHFILE','main_path_tree') == 'yyyy/mm/dd/') :
            path_file = config.get('PATHFILE','main_path') + date.strftime('%Y/%m/%d/') + or0_file
            
        
        """Compose PathFileName of image-File and add to config to use in plot module"""
        image_path_file = config.get('PATHFILE','image_path') + eval( config.get('PATHFILE','image_subpath_file_regex') )
        config.set("PATHFILE", "image_path_file", image_path_file)
        
        
        """Compose PathFileName of netcdf-File and add to config"""        
        netcdf_path_file = config.get('PATHFILE','netcdf_path') + eval( config.get('PATHFILE','netcdf_subpath_file_regex') )
        config.set("PATHFILE", "netcdf_path_file", netcdf_path_file)


        """check file exists"""
        if os.path.isfile(path_file):  # see if the .OR0 file exist
            if os.stat(path_file).st_size<1:  # controls if the file is not empty
                logger.warn('file is empty '+path_file)
                if args.statistics:
                    df = df.append({'date': date.date(), missing_files_key_name : dict_lookup_missing_value["file_empty"]}, ignore_index=True)
            else:
                if args.statistics:
                    if os.stat(path_file).st_size<1048576:  # controls if the file is less than 1mb
                        df = df.append({'date': date.date(), missing_files_key_name : dict_lookup_missing_value["file_less_than_1mb"]}, ignore_index=True)
                    else:
                        df = df.append({'date': date.date(), missing_files_key_name : dict_lookup_missing_value["file_size_ok"]}, ignore_index=True)
                        
                """Check if netcdf (sub)directory exists"""
                if args.netcdf or args.image:
                    
                    """checking if the directory already exists, create subdir"""
                    if not os.path.isdir( os.path.dirname(netcdf_path_file) ):
                        os.makedirs( os.path.dirname(netcdf_path_file) )
                        logger.info('Create directory     : ' + os.path.dirname(netcdf_path_file) )
                
                """Obtanin the directory data from the OR0 files"""
                if args.netcdf:
                    d_bts1day=bts_read.read_oro_bts(path_file,methodbts,date.strftime('%Y%m%d'))
                    if args.netcdf:
                        
                        """checking if the file does already exist, and delete if so."""
                        if os.path.isfile( netcdf_path_file ):
                            os.remove( netcdf_path_file )
                            bts2netCDF.netCDF_file(d_bts1day,netcdf_path_file,cfjson,config) 
                        else:
                            """Save the data processed by the bts function in a netCDF file"""
                            bts2netCDF.netCDF_file(d_bts1day,netcdf_path_file,cfjson,config)
                
                if args.image:
                    """checking if the file does already exist"""
                    """ If it exist, opens data in xarray.
                        If not, creates netCDF file and load data in xarray"""
                    if os.path.isfile( netcdf_path_file ):
                        nc=xr.open_dataset( netcdf_path_file )
                    else:
                        d_bts1day=bts_read.read_oro_bts(path_file,methodbts,date.strftime('%Y%m%d')) 
                        bts2netCDF.netCDF_file(d_bts1day,netcdf_path_file,cfjson,config)
                        nc=xr.open_dataset(netcdf_path_file)
                    
                    """Plotting data"""
                    bts2plot.plotme(nc,date,config)
                    

        else:
            logger.error("File not exist "+ path_file)
            if args.statistics:
                df = df.append({'date': date.date(), missing_files_key_name : dict_lookup_missing_value["file_not_exists"]}, ignore_index=True)
        
        """plot statistics"""
        if (args.statistics):
            """generate filename"""
            picture_filename = \
                config.get('PATHFILE','image_path') + config.get('STATION','station_prefix') + '_' + \
                str( df['date'][0].strftime('%Y%m%d') ) + \
                '_' + \
                str(df['date'][len(df.index)-1].strftime('%Y%m%d') ) + \
                '_missing_data'
                
            """plot first or second half of year"""
            if (date.strftime('%m%d')=='0630' or date.strftime('%-m%d')=='1231'):
                logger.info('Plot ' + picture_filename )
                
                """transform column date to datetime"""
                df['date'] =  pd.to_datetime(df['date'])
                
                plthtmp.main(
                    {
                    'data_import_type' : 'DataFrame',
                    'picture_filename' : picture_filename,
                    'DataFrame' : df
                    }
                )
                
                """init new dataframe"""
                df = pd.DataFrame({'date' : [], missing_files_key_name : [] })
                
            #plot period after the last half year
            elif (date.strftime('%Y%m%d') == args.fd):
                logger.info('Plot short period: ' + picture_filename )
                    
                # transform column date to datetime
                df['date'] =  pd.to_datetime(df['date'])
                
                plthtmp.main(
                    {
                    'data_import_type' : 'DataFrame',
                    'picture_filename' : picture_filename,
                    'DataFrame' : df
                    }
                )
    logger.info('End uv-processing')

#####################################################################################        



#####################################################################################                                                    
# getting args, setting logger, load configs
def adjust(argv):
    
    # get name of directory where main script is located
    current_dirname = os.path.dirname(os.path.realpath(__file__))
    
    # get the name of the directory from where the script was executed
    exec_dirname = os.getcwd()
    
    # define log_path_file + create dir
    #log_path_file = current_dirname + "/log/uv_processing.log"
    log_path_file = exec_dirname + "/uv_processing.log"
    json_file  = os.path.dirname(os.path.realpath(__file__))  + '/config/templates/uv_js_meta.json'
    
    
        
    """Insert de initial and final dates as strings as 20190107(year:2019/month:01/day:07)"""
    
    """for calling the function from the terminal"""
    parser = argparse.ArgumentParser(description='Process UV radiometer measurements.') 
    parser.add_argument('-s', required=True, type=str, dest='id', # la variable se guarda en args.id como string
                    help='processing start date as 20190107 (y:2019 m:01 d:07)')
    parser.add_argument('-e', required=True, type=str, dest='fd',
                    help='processing end date as 20190107 (y:2019 m:01 d:07)')
    parser.add_argument('--configfile', required=True, type=str, dest='your_config_file',
                    help='config  path and file name')
    parser.add_argument('-i', '--image', action='store_true', 
                    help="switch to create images files")
    parser.add_argument('-n', '--netcdf', action='store_true', 
                    help="switch to create netCDF files")
    parser.add_argument('-st', '--statistics', action='store_true', 
                    help="switch to create statistics of missing files")
    parser.add_argument('--loglevel', default='INFO', dest='loglevel',
                    help="define loglevel to output screen INFO (default) | WARNING | ERROR ")
    parser.add_argument('--logfile', default=log_path_file, dest='logfile',
                    help="define logfile (default: " +  log_path_file + ") ")
    parser.add_argument('--jsonfile', default=json_file, dest='jsonfile',
                    help="define jsonfile (default: pathfile " + json_file + ") ")
    args = parser.parse_args()
    
    # create directory to store logfile if necessary
    log_path_file = args.logfile
    if not os.path.isdir(  os.path.dirname( log_path_file ) ):
        os.makedirs( os.path.dirname( log_path_file ) )
        print('Create directory     : ' + os.path.dirname(log_path_file) )
    
    
        
    # create logger with 'UV'
    logger = logging.getLogger('uv-processing')
    logger.setLevel(logging.DEBUG)
    
    # create file handler which logs even debug messages
    fh = logging.FileHandler( log_path_file )
    fh.setLevel(logging.DEBUG)
    
    # create/check level
    screen_level = logging.getLevelName(args.loglevel)
    
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    #ch.setLevel(logging.WARNING)
    ch.setLevel(screen_level)
    
    # create formatter and add it to the handlers
    formatter = logging.Formatter(fmt='%(asctime)s | %(name)-24s | %(levelname)-8s | %(message)s | %(module)s (%(lineno)d)', datefmt='%Y-%m-%d %H:%M:%S',)
    
    # add formatter to the handlers
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    # add first log mesage
    logger.info('Start uv-processing')
    
   
    
    if args.id is None or args.fd is None:
        logger.error('Less two arguments expected: startdate and enddate')
        exit()
    
    
    
    """Break in case the dates weren't correct"""
    if len(args.id)!=8 or len(args.fd)!=8:
        logger.error('Wrong date introduced, 8 digits required!')
        exit()
    if int(args.id)>int(args.fd):
        logger.error('Wrong date, start date < = end date required!')
        exit()
    
    """Check python version"""
    python_version = platform.python_version().split(".")
    if int(python_version[0]) < 3:
        logger.error( "Your python version is: " + platform.python_version() )
        logger.error( "Script will be terminated cause python version < 3 is required !" )
        exit()
    
    
    """Check python Submodule is already installed"""
    if (args.statistics):
        try:
            from Submodule import PlotHeatmap as plthtmp
        except ImportError:
            logger.error('There was no such module installed: PlotHeatmap')
            exit()


    # check if configs exists
    default_config_file = os.path.dirname(os.path.realpath(__file__))  + '/config/templates/config.ini'
    your_config_file    = args.your_config_file
    
    if not os.path.isfile( default_config_file ):
        logger.warn('default config file not exists: ' + default_config_file)
        quit()
    if not os.path.isfile( your_config_file ):
        logger.warn('local config file not exists: ' + your_config_file)
        quit()
        
    # get summarised config
    config = get_config.main(default_config_file, your_config_file)
    
    

    if not os.path.isfile( args.jsonfile ):
        logger.error( 'File json not exists: '+ args.jsonfile )
        quit()
    
    # call main function
    loop(args, config, logger)


#####################################################################################                                                    
if __name__ == "__main__":
    # execute only if run as a script
    print("___ bts_process __main__")
    adjust(sys.argv[1:])

#####################################################################################                                                    
def run():
    # execute only if run as a setuptoolscript
    print("___ bts_process run")
    adjust(sys.argv[1:])


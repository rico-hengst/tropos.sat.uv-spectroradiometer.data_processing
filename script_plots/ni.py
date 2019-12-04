#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 12:59:26 2019

@author: bayer
"""
import os
import read_bts2048rh as bts
import plotme
import calendar

"""Insert de initial and final dates as strings as 20190107(year:2019/month:01/day:07)"""

def statistic(i8date,f8date):
    methodbts = "global" 
    iy=int(i8date[0:4])
    im=int(i8date[4:6])
    ida=int(i8date[6:8])
    fy=int(f8date[0:4])
    fm=int(f8date[4:6])
    fda=int(f8date[6:8])
    
    """Define the main path where the files are in"""
    main_path="/vols/satellite/datasets/surfrad/uv_radiometer/"
    
    """Define the main path where the images should be saved"""
    image_path="/home/bayer/uv/images/"

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
                                plotme.plotme(d_bts1day,i8date,image_path)
                                iday=iday+1
                        else:
                            print(path_file+" does not exist")
                            iday=iday+1
    
#####################################################################################                                                            
statistic('20190302','20190302')

"""files that show error: 
20180815
"""

"""
    for iy in range(iy,fy+1):
        if iy!=fy:
            path = main_path + str(iy) + "/"
            for im in range(im,14):
                path1=path+str(im).zfill(2)+"/"
                if im<=12:   
                    numberOfDays = calendar.monthrange(iy, im)[1]
                    for ida in range(ida,numberOfDays + 2):
                        if ida<=numberOfDays:
                            path2 = path1 + str(ida).zfill(2) + "/"
                            path_file=path2+"MP"+str(iy-2000).zfill(2)+str(im).zfill(2)+str(ida).zfill(2)+".OR0"
                            if os.path.isfile(path_file):
                                if os.stat(path_file).st_size<1:
                                    print('file is empty '+path_file)
                                    ida=ida+1
                                else:
                                    i8date=str(iy)+str(im).zfill(2)+str(ida).zfill(2)
                                    d_bts1day=bts.read_oro_bts(path_file,methodbts,i8date)
                                    plotme.plotme(d_bts1day,i8date,image_path)
                                    ida=ida+1
                            else:
                                ida=ida+1
                                print(path_file+" does not exist")
                        elif ida==numberOfDays + 1:   
                            ida=1   
                            im=im+1
                            path1 = path + str(im).zfill(2) + "/"
                elif im==13:
                    im=1
                    iy=iy+1 
                    path = main_path + str(iy) + "/"
        elif iy==fy:
            path = main_path + str(iy) + "/"
            for im in range(im,fm+1):
                path1 = path + str(im).zfill(2) + "/"
                if im<fm:
                    numberOfDays = calendar.monthrange(iy, im)[1]
                    for ida in range(ida,numberOfDays + 2):
                        path2=path1+str(ida).zfill(2)+"/"
                        if ida<=numberOfDays:
                            path_file=path2+"MP"+str(iy-2000).zfill(2)+str(im).zfill(2)+str(ida).zfill(2)+".OR0"
                            if os.path.isfile(path_file):
                                if os.stat(path_file).st_size<1:
                                    print('file is empty '+path_file)
                                    ida=ida+1
                                else:
                                    i8date=str(iy)+str(im).zfill(2)+str(ida).zfill(2)
                                    d_bts1day=bts.read_oro_bts(path_file,methodbts,i8date)
                                    plotme.plotme(d_bts1day,i8date,image_path)
                                    ida=ida+1
                            else:
                                ida=ida+1
                                print(path_file+" does not exist")
                        elif ida==numberOfDays + 1:   
                            ida=1   
                            im=im+1
                            path1 = path + str(im).zfill(2) + "/"    
                elif im==fm:
                    path1 = path + str(im).zfill(2) + "/"
                    for ida in range(ida,fda+1):
                        path2= path1 + str(ida).zfill(2) + "/"
                        path_file=path2+"MP"+str(iy-2000).zfill(2)+str(im).zfill(2)+str(ida).zfill(2)+".OR0"
                        if os.path.isfile(path_file):
                            if os.stat(path_file).st_size<1:
                                print('file is empty '+path_file)
                                ida=ida+1
                            else:
                                i8date=str(iy)+str(im).zfill(2)+str(ida).zfill(2)
                                d_bts1day=bts.read_oro_bts(path_file,methodbts,i8date)
                                plotme.plotme(d_bts1day,i8date,image_path)
                                ida=ida+1
                        else:
                            ida=ida+1 
                            print(path_file+" does not exist")
"""                            
                            
                            
                            
                            
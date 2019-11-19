#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 11:46:17 2019

@author: bayer
"""
import sys,os
import numpy as np
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import datetime
#import the dictionary of the data
import read_bts2048rh as bts
import glob
# to display datetime on x-axis in a individual way
from matplotlib.dates import DayLocator, HourLocator, DateFormatter
#ax.xaxis.set_major_formatter(DateFormatter('%d.%m. %H:%M'))

i8date = '20181230'
f8date= '20181230'   
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

"""my script for ploting"""
#plt.rcParams["figure.figsize"] = (13, 20)
def niplot(d_bts1day,fdate):
    fig, (ax,ax1,ax2,ax3)=plt.subplots(4)
    fig.suptitle('Date: '+ str(ida) + '/' + str(im) + '/' + str(iy))
    ax.set_title("UVA")
    ax.plot(d_bts1day["datetime"],d_bts1day["uva"], 'r', label="UVA")
    ax.xaxis.set_tick_params(labelsize=10)
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    ax.legend()
    ax.set_xlabel('Time')
    ax.set_ylabel('Radiant flux density [$mW/m^2$]')
    #f, (ax1) = plt.subplots(1, 1, sharey=True)
    ax1.set_title("UVB")
    ax1.plot(d_bts1day["datetime"],d_bts1day["uvb"], 'b', label="UVB")
    ax1.xaxis.set_tick_params(labelsize=10)
    ax1.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    ax1.legend()
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Radiant flux density [$mW/m^2$]')
    #f, (ax2) = plt.subplots(1, 1, sharey=True)
    ax2.set_title("Spektrum")
    ax2.plot(d_bts1day["datetime"],d_bts1day["spect"], label="spect")
    ax2.xaxis.set_tick_params(labelsize=10)
    ax2.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    #ax2.legend()
    ax2.set_xlabel('Time')
    #f, (ax3) = plt.subplots(1, 1, sharey=True)
    ax3.set_title("SHAPE wvl")
    plt.plot(d_bts1day["wvl"],'y')
    #ax3.legend()
    plt.show()
    #print("SHAPE wvl" + str(d_bts1day["wvl"].shape))
    plot_name= fdate + '.pdf'
    fig.savefig(plot_name)                        
################################################################################ 
    
methodbts = "global" 
main_path="/vols/satellite/datasets/surfrad/uv_radiometer/"
for iy in range(iy,fy+1):
    if iy!=fy:
        path = main_path + str(iy) + "/"
        for im in range(im,14):
            path1=path+str(im).zfill(2)+"/"
            if im<=12:   
                for ida in range(ida,33):
                    if ida<=31:
                        path2 = path1 + str(ida).zfill(2) + "/"
                        path_file=path2+"MP"+str(iy-2000).zfill(2)+str(im).zfill(2)+str(ida).zfill(2)+".OR0"
                        if os.path.isfile(path_file):
                            fdate=str(iy)+str(im)+str(ida)
                            ida=ida+1
                            d_bts1day=bts.read_oro_bts(path_file,methodbts,fdate)
                            niplot(d_bts1day,fdate)
                            print(path_file)
                        else:
                            ida=ida+1
                            print(path_file+" does not exist")
                    elif ida==32:   
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
                for ida in range(ida,32):
                    path2=path1+str(ida).zfill(2)+"/"
                    if ida<=31:
                        path2 = path1 + str(ida).zfill(2) + "/"
                        path_file=path2+"MP"+str(iy-2000).zfill(2)+str(im).zfill(2)+str(ida).zfill(2)+".OR0"
                        if os.path.isfile(path_file):
                            fdate=str(iy)+str(im)+str(ida)
                            ida=ida+1
                            d_bts1day=bts.read_oro_bts(path_file,methodbts,fdate)
                            niplot(d_bts1day,fdate)
                            print(path_file)
                        else:
                            ida=ida+1
                            print(path_file+" does not exist")
                    else:   
                        ida=1   
                        im=im+1
                        path1 = path + str(im).zfill(2) + "/"       
            elif im==fm:
                path1 = path + str(im).zfill(2) + "/"
                for ida in range(ida,fda+1):
                    path2= path1 + str(ida).zfill(2) + "/"
                    path_file=path2+"MP"+str(iy-2000).zfill(2)+str(im).zfill(2)+str(ida).zfill(2)+".OR0"
                    if os.path.isfile(path_file):
                        fdate=str(iy)+str(im)+str(ida)
                        ida=ida+1
                        d_bts1day=bts.read_oro_bts(path_file,methodbts,fdate)
                        niplot(d_bts1day,fdate)
                        print(path_file)
                    else:
                        ida=ida+1        
                        print(path_file+" does not exist")
                       
                          

"""
plt.rcParams["figure.figsize"] = (13, 5)

# plot UVA
fig, ax = plt.subplots(1,1,figsize=(14,5))
ax.plot(d_bts1day["datetime"],d_bts1day["uva"], 'g', label="UVA")
#ax = plt.plot(d_bts1day["datetime"],d_bts1day["uva"],'g')
ax.xaxis.set_tick_params(rotation=5, labelsize=10)
ax.xaxis.set_major_formatter(DateFormatter('%d.%m. %H:%M'))
ax.legend()
ax.set_xlabel('DateTime')
ax.set_ylabel('Radiant flux density [$mW/m^2$]')
plt.show()
   
# plot UVB
fig, ax = plt.subplots(1,1,figsize=(14,5))
ax.plot(d_bts1day["datetime"],d_bts1day["uvb"], 'b', label="UVB")
ax.xaxis.set_tick_params(rotation=5, labelsize=10)
ax.xaxis.set_major_formatter(DateFormatter('%d.%m. %H:%M'))
ax.legend()
ax.set_xlabel('DateTime')
ax.set_ylabel('Radiant flux density [$mW/m^2$]')
    
plt.show()
print("SHAPE uvb" + str(d_bts1day["uvb"].shape))
    
# plot spectrum
fig, ax = plt.subplots(1,1,figsize=(14,5))
ax.plot(d_bts1day["datetime"],d_bts1day["spect"], label="spect")
ax.xaxis.set_tick_params(rotation=5, labelsize=10)
ax.xaxis.set_major_formatter(DateFormatter('%d.%m. %H:%M'))
#ax.legend()
ax.set_xlabel('DateTime')
plt.show()
print("SHAPE spect" + str(d_bts1day["spect"].shape))
    
# plot wavelength
plt.plot(d_bts1day["wvl"],'y')
plt.show()
print("SHAPE wvl" + str(d_bts1day["wvl"].shape))                        
"""                          
""" ORIGINAL PROGRAM
# import python libs
import os
import math
%matplotlib inline
import matplotlib.pyplot as plt

from datetime import datetime
from datetime import timedelta

# local module
import read_bts2048rh as bts

# set variables
p_bts = "data/"
#nam_bts = "MP190623.OR0"
nam_bts = "MP190901.OR0"
methodbts = "global"
#i8date = 20190623
i8date = 20190901
f_bts = p_bts+nam_bts
# call function of module
d_bts1day = bts.read_oro_bts(f_bts,methodbts,i8date)

# set default figure size
plt.rcParams["figure.figsize"] = (13, 5)

# to display datetime on x-axis in a individual way
from matplotlib.dates import DayLocator, HourLocator, DateFormatter
#ax.xaxis.set_major_formatter(DateFormatter('%d.%m. %H:%M'))

# plot UVA
fig, ax = plt.subplots(1,1,figsize=(14,5))
ax.plot(d_bts1day["datetime"],d_bts1day["uva"], 'g', label="UVA")
#ax = plt.plot(d_bts1day["datetime"],d_bts1day["uva"],'g')
ax.xaxis.set_tick_params(rotation=5, labelsize=10)
ax.xaxis.set_major_formatter(DateFormatter('%d.%m. %H:%M'))
ax.legend()
ax.set_xlabel('DateTime')
ax.set_ylabel('Radiant flux density [$mW/m^2$]')
plt.show()

# plot UVB
fig, ax = plt.subplots(1,1,figsize=(14,5))
ax.plot(d_bts1day["datetime"],d_bts1day["uvb"], 'b', label="UVB")
ax.xaxis.set_tick_params(rotation=5, labelsize=10)
ax.xaxis.set_major_formatter(DateFormatter('%d.%m. %H:%M'))
ax.legend()
ax.set_xlabel('DateTime')
ax.set_ylabel('Radiant flux density [$mW/m^2$]')

plt.show()
print("SHAPE uvb" + str(d_bts1day["uvb"].shape))

# plot spectrum
fig, ax = plt.subplots(1,1,figsize=(14,5))
ax.plot(d_bts1day["datetime"],d_bts1day["spect"], label="spect")
ax.xaxis.set_tick_params(rotation=5, labelsize=10)
ax.xaxis.set_major_formatter(DateFormatter('%d.%m. %H:%M'))
#ax.legend()
ax.set_xlabel('DateTime')
plt.show()
print("SHAPE spect" + str(d_bts1day["spect"].shape))

# plot wavelength
plt.plot(d_bts1day["wvl"],'y')
plt.show()
print("SHAPE wvl" + str(d_bts1day["wvl"].shape))
"""


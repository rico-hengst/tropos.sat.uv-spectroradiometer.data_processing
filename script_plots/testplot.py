#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 13:45:50 2019

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

"""Aligning x-axis using sharex

fig, (ax1, ax2) = plt.subplots(2, sharex=True)
fig.suptitle('Aligning x-axis using sharex')
ax1.plot(x, y)
ax2.plot(x + 1, -y) """
###############################################################################
"""my script for ploting"""
plt.rcParams["figure.figsize"] = (13, 5)
fig, ax=plt.subplots()
fig.suptitle('Date: '+ str(ida) + '/' + str(im) + '/' + str(iy))
ax.set_title("UVA")
ax.plot(d_bts1day["datetime"],d_bts1day["uva"], 'r', label="UVA")
ax.xaxis.set_tick_params(labelsize=10)
ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
ax.legend()
ax.set_xlabel('Time')
ax.set_ylabel('Radiant flux density [$mW/m^2$]')

f, (ax1) = plt.subplots(1, 1, sharey=True)
ax1.set_title("UVB")
ax1.plot(d_bts1day["datetime"],d_bts1day["uvb"], 'b', label="UVB")
ax1.xaxis.set_tick_params(labelsize=10)
ax1.xaxis.set_major_formatter(DateFormatter('%H:%M'))
ax1.legend()
ax1.set_xlabel('Time')
ax1.set_ylabel('Radiant flux density [$mW/m^2$]')

f, (ax2) = plt.subplots(1, 1, sharey=True)
ax2.set_title("Spektrum")
ax2.plot(d_bts1day["datetime"],d_bts1day["spect"], label="spect")
ax2.xaxis.set_tick_params(labelsize=10)
ax2.xaxis.set_major_formatter(DateFormatter('%H:%M'))
#ax2.legend()
ax2.set_xlabel('Time')


f, (ax3) = plt.subplots(1, 1, sharey=True)
ax3.set_title("SHAPE wvl")
plt.plot(d_bts1day["wvl"],'y')
#ax3.legend()
plt.show()
#print("SHAPE wvl" + str(d_bts1day["wvl"].shape))

plot_name= fdate + '.pdf'
fig.savefig(plot_name)                        
                          
###############################################################################
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

"""To save them to the same file, use subplots:

>>> fig = plt.figure()
>>> axis1 = fig.add_subplot(211)
>>> axis1.plot(range(10))
>>> axis2 = fig.add_subplot(212)
>>> axis2.plot(range(10,20))
>>> fig.savefig('multipleplots.png')

plot_name= fdate + '.pdf'"""

###############################################################################




#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 13:13:35 2019

@author: bayer
"""
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import pandas as pd
import pytz
import numpy as np
# units, see also https://www.uni-kiel.de/med-klimatologie/uvinfo.html
# https://www.bundesfachverband-besonnung.de/fileadmin/download/solaria2005/Solarium_Sonne.pdf

def plotme(d_bts1day, day, config):
  
    """creating plot title"""
    plt.suptitle(config.get('STATION','station_name') + ' ('+ config.get('STATION','station_lat') + ' '+\
                 config.get('STATION','station_lon') + ')\nDate: '+day.strftime('%Y')+ '/' + day.strftime('%m')+ \
                 '/' + day.strftime('%d'))
        
    """creating the 3 y axes for the ploting"""
    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(right=0.75)
    par1 = host.twinx()
    par2 = host.twinx()
    offset = 60
    new_fixed_axis = par2.get_grid_helper().new_fixed_axis
    par2.axis["right"] = new_fixed_axis(loc="right", axes=par2,
                                        offset=(offset, 0))
    par1.axis["right"] = new_fixed_axis(loc="right", axes=par1)
    par2.axis["right"].toggle(all=True)
    
    """Label the axes"""
    host.set_xlabel("Time (UTC)")
    host.set_ylabel("UV-Index")
    par1.set_ylabel("UV-B Irradiance [$W/m^2$]")
    par2.set_ylabel("UV-A Irradiance [$W/m^2$]")
    """adding the varibles for plotting and setting the colors and labels"""
    
    
#    if config.get('TIMEZONE','local_time') in config:    
    """define local timezone from the config file"""
    new_timezone = pytz.timezone(config.get('TIMEZONE','local_time', fallback='UTC'))
    
    """changing time for local time"""
    for x in range(0,len(d_bts1day['datetime'])):
        a=pd.Timestamp(d_bts1day['datetime'][x])
        a=pytz.UTC.localize(a)
        d_bts1day['datetime'][x]=float(a.astimezone(new_timezone).strftime("%H%M"))/100
    x=np.array(d_bts1day['datetime'])
    x=x.astype('float64') 
    host.set_xlabel("Time ("+str(new_timezone)+")")
    # else:
    #     x=np.array(d_bts1day['time'])
    #     x=x.astype('float64')
    #     host.set_xlabel("Time (UTC)")
        
        
    p1, = host.plot(x,d_bts1day["uvind"],"k-",linestyle=':', label="UV-Index")
    p2, = par1.plot(x,d_bts1day["uvb"], "r-", label="UV-B")
    p3, = par2.plot(x,d_bts1day["uva"], "b-", label="UV-A")
    
    """defining the limits of the axes"""  #preguntar como hacer cn los limites
    host.set_xlim(4, 22)
    host.set_ylim(0, 13)
    par1.set_ylim(0, 20)
    par2.set_ylim(0, 70)
    
    """adding legend and function"""
    host.legend()
    host.grid()

    """coloring the axis"""
#    host.axis["left"].label.set_color(p1.get_color())
    par2.axis["right"].label.set_color(p3.get_color())
    par1.axis["right"].label.set_color(p2.get_color())
    
    """full filling the curve under the UV-Index curve"""
    plt.fill_between(x, d_bts1day["uvind"],  where=d_bts1day["uvind"]<2, 
                        facecolor='green', alpha='0.5', interpolate=True)
    plt.fill_between(x, d_bts1day["uvind"],  where=d_bts1day["uvind"] >2 , 
                        facecolor='yellow', alpha='0.5', interpolate=True)
    plt.fill_between(x, d_bts1day["uvind"],  where=d_bts1day["uvind"] >5 , 
                        facecolor='orange', alpha='0.5', interpolate=True)
    plt.fill_between(x, d_bts1day["uvind"],  where=d_bts1day["uvind"] >7 , 
                        facecolor='red', alpha='0.5', interpolate=True)
    plt.fill_between(x, d_bts1day["uvind"],  where=d_bts1day["uvind"]>10, 
                        facecolor='purple', alpha='0.5', interpolate=True)
    
    """adding footnote"""
    plt.annotate('Leibnitz Institut für \nTroposphärenforschung', xy= (0,-1), xycoords='figure fraction',
                 xytext=(0, 25), textcoords='offset points', ha="left", va="bottom")

    """save the plot as pdf file """
    plot_name = config.get('DEFAULT','image_path') + 'BTS_plot-' + day.strftime('%Y%m%d') + '.pdf'
    plt.savefig(plot_name)
    print("%-21s: %-60s" %('Plot data to file', plot_name))

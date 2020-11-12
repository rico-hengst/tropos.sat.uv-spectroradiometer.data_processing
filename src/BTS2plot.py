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
from matplotlib.ticker import FixedLocator
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import xarray as xr
# units, see also https://www.uni-kiel.de/med-klimatologie/uvinfo.html
# https://www.bundesfachverband-besonnung.de/fileadmin/download/solaria2005/Solarium_Sonne.pdf

def plotme(nc, day, config):
    
    """get wished timezone from the config file"""
    new_timezone = pytz.timezone(config.get('TIMEZONE','plotting_timezone', fallback='UTC'))
    
    fig, ax = plt.subplots()
    ax.axis('off')
  
    """creating plot title"""
    plt.suptitle('Station: ' + config.get('STATION','station_name') + \
    '\nDate/Timezone: '+day.strftime('%Y-%m-%d')+ \
    ' / ' + str(new_timezone))
        
    """creating the 3 y axes for the ploting"""
    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(right=0.75)
    par1 = host.twinx()
    par2 = host.twinx()
    offset = 50
    new_fixed_axis = par2.get_grid_helper().new_fixed_axis
    par2.axis["right"] = new_fixed_axis(loc="right", axes=par2,
                                        offset=(offset, 0))
    par1.axis["right"] = new_fixed_axis(loc="right", axes=par1)
    par2.axis["right"].toggle(all=True)
    
    """Label the axes"""
    host.set_ylabel("UV-Index")
    host.set_xlabel("Time [$hour$]")
    par1.set_ylabel("UV-A Irradiance [$W/m^2$]")
    par2.set_ylabel("UV-B Irradiance [$W/m^2$]")
    """adding the varibles for plotting and setting the colors and labels"""
    
    
    """changing time for local time"""
    time=nc.time.to_index()
    time_utc = time.tz_localize(pytz.UTC)
    time_local = time_utc.tz_convert(new_timezone)
    time_local=time_local[:].hour+time_local[:].minute/60 +time_local[:].second/3600
    
    
    #p0, = host.plot(x,d_bts1day["uvind"],"k-",linestyle=':', label="UV-Index")
    p1, = par1.plot(time_local,nc["uva"], "b-", label="UV-A")
    p2, = par2.plot(time_local,nc["uvb"], "r-", label="UV-B")
    
    
    """defining the limits of the axes"""  #preguntar como hacer cn los limites
    # utcoffset = x_dict["datetime_new"][1].utcoffset().total_seconds()/3600
    # host.set_xlim(2+utcoffset, 20+utcoffset)
    host.set_xlim(time_local[0]-1, max(time_local)+1)
    host.xaxis.set_major_locator(FixedLocator(np.arange(round(time_local[0]-1), round(max(time_local)+1), 2)))
    host.set_ylim(0, 10)
    par1.yaxis.set_major_locator(FixedLocator(np.arange(0, 10, 2)))

    par1.set_ylim(0, 70)
    par1.yaxis.set_major_locator(FixedLocator(np.arange(0, 70.1, 14)))

    par2.set_ylim(0, 10)
    par2.yaxis.set_major_locator(FixedLocator(np.arange(0, 10.1, 2)))
    
    """adding legend and function"""
    host.legend()
    host.grid()


    """coloring the axis"""
    par1.axis["right"].label.set_color(p1.get_color())    #coloring the label    
    par2.axis["right"].label.set_color(p2.get_color())
    
    par1.axis["right"].line.set_color(p1.get_color())
    par1.axis["right"].major_ticks.set_color(p1.get_color())
    par1.axis["right"].major_ticklabels.set_color(p1.get_color())
    
    par2.axis["right"].line.set_color(p2.get_color())
    par2.axis["right"].major_ticks.set_color(p2.get_color())
    par2.axis["right"].major_ticklabels.set_color(p2.get_color())


    """Add chart plot UV index"""
    # Get a color map
    my_cmap = cm.get_cmap('RdYlGn',10)
    # reverse
    my_cmap_r = my_cmap.reversed()
     
    # Get normalize function (takes data in range [vmin, vmax] -> [0, 1])
    my_norm = Normalize(vmin=0, vmax=10)
    time_step=1/30 # in hours
    plt.bar(time_local, nc["uvind"], color=my_cmap_r(my_norm(nc["uvind"])), edgecolor='none', width=time_step)
    
    """Add colorbar"""
    # https://stackoverflow.com/questions/51204505/python-barplot-with-colorbar
    sm = ScalarMappable(cmap=my_cmap_r, norm=plt.Normalize(0,12))
    sm.set_array([])

    # https://stackoverflow.com/questions/32462881/add-colorbar-to-existing-axis
    cax = fig.add_axes([0.125, 0.11, 0.01, 0.77])
    
    cbar = plt.colorbar(sm, cax=cax, ticks=[])
    #cbar.set_label('UV index', rotation=90,labelpad=5)
    cbar.ax.tick_params(labelsize=7)
    # END # colornar
    

    """save the plot as file """
    plot_name = config.get('DEFAULT','image_path') + config.get('STATION','station_prefix') + '_' + day.strftime('%Y%m%d') + '_plot.png'
    plt.savefig(plot_name, dpi=300)
    plt.close()
    print("%-21s: %-60s" %('Plot data to file', plot_name))

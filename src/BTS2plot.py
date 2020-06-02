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

# units, see also https://www.uni-kiel.de/med-klimatologie/uvinfo.html
# https://www.bundesfachverband-besonnung.de/fileadmin/download/solaria2005/Solarium_Sonne.pdf

def plotme(d_bts1day, day, config):    
    plt.suptitle(config.get('STATION','station_name') + ' ('+ config.get('STATION','station_lat') + ' '+\
                 config.get('STATION','station_lon') + ')\nDate: '+day.strftime('%Y')+ '/' + day.strftime('%m')+ \
                 '/' + day.strftime('%d'))
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
    p1, = host.plot(d_bts1day["time"],d_bts1day["uvind"],"k-",linestyle=':', label="UV-Index")
    p2, = par1.plot(d_bts1day["time"],d_bts1day["uvb"]*10, "r-", label="UV-B")
    p3, = par2.plot(d_bts1day["time"],d_bts1day["uva"], "b-", label="UV-A")
    
    """defining the limits of the axes"""
    host.set_xlim(4, 21)
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
    plt.fill_between(d_bts1day["time"], d_bts1day["uvind"],  where=d_bts1day["uvind"]<2, 
                        facecolor='green', alpha='0.5', interpolate=True)
    plt.fill_between(d_bts1day["time"], d_bts1day["uvind"],  where=d_bts1day["uvind"] >2 , 
                        facecolor='yellow', alpha='0.5', interpolate=True)
    plt.fill_between(d_bts1day["time"], d_bts1day["uvind"],  where=d_bts1day["uvind"] >5 , 
                        facecolor='orange', alpha='0.5', interpolate=True)
    plt.fill_between(d_bts1day["time"], d_bts1day["uvind"],  where=d_bts1day["uvind"] >7 , 
                        facecolor='red', alpha='0.5', interpolate=True)
    plt.fill_between(d_bts1day["time"], d_bts1day["uvind"],  where=d_bts1day["uvind"]>10, 
                        facecolor='purple', alpha='0.5', interpolate=True)
    
    """adding footnote"""
    plt.annotate('Leibnitz Institut für \nTroposphärenforschung', xy= (0,-1), xycoords='figure fraction',
                 xytext=(0, 25), textcoords='offset points', ha="left", va="bottom")

    """save the plot as pdf file """
    plot_name = config.get('DEFAULT','image_path') + 'BTS_plot-' + day.strftime('%Y%m%d') + '.pdf'
    plt.savefig(plot_name)
    print("%-21s: %-60s" %('Plot data to file', plot_name))

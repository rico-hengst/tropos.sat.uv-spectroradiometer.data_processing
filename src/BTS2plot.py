#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 13:13:35 2019

@author: bayer
"""
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as DateFormatter
#import pandas as pd 
# from matplotlib import colors
# import matplotlib as mpl
# import numpy as np


def plotme(d_bts1day, i8date, image_path):
    
    plt.rcParams["figure.figsize"] = (13, 24)
    fig, (ax,ax1,ax2,ax3)=plt.subplots(4)
    fig.suptitle('Date: '+ i8date[0:4] + '/' + i8date[4:6] + '/' +  i8date[6:8])
    ax.set_title("UVA")
    ax.plot(d_bts1day["time"],d_bts1day["uva"], 'r', label="UVA")
    ax.xaxis.set_tick_params(labelsize=10)
    ax.set_xlim(6,18)
    # ax.set_xlim(datetime(2019, 1, 1, 6, 0),datetime(2019, 1, 1, 18, 30))
    # ax.xaxis.set_major_formatter(DateFormatter('%h-%m'))
    ax.legend()
    ax.set_xlabel('Time hours in UTC')
    ax.set_ylabel('Radiant flux density [$mW/m^2$]')
    ax.set_ylim(( 0, 60))  ###y limits
    ax1.set_title("UVB")
    ax1.plot(d_bts1day["time"],d_bts1day["uvb"], 'b', label="UVB")
    ax1.xaxis.set_tick_params(labelsize=10)
    ax1.set_xlim(6,18)
#    ax1.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    ax1.legend()
    ax1.set_xlabel('Time in UTC')
    ax1.set_ylabel('Radiant flux density [$mW/m^2$]')
    ax1.set_ylim(( 0, 1.4))
    ax2.set_title("Spektrum")
    ax2.plot(d_bts1day["time"],d_bts1day["spect"], label="spect")
    ax2.xaxis.set_tick_params(labelsize=10)
    ax2.set_xlim(6,18)    
#    ax2.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    ax2.set_xlabel('Time in UTC')
    ax3.set_title("UV Index")
    ax3.plot(d_bts1day["time"],d_bts1day["uvind"], 'k', label="UV")
    ax3.xaxis.set_tick_params(labelsize=10)
    ax3.set_xlim(6,18)
#    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
#    ax3.legend()
    ax3.set_xlabel('Time hours in UTC')
    ax3.set_ylabel('UV index')
    ax3.set_ylim(( 0, 11))
    #ax3.grid()
    """Set the colors inside the plot """
    ax3.axhspan(0, 3, facecolor='green', alpha=0.5)
    ax3.axhspan(3, 6, facecolor='yellow', alpha=0.5)
    ax3.axhspan(6, 8, facecolor='orange', alpha=0.5)
    ax3.axhspan(8, 11, facecolor='red', alpha=0.5) 
    ax3.text(17.8, 1.5, 'Low', fontsize=15, ha='right')
    ax3.text(17.8, 4.5, 'Moderate', fontsize=15, ha='right')
    ax3.text(17.8, 7, 'High', fontsize=15, ha='right')
    ax3.text(17.8, 9, 'Very High', fontsize=15, ha='right')
#    ax3.colorbar()
    """save the plot as pdf file """
    plot_name = image_path + i8date + '.pdf'
    fig.savefig(plot_name)
    
    # close figure
    plt.close(fig)

    print("%-21s: %-60s" %('Plot data to file', plot_name))


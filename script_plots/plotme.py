#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 13:13:35 2019

@author: bayer
"""
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib as mpl
import numpy as np
import pygal
from pylab import *

def plotme(d_bts1day, i8date, image_path):
    
    plt.rcParams["figure.figsize"] = (13, 24)
    fig, (ax,ax1,ax2,ax3)=plt.subplots(4)
    fig.suptitle('Date: '+ i8date[0:4] + '/' + i8date[4:6] + '/' +  i8date[6:8])
    ax.set_title("UVA")
    ax.plot(d_bts1day["time"],d_bts1day["uva"], 'r', label="UVA")
    ax.xaxis.set_tick_params(labelsize=10)
    ax.set_xlim(6,18)
#    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
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
    ax3.grid()
    """Set the colors inside the plot """
    ax3.axhspan(0, 3, facecolor='green', alpha=0.5)
    ax3.axhspan(3, 6, facecolor='yellow', alpha=0.5)
    ax3.axhspan(6, 8, facecolor='orange', alpha=0.5)
    ax3.axhspan(8, 11, facecolor='red', alpha=0.5) 
    ax3.text(17, 2, 'Low', fontsize=15)
    ax3.text(16.5, 5, 'Moderate', fontsize=15)
    ax3.text(17, 7, 'High', fontsize=15)
    ax3.text(16.5, 10, 'Very High', fontsize=15)
#    ax3.colorbar()
    """save the plot as pdf file """
    plot_name = image_path + i8date + '.pdf'
    fig.savefig(plot_name)
#    cmap = mpl.colors.ListedColormap(['green', 'yellow', 'orange', 'red'])                                  
#    cmap.set_over('violet')
#    cmap.set_under('green')
#    bounds = [1, 3, 6, 8, 10]
#    ax4.norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
#    ax4.cb3 = mpl.colorbar.ColorbarBase(ax, cmap=cmap, boundaries=[-10] + bounds + [10],
#    extend='both', extendfrac='auto', ticks=bounds, spacing='uniform', orientation='horizontal')
#    ax4.cb3.set_label('Custom extension lengths, some other units')

#    horizontalbar_chart = pygal.HorizontalBar()
#    horizontalbar_chart.add('Low ', 3)
#    horizontalbar_chart.add('Moderate ', 6)
#    horizontalbar_chart.add('High ', 8)
#    horizontalbar_chart.add('Very High ', 11)
#    horizontalbar_chart.render()    
#    norm = colors.Normalize(uvmin=0, uvmax=11)
#    im = ax3.imshow(np.arange(11)
    #add_colorbar(im)
    #plt.colorbar(im,orientation='horizontal', fraction=0.046, pad=0.04)
    
#fig, ax = plt.subplots(figsize=(4, 1))
#fig.subplots_adjust(bottom=0.6)
#
#cmap = mpl.cm.cool
#norm = mpl.colors.Normalize(vmin=0, vmax=11)
#
#cb1 = mpl.colorbar.ColorbarBase(ax, cmap=cmap, norm=norm, orientation='horizontal')
#cb1.set_label('UV Index')
#fig.show()
#
#ax.set_ticklabels(['low', 'medium', 'high'])
#
#fig, ax = plt.subplots(figsize=(10, 1))
#fig.subplots_adjust(bottom=0.5)
#
#cmap = mpl.colors.ListedColormap(['green', 'yellow', 'orange', 'red'])
#bounds = [0,3,6,8,11]
#norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
#cb2 = mpl.colorbar.ColorbarBase(ax, cmap=cmap,
#                                norm=norm,
#                                ticks=bounds,
#                                spacing='proportional',
#                                orientation='horizontal')
#cb2.set_label('UV Index')
#fig.show()
# 
#    ax3.cbar = fig.colorbar(d_bts1day["uvind"],  shrink=0.95)
#    ax3.cbar.set_ticks(np.arange(0, 1.1, 0.5))
#    ax3.cbar.set_ticklabels(['low', 'moderate', 'high', 'very high'])
#    fig.colorbar( ax=ax4, orientation='horizontal', fraction=.1)
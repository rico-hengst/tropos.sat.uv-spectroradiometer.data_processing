#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 13:13:35 2019

@author: bayer
"""
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
def plotme(d_bts1day, i8date, image_path):
    
    plt.rcParams["figure.figsize"] = (13, 20)
    fig, (ax,ax1,ax2,ax3)=plt.subplots(4)
    fig.suptitle('Date: '+ i8date[0:4] + '/' + i8date[4:6] + '/' +  i8date[6:8])
    ax.set_title("UVA")
    ax.plot(d_bts1day["datetime"],d_bts1day["uva"], 'r', label="UVA")
    ax.xaxis.set_tick_params(labelsize=10)
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    ax.legend()
    ax.set_xlabel('Time')
    ax.set_ylabel('Radiant flux density [$mW/m^2$]')
    ax1.set_title("UVB")
    ax1.plot(d_bts1day["datetime"],d_bts1day["uvb"], 'b', label="UVB")
    ax1.xaxis.set_tick_params(labelsize=10)
    ax1.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    ax1.legend()
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Radiant flux density [$mW/m^2$]')
    ax2.set_title("Spektrum")
    ax2.plot(d_bts1day["datetime"],d_bts1day["spect"], label="spect")
    ax2.xaxis.set_tick_params(labelsize=10)
    ax2.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    ax2.set_xlabel('Time')
    ax3.set_title("SHAPE wvl")
    plt.plot(d_bts1day["wvl"],'y')
    plot_name= image_path + i8date + '.pdf'
    fig.savefig(plot_name)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 14:15:43 2020

@author: nbayer
"""


import matplotlib.pyplot as plt
import datetime

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def plot_st(missing_days, s, f, config):

    """Transform dict to python array"""
    x=list( missing_days.keys() )
    y=list( missing_days.values() )


    if f==00: f=12
    #plt.bar(range(len(missing_days)),list(missing_days.values()),linewidth=2.0)
       
    """Plot dictionary: https://stackoverflow.com/questions/37266341/plotting-a-python-dict-in-order-of-key-values/37266356"""
    #plt.bar(*zip(*sorted(missing_days.items())), linewidth=1.0)
    

    """FIGURE"""
    fig = plt.figure()

    #ax = fig.add_subplot(111)
    ax = fig.add_axes([0.1, 0.25, 0.8, 0.6])
    #fig.subplots_adjust(top=0.95)


    """Add figure creating timestamp"""
    """https://riptutorial.com/matplotlib/example/16030/coordinate-systems-and-text"""
    plt.text(  # position text relative to Figure
        0.0, 0.02, 'Figure generated: ' + str(now) + '\nStation: ' + config.get('DEFAULT','station_prefix'), fontsize=5,
        ha='left', va='baseline',
        transform=fig.transFigure
    )

    """Plot data"""
    dataset1 = ax.bar(x,y, linewidth=18.0,  color='red')

    """Plot legend"""
    ax.legend( [dataset1], ['Missing Data'], bbox_to_anchor=(0.35, 0.5), loc='upper left', borderaxespad=0.)


    
    """Add labels and title"""
    plt.xlabel('time [day of month]')
    plt.title('Missing Data: '+str(s) +'/'+str(f).zfill(2))

    """Add lims and ticks"""
   # plt.xticks(range(len(missing_days)),list(missing_days.keys()),rotation='vertical')
    plt.xticks(list(x),rotation='vertical')
    plt.yticks([])
    plt.xlim((0,32))


    
    

    """Remove ax spines (frames"""
    """https://brohrer.github.io/matplotlib_framing.html"""
    ax.spines["top"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)




    """save the plot as pdf file """
    plot_name =config.get('DEFAULT','image_path')+'MissingData_'+str(s) +'-'+str(f).zfill(2)+ '.pdf'

    plt.savefig(plot_name)


    """Clear figure, very important"""
    plt.clf()

    #plt.show()


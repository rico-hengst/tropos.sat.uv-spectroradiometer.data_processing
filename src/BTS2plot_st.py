#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 14:15:43 2020

@author: nbayer
"""


import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons


def plot_st(missing_days, s, f, image_path):
    if f==00: f=12
    plt.bar(range(len(missing_days)),list(missing_days.values()),linewidth=2.0)
    plt.xticks(range(len(missing_days)),list(missing_days.keys()),rotation='vertical')
    plt.ylim((0,1))
    plt.title('Missing Days: '+str(s) +'/'+str(f).zfill(2))
    """save the plot as pdf file """
    plot_name =image_path+'MissingDays_'+str(s) +'-'+str(f).zfill(2)+ '.pdf'
    plt.savefig(plot_name)
    plt.show()

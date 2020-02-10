#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 14:15:43 2020

@author: nbayer
"""


import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons


def plot_st(missing_days, s, f, image_path):
    plt.bar(range(len(missing_days)),list(missing_days.values()),linewidth=2.0)
    plt.xticks(range(len(missing_days)),list(missing_days.keys()),rotation='vertical')
    plt.title('Missing Days: '+s +'-'+f)
    
    
    
    """save the plot as pdf file """
    plot_name =image_path+'MissingDays_'+s +'-'+f+ '.pdf'
    plt.savefig(plot_name)
    plt.show()
    
#,top=0.966, bottom=0.054, left=0.024, right=0.992, hspace=0.0, wspace=0.0    

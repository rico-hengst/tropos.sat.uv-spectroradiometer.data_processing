#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 14:15:43 2020

@author: nbayer
"""


import matplotlib.pyplot as plt



def plot_st(missing_days, s, f, image_path):
    print(range(len(missing_days)))
    plt.bar(range(len(missing_days)),list(missing_days.values()))
    plt.xticks(range(len(missing_days)),list(missing_days.keys()),rotation='vertical')
    plt.title('Missing days: '+s +'-'+f)
    """save the plot as pdf file """
    plot_name =image_path+'Missing days: '+s +'-'+f+ '.pdf'
    plt.savefig(plot_name)
    plt.show()
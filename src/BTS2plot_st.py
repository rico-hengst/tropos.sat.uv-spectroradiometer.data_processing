#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 14:15:43 2020

@author: nbayer
"""


import matplotlib.pyplot as plt



def plot_st(missing_days, s, f):
    print(range(len(missing_days)))
    plt.bar(range(len(missing_days)),list(missing_days.values()))
    plt.xticks(range(len(missing_days)),list(missing_days.keys()),rotation='vertical')
    plt.title('Missing days: '+s +'-'+f)
    plt.show()
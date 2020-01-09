#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 08:51:07 2019

@author: austinpeel
"""
import pandas as pd
import pickle
import seaborn as sns

import os
print(os.getcwd())


with open('models/segment_log_param_stats.pkl', 'rb') as f:
    param_stats = pickle.load(f)

with open('models/segment_log_y_pred_stats.pkl', 'rb') as f:
    y_pred_stats = pickle.load(f)

with open('models/segment_log_y_preds.pkl', 'rb') as f:
    y_preds = pickle.load(f)
    
    
dfs = []
for k in y_preds:
    _df = pd.DataFrame(y_preds[k])
    _df['Fare Type'] = k[0]
    _df['Booking Lead Time Logged'] = 10**k[1]
    _df = _df.rename({0:'Cost per Mile'}, axis = 1)
    dfs.append(_df)
    
y_pred_df = pd.concat(dfs)

y_pred_df.to_csv("data/segment_log_predictions.csv")
#standardized booking_days
sns.set(color_codes = True)
lm = sns.lmplot(x = "Booking Lead Time Logged",
                y = "Cost per Mile",
                hue = "Fare Type",
                data = y_pred_df,
                x_jitter = 4,
                y_jitter = .02,
                scatter_kws={"s": .0005}, #changes the marker size
                ci = None) 
lm.fig.set_size_inches(15, 8)
lm.set(xlim=(0, 300))

#save the fig to disk
#fig = lm.get_figure()
lm.savefig('analysis/Cost per Mile vs Booking Lead Time.png') 



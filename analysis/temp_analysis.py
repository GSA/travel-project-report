#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 15:05:55 2019

@author: austinpeel
"""

from models.models import Segment , Transactions, Train_Plane, Trip

import statsmodels.api as sa

import sys
sys.path.append('/Users/austinpeel/.pyenv/versions/3.6.6/lib/python3.6/site-packages')

import linearmodels.panel as  lp 
import pandas as pd

# Segment level analysis
seg = Segment()

#what does this look like
seg
print(seg)

#need help interpreting columns
seg.describe("")


#lets look at model 1
model = seg.model_1()

#what are we doing with this model
print(model)

#this is the data we are using 
df = model.model_data



year = pd.Categorical(df.Year)
df = df.set_index(['city_pair_code','Year'])
df['Year'] = year

exog_cols= ['fare_type' , 'market_share_log']
exog = sa.add_constant(df[exog_cols])
model = lp.PanelOLS(df.cost_per_mile,exog,entity_effects= True,time_effects=True).fit()

            
          
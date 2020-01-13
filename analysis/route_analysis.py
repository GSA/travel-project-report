#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 15:05:55 2019

@author: austinpeel
"""

import statsmodels.formula.api as sm
from models.models import  Route

# Segment level analysis
trip = Route()

#lets look at model 1
model = Route.model_1()

#this is the data we are using 
df = model.model_data

'''
This model uses business fares and govt fare to get an idea of how well the
 government is doing compared to the business fares. 
 
 The most imporant variable is the interaction between fare_type and booking days
 beacuse most savings with regular booking happen outside the 14 day window

'''
result = sm.ols(formula = "cost_per_mile ~    C(Year) +  ticketing_adv_booking_group+ ticketing_adv_booking_group*C(fare_type, Treatment(reference='YCA')) + city_pair ",data=df).fit()
print(result.summary())
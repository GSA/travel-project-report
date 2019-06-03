#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 11:38:17 2019

@author: austinpeel
"""


from models.models import Segment 

import statsmodels.formula.api as sm

#Using model 1
model = Segment().model_1()

#this is the data we are using 
df = model.model_data


#this model uses the standarized booking advanced days
result = sm.ols(formula = "cost_per_mile ~   market_share_log  + month + day_of_week + C(Year) + no_CA_award + booking_days_standarized + booking_days_standarized*C(fare_type, Treatment(reference='Dash CA')) + city_pair_code + self_booking_indicator",data=df).fit()
print(result.summary())

#this model log transforms booking advanced days
result = sm.ols(formula = "cost_per_mile ~   market_share_log  + month + day_of_week + C(Year) + no_CA_award + booking_days_log + booking_days_log*C(fare_type, Treatment(reference='Dash CA')) + city_pair_code + self_booking_indicator",data=df).fit()
print(result.summary())




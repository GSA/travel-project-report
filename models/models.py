#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 10:26:07 2019

@author: austinpeel
"""

# -*- coding: utf-8 -*-


import statsmodels.formula.api as sm


import pandas as pd

segment  = pd.read_csv('/data/by_segment.csv')


segment  = segment[segment['paid_fare_including_taxes_and_fees'] >0 ]

#cornerstone can not get accurate segment data when they have split fare_types 
#i removed them here
segment  = segment[segment.YCA_y != 1 ]
segment  = segment[segment.DashCA_y != 1 ]

#only take flights with a simple go and return trip
segment  = segment[segment.count_y == 2 ]

#only flights where city pair has awarded a contract
segment  = segment[segment.awarded ==1 ]

#calculate dash CA contract per mile
segment['dash_per_mile'] = segment.XCA_FARE / segment.nsmiles

#calculate yca per mile
segment['YCA_per_mile'] = segment.YCA_FARE / segment.nsmiles

#calculate actual cost per mile travelled
segment['cost_per_mile'] = segment.paid_fare_including_taxes_and_fees / segment.nsmiles

#calculate ratio of XCA to YCA contract 
segment['city_pair_ratio'] = segment.dash_per_mile / segment.YCA_per_mile

#filter for coach fares
fare = ['YCA','Dash CA','Other','DG']
segment = segment[segment.fare_type.isin(fare)]

#regression on cost_per_mile
result = sm.ols(formula = 'cost_per_mile ~ city_pair_ratio + fare_type + segment_refund_indicator + ticket_exchange_indicator + ticketing_adv_booking_group + fare_type*ticketing_adv_booking_group + airline_carrier + city_pair_code',data=segment).fit()
print(result.summary())


#logistic regressions





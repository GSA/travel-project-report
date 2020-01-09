#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 14:24:29 2019

@author: austinpeel
"""

import pandas as pd
import statsmodels.formula.api as sm


from utils import segment , data
from models import models


def get():
        
    #Using model 1
    model = models.Segment().model_1()
    
    #this is the data we are using 
    df = model.model_data
    
    segment_data = segment.group_segment_by_quarter(df)
    
    #pull in business fares
    bus = data.get(data="business_fares")
    
    #no saturday night stay day
    bus = bus[bus['SAT NIGHT STAY']== 'N']
    
    #rename columns so they are aligned to append later
    bus= bus.rename(columns={"PassengerCount":"no_of_segments","CityPair":"city_pair_code","Y vs Non Y":"fare_type","Advance Purchase Group":'ticketing_adv_booking_group',"Avg Seg Price": "paid_fare_including_taxes_and_fees"})
    
    
    #limit columns so they are balanced across the two datasets
    cols= ['Year',
     'city_pair_code',
     'ticketing_adv_booking_group',
     'no_of_segments',
     'fare_type',
     'paid_fare_including_taxes_and_fees']
    bus = bus[cols]
    
    
    #remove non included city pair
    city_pair = list(segment_data.city_pair_code.unique())
    bus = bus[bus.city_pair_code.isin(city_pair)]
       
    
    #append data
    total = bus.append(segment_data)
    
    #pull in miles data
    miles = segment.get_miles()
    
    #merge data
    total = pd.merge(total,miles,on=['city_pair_code'],how='inner')
    
    total.to_csv('data/by_route.csv')
    


 









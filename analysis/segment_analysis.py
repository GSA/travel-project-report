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


'''
These models try to predict price by certain factors. The most important being
days booked in advance and fare type. The most imporant being the interaction between them 
as slopes vary and booking time adavanced matter more depeding on the fare type
(contract v non contract). Using these models we can estimate a cost savings if 
govt moves away from YCA fares in favor of _dca and open market booking concepts

'''

'''
this model used  booking advanced days without any transformation to the booking
day variable. There is strong multicollinearity. This is the result of some 
fares have routes that are only YCA or _CA it 
is addressed with the model by transforming the booking days

'''
result = sm.ols(formula = "cost_per_mile ~    C(month) + day_of_week + C(Year) + no_CA_award + booking_advanced_days+ booking_advanced_days*C(fare_type, Treatment(reference='Dash CA')) + city_pair_code + self_booking_indicator",data=df).fit()
print(result.summary())


'''
this model uses the standarized booking advanced days. it helps to resolve some of the multicollinearity and does not  change the the effect of the booking-days importance

'''
result = sm.ols(formula = "cost_per_mile ~   market_share_log  + C(month) + day_of_week + C(Year) + no_CA_award + booking_days_standarized + booking_days_standarized*C(fare_type, Treatment(reference='Dash CA')) + city_pair_code + self_booking_indicator",data=df).fit()
print(result.summary())



'''
this model log transforms booking advanced days. It does less well but is still a useful check and robustness

'''
result = sm.ols(formula = "cost_per_mile ~  no_CA_award + C(month) + day_of_week + C(Year) + booking_days_log +  booking_days_log*C(fare_type, Treatment(reference='Dash CA')) + city_pair_code + self_booking_indicator",data=df).fit()
print(result.summary())






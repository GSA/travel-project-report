#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 11:38:17 2019

@author: austinpeel
"""


from models.models import Segment
import statsmodels.formula.api as sm
import statsmodels.api as sm2
import matplotlib.pyplot as plt
from statsmodels.iolib.summary2 import summary_col


# Segment level analysis
seg = Segment()

#what does this look like
seg
print(seg)

#need help interpreting columns
seg.describe("cost_per_mile")


#lets look at model 1
model = seg.model_1()

#what are we doing with this model
print(model)

#this is the data we are using 
df = model.model_data


#model your own regression
result = sm.ols(formula = 'cost_per_mile ~ city_pair_ratio +no_CA_award + market_share_log + fare_type +  ticketing_adv_booking_group + city_pair_code ',data=model.model_data).fit()
print(result.summary())


#here are some pre-defined regression. we will put the ones in final analysis here. 
res1 = model.regression_1()
res2 = model.regression_2()
res3 = model.regression_3()
res4 = model.regression_4()


# combining similar models into one output
dfoutput = summary_col([res1,res2,res3,res4],stars=True)
print(dfoutput)


#some plots and stuff
fig = plt.figure(figsize=(15,8))
fig = sm2.graphics.plot_regress_exog(res4, "city_pair_ratio", fig=fig)

model.model_data.plot.scatter(x='large_ms', y='cost_per_mile', c='DarkBlue')





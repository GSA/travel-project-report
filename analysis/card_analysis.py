#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 10:53:26 2019

@author: austinpeel
"""


from models.models import  Transactions

import statsmodels.formula.api as sm
import statsmodels.api as sm2
import matplotlib.pyplot as plt

#initate class
card = Transactions()
print(card)


card.describe("days")
card.describe("meals_total")
card.describe("meals_card")

model = card.model_1()



#this is the data we are using 
df = model.model_data



df['meals_card_percent'] = df['M&IE-PerDiem_card'] /df['meals_total']

df =df[df['meals_total'] >0 ]
df =df[df['meals_card_percent'] < 1 ]

result = sm.ols(formula = 'meals_total_per_day ~ meals_card_percent + trip_count + days',data=df).fit()
print(result.summary())


fig = plt.figure(figsize=(15,8))
fig = sm2.graphics.plot_regress_exog(result, "meals_card_percent", fig=fig)


df.plot.scatter(x='meals_card_percent', y='meals_total_per_day', c='DarkBlue')



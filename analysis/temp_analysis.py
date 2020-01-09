#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 15:05:55 2019

@author: austinpeel
"""

import statsmodels.formula.api as sm
from models.models import  Trip

import statsmodels.api as sa

import sys
sys.path.append('/Users/austinpeel/.pyenv/versions/3.6.6/lib/python3.6/site-packages')

import linearmodels.panel as  lp 
import pandas as pd

# Segment level analysis
trip = Trip()



#lets look at model 1
model = trip.model_3()

#what are we doing with this model
print(model)

#this is the data we are using 
df = model.model_data
df['b_fees'] = df['Baggage Fees']



df = df.fillna(0)

df = df[df['number_of_segments'] == 2]
df = df[df['refund'] == 0]
df = df[df['exchange'] == 0]
df = df[df['domestic_international_indicator']== 'D']
df = df[df['total_air'] > 55]


df['total_air'] = df.airline_total + df.b_fees + df['Seat Selection Fee']

result = sm.ols(formula = "total_air ~ total_flight_miles + validating_airline_code",data=df).fit()
print(result.summary())

df.plot.scatter(x='total_air', y='total_flight_miles', c='DarkBlue')

df2 = pd.DataFrame.from_dict({
'Southwest Airlines':['Southwest Airlines','Free'],
 'American Airlines':['American Airlines','First_bag'],
 'United Airlines':[ 'United Airlines','First_bag'],
 'Silver Airways Corp':['Silver Airways Corp','First_bag'],
 'Delta Air Lines':['Delta Air Lines','First_bag'],
 'Alaska Airlines':['Alaska Airlines','First_bag'],
 'Jetblue':['Jetblue','Over_50'],
 'Hawaiian':['Hawaiian','First_bag']},orient='index',columns=['validating_airline_name','fee_structure'])


df3 = pd.merge(df,df2,on='validating_airline_name',how='inner')


def take_major_airports(data, n=40):
    df_g = data
    df_g['ticket'] = 1
    df_g = df_g[['city_pair_code','ticket']]
    df_g = df_g.groupby(by ='city_pair_code',as_index=False).sum()
    a = df_g[df_g.ticket > n]
    codes = list(a.city_pair_code)
    data2 = data[data.city_pair_code.isin(codes)]
    return data2

df4 = take_major_airports(df3,n=100)

result = sm.ols(formula = "total_air ~ fee_structure + fare_type + total_flight_miles + trip_departure_day_of_week",data=df4).fit()
print(result.summary())

df5= df4[['city_pair_code','validating_airline_name','FY']]

df5 = df5.drop_duplicates()

codes = ['ATL-FLL','DCA-DEN','DCA-MCO','DCA-SAN','SAN-SFO','LAX-SFO','IAD-SAN','DEN-SFO','DEN-IAD','DEN-STL','DCA-SFO']

df6 = df4[df4.city_pair_code.isin(codes)]

result = sm.ols(formula = "total_air ~ fee_structure + fare_type + trip_departure_day_of_week",data=df6).fit()
print(result.summary())


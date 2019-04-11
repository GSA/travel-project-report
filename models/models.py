#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 10:26:07 2019

@author: austinpeel
"""

# -*- coding: utf-8 -*-


import statsmodels.formula.api as sm

import numpy as np
import pandas as pd

segment  = pd.read_csv('data/by_segment.csv')


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




transactions = pd.read_csv('data/by_person.csv')

transactions['total_variable_expense'] =  transactions['Charge Card Fees'] +transactions[ 'Laundry_total']+transactions['M&IE-PerDiem']+transactions[ 'Meals Actuals']+transactions['Misc Expense_total']+transactions['Parking_total']+transactions['Public Transportation_total']+transactions['Taxi_total']
transactions['variable_cost_per_day'] = transactions['total_variable_expense'] / transactions['daysTravelled']

transactions['misc_cost_per_day'] = transactions['Misc Expense_card'] / transactions['daysTravelled']
transactions['misc_ratio'] =  transactions['Misc Expense_card']  / ( transactions['M&IE-PerDiem']+ transactions['Misc Expense_total']+ transactions['Meals Actuals']+)



transactions['Taxi_per_day'] = transactions['Taxi_card'] / transactions['daysTravelled']

transactions['Public_Transportation_cost_per_day'] = transactions['Public Transportation_card'] / transactions['daysTravelled']

transactions['Parking_cost_per_day'] = transactions['Parking_card'] / transactions['daysTravelled']


transactions['lodging_cost_per_day']  = transactions['Lodging_total'] / transactions['daysTravelled']



cols = ['variable_cost_per_day', 'misc_ratio', 'misc_cost_per_day','lodging_cost_per_day','Public_Transportation_cost_per_day','Parking_cost_per_day','trip_count']
df = transactions[cols]
df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna()
result = sm.ols(formula = 'variable_cost_per_day ~ misc_ratio + lodging_cost_per_day + trip_count',data=df).fit()



print(result.summary())

total_fields= [
 'Communication Serv_total',
 'Laundry_total',
 'M&IE-PerDiem',
 'Meals Actuals',
 'Mileage - Private Airplane',
 'Mileage - Priv Auto (Advantageous)',
 'Mileage - Priv Auto (GOV Avail/Not Used)',
 'Mileage - Priv Motorcycle',
 'Misc Expense_total',
 'Registration Fees_total',
 'Rental Car_total',
 'Rental Car - Gasoline_total',
 'Rental Car - Optional Equipment',
 'Spec Med Needs Empl',
 'Service Fees',
 'Highway/Bridge Tolls_total',
 'Limousine Service',
 'Parking_total',
 'Public Transportation_total',
 'Seat Selection Fee',
 'Shuttle - Air',
 'Shuttle - Ground',
 'Taxi_total']

card_fields = ['Airline Flight_card',
 'Communication Serv_card',
 'Highway/Bridge Tolls_card',
 'Laundry_card',
 'Misc Expense_card',
 'Parking_card',
 'Public Transportation_card',
 'Registration Fees_card',
 'Rental Car_card',
 'Rental Car - Gasoline_card',
 'Taxi_card']

transactions['card_total'] = transactions[card_fields].sum(axis=1)

transactions['total_cost'] = transactions[total_fields].sum(axis=1)


transactions['total_ratio'] = transactions['card_total'] / transactions['total_cost']

transactions['cost_per_day'] = transactions['total_cost'] / transactions['daysTravelled']
transactions['card_per_day'] = transactions['card_total'] / transactions['daysTravelled']
transactions['lodging_cost_per_day']  = transactions['Lodging_total'] / transactions['daysTravelled']


transactions['log_card_per_day'] = np.log(transactions['card_per_day'])
transactions['log_total_per_day'] = np.log(transactions['cost_per_day'])

cols = ['cost_per_day','log_total_per_day','lodging_cost_per_day' ,'log_card_per_day','card_per_day', 'total_ratio','trip_count']
df = transactions[cols]
df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna()

df= df[df.total_ratio <= 1]
result = sm.ols(formula = 'log_total_per_day ~ total_ratio + lodging_cost_per_day +trip_count',data=df).fit()
print(result.summary())

df.plot.scatter(x='total_ratio', y='log_total_per_day', c='DarkBlue')



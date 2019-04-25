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




class Segment():
    
    def __init__(self):
        '''
        any fields that need to be created for the overall data, do not remove/subset change data here
        
        '''
        data  = pd.read_csv('data/by_segment.csv')

        #calculate dash CA contract per mile
        data['dash_per_mile'] = data.XCA_FARE / data.nsmiles
        
        #calculate yca per mile
        data['YCA_per_mile'] = data.YCA_FARE / data.nsmiles
        
        #calculate actual cost per mile travelled
        data['cost_per_mile'] = data.paid_fare_including_taxes_and_fees / data.nsmiles
        
        #calculate ratio of XCA to YCA contract 
        data['city_pair_ratio'] = data.dash_per_mile / data.YCA_per_mile



        self.data = data

    class model_1(object):
        '''
        Model 1 looks at the ratio of YCA fare to XCA fare and the effect on price
        '''
        def __init__(self):
            '''
            
            This is the logic for data subsetting and any changes to the data
            '''
            print("preparing data")
            data = Segment().data
            
            # only took fares with actual cost
            data  = data[data['paid_fare_including_taxes_and_fees'] >0 ]

            #cornerstone can not get accurate segment data when they have split fare_types 
            #i removed them here so i only take
            data  = data[data.YCA_y != 1 ]
            data = data[data.DashCA_y != 1 ]
            
            #only take flights with a simple go and return trip
            data  = data[data.count_y == 2 ]
            
            #only flights where city pair has awarded a contract
            data  = data[data.awarded ==1 ]   
            
            #filter for coach fares
            fare = ['YCA','Dash CA','Other','DG']
            data = data[data.fare_type.isin(fare)]
            
            #take only city pairs with atleast 50 flights
            df_g = data
            df_g['ticket'] = 1
            df_g = df_g[['city_pair_code','ticket']]
            df_g = df_g.groupby(by ='city_pair_code',as_index=False).sum()
            a = df_g[df_g.ticket > 50]
            codes = list(a.city_pair_code)
            data = data[data.city_pair_code.isin(codes)]
            
            self.model_data = data
    
        def regression_1(self):
            '''
            
            
            '''
            result = sm.ols(formula = 'cost_per_mile ~ city_pair_ratio +no_CA_award + fare_type + city_pair_code',data=self.model_data).fit()
            #print(result.summary())
            return result


        def regression_2(self):
            result = sm.ols(formula = 'cost_per_mile ~ city_pair_ratio + fare_type + no_CA_award + ticketing_adv_booking_group ' ,data=self.model_data).fit()
            #print(result.summary())
            return result

        def regression_3(self):
            '''
            
            
            '''
            result = sm.ols(formula = 'cost_per_mile ~ city_pair_ratio + fare_type + fare_type*city_pair_ratio  + ticketing_adv_booking_group  + airline_carrier + city_pair_code',data=self.model_data).fit()
            #print(result.summary())
            return result

        def regression_4(self):
            '''
            
            
            '''
            result = sm.ols(formula = 'cost_per_mile ~ city_pair_ratio + fare_type + fare_type*city_pair_ratio + no_CA_award + ticketing_adv_booking_group + + airline_carrier + ticketing_adv_booking_group*fare_type + city_pair_code',data=self.model_data).fit()
            #print(result.summary())
            return result








model = Segment().model_1()      
res1 = model.regression_1()
res2 = model.regression_2()
res3 = model.regression_3()
res4 = model.regression_4()

from statsmodels.iolib.summary2 import summary_col
dfoutput = summary_col([res1,res2,res3,res4],stars=True)
print(dfoutput)



#logistic regressions


class transactions:
    def __init__(self):
        
        self.transactions = pd.read_csv('data/by_person.csv')

    def prepare(self):
        transactions = self.transactions
        #calculate vairable expenses
        transactions['total_variable_expense'] =  transactions['Charge Card Fees'] +transactions[ 'Laundry_total']+transactions['M&IE-PerDiem']+transactions[ 'Meals Actuals']+transactions['Misc Expense_total']+transactions['Parking_total']+transactions['Public Transportation_total']+transactions['Taxi_total']
        transactions['variable_cost_per_day'] = transactions['total_variable_expense'] / transactions['daysTravelled']
        
        #calculate only misc expenses
        transactions['misc_cost_per_day'] = transactions['Misc Expense_card'] / transactions['daysTravelled']
        transactions['misc_ratio'] =  transactions['Misc Expense_card']  / ( transactions['M&IE-PerDiem']+ transactions['Misc Expense_total']+ transactions['Meals Actuals'])


        #caluclate Taxi cost per day
        transactions['Taxi_per_day'] = transactions['Taxi_card'] / transactions['daysTravelled']
        
        #calculate Pub lic transportation cost per data
        transactions['Public_Transpxortation_cost_per_day'] = transactions['Public Transportation_card'] / transactions['daysTravelled']
        
        #parking cost per day
        transactions['Parking_cost_per_day'] = transactions['Parking_card'] / transactions['daysTravelled']

        #lodging cost per day
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



df= pd.read_csv('data/by_trip.csv')






df = pd.read_csv('data/train_plane.csv')       
train = df[df.train == 1]  
train_g = train.groupby(by='city_pair',as_index=False).sum()
train_g = train_g[['city_pair','train']]
plane = df[df.plane ==1]
plane_g = plane.groupby(by='city_pair',as_index=False).sum()
plane_g = plane_g[['city_pair','plane']]

merged = pd.merge(plane_g,train_g,on='city_pair',how='inner')


a = merged[(merged.plane >= 15) & (merged.train >= 15)]

df = pd.merge(df,a,on='city_pair',how='inner')

df = df[df.fare_combined >0]



df = df[df.segments_combined == 2]



df['type'] = df['fare_type'].fillna(df['Class of Service'])


df['type'] = df["type"].replace(1, "Train") 
fare = ['YCA','Dash CA','DG','Acela Business Class Seat', 'Coach Reserved Seat']
df = df[df.type.isin(fare)]



df['grade'] = df.GRADE_CODE.str[:2]


route = ['New York-Washington','Philadelphia-Richmond','Boston-New York']
df = df[df.city_pair.isin(route)]

result = sm.ols(formula = 'fare_combined ~ type + trip_duration + grade',data=df).fit()
print(result.summary())

result = sm.ols(formula = 'fare_combined ~ train_x ',data=df).fit()
print(result.summary())


gradeKeep = ['11','12','13','14','15']
df_grade = df[df.grade.isin(gradeKeep)]

result = sm.ols(formula = 'train_x ~ grade + city_pair',data=df_grade).fit()
print(result.summary())


df = df.fillna(0)
travel_cost =[ 'Mileage - Private Airplane',
 'Mileage - Priv Auto (Advantageous)',
 'Mileage - Priv Auto (GOV Avail/Not Used)',
 'Mileage - Priv Motorcycle',
 'Misc Expense',
 'Registration Fees',
 'Rental Car',
 'Rental Car - Gasoline',
 'Rental Car - Optional Equipment',
 'Spec Med Needs Empl',
 'Service Fees',
 'Highway/Bridge Tolls',
 'Limousine Service',
 'Parking',
 'Public Transportation',
 'Seat Selection Fee',
 'Shuttle - Air',
 'Shuttle - Ground',
 'Taxi',
 'fare_combined']
df['variable_travel_cost'] = df[travel_cost].sum(axis=1)


result = sm.ols(formula = 'variable_travel_cost ~ type + trip_duration',data=df).fit()
print(result.summary())
result = sm.ols(formula = 'variable_travel_cost ~ train_x + trip_duration',data=df).fit()
print(result.summary())


train['classS']= train['Class of Service']
train = train[train.segments_combined == 2]
train = train[train.traineDif > 0]



result = sm.ols(formula = 'fare_combined ~ traineDif + classS + miles',data=regDF).fit()
print(result.summary())



df = pd.read_csv('data/by_trip.csv')

df['travel_fees'] = df['Travel Transxn Fees']
cols =['travel_fees','self_booking_indicator', 'GRADE_CODE', 'refund','exchange']
reg = df[cols]

reg = reg.dropna()
reg = reg[reg.GRADE_CODE != '0']


result = sm.ols(formula = 'travel_fees ~ self_booking_indicator + GRADE_CODE + refund + exchange',data=reg).fit()
print(result.summary())

df['airline_total'] = df['Travel Transxn Fees'] + df['paid_fare_including_taxes_and_fees']
cols =['airline_total','self_booking_indicator', 'GRADE_CODE', 'refund','exchange','trip_duration']

reg = df[cols]

reg = reg.dropna()
reg = reg[reg.GRADE_CODE != '0']

reg['no_travel'] = np.where(reg['trip_duration']==0, 1, 0)


result = sm.ols(formula = 'airline_total ~ self_booking_indicator + GRADE_CODE + refund + exchange',data=reg).fit()
print(result.summary())

reg['no_travel'] = np.where(reg['trip_duration']==0, 1, 0)

result = sm.ols(formula = 'airline_total ~ city_pair_code +self_booking_indicator + trip_duration + number_of_segments + refund + exchange + total_flight_miles  ',data=df).fit()
print(result.summary())




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
from models.columns import  segment_columns , transaction_columns



class Segment():
    
    def prepare(self):
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



        return data

    def __str__(self):
        return 'flight route and cost by segement of trip '
    
    def __repr__(self):
        return '[{}]'.format( ', '.join(  i  for i in dir(self) if i.startswith('mod')))

    @staticmethod    
    def columns_to_keep():
        cols =[]
        for i in segment_columns:
            if segment_columns[i]['keep']:
                cols.append(i) 
        return cols
    
    @staticmethod
    def describe(col_name):
        for i in segment_columns:
            if i == col_name:
                print(segment_columns[i]['description'] )
    
    class model_1(object):
        '''
        Model 1 looks at the ratio of YCA fare to XCA fare and the effect on price
        '''
        def __init__(self):
            '''
            
            This is the logic for data subsetting and any changes to the data
            '''
            print("preparing data")
            data = Segment().prepare()
            
            # only took fares with actual cost
            data  = data[data['paid_fare_including_taxes_and_fees'] > 30 ]

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
            
            
            #
            data['market_share_log'] = np.log(data['large_ms'])
            data['market_share_sq'] = data.large_ms * data.large_ms
            
            #keep only the data we need
            cols_to_keep = Segment().columns_to_keep()
            data = data[cols_to_keep]
            
            self.model_data = data
       
        def __str__(self):
            return "This model looks at the ratio of YCA fare to XCA fare and the effect on price"
        
        def __repr__(self):
            return '[{}]'.format( ', '.join(  i  for i in dir(self) if i.startswith('reg')))

        
        def regression_1(self):
            '''
            
            
            '''
            result = sm.ols(formula = 'cost_per_mile ~ city_pair_ratio +no_CA_award + market_share_log + fare_type +  ticketing_adv_booking_group + city_pair_code ',data=self.model_data).fit()
            print(result.summary())
            return result


        def regression_2(self):
            result = sm.ols(formula = 'cost_per_mile ~ city_pair_ratio + fare_type + no_CA_award + market_share_log + ticketing_adv_booking_group + city_pair_code  ' ,data=self.model_data).fit()
            #print(result.summary())
            return result

        def regression_3(self):
            '''
            
            
            '''
            result = sm.ols(formula = 'cost_per_mile ~ city_pair_ratio +  fare_type + market_share_log + fare_type*city_pair_ratio  + ticketing_adv_booking_group  + city_pair_code',data=self.model_data).fit()
            #print(result.summary())
            return result

        def regression_4(self):
            '''
            
            
            '''
            result = sm.ols(formula = 'cost_per_mile ~ city_pair_ratio + fare_type  + market_share_log  + fare_type*city_pair_ratio + no_CA_award + ticketing_adv_booking_group  + ticketing_adv_booking_group*fare_type + city_pair_code',data=self.model_data).fit()
            #print(result.summary())
            return result

    class model_2(object):
        '''
        This will be a logistic regression predicing various fare-types
        
        '''
        def __init__(self):
            return None
        
        def regression_1(self):
            return None
        




class Transactions():
    
    def prepare(self):
        
        transactions = pd.read_csv('data/by_person.csv')

   
        
        #calculate vairable expenses
        transactions['total_variable_expense'] =  transactions['Charge Card Fees'] +transactions[ 'Laundry_total']+transactions['M&IE-PerDiem_total']+transactions[ 'Meals Actuals']+transactions['Misc Expense_total']+transactions['Parking_total']+transactions['Public Transportation_total']+transactions['Taxi_total']
        transactions['variable_cost_per_day'] = transactions['total_variable_expense'] / transactions['daysTravelled']
        
        #calculate only misc expenses
        transactions['misc_card_per_day'] = transactions['Misc Expense_card'] + transactions['M&IE-PerDiem_card'] / transactions['daysTravelled']
        transactions['misc_ratio'] =  transactions['Misc Expense_card']  / ( transactions['M&IE-PerDiem_total']+ transactions['Misc Expense_total']+ transactions['Meals Actuals'])
        
        transactions['M&IE_card_per_day'] =  transactions['M&IE-PerDiem_card'] / transactions['daysTravelled']
        transactions['M&IE_cost_per_day'] =  transactions['M&IE-PerDiem_total'] / transactions['daysTravelled']
        
        #caluclate Taxi cost per day
        transactions['Taxi_card_per_day'] = transactions['Taxi_card'] / transactions['daysTravelled']
        
        #calculate Pub lic transportation cost per data
        transactions['Public_card_Transportation_per_day'] = transactions['Public Transportation_card'] / transactions['daysTravelled']
        
        #parking cost per day
        transactions['Parking_card_per_day'] = transactions['Parking_card'] / transactions['daysTravelled']

        #lodging cost per day
        transactions['lodging_cost_per_day']  = transactions['Lodging_total'] / transactions['daysTravelled']
        
         #lodging cost per day
        transactions['lodging_card_per_day']  = transactions['Lodging_card'] / transactions['daysTravelled']
        
        #creat column that creats all cost on card total
        transactions['card_total'] = transactions[transaction_columns['card_fields']].sum(axis=1)
        
        #create columns for total cost
        transactions['total_cost'] = transactions[transaction_columns['total_fields']].sum(axis=1)
        
        #how much money on card to not
        transactions['total_ratio'] = transactions['card_total'] / transactions['total_cost']
        
        #costs day
        transactions['cost_per_day'] = transactions['total_cost'] / transactions['daysTravelled']
        transactions['card_per_day'] = transactions['card_total'] / transactions['daysTravelled']
        transactions['lodging_cost_per_day']  = transactions['Lodging_total'] / transactions['daysTravelled']
        
        #log cost and card per day
        transactions['log_card_per_day'] = np.log(transactions['card_per_day'])
        transactions['log_total_per_day'] = np.log(transactions['cost_per_day'])
        
        #if credit card was not used a 0 for all fields
        transactions= transactions.fillna(0)
        return transactions
    
    def __str__(self):
        return 'his data is aggregated by person by year.  It is good for analysis with credit card transactions'
    
    def __repr__(self):
        return '[{}]'.format( ', '.join(  i  for i in dir(self) if i.startswith('mod')))


    class model_1(object):
        '''
        summary of what we expect from this model
        '''
        def __init__(self):
            self.model_data = Transactions().prepare()
            '''
            any modifications for just this model here
            '''
        def regression_1(self):
            cols = ['variable_cost_per_day', 'misc_ratio', 'misc_cost_per_day','lodging_cost_per_day','Public_Transportation_cost_per_day','Parking_cost_per_day','trip_count']
            df = self.model_data[cols]
            df = df.replace([np.inf, -np.inf], np.nan)
            df = df.dropna()
            result = sm.ols(formula = 'variable_cost_per_day ~ misc_ratio + lodging_cost_per_day + trip_count',data=df).fit()
            print(result.summary())
            return result
        
        def regression_2(self):   

           
            
            cols = ['cost_per_day','log_total_per_day','lodging_cost_per_day' ,'log_card_per_day','card_per_day', 'total_ratio','trip_count']
            df = self.model_data[cols]
            df = df.replace([np.inf, -np.inf], np.nan)
            df = df.dropna()
            
            df= df[df.total_ratio <= 1]
            result = sm.ols(formula = 'log_total_per_day ~ total_ratio + lodging_cost_per_day +trip_count',data=df).fit()
            print(result.summary())



        def graph(self):
            graphs = {}
            one = self.model_data.plot.scatter(x='total_ratio', y='log_total_per_day', c='DarkBlue')
            graphs.update({"scatter":one})
            return graphs




class Train_Plane:
   
    def prepare(self):   
        df = pd.read_csv('data/train_plane.csv') 
        
        
        #clean up grade code
        df['grade'] = df.GRADE_CODE.str[:2]
    
        #merge plan and train fare types into one
        df['type'] = df['fare_type'].fillna(df['Class of Service'])

        #replace train value with "train"
        df['type'] = df["type"].replace(1, "Train") 
        print("data in")
        return df
    
    def __str__(self):
        return 'This data is aggregated bytrip and combines train and planes into one.  It is good for analysis when you want to use both trains and planes'
    
    def __repr__(self):
        return '[{}]'.format( ', '.join(  i  for i in dir(self) if i.startswith('mod')))
        
    class model_1(object):
        
        def __init__(self):
            df = Train_Plane().prepare()
    
            print("two")
            #only take data with more than 15 trips per route
            train = df[df.train == 1]  
            train_g = train.groupby(by='city_pair',as_index=False).sum()
            train_g = train_g[['city_pair','train']]
     
            print("three")
            plane = df[df.plane ==1]
            plane_g = plane.groupby(by='city_pair',as_index=False).sum()
            plane_g = plane_g[['city_pair','plane']]
            
            merged = pd.merge(plane_g,train_g,on='city_pair',how='inner')
            
            
            a = merged[(merged.plane >= 15) & (merged.train >= 15)]

            df = pd.merge(df,a,on='city_pair',how='inner')

            #only take positive values
            df = df[df.fare_combined >0]

            #only take go and return trips
            df = df[df.segments_combined == 2]

            
            #only take regular class fares
            fare = ['YCA','Dash CA','DG','Acela Business Class Seat', 'Coach Reserved Seat']
            df = df[df.type.isin(fare)]
            
            print("four")
            self.model_data = df  
            
        def regression_1(self):
            df = self.model_data
            #compare only most common routes
            route = ['New York-Washington','Philadelphia-Richmond','Boston-New York']
            df = df[df.city_pair.isin(route)]
            
            result = sm.ols(formula = 'fare_combined ~ type  + city_pair',data=df).fit()
            print(result.summary())
        def regression_2(self):
            
            df = self.model_data
            
            #compare only mose common routes
            route = ['New York-Washington','Philadelphia-Richmond','Boston-New York']
            df = df[df.city_pair.isin(route)]
            
            result = sm.ols(formula = 'fare_combined ~ train_x ',data=df).fit()
            print(result.summary())

        def regression_3(self):
            
            df = self.model_data
            
            #compare only mose common routes
            route = ['New York-Washington','Philadelphia-Richmond','Boston-New York']
            df = df[df.city_pair.isin(route)]
            
            #keep only most common grades
            gradeKeep = ['11','12','13','14','15']
            df_grade = df[df.grade.isin(gradeKeep)]

            result = sm.ols(formula = 'train_x ~ grade + city_pair',data=df_grade).fit()
            print(result.summary())
            
    class model_2(object):
        def __init__(self):
            df = Train_Plane().prepare()
    

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
            
            #only take positive values
            df = df[df.fare_combined >0]

            #only take go and return trips
            df = df[df.segments_combined == 2]

            #only take regular class fares
            fare = ['YCA','Dash CA','DG','Acela Business Class Seat', 'Coach Reserved Seat']
            df = df[df.type.isin(fare)]
            
            self.model_data = df
            
        def regression_1(self):
            
            result = sm.ols(formula = 'variable_travel_cost ~ type + trip_duration',data=self.model_data).fit()
            print(result.summary())


        def regression_2(self):
            result = sm.ols(formula = 'variable_travel_cost ~ train_x + trip_duration',data=self.model_data).fit()
            print(result.summary())


    class model_3(object):
       
        def __init__(self):
            df = Train_Plane().prepare()
        
        
            #only take data with more than 15 trips per route
            train = df[df.train == 1] 
            
            #create new columns without any spaces (i know i can rename it)
            train['classS']= train['Class of Service']
            
            # take only segemnts with out and back travel
            train = train[train.segments_combined == 2]
            
            # if travel took longer than than 0 
            train = train[train.traineDif > 0]

            self.train = train
        
        def regression_1(self):
            
            result = sm.ols(formula = 'fare_combined ~ traineDif + classS + miles',data=self.train).fit()
            print(result.summary())



class Trip():
    def prepare(self):

        df = pd.read_csv('data/by_trip.csv')
        
        return df
    
    def __str__(self):
        return 'This is an aggregate level view of trip level data. It merges on total trip exepenses. and calculates flight cost based on segment level data'
    
    def __repr__(self):
        return '[{}]'.format( ', '.join(  i  for i in dir(self) if i.startswith('mod')))

    class model_1(object):
        def __init__(self):
            
            df = Trip().prepare()
            #rename travel fees
            df['travel_fees'] = df['Travel Transxn Fees']
            
            #take only these columns
            cols =['travel_fees','self_booking_indicator', 'GRADE_CODE', 'refund','exchange']
            df = df[cols]
        
            # drop NAs
            df = df.dropna()
            
            #exclude when grade is not known
            df = df[df.GRADE_CODE != '0']
            
            self.model_data = df
        def regression_1(self):
            
            result = sm.ols(formula = 'travel_fees ~ self_booking_indicator + GRADE_CODE + refund + exchange',data=self.model_data).fit()
            print(result.summary())

    class model_2(object):
        
        def __init__(self):
            df =Trip().prepare()

            # airline total cost
            df['airline_total'] = df['Travel Transxn Fees'] + df['paid_fare_including_taxes_and_fees']
            
            #only take certain columns
            cols =['airline_total','self_booking_indicator', 'GRADE_CODE', 'refund','exchange','trip_duration']
            df = df[cols]

            #drop NAs
            df = df.dropna()
            
            #drop when grade in unkowns
            df = df[df.GRADE_CODE != '0']
            
            self.model_data = df

        def regression_1(self):
        
            result = sm.ols(formula = 'airline_total ~ self_booking_indicator + GRADE_CODE + refund + exchange',data=self.model_data).fit()
            print(result.summary())

    class model_3(object):
        def __init__(self):
            df =Trip().prepare()
            
             # airline total cost
            df['airline_total'] = df['Travel Transxn Fees'] + df['paid_fare_including_taxes_and_fees']
            
            self.model_data = df
        def regression_1(self):
            
            result = sm.ols(formula = 'airline_total ~ city_pair_code +self_booking_indicator + trip_duration + number_of_segments + refund + exchange + total_flight_miles  ',data=self.model_data).fit()
            print(result.summary())







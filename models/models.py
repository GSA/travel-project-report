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
from models.columns import  segment_columns , transaction_columns, aggregate_fields,trip_columns
from sklearn import preprocessing

class Route():
    
    def prepare(self):
        data = pd.read_csv('data/by_route.csv')
        
        #calculate cost per mile
        data['cost_per_mile'] = data.paid_fare_including_taxes_and_fees / data.miles

        return data
    
    class model_1(object):
        
        def __init__(self):
            
            data = Route().prepare()
            
            # only non Y
            data = data[data['fare_type'] != 'Y']
            
            self.model_data = data
        
        def regression_1(self):
            '''
            this regression looks at business fares and compares them against the government fares using interaction effects with booking lead time
            '''
            result = sm.ols(formula = "cost_per_mile ~   C(Year) + ticketing_adv_booking_group  + C(fare_type, Treatment(reference='YCA')) +C(fare_type, Treatment(reference='YCA'))*ticketing_adv_booking_group +  city_pair_code",data=self.model_data).fit()
            print(result.summary())
            
            return result

class Segment():
    
    def prepare(self):
        '''
        any fields that need to be created for the overall data, do not remove/subset change data here
        
        '''
        data  = pd.read_csv('data/by_segment.csv')

        #calculate dash CA contract per mile
        data['dash_per_mile'] = data.XCA_FARE / data.miles
        
        #calculate yca per mile
        data['YCA_per_mile'] = data.YCA_FARE / data.miles
        
        #calculate actual cost per mile travelled
        #data['cost_per_mile'] = data.paid_fare_including_taxes_and_fees / data.miles
        data['cost_per_mile'] = data.base_fare / data.miles
        
        #calculate ratio of XCA to YCA contract 
        data['city_pair_ratio'] = data.dash_per_mile / data.YCA_per_mile
        
        #get region 
        data['region'] = data.Organization.str.extract('(\d+)')
        data['region'] = data.region.fillna('CO')
        
        #get bureau
        data['bureau'] = data.Organization.str.extract("([^GSA\W\d])")
        
        #get grade
        data['grade'] = data.GRADE_CODE.str[:2]
        
        #datetime of departure date
        data['segment_departure_date'] = pd.to_datetime(data.segment_departure_date)
        
        #datetime booking
        data['ticket_booking_date'] = pd.to_datetime(data.ticket_booking_date)
        
        #booking days calculated
        data['booking_advanced_days'] =(data.segment_departure_date  - data.ticket_booking_date).dt.days
        
        
        
        
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
            
            # only took fares with actual cost. some data has low cost like $7 which i determined was either an exchange not specified or bad data
            data  = data[data['paid_fare_including_taxes_and_fees'] > 30 ]

            #cornerstone can not get accurate segment data when they have split fare_types 
            #i removed them here so i only take when not split fare
            data  = data[data.YCA_y != 1 ]
            data = data[data.DashCA_y != 1 ]
            
            #only take flights with a simple go and return trip
            data  = data[data.count_y == 2 ]
            
            #only flights where city pair has awarded a contract
            data  = data[data.awarded ==1 ]   
            
            #filter for coach fares
            fare = ['YCA','Dash CA','Other','DG']
            data = data[data.fare_type.isin(fare)]
            
            #take only city pairs with atleast 40 flights
            df_g = data
            df_g['ticket'] = 1
            df_g = df_g[['city_pair_code','ticket']]
            df_g = df_g.groupby(by ='city_pair_code',as_index=False).sum()
            a = df_g[df_g.ticket > 40]
            codes = list(a.city_pair_code)
            data = data[data.city_pair_code.isin(codes)]
            
            #only if booked with positive days
            data = data[data['booking_advanced_days'] >= 0]
            
            #log of market share
            data['market_share_log'] = np.log(data['large_ms'])
            
            #only take economy 
            data = data[data['cabin_svc_class_of_segment'] == 'ECONOMY']
            
            #days of week and month 
            data['day_of_week'] = data['segment_departure_date'].dt.weekday_name
            data['month'] = data['segment_departure_date'].dt.month
            
            #days logged transformed
            print("doing actual log")
            data['booking_days_log'] = np.log10(data['booking_advanced_days']+1)
            
            #standarize the booking days
            x = data[['booking_advanced_days']].values 
            min_max_scaler = preprocessing.MinMaxScaler()
            x_scaled = min_max_scaler.fit_transform(x)
            df2 = pd.DataFrame(x_scaled)
            data = data.reset_index()
            data = data.join(df2,how='inner')
            data = data.rename(columns={0:'booking_days_standarized'})
            
            #keep only the data we need
            cols_to_keep = Segment().columns_to_keep()
            data = data[cols_to_keep]
            
            data['city_pair_ratio_2'] = data['city_pair_ratio'] * data['city_pair_ratio']
            
            self.model_data = data
       
        def __str__(self):
            return "This model looks at the cost per mile and various effects upon price"
        
        def __repr__(self):
            return '[{}]'.format( ', '.join(  i  for i in dir(self) if i.startswith('reg')))

        
        def regression_1(self):
            '''
            
            
            '''
            result = sm.ols(formula = "cost_per_mile ~   market_share_log  + month + day_of_week + C(Year) + no_CA_award + booking_days_log + booking_days_log*C(fare_type, Treatment(reference='Dash CA')) + city_pair_code + self_booking_indicator",data=self.model_data).fit()
            print(result.summary())
            return result


        def regression_2(self):
            result = sm.ols(formula = 'cost_per_mile ~ city_pair_ratio + fare_type + no_CA_award + market_share_log + ticketing_adv_booking_group + city_pair_code  ' ,data=self.model_data).fit()
            #print(result.summary())
            return result

        def regression_3(self):
            df = self.model_data
            df['CPP'] = df.DashCA_x + df.YCA_x
            df['ratio_squared'] = df.city_pair_ratio * df.city_pair_ratio
            result = sm.logit(formula = 'CPP ~ dash_per_mile + YCA_per_mile + PAX_COUNT + cost_per_mile + market_share_log + booking_advanced_days +city_pair_ratio + c_squared',data=df).fit()
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
        '''
        data prep work, use this space to construct all new variables 
        
        '''
        
        transactions = pd.read_csv('data/by_person.csv')
        
        #true days of travel started at 0. 
        transactions['days'] = transactions.daysTravelled + (1*transactions.trip_count)
        
        #loop through and create aggreate fields based on the type of cost
        for column in aggregate_fields:
            transactions[column] = transactions[Transactions().get_columns(aggregate_fields[column])].sum(axis=1)
            transactions[column+"_per_day"] = transactions[column] / transactions['days']
        
        #if credit card was not used a 0 for all fields
        transactions= transactions.fillna(0)
    
        
        # if for some reason there are inf convert them to 0s 
        transactions = transactions.replace(np.inf, 0)
        
        return transactions
    
    def __str__(self):
        return 'This data is aggregated by person by year.  It is good for analysis with credit card transactions'
    
    def __repr__(self):
        return '[{}]'.format( ', '.join(  i  for i in dir(self) if i.startswith('mod')))

    @staticmethod    
    def columns_to_keep():
        cols =[]
        for i in transaction_columns:
            if transaction_columns[i]['keep']:
                cols.append(i) 
        return cols
    
    
    @staticmethod
    def describe(col_name):
        for i in transaction_columns:
            if i == col_name:
                print(transaction_columns[i]['description'] )
    
    @staticmethod
    def get_columns(type_and_source):
        s = []
        for i in transaction_columns:
            field =  transaction_columns[i]['type'] +" " + transaction_columns[i]['source']
            if field == type_and_source:
               s.append(i)
        return s        
                
    class model_1(object):
        '''
        summary of what we expect from this model
        '''
        def __init__(self):
            data = Transactions().prepare()
            
            
            cols_to_keep = Transactions().columns_to_keep()
            data = data[cols_to_keep]
            
            self.model_data = data
            
        def regression_1(self):
            None
        
        def regression_2(self):   
            
            None


        def graph(self):
            graphs = {}
            return graphs

    class model_2(object):
        def __init__(self):
            transactions = Transactions().prepare()
            cols_to_keep = Transactions().columns_to_keep()
            transactions = transactions[cols_to_keep]
            
            trip = Trip().prepare()
            
            transactions = transactions[transactions.trip_count ==1]
            trip['invoice_date'] = pd.to_datetime(trip.invoice_date)

            trip['fiscal_year'] = trip.invoice_date.apply(pd.Period, freq='A-SEP').dt.year
            transactions['fiscal_year'] = pd.to_datetime(transactions['FY'],format='%Y').dt.year
            
            self.model_data = pd.merge(transactions,trip[trip_columns],left_on=['Employee Email Address','FY'],right_on=['EMAIL','fiscal_year'],how='inner')
            
        def regression_1(self):
            None
        
        def regression_2(self):   
            
            None

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
            fare = ['YCA','Dash CA','Acela Business Class Seat', 'Coach Reserved Seat']
            df = df[df.type.isin(fare)]
            df['cost_per_mile'] = df.fare_combined / df.miles
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
            #route = ['New York-Washington','Philadelphia-Richmond','Boston-New York']
            #df = df[df.city_pair.isin(route)]
            
            #keep only most common grades
            #gradeKeep = ['11','12','13','14','15']
            #df_grade = df[df.grade.isin(gradeKeep)]

            result = sm.ols(formula = 'fare_combined ~ train_x + miles',data=df).fit()
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



class Quarter():
    def prepare(self):

        df = pd.read_csv('data/by_quarter.csv')
        
        return df
    
    def __str__(self):
        return 'This is an aggregate level by quarter if segement routes'
    
    def __repr__(self):
        return '[{}]'.format( ', '.join(  i  for i in dir(self) if i.startswith('mod')))

    class model_1(object):
        def __init__(self):
            
            df = Quarter().prepare()
            
            
            self.model_data = df
        def regression_1(self):
            
            ##esult = sm.ols(formula = 'travel_fees ~ self_booking_indicator + GRADE_CODE + refund + exchange',data=self.model_data).fit()
            #print(result.summary())
            print(None)


            
 


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 08:32:31 2019

@author: austinpeel
"""
import pandas as pd
import numpy as np
#from geotext import GeoText



def get(df):
    df = keep_certain(df)
    df = apply_new_columns(df)
    cities = get_unique_city_list(df)
    df = merge_records(df,cities)
    df = get_city_pair(df)
    df = merge_miles(df)
    miles = df.drop_duplicates(subset='city_pair_code')
    miles = miles[['city_pair_code','city_pair','miles']]
    miles.to_csv('data/city_pair_info/miles.csv')

    #df =df[cols]
    df.to_csv("data/train_plane.csv")
    
def keep_certain(df):
    df['train'] = np.where(df.legs > 0,1,0)
    df['plane'] = np.where(df.no_of_tickets > 0,1,0)
    condition = ((df.train ==1) & (df.plane ==1))
    df = df[~condition]
    return(df)

def apply_new_columns(df):
    
    df['ticket_departure_date'] = pd.to_datetime(df.ticket_departure_date)
    df['booking_date'] = pd.to_datetime(df.booking_date)
    
    df['Departure Date/Time'] = pd.to_datetime(df['Departure Date/Time'])
    df['Purchased Date'] = pd.to_datetime(df['Purchased Date'])
    
    df['planeDif'] =(df.ticket_departure_date  - df.booking_date).dt.days
    df['traineDif'] = (df['Departure Date/Time'] - df['Purchased Date'] ).dt.days
    df['dif'] = df['planeDif'].fillna(df['traineDif'])
    
    df['departure_combined'] = df['origin_city_name'].fillna(df['Departure Location'])
    df['arrival_combined'] = df['destination_city_name'].fillna(df['Arrival Location'])
    
    df["departure_combined"]= df["departure_combined"].replace("NEW YORK, NEW YORK, US", "New York, NY") 
    df["arrival_combined"]= df["arrival_combined"].replace("NEW YORK, NEW YORK, US", "New York, NY") 
   
    
    df['segments_combined'] = df['number_of_segments'].fillna(df['legs'])
    
    
    df['fare_combined'] = df['paid_fare_including_taxes_and_fees'].fillna(df['Total Rail Amount'])
    df['fare_combined2'] = df['Airline Flight'].fillna(df['Total Rail Amount'])
    return df



def get_unique_city_list(df):
    cities = list(df['departure_combined'].unique())
    
    cities2 = list(df['arrival_combined'].unique())
    cities.extend(x for x in cities2 if x not in cities)
    records = pd.DataFrame(cities)
    return records


#from geopy.geocoders import Nominatim
#geolocator = Nominatim(user_agent="specify_your_app_name_here")
#from geopy.distance import geodesic

def lat_and_long(city):
    try:
        location = geolocator.geocode(city) 
        return location.latitude, location.longitude
    except:
        return None, None

def get_clean_cities(city):
    try:
        place = GeoText(city)
        return place.cities[0]
    except:
        return "no place matched"


def get_distance(lat1,long1,lat2,long2):  
    city1 = (lat1,long1)
    city2 = (lat2,long2)
    try:
        miles = geodesic(city1, city2).miles
        print(miles)
        print(city1,city2)
    except:
        miles= None
    return miles

def merge_miles(df):
    cities = pd.DataFrame(np.unique(df[['lat_a','long_a','lat_d','long_d']],axis=0))
    cities = cities.rename(columns={0:'lat_a',1:'long_a',2:'lat_d',3:'long_d'})
    cities['miles'] = cities.apply(lambda x: get_distance(x.lat_a, x.long_a,x.lat_d,x.long_d), axis=1)
    df = pd.merge(df,cities,on=['lat_a','long_a','lat_d','long_d'],how='left')
    return df

def merge_records(df,records):
    records['departure_clean'] = records[0].apply(get_clean_cities)
    records[['lat_d','long_d']] = records[0].apply(lat_and_long).apply(pd.Series)
    records = records.rename(columns={0:'departure_combined'})
    df = pd.merge(df,records,on="departure_combined",how='left')
    
    
    records = records.rename(columns={'departure_combined':'arrival_combined','departure_clean':'arrival_clean','lat_d':'lat_a','long_d':'long_a'})
    
    df = pd.merge(df,records,on="arrival_combined",how='left')
    
    return df


def get_city_pair(df):
    print("getting unique city pair, this takes a little time, janky code")
    for index, row  in df.iterrows():
        try:
            city_sorted = sorted(list([str(row['departure_clean']),str(row['arrival_clean'])]))
            city_pair = "-".join(str(e)for e in city_sorted)
            df.loc[index,'city_pair'] = city_pair
        except:
            print("Cant iterate row")            
    print("done getting city pair")
    return df
    


   
cols=['fare_type',
'refund',
'exchange',
'base_fare',
'paid_fare_including_taxes_and_fees',
'total_taxes',
'Trip Type',
'Purpose',
'TDY Location',
'Total Amount',
'Baggage Fees',
'Charge Card Fees',
'Airline Flight',
'Bus',
'Train',
'Communication Serv',
'Foreign Travel',
'Laundry',
'Lodging',
'Lodging Resort Fee',
'Lodging Tax',
'Lodging-PerDiem',
'M&IE-PerDiem',
'Meals Actuals',
'Mileage - Private Airplane',
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
'Transxn Fees',
'Travel Transxn Fees',
'FILEDATE',
'AGYSUB_DESC',
'PAYPLAN_CODE',
'GRADE_CODE',
'train',
'plane',
'planeDif',
'traineDif',
'departure_combined',
'arrival_combined',
'departue_clean',
'arrival_clean',
'segments_combined',
'fare_combined',
'city_pair',
'miles',
'lat_a',
'long_a',
'lat_d',
'long_d']


 
    

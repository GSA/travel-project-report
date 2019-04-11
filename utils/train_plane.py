#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 08:32:31 2019

@author: austinpeel
"""
import pandas as pd
import numpy as np
from geotext import GeoText



def get(df):
    df = keep_certain(df)
    df = apply_new_columns(df)
    cities = get_unique_city_list(df)
    df = merge_records(df,cities)
    df = get_city_pair(df)
    df =df[cols]
    df.to_csv("data/train_plane.csv")
    
def keep_certain(df):
    df['train'] = np.where(df.legs > 0,1,0)
    df['plane'] = np.where(df.no_of_tickets > 0,1,0)
    condition = ((df.train ==1) & (df.plane ==1))
    df = df[~condition]
    return(df)

def apply_new_columns(df):
    
    df['ticket_departure_date'] = pd.to_datetime(df.ticket_departure_date)
    df['booking_date'] = pd.to_datetime(df.ticket_departure_date)
    
    df['Departure Date/Time'] = pd.to_datetime(df['Departure Date/Time'])
    df['Purchased Date'] = pd.to_datetime(df['Purchased Date'])
    
    df['planeDif'] =(df.ticket_departure_date  - df.booking_date).dt.days
    df['traineDif'] = (df['Departure Date/Time'] - df['Purchased Date'] ).dt.days
    
    
    df['departure_combined'] = df['origin_city_name'].fillna(df['Departure Location'])
    df['arrival_combined'] = df['destination_city_name'].fillna(df['Arrival Location'])
    
    
    df['segments_combined'] = df['number_of_segments'].fillna(df['legs'])
    
    
    df['fare_combined'] = df['base_fare'].fillna(df['Total Rail Amount'])
    return df



def get_unique_city_list(df):
    cities = list(df['departure_combined'].unique())
    
    cities2 = list(df['arrival_combined'].unique())
    cities.extend(x for x in cities2 if x not in cities)
    records = pd.DataFrame(cities)
    return records



def get_clean_cities(city):
    try:
        place = GeoText(city)
        return place.cities[0]
    except:
        return "no place matched"

def merge_records(df,records):
    records['departure_clean'] = records[0].apply(get_clean_cities)
    records = records.rename(columns={0:'departure_combined'})
    df = pd.merge(df,records,on="departure_combined",how='left')
    
    records = records.rename(columns={'departure_combined':'arrival_combined','departure_clean':'arrival_clean'})
    df = pd.merge(df,records,on="arrival_combined",how='left')
    return df


def get_city_pair(df):
    print("getting unique city pair, this takes a little time, janky code")
    for index, row  in df.iterrows():
        try:
            city_sorted = sorted(list([str(row['departure_combined']),str(row['arrival_combined'])]))
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
'segments_combined']

if __name__ == "__main__":
    try:
        df = pd.read_csv("data/by_trip.csv")
    except:
       print('no by_trip.csv file') 
    df = get(df)

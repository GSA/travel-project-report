# -*- coding: utf-8 -*-

from utils import data,trip
import pandas as pd
import numpy as np


#####################
#main Function


class get():

    def __init__(self):
        self.segment = data.get(data="segment")
        self.consumer = get_consumer()
        
               
    def by_quarter(self,save=True):
        segment_grouped= group_segment_by_quarter(self.segment)
        segment_grouped = filter_for_coach(segment_grouped)
        #merged_data = merge_consumer_segment(self.consumer,segment_grouped)
        #merged_data = keep_only_n_segment(merged_data,self.segment,n=50)
        merged_data = merge_award(segment_grouped)
        if save:
            merged_data.to_csv("data/by_quarter.csv")
        else:
            return merged_data
        
    def by_segment(self,save=True):
        self.segment= add_labels_segment(self.segment)
        merged_data = merge_consumer_segment(self.consumer,self.segment)
        merged_data =  merge_award(merged_data)
        merged_data =  merge_daily_demand(merged_data,self.segment)
        merged_data = merge_counts(merged_data,self.segment)
        miles = get_miles()
        merged_data = merge_miles(merged_data,miles)
        
        pnr = trip.get_travel_auth_to_pnr()
        pnr= pnr.drop_duplicates()

        merged_data = pd.merge(merged_data,pnr,on='pnr',how='left')
        voucher = data.get(data="voucher")
        voucher = voucher.drop_duplicates(subset=['Travel Authorization Number'])

        cols =['Organization', 'Employee Email Address', 'Travel Authorization Number','Trip Type','Purpose']
        voucher = voucher[cols]

        merged_data =pd.merge(merged_data,voucher,how='left',on=['Travel Authorization Number'])

        email = trip.get_email()
        merged_data = merge_email(merged_data,email)
        
        reservations = get_self_booking_indicator()
        merged_data = pd.merge(merged_data,reservations,how='left',on='pnr')
        
        if save:
            print("saving data, please hold")
            merged_data.to_csv("data/by_segment.csv")
        else:
            return merged_data
    
    
#################################################

def get_miles():
    miles = pd.read_csv('data/city_pair_info/miles.csv')
    return miles

def merge_miles(df,miles):
    df = pd.merge(df,miles,on='city_pair_code',how='left')
    df['miles'] = df['nsmiles'].fillna(df['miles'])
    return df

def get_consumer():
    consumer = pd.read_csv("data/consumer/consumer.csv")
    consumer['fiscal_quarter_invoice_date'] = pd.to_numeric(consumer.quarter) +1
    consumer['fiscal_quarter_invoice_date'] = np.where(consumer['fiscal_quarter_invoice_date']==5, 1,consumer['fiscal_quarter_invoice_date'])
    consumer['fiscal_year_invoice_date'] = pd.to_numeric(consumer.Year)
    consumer['fiscal_year_invoice_date'] = np.where(consumer['fiscal_quarter_invoice_date']==1, consumer['fiscal_year_invoice_date'] +1,consumer['fiscal_year_invoice_date'])
    return consumer



def filter_for_coach(data):
    fare = ['YCA','Dash CA','Other']
    data = data[data.fare_type.isin(fare)]
    return data


def add_labels_segment(segment):
    segment['DashCA'] = np.where(segment['fare_type']=='Dash CA', 1, 0)
    segment['YCA'] = np.where(segment['fare_type']=='YCA', 1, 0)
    segment['DG'] = np.where(segment['fare_type']=='DG', 1, 0)
    segment['Other'] = np.where(segment['fare_type']=='Other', 1, 0)
    segment['CPP Business'] = np.where(segment['fare_type']=='CPP Business', 1, 0)
    segment['Business'] = np.where(segment['fare_type']=='Business', 1, 0)
    segment['First'] = np.where(segment['fare_type']=='First', 1, 0)
    segment['21 Days'] = np.where(segment['ticketing_adv_booking_group']=='21+ Days', 1, 0)
    segment['count'] = 1
    return segment



def group_segment_by_quarter(segment):
    segment = segment[segment.no_of_segments > 0]
    seg = segment.groupby(by = ['Year','ticketing_adv_booking_group','city_pair_code','fare_type'],as_index=False ).sum()
    seg = seg[['Year','city_pair_code','ticketing_adv_booking_group','no_of_segments','fare_type']]
    seg2 = segment.groupby(by = ['Year','ticketing_adv_booking_group','city_pair_code','fare_type'],as_index=False ).mean()
    seg2 = seg2[['Year','ticketing_adv_booking_group','city_pair_code','fare_type','paid_fare_including_taxes_and_fees']]
    segTotal = pd.merge(seg,seg2,how='inner',on=['Year','ticketing_adv_booking_group','city_pair_code','fare_type'])
    return segTotal


def merge_consumer_segment(consumer,segTotal,non_award=True):
    consumer['city_pair_code'] = consumer.airport_1 + "-" + consumer.airport_2
    segTotal1 = pd.merge(segTotal,consumer,how="inner", on=['fiscal_year_invoice_date','ticketing_adv_booking_group','city_pair_code'])
    
    consumer['city_pair_code'] = consumer.airport_2 + "-" + consumer.airport_1
    segTotal2 = pd.merge(segTotal,consumer,how="inner", on=['fiscal_year_invoice_date','ticketing_adv_booking_group','city_pair_code'])

    
    merged_data = segTotal1.append(segTotal2)
    if non_award:
        a = segTotal1[list(segTotal.columns)].append(segTotal2[list(segTotal.columns)])
        a = a.append(segTotal)
        a = a.drop_duplicates(keep=False)
        a['awarded'] = 0
        merged_data['awarded'] = 1
        merged_data = merged_data.append(a)
    return merged_data

def keep_only_n_segment(merged_data,segment,n=100):
    seg = segment.groupby(by = ['city_pair_code'],as_index=False ).sum()
    seg = seg[seg.no_of_segments > n]
    seg = seg[['city_pair_code']]
    seg['keep'] = 1
    merged_data = pd.merge(merged_data,seg,how='inner',on='city_pair_code')
    return merged_data


def merge_award(merged_data):
    awards= data.get(data="award")
    awards['fiscal_year_invoice_date'] = awards.AWARD_YEAR 
    awards['city_pair_code'] = awards.ORIGIN_AIRPORT_ABBREV + "-" + awards.DESTINATION_AIRPORT_ABBREV 
    awards = awards.drop_duplicates(subset=['AWARD_YEAR','city_pair_code'])
    merged_data = pd.merge(merged_data,awards,how="inner",on=['city_pair_code','fiscal_year_invoice_date'])
    merged_data['no_CA_award'] =np.where(merged_data['XCA_FARE']==0, 1, 0)
    return merged_data


def merge_daily_demand(merged_data,segment):
    seg = segment.groupby(by = ['segment_departure_date','city_pair_code'],as_index=False ).sum()
    seg = seg[['segment_departure_date','city_pair_code','no_of_segments']]
    seg = seg.rename(columns={'no_of_segments':'daily_demand'})
    merged_data = pd.merge(merged_data,seg,how='left',on=['segment_departure_date','city_pair_code'])
    return merged_data

def merge_counts(merged_data,segment):
    grouped = segment.groupby(by = ['pnr'],as_index=False ).sum()
    cols = ['pnr','DashCA','YCA','DG','Other','CPP Business','Business','First','count']
    grouped = grouped[cols]
    merged_data = pd.merge(merged_data,grouped,how='left',on='pnr')
    return merged_data


def merge_email(data,email):
    data['FILEDATE'] = "20" + data["segment_departure_date"].str[-2:]
    data['FILEDATE'] =  pd.to_numeric(data.FILEDATE)
    data = data.rename(columns={"Employee Email Address":"EMAIL"})
    data['EMAIL'] = data['EMAIL'].str.lower()
    email['EMAIL'] = email['EMAIL'].str.lower()
    data = pd.merge(data,email,how="left", on =['FILEDATE','EMAIL'])
    return data


def get_self_booking_indicator():
    reservations = data.get(data="reservation")
    reservations = reservations[['pnr','self_booking_indicator']] 
    reservations = reservations.drop_duplicates(subset='pnr')
    return reservations


    
    
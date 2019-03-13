# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 10:13:12 2019

@author: AustinPeel
"""


import pandas as pd
from utils import data



#main function that merges on all data
def get(save=True):
    #get reservations
    reservations = get_reservation_data()
    reservations = reservations[data.cols_to_keep]
    
    #aggregate segment and merge this gets the true cost of the flight
    segment_aggregated = get_segment_data()
    total = pd.merge(reservations,segment_aggregated,on='pnr',how='left')
    
    #get merge travel auth so we can merge on voucher data on the next section
    pnrToAuth = get_travel_auth_to_pnr()
    pnrToAuth = pnrToAuth.drop_duplicates()
    total = pd.merge(total,pnrToAuth,how='outer',on='pnr')
    
    #merge voucher data
    voucher = data.get(data="voucher")
    voucher = voucher.drop_duplicates(subset=['Travel Authorization Number'])
    total =pd.merge(total,voucher,how='outer',on=['Travel Authorization Number'])
    total = total.drop_duplicates(subset=['Travel Authorization Number'],keep=False)

    #merge on email demographics
    email = get_email()
    total = merge_email_data(total,email)
    

    if save:
        total.to_csv("data/by_trip.csv")
    else:
        return total

#######################################################


def get_reservation_data():
    #main function to clean reservation data.
    reservations = data.get(data="reservation")
    exchanged = _get_if_ticket_was_exchanged(reservations)
    refund =  _get_if_ticket_was_returned(reservations)
    reservations = _keep_only_ticketed(reservations)
    reservations = _drop_duplicated(reservations)
    reservations = _get_finished_reservations(reservations,refund,exchanged)
    return reservations

def get_segment_data():
    #main function to get segment data
    segment= data.get(data="segment")
    cols = ['pnr','base_fare','paid_fare_including_taxes_and_fees','total_taxes']
    seg = segment.groupby(by = ['pnr'],as_index=False ).sum()
    negatives = segment[ segment.base_fare < 0]
    reimburse = negatives.groupby(by = ['pnr'],as_index=False ).sum()
    seg = seg[cols]
    reimburse = reimburse[['pnr','paid_fare_including_taxes_and_fees']]
    reimburse= reimburse.rename(columns={'paid_fare_including_taxes_and_fees':'refunded_amount'})
    segment_aggregated = pd.merge(seg,reimburse,on='pnr',how='left')
    segment_aggregated['refunded_amount'] = segment_aggregated.refunded_amount.fillna(0)
    return segment_aggregated

def get_travel_auth_to_pnr():
    #this get travel authorization number to pnr. we need this because voucher doesnt use pnr
    cost = data.get(data="cost")
    cols= ['Travel Authorization Number','Record Locator','Total Paid(Incl Credits or Fees)']
    cost = cost[cols]
    cost = cost.dropna()
    cost['cost'] = cost.groupby(['Record Locator']).cumcount()+1
    piv = cost.pivot(index='Record Locator',columns='cost',values='Total Paid(Incl Credits or Fees)')
    piv['pnr'] = piv.index
    pnrToAuth = cost[['Record Locator','Travel Authorization Number']]
    pnrToAuth = pnrToAuth.rename(columns ={'Record Locator':'pnr'})
    return pnrToAuth

def get_email():
    #gets email demographics
    df = data.get(data="email")
    df = df.drop_duplicates(subset=["EMAIL","FILEDATE"])
    cols = ["FILEDATE"	,"EMAIL" ,"AGYSUB_DESC",	"PAYPLAN_CODE","GRADE_CODE"	 ]
    df = df[cols]
    return df


def merge_email_data(reservations,email):
    #this function merges on email demographics
    reservations['FILEDATE'] = "20" + reservations["ticket_departure_date"].str[-2:]
    reservations['FILEDATE'] =  pd.to_numeric(reservations.FILEDATE)
    reservations = reservations.rename(columns={"Employee Email Address":"EMAIL"})
    reservations['EMAIL'] = reservations['EMAIL'].str.lower()
    email['EMAIL'] = email['EMAIL'].str.lower()
    reservations = pd.merge(reservations,email,how="inner", on =['FILEDATE','EMAIL'])
    return reservations


############# function to clean data ##########################################
###############################################################################

def _get_if_ticket_was_exchanged(reservations):
    #produces a df with an indicator if ticket was exchanged
    exchange = reservations[ (reservations.exchange_indicator == 'Y') ]
    exchange = exchange.drop_duplicates(subset=['pnr'])
    exchange['exchange'] =1
    exchange = exchange[['pnr','exchange']]
    exchange = exchange.drop_duplicates()
    return exchange

def _get_if_ticket_was_returned(reservations):
    #produces a df with an indicator if ticket was refunded
    refund = reservations[ reservations.refund_indicator == 'Y' ]
    refund = refund.drop_duplicates(subset=['pnr'])
    refund['refund'] = 1
    refund = refund[['pnr','refund']]
    refund = refund.drop_duplicates()
    return refund


def _keep_only_ticketed(reservations):
    #gets only the reservations that are ticketed
    reservations = reservations[ reservations.base_fare > 0]
    reservations = reservations[ (reservations.exchange_indicator == 'N') &  (reservations.refund_indicator == 'N') ]
    reservations = reservations.drop_duplicates(subset=['pnr','base_fare'],keep='last')
    return reservations

def _drop_duplicated(reservations):
    #some data here appears to be dubplicted. i kept the largest cost. but do not use this cost for regression or analysis
    reservations= reservations.sort_values(by=['base_fare'])
    reservations = reservations.sort_values(by=['round_trip_indicator'],ascending=False)
    reservations = reservations.drop_duplicates(subset=['pnr'])
    return reservations

def _get_finished_reservations(reservations,refund,exchange):
    #merges refund and exchange indicator.
    reservations = pd.merge(reservations,refund, how='left',on='pnr')
    reservations = pd.merge(reservations,exchange,how='left',on='pnr')
    reservations['refund'] = reservations.refund.fillna(0)
    reservations['exchange'] = reservations.exchange.fillna(0)
    return reservations
 
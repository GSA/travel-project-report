# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 10:38:44 2019

@author: AustinPeel
"""

import pandas as pd
from utils import data
import re


def get(save=True):
    voucher = data.get(data='voucher')
    voucher = clean_vouchers(voucher)
    aggregated = aggegate_voucher_by_email(voucher)
    transactions = get_transactions_pivot()
    transactions = clean_transactions_pivot(transactions)
   
    merged = pd.merge(aggregated,transactions,on=['Employee Email Address','FY'],how='left')    
    merged = merged.rename(columns=lambda x: re.sub('\_x','_total',x))
    merged = merged.rename(columns=lambda x: re.sub('\_y','_card',x))
    if save:
        merged.to_csv('data/by_person.csv')
    else:
        return merged

    
def clean_vouchers(voucher):
    # drop duplicates
    voucher = voucher.drop_duplicates(subset=['Travel Authorization Number'])
    
    voucher['Employee Email Address'] = voucher['Employee Email Address'].str.lower()
    
    voucher = voucher.fillna(0)
    
    voucher['return'] = pd.to_datetime(voucher['Trip Return Date'])
    voucher['start'] = pd.to_datetime(voucher['Trip Departure Date'])
    
    voucher['daysTravelled'] = (voucher['return'] - voucher['start']).dt.days
    voucher['trip_count'] = 1
    return voucher
    

# replace all commas to aggreate then groupby
def aggegate_voucher_by_email(voucher):
    for i in list(voucher.columns):
        try:
            voucher[i] = voucher[i].replace({',':''},regex=True).apply(pd.to_numeric,1)
        except:
            print("cant replace comma in " + i)
    aggregated = voucher.groupby(by = ['Employee Email Address','FY'],as_index=False ).sum()
    return aggregated


####insert read tranaactions the data should be merged with the get function and 
def get_transactions_pivot():
    transactions = data.get(data='transactions')   
    transactions['Transaction Amount'] = (transactions['Transaction Amount'].replace( '[\$,)]','', regex=True ).replace( '[(]','-',   regex=True ).astype(float))
    transactions['Expense Category'] = transactions['MCC Description'].map(data.transaction_dict) 
    transactions_g= transactions[['Account e-mail Address','Expense Category','Transaction Amount','FY']].groupby(
        ['Account e-mail Address','FY','Expense Category'],as_index = False).sum()
    transactions_g = transactions_g.pivot_table(values=['Transaction Amount'], index=['Account e-mail Address','FY'], columns='Expense Category').fillna(0)
    transactions_g.columns = transactions_g.columns.droplevel(0)
    transactions_g= transactions_g.reset_index().rename_axis(None, axis=1)
    return transactions_g


def clean_transactions_pivot(transactions):
    transactions['Account e-mail Address'] = transactions['Account e-mail Address'].str.lower()
    transactions = transactions.rename(columns={'Account e-mail Address':'Employee Email Address'})
    return transactions

if __name__ == "__main__":
    get()
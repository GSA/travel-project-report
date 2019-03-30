# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 10:13:12 2019

@author: AustinPeel
"""




import pandas as pd
import os

#function to specify which data to pull and merge
def get(data):
    #get data by dataset
    if data == "voucher":
        data_dict = getFolderData("data/vouchers/")
    elif data == "cost":
        data_dict = getFolderData("data/airfare/cost/")
    elif data == "reservation":
        data_dict =   getFolderData("data/reservation/Ticket/")
    elif data == "segment":
        data_dict =   getFolderData("data/reservation/Segment/")
    elif data == "email":
        data_dict =   getFolderData("data/email/")
    elif data == "award":
        data_dict =   getFolderData("data/awards/")
    elif data == "amtrak":
        data_dict = getFolderData('data/amtrak/')
    else:
        print("please specify which data")
    df = pd.DataFrame()
    for data in data_dict:
        df = df.append(data_dict[data])
    return df


#helper function to pull all data in a directory
def getFolderData(dataLocation):
    dataDict = {}
    for filename in os.listdir(dataLocation):
                if filename.endswith('.xlsx'):
                    print("importing: " +filename)
                    sheets = pd.ExcelFile(dataLocation + filename).sheet_names
                    for sheet in sheets:
                        df = pd.read_excel(dataLocation + filename, sheet)
                        dataDict[filename + "_" + sheet] = df
                elif filename.endswith(".csv"):
                    print("importing: " +filename)
                    try:
                        df = pd.read_csv(dataLocation + filename)  
                        dataDict[filename] = df
                    except:
                        df = pd.read_csv(dataLocation + filename,encoding="ISO-8859-1") 
                        dataDict[filename] = df
    return dataDict   
              



#columns I tucked away to specify which columns we should keep
cols_to_keep =[
 'agency_name',
 'bi_directional_o___d_code',
 'bi_directional_o_d_description',
 'booking_date',
 'cabin_service_class',
 'city_pair_code',
 'city_pair_description',
 'compare_fare',
 'continent_to_continent',
 'country_to_country',
 'cpp_ticket_indicator',
 'department',
 'destination_city_code',
 'destination_city_name',
 'destination_continent',
 'destination_country',
 'domestic_international_indicator',
 'exchange_indicator',
 'extcabinclass',
 'fare_justification_code',
 'fare_justification_reason',
 'fare_type',
 'invoice_date',
 'leg_routing_string',
 'lowest_available_fare',
 'no_of_tickets',
 'number_of_segments',
 'organization',
 'origin_city_code',
 'origin_city_name',
 'origin_continent',
 'origin_country',
 'original_ticket_number',
 'pnr',
 'predominant_fare_basis',
 'pseudo_city_code',
 'reckey',
 'refund_indicator',
 'round_trip_indicator',
 'segment_routing_string',
 'self_booking_indicator',
 'ticket_departure_date',
 'ticket_number',
 'ticket_origin_airport',
 'total_flight_miles',
 'total_taxes_amount',
 'tour_code',
 'transaction_id',
 'trip_departure_day_of_week',
 'trip_duration',
 'validating_airline_code',
 'validating_airline_name',
 'refund',
 'exchange']
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 06:44:31 2019

@author: austinpeel
"""


segment_columns = {
 '21 Days' : {'description':'whether ticket was bought more than 21 days ago','source':'','type':'','keep':True},
 'Business_x' :{'description':'if business class','source':'','type':'','keep':False},
 'CPP Business_x' : {'description':'if a CPP business class','source':'','type':'','keep':False},
 'DG_x' : {'description':'if a DG class ticket','source':'','type':'','keep':True},
 'DashCA_x' : {'description':'if a _CA  ticket','source':'','type':'','keep':True},
 'First_x' :  {'description':'if a first class  ticket','source':'','type':'','keep':False},
 'Geocoded_City1' : {'description':'','source':'','type':'','keep':False},
 'Geocoded_City2' : {'description':'','source':'','type':'','keep':False},
 'Other_x' : {'description':'unresticed airfare ticket','source':'','type':'','keep':True},
 'YCA_x' : {'description':'if YCA ticket far','source':'','type':'','keep':True},
 'Year' : {'description':'','source':'','type':'','keep':True},
 'agency_name' : {'description':'','source':'','type':'','keep':False},
 'airline_carrier' : {'description':'airline short name','source':'','type':'','keep':False},
 'airline_carrier_name' : {'description':'airline long name','source':'','type':'','keep':True},
 'airport_1' : {'description':'','source':'','type':'','keep':False},
 'airport_2' : {'description':'','source':'','type':'','keep':False},
 'airportid_1' : {'description':'','source':'','type':'','keep':False},
 'airportid_2' : {'description':'','source':'','type':'','keep':False},
 'awarded' : {'description':'whether the route was awarded a city-pair contract','source':'','type':'','keep':True},
 'base_fare': {'description':'base fair not including taxes or fees','source':'','type':'','keep':True},
 'bi_direction_o___d_descript': {'description':'','source':'','type':'','keep':False},
 'bi_directional_o___d_code': {'description':'','source':'','type':'','keep':False},
 'cabin_svc_class_of_segment': {'description':'class of service','source':'','type':'','keep':True},
 'carrier_lg': {'description':'the airline with the most flights for route','source':'','type':'','keep':True},
 'carrier_low': {'description':'the airline with the least flights for route','source':'','type':'','keep':False},
 'city1': {'description':'','source':'','type':'','keep':False},
 'city2': {'description':'','source':'','type':'','keep':False},
 'city_pair_code': {'description':'city pair route','source':'','type':'','keep':True},
 'city_pair_description': {'description':'','source':'','type':'','keep':False},
 'citymarketid_1': {'description':'','source':'','type':'','keep':False},
 'citymarketid_2': {'description':'','source':'','type':'','keep':False},
 'continent_to_continent': {'description':'','source':'','type':'','keep':False},
 'count_x': {'description':'','source':'','type':'','keep':False},
 'country_to_country': {'description':'','source':'','type':'','keep':False},
 'department': {'description':'','source':'','type':'','keep':False},
 'destination_city_code': {'description':'destination code','source':'','type':'','keep':True},
 'destination_city_name': {'description':'','source':'','type':'','keep':False},
 'destination_continent': {'description':'','source':'','type':'','keep':False},
 'destination_country': {'description':'','source':'','type':'','keep':False},
 'domestic_international_indicator_of_segment': {'description':'','source':'','type':'','keep':False},
 'extcabinclass': {'description':'','source':'','type':'','keep':False},
 'fare': {'description':'the average non government consumers paid for fare by aggregated by quarter','source':'Dept of Transportation','type':'','keep':True},
 'fare_lg': {'description':'largest fare for consumers paid by quarter','source':'Dept of Transportation','type':'','keep':True},
 'fare_low': {'description':'the lowest consumers paid per quarter per route','source':'Dept of Transportation','type':'','keep':True},
 'fare_type': {'description':'the fare used','source':'','type':'','keep':True},
 'first_of_month_invoice_date': {'description':'','source':'','type':'','keep':False},
 'fiscal_quarter_invoice_date': {'description':'','source':'','type':'','keep':False},
 'fiscal_year_invoice_date': {'description':'','source':'','type':'','keep':False},
 'invoice_number': {'description':'','source':'','type':'','keep':False},
 'large_ms': {'description':'market share by the largest airline for route','source':'','type':'','keep':True},
 'legcntr': {'description':'','source':'','type':'','keep':False},
 'legplusmin': {'description':'','source':'','type':'','keep':False},
 'lf_ms': {'description':'','source':'','type':'','keep':False},
 'no_of_segments': {'description':'number of total segments traveller went on','source':'','type':'','keep':True},
 'nsmiles': {'description':'miles of flight','source':'','type':'','keep':True},
 'organization': {'description':'','source':'','type':'','keep':False},
 'origin_city_code': {'description':'origin code','source':'','type':'','keep':True},
 'origin_city_name': {'description':'','source':'','type':'','keep':False},
 'origin_continent': {'description':'','source':'','type':'','keep':False},
 'origin_country': {'description':'','source':'','type':'','keep':False},
 'paid_fare_including_taxes_and_fees': {'description':'the actual government paid for flight','source':'','type':'','keep':True},
 'passengers': {'description':'average passangers per quarter per route','source':'','type':'','keep':True},
 'plusmin': {'description':'','source':'','type':'','keep':False},
 'pnr': {'description':'','source':'','type':'','keep':False},
 'predominant_fare_basis_code': {'description':'','source':'','type':'','keep':False},
 'quarter': {'description':'the quarter of year travelled','source':'','type':'','keep':True},
 'reckey': {'description':'','source':'','type':'','keep':False},
 'segment_arrival_date': {'description':'','source':'','type':'','keep':False},
 'segment_departure_date': {'description':'','source':'','type':'','keep':False},
 'segment_exchange_indicator': {'description':'','source':'','type':'','keep':False},
 'segment_level_transaction_id': {'description':'','source':'','type':'','keep':False},
 'segment_refund_indicator': {'description':'','source':'','type':'','keep':False},
 'segment_sequence_number': {'description':'','source':'','type':'','keep':False},
 'tbl': {'description':'','source':'','type':'','keep':False},
 'tbl1apk': {'description':'','source':'','type':'','keep':False},
 'ticket_booking_date': {'description':'','source':'','type':'','keep':False},
 'ticket_exchange_indicator': {'description':'if ticket was exchanged','source':'','type':'','keep':True},
 'ticket_invoice_date': {'description':'','source':'','type':'','keep':False},
 'ticket_number': {'description':'','source':'','type':'','keep':False},
 'ticket_origin_airport': {'description':'','source':'','type':'','keep':False},
 'ticket_refund_indicator': {'description':'','source':'','type':'','keep':False},
 'ticketing_adv_booking_group': {'description':'how many days prior to book ticket','source':'','type':'','keep':True},
 'ticketing_departure_date': {'description':'','source':'','type':'','keep':False},
 'total_taxes': {'description':'total taxes paid','source':'','type':'','keep':True},
 'transaction_id': {'description':'','source':'','type':'','keep':False},
 'trip_departure_day_of_week': {'description':'','source':'','type':'','keep':False},
 'ITEM_NUM': {'description':'','source':'','type':'','keep':False},
 'AWARD_YEAR': {'description':'','source':'','type':'','keep':False},
 'ORIGIN_AIRPORT_ABBREV': {'description':'','source':'','type':'','keep':False},
 'DESTINATION_AIRPORT_ABBREV': {'description':'','source':'','type':'','keep':False},
 'ORIGIN_CITY_NAME': {'description':'','source':'','type':'','keep':False},
 'ORIGIN_STATE': {'description':'','source':'','type':'','keep':False},
 'ORIGIN_COUNTRY': {'description':'','source':'','type':'','keep':False},
 'DESTINATION_CITY_NAME': {'description':'','source':'','type':'','keep':False},
 'DESTINATION_STATE': {'description':'','source':'','type':'','keep':False},
 'DESTINATION_COUNTRY': {'description':'','source':'','type':'','keep':False},
 'AIRLINE_ABBREV': {'description':'','source':'','type':'','keep':False},
 'AWARDED_SERV': {'description':'','source':'','type':'','keep':False},
 'PAX_COUNT': {'description':'the government-wide passanger count per quarter','source':'city pair','type':'','keep':True},
 'YCA_FARE': {'description':'the YCA contract award amount for route ','source':'city pair','type':'','keep':True},
 'XCA_FARE': {'description':'the _DC contract award amount for route','source':'city pair','type':'','keep':True},
 'BUSINESS_FARE': {'description':'','source':'','type':'','keep':False},
 'ORIGIN_AIRPORT_LOCATION': {'description':'','source':'','type':'','keep':False},
 'DESTINATION_AIRPORT_LOCATION': {'description':'','source':'','type':'','keep':False},
 'ORIGIN_CITY_STATE_AIRPORT': {'description':'','source':'','type':'','keep':False},
 'DESTINATION_CITY_STATE_AIRPORT': {'description':'','source':'','type':'','keep':False},
 'EFFECTIVE_DATE': {'description':'','source':'','type':'','keep':False},
 'EXPIRATION_DATE': {'description':'','source':'','type':'','keep':False},
 'no_CA_award': {'description':'if contract had no _CA award for route','source':'custom','type':'','keep':True},
 'daily_demand': {'description':'an attempt at getting the amount of demand daily for route','source':'custom','type':'','keep':True},
 'DashCA_y': {'description':'','source':'','type':'','keep':False},
 'YCA_y': {'description':'','source':'','type':'','keep':False},
 'DG_y': {'description':'','source':'','type':'','keep':False},
 'Other_y': {'description':'','source':'','type':'','keep':False},
 'CPP Business_y': {'description':'','source':'','type':'','keep':False},
 'Business_y': {'description':'','source':'','type':'','keep':False},
 'First_y': {'description':'','source':'','type':'','keep':False},
 'count_y': {'description':'','source':'','type':'','keep':False},
 'dash_per_mile': {'description':'contract cost per mile (not actual)','source':'','type':'','keep':True},
 'YCA_per_mile': {'description':'contract cost per mile (not actual)','source':'','type':'','keep':True},
 'cost_per_mile': {'description':'Actual cost per mile travelled','source':'','type':'','keep':True},
 'city_pair_ratio': {'description':'the ratio of _CA to YCA fare per route','source':'','type':'','keep':True},
 'ticket': {'description':'','source':'','type':'','keep':False},
 'market_share_log': {'description':'','source':'','type':'','keep':True}
 }




transaction_columns= {

'total_fields' : [
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
 'Taxi_total'],

'card_fields' : ['Airline Flight_card',
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
}
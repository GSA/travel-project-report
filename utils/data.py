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
    elif data == "transactions":
        data_dict = getFolderData('data/transactions/')
    elif data == "lodging":
        data_dict = getFolderData('data/lodging_details/')
    elif data == "rental_car":
        data_dict = getFolderData('data/rental_car_details/')
    elif data == "credit_card":
        data_dict = getFolderData('data/credit_card/')
    elif data == 'business_fares':
        data_dict = getFolderData('data/business_fares/')
    else:
        print("please specify which data / wrong dataname")
        return None
    df = pd.DataFrame()
    for csv in data_dict:
        if data == 'transactions':
            data_dict[csv] = attach_fiscal_year(data_dict[csv],"Transaction Date")
            df = df.append(data_dict[csv])
        elif data == 'voucher':
            data_dict[csv] = attach_fiscal_year(data_dict[csv],"Trip Departure Date")
            df = df.append(data_dict[csv])
        else:    
            df = df.append(data_dict[csv])
    return df






def attach_fiscal_year(df,date_column=''):
    '''function to fix issues with transaction  data before appending
    adding fy and getting rid of money sign'''
    date = max(pd.to_datetime(df[date_column]))
    year = date.year
    df['FY'] = year
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




transaction_dict =	{
  'Gaylord Palms':'Lodging',
  'Taj Hotels International':'Lodging',
  'Mainstay Suites':'Lodging',
  'Hilton International':'Lodging',
  'Telecommunication Services':'Communication Serv',
  'Drury Inn':'Lodging',
  'Austrian Airlines':'Airline Flight',
  'Quick Copy, Reproduction, and Blueprinting Services':'Misc Expense',
  'Coast Hotel':'Lodging',
  'Best Western Hotels':'Lodging',
  'Miscellaneous Food Stores':'M&IE-PerDiem',
  'THE RITZ-CARLTON':'Lodging',
  'Triangle Rent A Car':'Rental Car',
  'Crowne Plaza Hotels':'Lodging',
  'Delta':'Airline Flight',
  'Mandalay Bay Resort':'Lodging',
  'Summerfield Suites Hotel':'Lodging',
  'Radisson':'Lodging',
  'Hilton Garden Inn':'Lodging',
  'Ballys Hotel and Casino':'Lodging',
  'Paris Las Vegas Hotel':'Lodging',
  'United Airlines	Airline':'Flight',
  'Fairmont Hotels':'Lodging',
  'Laundries - Family and Commercial':'Laundry',
  'Utilities - Electric, Gas, Heating Oil, Sanitary, Water':'Misc Expense',
  'Commercial Equipment - Not Elsewhere Classified':'Misc Expense',
  'Bus Lines':'Bus',
  'Alamo Rent-A-Car':'Rental Car',
  'Town and Country Resort & Convention Center':'Lodging',
  'Microtel Inn and Suites':'Lodging',
  'Automotive Service Shops (Non-Dealer)':'Misc Expense',
  'Hertz':'Rental Car',
  'BRIDGE AND ROAD FEES, TOLLS':'Highway/Bridge Tolls',
  'Travel Agencies and Tour Operators':'Travel Transxn Fees',
  'Loews Hotels':'Lodging',
  'Candy, Nut, and Confectionery Stores':'M&IE-PerDiem',
  'Hotel Indigo':'Lodging',
  'Fairfield Hotels':'Lodging',
  'Hyatt Hotels':'Lodging',
  'Silver Legacy Hotel and Casino':'Lodging',
  'Hyatt Place':'Lodging',
  'TRANSPRTN-SUBRBN & LOCAL COMTR PSNGR, INCL FERRIES':'Public Transportation',
  'LA QUINTA INN AND SUITES':'Lodging',
  'Transportation Services - Not Elsewhere Classified':'Public Transportation',
  'Caterers':'Misc Expense',
  'Sofitel Hotels':'Lodging',
  'Southwest Airlines':'Airline Flight',
  'Luxor Hotel and Casino':'Lodging',
  'Airports, Airport Terminals, Flying Fields':'Airline Flight',
  'Courtyard by Marriott':'Lodging',
  'Spirit Airlines':'Airline Flight',
  'Government Services - Not Elsewhere Classified':'Misc Expense',
  'W Hotels':'Lodging',
  'Renaissance Hotels':'Lodging',
  'Grand Sierra Resort':'Lodging',
  'Golden Nugget':'Lodging',
  'Adams Mark Hotels':'Lodging',
  'Budget Hosts Inns':'Lodging',
  'CSA Ceskoslovenske Aerolinie':'Airline Flight',
  'Americas Best Value Inn':'Lodging',
  'Womens Ready to Wear Stores':'Misc Expense',
  'Motel 6':'Lodging',
  'FREIGHT CARRIER,TRUCKING-LCL/LNG DIST, MVG/STORAGE':'Misc Expense',
  'National Car Rental':'Rental Car',
  'Harrahs Hotels and Casinos':'Lodging',
  'Holiday Inns':'Lodging',
  'Eating Places, Restaurants':'M&IE-PerDiem',
  'The Roosevelt Hotel NY':'Lodging',
  'Outrigger Hotels & Resorts':'Lodging',
  'Peppermill Hotel Casino':'Lodging',
  'Autograph':'Misc Expense',
  'Wyndham':'Lodging',
  'Knights Inn':'Lodging',
  'Automobile Rental Agency - Not Elsewhere Classified':'Rental Car',
  'HOME2 SUITES BY HILTON':'Lodging',
  'Invalid MCC Code':'Misc Expense',
  'Hawaiian Air':'Airline Flight',
  'Real Estate Agents and Managers - Rentals':'Misc Expense',
  'Travelodge':'Lodging',
  'CP (Canadian Pacific) Hotels':'Lodging',
  'Candlewood Suites':'Lodging',
  'Four Points Hotels':'Lodging',
  'Howard Johnson':'Lodging',
  'Vagabond Hotels':'Lodging',
  'Air Canada	Airline':'Flight',
  'Intercontinental Hotels':'Lodging',
  'Mens and Boys Clothing and Accessories Stores':'Misc Expense',
  'Hotels Melia':'Lodging',
  'H Curio Hotels':'Lodging',
  'Red Lion Inns':'Lodging', 
  'Shoneys Inn':'Lodging',
  'Park Inn by Radisson':'Lodging',
  'Shilo Inn':'Lodging',
  'U.S. Airways':'Airline Flight',
  'Days Inns':'Lodging',
  'St. Regis Hotel':'Lodging',
  'Monte Carlo Hotel and Casino':'Lodging',
  'Extended Stay':'Lodging',
  'aloft (aloft hotels)':'Lodging',
  'Hotel Okura':'Lodging',
  'Asiana Airlines':'Airline Flight',
  'Broadmoor Hotel':'Lodging',
  'Grand Casino Hotels':'Lodging',
  'Durable Goods - Not Elsewhere Classified':'Misc Expense',
  'Circus Circus Hotel and Casino':'Lodging',
  'Discount Stores':'Misc Expense',
  'Treasure Island Hotel and Casino':'Lodging',
  'Rosen Hotels and Resorts':'Lodging',
  'Department Stores':'Misc Expense',
  'Alaska Airlines Inc.':'Airline Flight',
  'Nondurable Goods - Not Elsewhere Classified':'Misc Expense',
  'Rodeway Inns':'Lodging',
  'ACCESSORY AND APPAREL STORES-MISCELLANEOUS':'Misc Expense',
  'VIRGIN AMERICA':'Airline Flight',
  'Embassy Suites':'Lodging',
  'Business Services - Not Elsewhere Classified':'Misc Expense',
  'Americana Hotels':'Lodging',
  'Delta Hotels':'Lodging',
  'FUEL DISPENSER, AUTOMATED':'Rental Car - Gasoline',
  'Professional Services - Not Elsewhere Classified':'Misc Expense',
  'ORGANIZATIONS, CHARITABLE AND SOCIAL SERVICES':'Misc Expense',
  'TownePlace Suites':'Lodging',
  'AUTOMATED CASH DISBURSEMENTS-CUSTOMER FINANCIAL INSTITUTION':'Transxn Fees',
  'Towing Services':'Misc Expense',
  'Cable, Satellite, Other Pay Television & Radio Services':'Communication Serv',
  'Lodging - Hotels, Motels, Resorts - Not Elsewhere Classified':'Lodging',
  'Disney Resorts':'Lodging',
  'Miscellaneous and Specialty Retail Stores':'Misc Expense',
  'Lufthansa':'Airline Flight',
  'Grocery Stores and Supermarkets':'M&IE-PerDiem',
  'Adria Airways':'Airline Flight',
  'American Airlines':'Airline Flight',
  'Car Washes':'Misc Expense',
  'Ramada Inns':'Lodging',
  'BAR,LOUNGE,DISCO,NIGHTCLUB,TAVERN-ALCOHOLIC DRINKS':'M&IE-PerDiem',
  'Comfort Inns':'Lodging',
  'Ala Moana Hotel':'Lodging',
  'Budget Rent-A-Car':'Rental Car',
  'Drug Stores and Pharmacies':'M&IE-PerDiem',
  'Variety Stores':'Misc Expense',
  'Service Stations':'Rental Car - Gasoline',
  'Pullman International Hotels':'Lodging',
  'Millennium Hotels':'Lodging',
  'MGM Grand Hotel':'Lodging',
  'Venetian Resort Hotel and Casino':'Lodging',
  'Air France':'Airline Flight',
  'AmericInn':'Lodging',
  'Frontier Airlines':'Airline Flight',
  'AUTOMOBILE PARKING LOTS AND GARAGES':'Parking',
  'Europcar':'Rental Car',
  'PARK PLAZA HOTEL':'Lodging',
  'Shoe Stores':'Misc Expense',
  'COUNTRY INN BY CARLSON':'Lodging',
  'RADISSON BLU':'Lodging',
  'Direct Marketing - Other Direct Marketers':'Misc Expense',
  'Meridien Hotels':'Lodging',
  'Enterprise Rent-A-Car':'Rental Car',
  'MANUAL CASH DISBURSEMENTS-CUSTOMER FINANCIAL INSTITUTION':'Cash Disburse',
  'Home Supply Warehouse Stores':'Misc Expense',
  'LIMOUSINES AND TAXICABS':'Taxi',
  'Stationery, Office Supplies, Printing and Writing Paper':'Misc Expense',
  'Wholesale Clubs':'Misc Expense',
  'Fairfield Inn':'Lodging',
  'Stratosphere Hotel and Casino':'Lodging',
  'Passenger Railways':'Train',
  'Sheraton (Sheraton Hotels)':'Lodging',
  'Swissotel':'Lodging',
  'Iberotel Hotels':'Lodging',
  'Dollar Rent A Car':'Rental Car',
  'Homewood Suites':'Lodging',
  'SIXT Car Rental':'Rental Car',
  'ORGANIZATIONS, MEMBERSHIP-NOT ELSEWHERE CLASSIFIED':'Registration Fees',
  'Doubletree Hotels':'Lodging',
  'Red Roof Inns':'Lodging',
  'Airlines and Air Carriers - Not Elsewhere Classified':'Airline Flight',
  'Automobile Associations':'Misc Expense',
  'OTHER SERVICES (NOT ELSEWHERE CLASSIFIED)':'Misc Expense',
  'WALDORF':'Lodging',
  'Fast Food Restaurants':'M&IE-PerDiem',
  'Piece Goods, Notions, and Other Dry Goods':'M&IE-PerDiem',
  'Payless Car Rental':'Rental Car',
  'Embassy Hotels':'Lodging',
  'Dry Cleaners':'Laundry',
  'Miscellaneous General Merchandise Stores':'Misc Expense',
  'Westin (Westin Hotels)':'Lodging',
  'Advertising Services':'Misc Expense',
  'Oxford Suites':'Lodging',
  'Courier Services':'Misc Expense',
  'Avis Rent A Car':'Rental Car',
  'Clarion Hotels':'Lodging',
  'Sleep Inns':'Lodging',
  'Sonesta Hotels':'Lodging',
  'Super 8 Motels':'Lodging',
  'Gaylord Opryland':'Lodging',
  'Cruise Lines':'Misc Expense',
  'Advantage Rent A Car':'Rental Car',
  'Hampton Inn Hotels':'Lodging',
  'All Nippon Airways':'Airline Flight',
  'Vdara':'Lodging',
  'Family Clothing Stores':'Misc Expense',
  'Excalibur Hotel and Casino':'Lodging',
  'Mirage Hotel and Casino':'Lodging',
  'JetBlue Airways':'Airline Flight',
  'News Dealers and Newsstands':'Misc Expense',
  'Marriott':'Lodging',
  'EconoLodges':'Lodging',
  'CLEANING, GARMENT, AND LAUNDRY SERVICES':'Laundry',
  'Residence Inn':'Lodging',
  'Tropicana Resort and Casino':'Lodging',
  'Thrifty Car Rental':'Rental Car',
  'LXR (Luxury Resorts)':'Lodging',
  'CAMPGROUNDS AND TRAILER PARKS':'Lodging',
  'New York, New York Hotel and Casino':'Lodging',
  'Mandarin Oriental Hotels':'Lodging',
  'Staybridge Suites':'Lodging',
  'Conrad Hotels':'Lodging',
  'Quality Inns':'Lodging',
  'Mens and Womens Clothing Stores':'Misc Expense',
  'Dairy Products Stores':'Misc Expense',
  'Aria':'Lodging',
  'Omni Hotels':'Lodging',
  'Shangri-La International':'Lodging',
  'Miyako Hotel':'Lodging',
  'GOLF COURSES-PUBLIC':'Misc Expense',
  'Hilton Hotels':'Lodging',
  'SpringHill Suites':'Lodging',
  'Caesars Hotel and Casino':'Lodging',
  'Element':'Lodging',
  'Bakeries':'M&IE-PerDiem',
  'The Flamingo Hotels':'Lodging'
  }







#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  2 08:46:35 2019

@author: austinpeel
"""

from utils import data

cc = data.get(data='credit_card')
cc['ticket_number'] = cc['Merchant Name'].str.extract('([0-9].*)', expand=True) 
cc = cc[['Transaction Amount','ticket_number']]


cc_g = cc.groupby("ticket_number",as_index=False).sum()

from models.models import Segment 

# Segment level analysis
seg = Segment()

#lets look at model 1
model = seg.model_1()

#this is the data we are using 
df = model.model_data


t = df[['ticket_number','base_fare']]

t['ticket_number'] = t['ticket_number'].astype(str)

t['ticket_number'] = t['ticket_number'].str.replace(r'\.\d*','')
import pandas as pd



cc_g['ticket_number'] = cc_g['ticket_number'].str.replace(r'[0][0][1]','')

t['ticket_number'] =  t['ticket_number'].str[:-1]
m = pd.merge(t,cc_g,on='ticket_number',how='inner')
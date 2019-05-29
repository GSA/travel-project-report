#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 09:37:13 2019

@author: austinpeel
"""
import pandas as pd
params = pd.DataFrame(reg.params)
params['coef'] =params.index

new = params[params['coef'].str.contains('adv')]
pat = "[0-9].*[0-9]"
new['days'] = new['coef'].str.findall(pat).astype('str')


interaction = new[new['coef'].str.contains('fare_type')]
interaction['coef']
interaction = interaction.rename(columns={'coef':'var',0:'coef'})


base = new[~new['coef'].str.contains('fare_type')]
base = base.rename(columns={0:'base'})
del base['coef']





total = pd.merge(interaction,base,on='days',how='left')

pat = "(?<=type).*$"
total['var'] = total['var'].str.findall(pat).astype('str')

base2 = base
base2['coef'] =0
base2['var'] = 'DG'
total = total.append(base2)

total['savings']= total.base + total.coef


total = total[['savings','days','var']]
wide = total.pivot(index='var',columns='days', values='savings')


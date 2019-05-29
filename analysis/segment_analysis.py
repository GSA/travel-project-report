#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 11:38:17 2019

@author: austinpeel
"""


from models.models import Segment , Transactions, Train_Plane, Trip

import statsmodels.formula.api as sm
import statsmodels.api as sm2
import matplotlib.pyplot as plt
from statsmodels.iolib.summary2 import summary_col


# Segment level analysis
seg = Segment()

#what does this look like
seg
print(seg)

#need help interpreting columns
seg.describe("")


#lets look at model 1
model = seg.model_1()

#what are we doing with this model
print(model)

#this is the data we are using 
df = model.model_data


#model your own regression
result = sm.ols(formula = 'cost_per_mile ~ city_pair_ratio +no_CA_award + market_share_log + fare_type +  ticketing_adv_booking_group + city_pair_code ',data=model.model_data).fit()
print(result.summary())
result = sm.ols(formula = 'cost_per_mile ~ city_pair_ratio + fare_type  + market_share_log  + fare_type*city_pair_ratio + no_CA_award + ticketing_adv_booking_group  + ticketing_adv_booking_group*fare_type + city_pair_code',data=model.model_data).fit()
print(result.summary())
#here are some pre-defined regression. we will put the ones in final analysis here. 
res1 = model.regression_1()
res2 = model.regression_2()
res3 = model.regression_3()
res4 = model.regression_4()

df['CPP'] = df.DashCA_x + df.YCA_x
df['ratio_squared'] = df.city_pair_ratio * df.city_pair_ratio
reg = sm.logit(formula = 'CPP ~ dash_per_mile + YCA_per_mile + PAX_COUNT + cost_per_mile + market_share_log +ticketing_adv_booking_group +city_pair_ratio + c_squared',data=model.model_data).fit().summary()

reg.as_html()

# combining similar models into one output
dfoutput = summary_col([res1,res2,res3,res4],stars=True)
html = dfoutput.as_html()

order.sort(reverse=True)

params = pd.DataFrame(res4.params)
order = list(params.index)
#some plots and stuff
fig = plt.figure(figsize=(15,8))
fig = sm2.graphics.plot_regress_exog(res4, "city_pair_ratio", fig=fig)




for i in df.city_pair_code.unique():
    new = df[df.city_pair_code == i]
    result = sm.ols(formula = ' booking_advanced_days ~  + fare_type ',data=new).fit()
    print(i)
    print(result.summary())

CLE-MDW
OAK-SAN
    
a = res4.summary().as_html()



from statsmodels.stats.diagnostic import het_breuschpagan as bp , het_white as hw
test = hw(res4.resid, res4.model.exog)



from statsmodels.stats.outliers_influence import variance_inflation_factor



import numpy as np
np.array(vif).mean()


df['booking_advanced_days'] = df.booking_advanced_days + 1
df['log_days'] = np.log(df.booking_advanced_days)


result = sm.ols(formula = ' booking_advanced_days ~  + city_pair_code ',data=model.model_data).fit()


new = df[['city_pair_code','DG_x','YCA_x','DashCA_x','Other_x']]
d = new.groupby(by =['city_pair_code'],as_index=False).sum()


new = df[df.city_pair_code != 'CLE-MDW']
new = new[new.city_pair_code != 'OAK-SAN']

result = sm.ols(formula = 'cost_per_mile ~  booking_advanced_days + city_pair_code ',data=df).fit()


result.summary()


booking_advanced_days

variables = result.model.exog
vif = [variance_inflation_factor(variables, i) for i in range(variables.shape[1])]
vif 




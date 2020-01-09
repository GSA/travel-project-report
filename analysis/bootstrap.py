#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 13:08:43 2019

@author: austinpeel
"""

import itertools
import os

import pickle
import random
import sys

module_path = os.path.abspath(os.path.join('..'))

sys.path.append(os.getcwd)

import pandas as pd
from scipy.stats import sem, t, norm
from scipy import mean
import seaborn as sns
import statsmodels.formula.api as sm

from ... import models.models.Segment as Segment

#Using model 1
model = Segment().model_1()

#this is the data we are using 
df = model.model_data

formula = (
           "cost_per_mile ~   market_share_log  + month + day_of_week + C(Year) + "
           "no_CA_award + booking_days_standarized + booking_days_standarized*C(fare_type, "
           "Treatment(reference='Dash CA')) + city_pair_code + self_booking_indicator"
          )
#this model uses the standarized booking advanced days
result = sm.ols(formula = formula, data = df).fit()
result.summary()

# add in placeholder col for the traveler until I updated models.py
#df['traveler'] = [random.choice(range(1000)) for i in range(df.shape[0])]

def cluster_bootstrap(df, cluster = 'EMAIL'):
    '''
    cluster resample with replacement from a dataframe
    '''
    n_rows = df.shape[0]
    unique_travelers = df[cluster].unique()

    data = []
    row_counter = 0
    while row_counter < n_rows:
        random_traveler = random.choice(unique_travelers)
        traveler_df = df[df[cluster] == random_traveler]
        data.append(traveler_df)
        row_counter += traveler_df.shape[0]

    bootstrapped_df = pd.concat(data)
    
    return bootstrapped_df


def gen_new_data(combinations, new_sample, exog_cont, exog_fact, booking_days_col):
    '''
    Genereates the simulated observations where all of the control variables equal their expected value
    and each combination of our interaction term is represented.
    '''
    new_data = []
    for c in combinations:
        #they all get the expected value for their control vars
        controls = list(new_sample.values[0])
        exog = list(c)
        row = controls + exog
        new_data.append(row)

    new_data_df = pd.DataFrame(new_data)
    new_data_df.columns = exog_cont + exog_fact + ['fare_type', booking_days_col]
    #this needs to be a float and not object in order to pass it into the model for predictions
    new_data_df[booking_days_col] = new_data_df[booking_days_col].astype(float)

    return new_data_df

def calc_ci(data, confidence = .95):
    '''
    given a series of data, calculate a 95% CI, returning the upper and lower bounds along with the std_err
    and p_value
    '''
    n = len(data)
    m = mean(data)
    std_err = sem(data)
    z = t.ppf((1 + confidence) / 2, n - 1)
    h = std_err * z

    start = m - h
    end = m + h
    
    p_value = norm.sf(abs(z))*2
    
    return start, end, std_err, p_value


def bootstrap_resample(df, formula, original_model, n = 10000, booking_days_col = 'booking_days_log'):
    '''
    Given a dataframe and OLS formula, bootstrap n times. Fit a model with each iteration, saving the results.
    Also randomly generate a new data point with the expected value for the control variables and randomly generated
    values for the variables of interest. Save that predicted value along with the randomly adjusted inputs.
    '''
    #specify control vars of interest from the model specification, distinguishing between factors and continuous vars
    exog_cont = ['cost_per_mile', 'market_share_log']
    exog_fact = ['month', 'day_of_week', 'Year', 'no_CA_award', 'city_pair_code', 'self_booking_indicator']

    #get expected values for these control variables
    fixed_exog_cont = pd.DataFrame(df[exog_cont].mean()).transpose()
    fixed_exog_fact = df[exog_fact].mode()

    #combine these expected values into a df that'll be re-used in each iteration
    new_sample = pd.concat([fixed_exog_cont, fixed_exog_fact], axis = 1)
    #get list of unique fare types to randomly draw from in each iteration
    fare_types = df['fare_type'].unique()
    #concat combinations of fare_type:booking_days_standardized to control vars
    booking_days_col_unique_values = df[booking_days_col].unique()
    combinations = list(itertools.product(fare_types, booking_days_col_unique_values))
    new_data_df = gen_new_data(combinations, new_sample, exog_cont, exog_fact, booking_days_col)
    
    #create a dict where the keys are the original model's coeffecients
    params = {k:[] for k in original_model.params.to_dict().keys()}
    y_preds = {k:[] for k in combinations}
    for i in range(n):
        #create bootstrap sample and fit a model using that sample
        bootstrapped_df = cluster_bootstrap(df)
        bootstrapped_result = sm.ols(formula = formula, data = bootstrapped_df).fit()

        #get the coeffecients
        _params = bootstrapped_result.params.to_dict()
        for k in _params:
            params[k].append(_params[k])

        y_pred = bootstrapped_result.predict(new_data_df)
        for combination, y_hat in zip(combinations, y_pred):
            y_preds[combination].append(y_hat)
        
        #log progress
        if i % 1000 == 0 and i != 0:
            print( f"Done with {i} iterations.")
    
    param_stats = {k:calc_ci(v) for k,v in params.items()}
    y_pred_stats = {k:calc_ci(v) for k,v in y_preds.items()}
    
    return param_stats, y_pred_stats, y_preds


#this takes a long time. Could possibly refactor to improve performance
param_stats, y_pred_stats, y_preds = bootstrap_resample(df, formula, result, n = 10000)


#Write results
with open('models/param_stats.pkl', 'wb') as f:
    pickle.dump(param_stats, f)
    
with open('models/y_pred_stats.pkl', 'wb') as f:
    pickle.dump(y_pred_stats, f)
    
with open('models/y_preds.pkl', 'wb') as f:
    pickle.dump(y_preds, f)




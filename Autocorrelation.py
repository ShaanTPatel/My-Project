#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 05:23:58 2023

@author: shaanpatel
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import acf

# Read the CSV files
temp_data = pd.read_csv('temp19602020.csv')
rainfall_data = pd.read_csv('totalrainfall19602020.csv')

# Convert the date column to datetime format
temp_data['Date'] = pd.to_datetime(temp_data['Date'])
rainfall_data['Date'] = pd.to_datetime(rainfall_data['Date'])

# Set the date column as the index
temp_data.set_index('Date', inplace=True)
rainfall_data.set_index('Date', inplace=True)

# Calculate monthly means
temp_monthly_mean = temp_data['1961-01-01':'2020-12-31'].resample('M').mean()
rainfall_monthly_mean = rainfall_data['1961-01-01':'2020-12-31'].resample('M').mean()

# Calculate autocorrelation for temperature and rainfall
temp_autocorr = acf(temp_monthly_mean['Mean Temp'], nlags=12)
rainfall_autocorr = acf(rainfall_monthly_mean['Total rainfall (mm)'], nlags=12)

# Plot autocorrelation
plt.figure(figsize=(10, 5))
plt.stem(temp_autocorr)
plt.title('Autocorrelation of mean (monthly) temperature across London from 1961-2020')
plt.xlabel('Lags')
plt.ylabel('Autocorrelation')

plt.figure(figsize=(10,5))
plt.stem(rainfall_autocorr)
plt.title('Autocorrelation of mean (monthly) rainfall across London from 1961-2020')
plt.xlabel('Lags')
plt.ylabel('Autocorrelation')

plt.tight_layout()
plt.show()

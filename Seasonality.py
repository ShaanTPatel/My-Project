#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 12:38:19 2023

@author: shaanpatel
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose

# Set the path to the dataset
file_path = "/Users/shaanpatel/Desktop/Data 2/TotalRainfall19602020.csv"

# Read the dataset into a pandas DataFrame
data = pd.read_csv(file_path)

# Convert the 'Date' column to datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Set 'Date' as the index column
data.set_index('Date', inplace=True)

# Resample the data to monthly frequency and calculate the sum for each month
monthly_rainfall = data['Total rainfall (mm)'].resample('M').sum()

# Perform seasonal decomposition
decomposition = seasonal_decompose(monthly_rainfall, model='additive', period=12)

# Plot the decomposed components
plt.figure(figsize=(12, 8))

plt.subplot(411)
plt.plot(monthly_rainfall, color='blue')
plt.title('Monthly Rainfall (mm) across London from 1961-2020')
plt.ylabel('Rainfall (mm)')
plt.legend(loc='best')

plt.subplot(412)
plt.plot(decomposition.trend, color='green')
plt.title('Trend')
plt.ylabel('Rainfall (mm)')
plt.legend(loc='best')

plt.subplot(413)
plt.plot(decomposition.seasonal, color='red')
plt.title('Seasonality')
plt.ylabel('Rainfall (mm)')
plt.legend(loc='best')

plt.subplot(414)
plt.plot(decomposition.resid, color='purple')
plt.title('Residuals')
plt.ylabel('Rainfall (mm)')
plt.legend(loc='best')

plt.tight_layout()
plt.show()



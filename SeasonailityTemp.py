#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 19:50:29 2023
@author: shaanpatel
"""

#Seasonality analysis of the historical temperature data.

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Define the file path
file_path = "/Users/shaanpatel/desktop/Data 2/Temp19602020.csv"

# Read the CSV file into a pandas DataFrame
data = pd.read_csv(file_path)

# Convert the 'Date' column to datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Set the 'Date' column as the DataFrame index
data.set_index('Date', inplace=True)

# Resample the data by month and calculate the mean temperature
monthly_data = data['Mean Temp'].resample('M').mean()

# Decompose the time series into trend, seasonal, and residual components
decomposition = sm.tsa.seasonal_decompose(monthly_data, model='additive')

# Get the trend, seasonal, and residual components
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

# Create a figure and axis objects for subplots
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 12))

# Plot the original time series in blue
ax1.plot(monthly_data.index, monthly_data, color='#990000', linewidth=2)
ax1.set_title('Monthly Temperature (°C) across London from 1961-2020')
ax1.set_ylabel('Temperature (°C)')

# Plot the trend component in green
ax2.plot(trend.index, trend, color='green', linewidth=2)
ax2.set_title('Trend Component')
ax2.set_ylabel('Temperature (°C)')

# Plot the seasonal component in red
ax3.plot(seasonal.index, seasonal, color='blue', linewidth=2)
ax3.set_title('Seasonal Component')
ax3.set_ylabel('Temperature (°C)')

# Plot the residual component in purple
ax4.plot(residual.index, residual, color='purple', linewidth=2)
ax4.set_title('Residual Component')
ax4.set_xlabel('Date')
ax4.set_ylabel('Temperature (°C)')

# Adjust the spacing between subplots
plt.tight_layout()

# Show the decomposition plots
plt.show()

# Plot the daily temperature data in a darker shade of red
daily_data = data['Mean Temp']

# Create a figure and axis objects for plotting
fig, ax = plt.subplots(figsize=(10, 6))

# Plot the daily temperature data in a darker shade of red
ax.plot(daily_data.index, daily_data, color='#990000', linewidth=2)  # Darker shade of red: '#990000'
ax.set_title('Daily Temperature Data')
ax.set_xlabel('Date')
ax.set_ylabel('Temperature (°C)')

# Rotate the x-axis labels for better readability
ax.tick_params(axis='x', rotation=45)

# Show the plot
plt.tight_layout()
plt.show()

# Assuming you already have the DataFrame 'data' with the 'Mean Temp' and 'Date' columns

# Convert the 'Date' column to datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Set the 'Date' column as the DataFrame index
data.set_index('Date', inplace=True)

# Resample the data by month and calculate the mean temperature
monthly_data = data['Mean Temp'].resample('M').mean()

# Plot the ACF
sm.graphics.tsa.plot_acf(monthly_data, lags=30)  # You can adjust the 'lags' parameter to display more or fewer lags.
plt.xlabel('Lags')
plt.ylabel('Autocorrelation')
plt.title('Autocorrelation Function (ACF) of Monthly Temperature Data')
plt.show()

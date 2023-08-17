#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 12:39:54 2023

@author: shaanpatel
"""

import pandas as pd
import matplotlib.pyplot as plt

# File path and name
file_path = '/users/shaanpatel/Desktop/Data 2/60km/MeanPrecipRCP85.csv'

# Read the CSV file into a pandas DataFrame
data = pd.read_csv(file_path)

# Convert 'Date' column to datetime type, ignoring invalid dates
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

# Drop rows with invalid dates
data.dropna(subset=['Date'], inplace=True)

# Set 'Date' column as the index
data.set_index('Date', inplace=True)

# Resample the data to monthly frequency
data_monthly = data.resample('M').mean()

# Get the remaining column names (y values)
y_values = data_monthly.columns[1:]

# Define colors for the plots with improved contrast
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#800080', '#00ff00']

# Calculate the number of rows and columns for the subplots
num_rows = 3
num_cols = 4

# Create a figure and subplots
fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 10))
fig.tight_layout(pad=3.0)

# Iterate over each column and plot the time series
for i, column in enumerate(y_values):
    row = i // num_cols
    col = i % num_cols
    ax = axes[row, col]

    # Plot the time series data
    ax.plot(data_monthly.index, data_monthly[column], color=colors[i], label=column)
    ax.set_title(column, fontsize=8)  # Set smaller font size for titles

    # Plot the seasonality trend line
    trend_line = data_monthly[column].rolling(window=12, min_periods=1).mean()
    ax.plot(data_monthly.index, trend_line, color='black', linewidth=1, linestyle='--', label='Seasonality Trend')

    # Format x-axis labels
    ax.xaxis.set_major_locator(plt.MaxNLocator(6))
    ax.xaxis.set_tick_params(rotation=90, labelsize=8)  # Rotate and set smaller font size for x-axis labels

    # Format x-axis tick labels
    ax.tick_params(axis='x', which='both', labelsize=5)  # Set smaller font size for x-axis tick labels

    # Set the legend with smaller font size and improved contrast
    ax.legend(fontsize=6)

# Hide any unused subplots
for i in range(len(y_values), num_rows * num_cols):
    row = i // num_cols
    col = i % num_cols
    axes[row, col].axis('off')

# Display the plots
plt.show()


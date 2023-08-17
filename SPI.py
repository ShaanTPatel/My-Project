#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 11:35:30 2023

@author: shaanpatel
"""

##SPI Analysis of the historical precipitation data.

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from scipy.stats import norm

# Define the necessary functions for SPI calculation
def calculate_spi(data, timescale):
    # Calculate the cumulative precipitation for the specified timescale
    cumulative_precip = data.groupby(pd.Grouper(freq=timescale)).sum()

    # Calculate the mean and standard deviation of the cumulative precipitation
    mean = cumulative_precip.mean()
    std_dev = cumulative_precip.std()

    # Calculate the SPI values
    spi_values = (cumulative_precip - mean) / std_dev

    return spi_values

# File path of the precipitation data
precipitation_file_path = '/users/shaanpatel/desktop/Data 2/Rainfall19612020.csv'

# Load the data from the CSV file
precip_data = pd.read_csv(precipitation_file_path)

# Convert the date column to datetime format
precip_data['Date'] = pd.to_datetime(precip_data['Date'])

# Set the date column as the index
precip_data.set_index('Date', inplace=True)

# Specify the column name for precipitation
precip_column = 'Total rainfall (mm)'  # Update with the correct column name

# Calculate the SPI for winter months (December to February)
winter_spi = calculate_spi(precip_data.loc[precip_data.index.month.isin([12, 1, 2])], 'Y')

# Calculate the SPI for summer months (June to August)
summer_spi = calculate_spi(precip_data.loc[precip_data.index.month.isin([6, 7, 8])], 'Y')

# Calculate the SPI on a yearly scale
yearly_spi = calculate_spi(precip_data, 'Y')

# Save the SPI values to CSV files
winter_spi_output_path = '/users/shaanpatel/desktop/Data 2/Winter_SPI_Results.csv'
summer_spi_output_path = '/users/shaanpatel/desktop/Data 2/Summer_SPI_Results.csv'
yearly_spi_output_path = '/users/shaanpatel/desktop/Data 2/Yearly_SPI_Results.csv'

winter_spi.to_csv(winter_spi_output_path)
summer_spi.to_csv(summer_spi_output_path)
yearly_spi.to_csv(yearly_spi_output_path)

print("Winter SPI calculation completed and results saved to:", winter_spi_output_path)
print("Summer SPI calculation completed and results saved to:", summer_spi_output_path)
print("Yearly SPI calculation completed and results saved to:", yearly_spi_output_path)

# Trend Analysis and PDF Plot - Winter SPI
winter_spi_data = pd.read_csv(winter_spi_output_path)
winter_spi_data['Date'] = pd.to_datetime(winter_spi_data['Date'])
winter_spi_data.set_index('Date', inplace=True)

fig, ax1 = plt.subplots(figsize=(12, 5))

# Winter SPI Trend Analysis
ax1.plot(winter_spi_data.index, winter_spi_data[precip_column], color='blue', linewidth=1.5)
ax1.set_xlabel('Year')
ax1.set_ylabel('SPI')
ax1.set_title('Winter SPI Trend Analysis')
ax1.grid(True)

# Format x-axis labels
ax1.xaxis.set_major_locator(mdates.YearLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.xticks(rotation=90)  # Rotate x-axis tick labels by 90 degrees

# Display the Winter SPI trend analysis plot
plt.show()

# Winter SPI Probability Distribution Function (PDF) Plot
fig, ax2 = plt.subplots(figsize=(8, 6))

# Winter SPI Probability Distribution Function (PDF)
ax2.hist(winter_spi_data[precip_column], bins=20, density=True, edgecolor='black', color='blue', alpha=0.7)
ax2.set_xlabel('SPI')
ax2.set_ylabel('Probability Density')
ax2.set_title('Winter SPI Probability Distribution Function')

# Fit a curve to the data
mean, std_dev = norm.fit(winter_spi_data[precip_column])
x = np.linspace(min(winter_spi_data[precip_column]), max(winter_spi_data[precip_column]), 100)
pdf = norm.pdf(x, mean, std_dev)
ax2.plot(x, pdf, 'r-', label='Fit')

# Display the legend
ax2.legend()

# Display the Winter SPI PDF plot
plt.xticks(rotation=90)  # Rotate x-axis tick labels by 90 degrees
plt.show()

# Trend Analysis and PDF Plot - Summer SPI
summer_spi_data = pd.read_csv(summer_spi_output_path)
summer_spi_data['Date'] = pd.to_datetime(summer_spi_data['Date'])
summer_spi_data.set_index('Date', inplace=True)

fig, ax1 = plt.subplots(figsize=(12, 5))

# Summer SPI Trend Analysis
ax1.plot(summer_spi_data.index, summer_spi_data[precip_column], color='red', linewidth=1.5)
ax1.set_xlabel('Year')
ax1.set_ylabel('SPI')
ax1.set_title('Summer SPI Trend Analysis')
ax1.grid(True)

# Format x-axis labels
ax1.xaxis.set_major_locator(mdates.YearLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.xticks(rotation=90)  # Rotate x-axis tick labels by 90 degrees

# Display the Summer SPI trend analysis plot
plt.show()

# Summer SPI Probability Distribution Function (PDF) Plot
fig, ax2 = plt.subplots(figsize=(8, 6))

# Summer SPI Probability Distribution Function (PDF)
ax2.hist(summer_spi_data[precip_column], bins=20, density=True, edgecolor='black', color='red', alpha=0.7)
ax2.set_xlabel('SPI')
ax2.set_ylabel('Probability Density')
ax2.set_title('Summer SPI Probability Distribution Function')

# Fit a curve to the data
mean, std_dev = norm.fit(summer_spi_data[precip_column])
x = np.linspace(min(summer_spi_data[precip_column]), max(summer_spi_data[precip_column]), 100)
pdf = norm.pdf(x, mean, std_dev)
ax2.plot(x, pdf, 'r-', label='Fit')

# Display the legend
ax2.legend()

# Display the Summer SPI PDF plot
plt.xticks(rotation=90)  # Rotate x-axis tick labels by 90 degrees
plt.show()

# Trend Analysis and PDF Plot - Yearly SPI
yearly_spi_data = pd.read_csv(yearly_spi_output_path)
yearly_spi_data['Date'] = pd.to_datetime(yearly_spi_data['Date'])
yearly_spi_data.set_index('Date', inplace=True)

fig, ax3 = plt.subplots(figsize=(12, 5))

# Yearly SPI Trend Analysis
ax3.plot(yearly_spi_data.index, yearly_spi_data[precip_column], color='green', linewidth=1.5)
ax3.set_xlabel('Year')
ax3.set_ylabel('SPI')
ax3.set_title('Yearly SPI Trend Analysis')
ax3.grid(True)

# Format x-axis labels
ax3.xaxis.set_major_locator(mdates.YearLocator())
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.xticks(rotation=90)  # Rotate x-axis tick labels by 90 degrees

# Display the Yearly SPI trend analysis plot
plt.show()

# Yearly SPI Probability Distribution Function (PDF) Plot
fig, ax4 = plt.subplots(figsize=(8, 6))

# Yearly SPI Probability Distribution Function (PDF)
ax4.hist(yearly_spi_data[precip_column], bins=20, density=True, edgecolor='black', color='blue', alpha=0.7)
ax4.set_xlabel('SPI')
ax4.set_ylabel('Probability Density')
ax4.set_title('Yearly SPI Probability Distribution Function')

# Fit a curve to the data
mean, std_dev = norm.fit(yearly_spi_data[precip_column])
x = np.linspace(min(yearly_spi_data[precip_column]), max(yearly_spi_data[precip_column]), 100)
pdf = norm.pdf(x, mean, std_dev)
ax4.plot(x, pdf, 'r-', label='Fit')

# Display the legend
ax4.legend()

# Display the Yearly SPI PDF plot
plt.xticks(rotation=90)  # Rotate x-axis tick labels by 90 degrees
plt.show()

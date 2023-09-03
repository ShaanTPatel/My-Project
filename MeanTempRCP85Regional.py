#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 00:45:43 2023

@author: shaanpatel
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file (mean temperature dataset)
file_path = "/users/shaanpatel/desktop/Data 2/12km/MeanTempRCP85Regional.csv"
data = pd.read_csv(file_path)

# Convert 'Date' column to datetime
data['Date'] = pd.to_datetime(data['Date'])

# Extract the year from the 'Date' column
data['Year'] = data['Date'].dt.year

# Calculate annual mean temperature for each model
annual_data = data.groupby(['Year']).mean()

# Separate the columns into models
models = annual_data.columns[0:12]  # Exclude the 'Year' column

# Plot models together
plt.figure(figsize=(10, 6))
plt.title('Mean Temperature for Different Models', fontsize=16)

# Prepare summary data for models
summary_columns = ['Model', '1981 Mean', '2080 Mean', 'Difference']
summary_data = []

for model in models:
    model_data = annual_data[model]
    
    color = np.random.rand(3,)  # Generate a random color for each model
    plt.plot(model_data.index, model_data, label=model, color=color)
    
    # Calculate statistics
    mean_1981 = model_data.loc[1981]
    mean_2080 = model_data.loc[2080] if 2080 in model_data.index else np.nan
    
    difference = mean_2080 - mean_1981  # Calculate the difference
    
    summary_data.append([model, mean_1981, mean_2080, difference])

# Show the plot
plt.xlabel('Year')
plt.ylabel('Mean Temperature (°C)')
plt.title('Annual Mean Temperature from 1981-2080 using Regional Models')

# Move the legend outside the plot area
plt.legend(fontsize=7, bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(np.arange(1981, 2090, 10), rotation='vertical', fontsize=8)
plt.show()

# Create a summary table for models
summary_table = pd.DataFrame(summary_data, columns=summary_columns)

# Save the summary table to a CSV file
summary_file_path = file_path.replace('.csv', '_summary_table.csv')
summary_table.to_csv(summary_file_path, index=False)

# Print the summary table
print("Models Summary Table:")
print(summary_table)
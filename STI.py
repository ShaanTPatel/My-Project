#STI analysis of the historical Temp data.

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from scipy.stats import norm

# Define the necessary functions for STI calculation
def calculate_sti(data, timescale):
    # Calculate the cumulative temperature for the specified timescale
    cumulative_temp = data.groupby(pd.Grouper(freq=timescale)).sum()

    # Calculate the mean and standard deviation of the cumulative temperature
    mean = cumulative_temp.mean()
    std_dev = cumulative_temp.std()

    # Calculate the STI values
    sti_values = (cumulative_temp - mean) / std_dev

    return sti_values

# File path of the temperature data
temperature_file_path = '/users/shaanpatel/desktop/Data 2/Temp19602020.csv'

# Load the data from the CSV file
temp_data = pd.read_csv(temperature_file_path)

# Convert the date column to datetime format
temp_data['Date'] = pd.to_datetime(temp_data['Date'])

# Set the date column as the index
temp_data.set_index('Date', inplace=True)

# Specify the column name for temperature
temp_column = 'Temperature (C)'  # Update with the correct column name

# Calculate the STI for winter months (December to February)
winter_sti = calculate_sti(temp_data.loc[temp_data.index.month.isin([12, 1, 2])], 'Y')

# Calculate the STI for summer months (June to August)
summer_sti = calculate_sti(temp_data.loc[temp_data.index.month.isin([6, 7, 8])], 'Y')

# Calculate the STI on a yearly scale
yearly_sti = calculate_sti(temp_data, 'Y')

# Save the STI values to CSV files
winter_sti_output_path = '/users/shaanpatel/desktop/Data 2/Winter_STI_Results.csv'
summer_sti_output_path = '/users/shaanpatel/desktop/Data 2/Summer_STI_Results.csv'
yearly_sti_output_path = '/users/shaanpatel/desktop/Data 2/Yearly_STI_Results.csv'

winter_sti.to_csv(winter_sti_output_path)
summer_sti.to_csv(summer_sti_output_path)
yearly_sti.to_csv(yearly_sti_output_path)

print("Winter STI calculation completed and results saved to:", winter_sti_output_path)
print("Summer STI calculation completed and results saved to:", summer_sti_output_path)
print("Yearly STI calculation completed and results saved to:", yearly_sti_output_path)

# Trend Analysis and PDF Plot - Winter STI
winter_sti_data = pd.read_csv(winter_sti_output_path)
winter_sti_data['Date'] = pd.to_datetime(winter_sti_data['Date'])
winter_sti_data.set_index('Date', inplace=True)

fig, ax1 = plt.subplots(figsize=(12, 5))

# Winter STI Trend Analysis
ax1.plot(winter_sti_data.index, winter_sti_data[temp_column], color='blue', linewidth=1.5)
ax1.set_xlabel('Year')
ax1.set_ylabel('STI')
ax1.set_title('Winter STI Trend Analysis')
ax1.grid(True)

# Format x-axis labels
ax1.xaxis.set_major_locator(mdates.YearLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.xticks(rotation=90)  # Rotate x-axis tick labels by 90 degrees

# Display the Winter STI trend analysis plot
plt.show()

# Winter STI Probability Distribution Function (PDF) Plot
fig, ax2 = plt.subplots(figsize=(8, 6))

# Winter STI Probability Distribution Function (PDF)
ax2.hist(winter_sti_data[temp_column], bins=20, density=True, edgecolor='black', color='blue', alpha=0.7)
ax2.set_xlabel('STI')
ax2.set_ylabel('Probability Density')
ax2.set_title('Winter STI Probability Distribution Function')

# Fit a curve to the data
mean, std_dev = norm.fit(winter_sti_data[temp_column])
x = np.linspace(min(winter_sti_data[temp_column]), max(winter_sti_data[temp_column]), 100)
pdf = norm.pdf(x, mean, std_dev)
ax2.plot(x, pdf, 'r-', label='Fit')

# Display the legend
ax2.legend()

# Display the Winter STI PDF plot
plt.xticks(rotation=90)  # Rotate x-axis tick labels by 90 degrees
plt.show()

# Trend Analysis and PDF Plot - Summer STI
summer_sti_data = pd.read_csv(summer_sti_output_path)
summer_sti_data['Date'] = pd.to_datetime(summer_sti_data['Date'])
summer_sti_data.set_index('Date', inplace=True)

fig, ax1 = plt.subplots(figsize=(12, 5))

# Summer STI Trend Analysis
ax1.plot(summer_sti_data.index, summer_sti_data[temp_column], color='red', linewidth=1.5)
ax1.set_xlabel('Year')
ax1.set_ylabel('STI')
ax1.set_title('Summer STI Trend Analysis')
ax1.grid(True)

# Format x-axis labels
ax1.xaxis.set_major_locator(mdates.YearLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.xticks(rotation=90)  # Rotate x-axis tick labels by 90 degrees

# Display the Summer STI trend analysis plot
plt.show()

# Summer STI Probability Distribution Function (PDF) Plot
fig, ax2 = plt.subplots(figsize=(8, 6))

# Summer STI Probability Distribution Function (PDF)
ax2.hist(summer_sti_data[temp_column], bins=20, density=True, edgecolor='black', color='red', alpha=0.7)
ax2.set_xlabel('STI')
ax2.set_ylabel('Probability Density')
ax2.set_title('Summer STI Probability Distribution Function')

# Fit a curve to the data
mean, std_dev = norm.fit(summer_sti_data[temp_column])
x = np.linspace(min(summer_sti_data[temp_column]), max(summer_sti_data[temp_column]), 100)
pdf = norm.pdf(x, mean, std_dev)
ax2.plot(x, pdf, 'r-', label='Fit')

# Display the legend
ax2.legend()

# Display the Summer STI PDF plot
plt.xticks(rotation=90)  # Rotate x-axis tick labels by 90 degrees
plt.show()

# Trend Analysis and PDF Plot - Yearly STI
yearly_sti_data = pd.read_csv(yearly_sti_output_path)
yearly_sti_data['Date'] = pd.to_datetime(yearly_sti_data['Date'])
yearly_sti_data.set_index('Date', inplace=True)

fig, ax3 = plt.subplots(figsize=(12, 5))

# Yearly STI Trend Analysis
ax3.plot(yearly_sti_data.index, yearly_sti_data[temp_column], color='green', linewidth=1.5)
ax3.set_xlabel('Year')
ax3.set_ylabel('STI')
ax3.set_title('Yearly STI Trend Analysis')
ax3.grid(True)

# Format x-axis labels
ax3.xaxis.set_major_locator(mdates.YearLocator())
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.xticks(rotation=90)  # Rotate x-axis tick labels by 90 degrees

# Display the Yearly STI trend analysis plot
plt.show()

# Yearly STI Probability Distribution Function (PDF) Plot
fig, ax4 = plt.subplots(figsize=(8, 6))

# Yearly STI Probability Distribution Function (PDF)
ax4.hist(yearly_sti_data[temp_column], bins=20, density=True, edgecolor='black', color='blue', alpha=0.7)
ax4.set_xlabel('STI')
ax4.set_ylabel('Probability Density')
ax4.set_title('Yearly STI Probability Distribution Function')

# Fit a curve to the data
mean, std_dev = norm.fit(yearly_sti_data[temp_column])
x = np.linspace(min(yearly_sti_data[temp_column]), max(yearly_sti_data[temp_column]), 100)
pdf = norm.pdf(x, mean, std_dev)
ax4.plot(x, pdf, 'r-', label='Fit')

# Display the legend
ax4.legend()

# Display the Yearly STI PDF plot
plt.xticks(rotation=90)  # Rotate x-axis tick labels by 90 degrees
plt.show()

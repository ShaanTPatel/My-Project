import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

# Load the CSV file
file_path = "/users/shaanpatel/desktop/Data 2/60km/MeanTempRCP85Global.csv"
data = pd.read_csv(file_path)

# Convert 'Date' column to datetime
data['Date'] = pd.to_datetime(data['Date'])

# Extract the year and month from the 'Date' column
data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month

# Calculate annual mean temperature for each model for all months
annual_data = data.groupby(['Year']).mean()

# Separate the columns into models
models = annual_data.columns[0:28]  # Exclude the 'Year' column

# Separate the models with 'HadGEM3' in their name
hadg3_models = [model for model in models if 'HadGEM3' in model]
other_models = [model for model in models if model not in hadg3_models]

# Plot 'HadGEM3' models together
plt.figure(figsize=(10, 6))
plt.title('HadGEM3 Models - Annual Mean Temperature', fontsize=16)

# Prepare summary data for HadGEM3 models
hadg3_summary_columns = ['Model', '1900 Mean', '2099 Mean', 'Difference']
hadg3_summary_data = []

for model in hadg3_models:
    model_data = annual_data[model]
    
    color = np.random.rand(3,)  # Generate a random color for each model
    plt.plot(model_data.index, model_data, label=model, color=color)
    
    # Calculate statistics
    mean_1900 = model_data.loc[1900]
    mean_2099 = model_data.loc[2099] if 2099 in model_data.index else np.nan
    
    difference = mean_2099 - mean_1900  # Calculate the difference
    
    hadg3_summary_data.append([model, mean_1900, mean_2099, difference])

# Show the 'HadGEM3' plot
plt.xlabel('Year')
plt.ylabel('Mean Temperature')
plt.title('Annual Mean Temperature across London from 1900-2100 using the HadGEM3-GC3.05 models')

# Move the legend outside the plot area
plt.legend(fontsize=7, bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(np.arange(1900, 2101, 10), rotation='vertical', fontsize=5)
plt.show()

# Create a summary table for HadGEM3 models
hadg3_summary_table = pd.DataFrame(hadg3_summary_data, columns=hadg3_summary_columns)

# Save the summary table to a CSV file for HadGEM3 models
hadg3_summary_file_path = file_path.replace('.csv', '_hadgem3_annual_summary_table.csv')
hadg3_summary_table.to_csv(hadg3_summary_file_path, index=False)

# Print the HadGEM3 summary table
print("HadGEM3 Models Annual Summary Table:")
print(hadg3_summary_table)

# Plot other models together on a separate plot
plt.figure(figsize=(10, 6))
plt.title('Other Models - Annual Mean Temperature', fontsize=16)

# Prepare summary data for other models
other_summary_columns = ['Model', '1900 Mean', '2099 Mean', 'Difference']
other_summary_data = []

for model in other_models:
    model_data = annual_data[model]
    
    color = np.random.rand(3,)  # Generate a random color for each model
    plt.plot(model_data.index, model_data, label=model, color=color)
    
    # Calculate statistics
    mean_1900 = model_data.loc[1900]
    mean_2099 = model_data.loc[2099] if 2099 in model_data.index else np.nan
    
    difference = mean_2099 - mean_1900  # Calculate the difference
    
    other_summary_data.append([model, mean_1900, mean_2099, difference])

# Show the 'Other Models' plot
plt.xlabel('Year')
plt.ylabel('Mean Temperature')
plt.title('Annual Mean Temperature across London from 1900-2100 using the CMIP5 multi-model ensemble')

# Move the legend outside the plot area
plt.legend(fontsize=7, bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(np.arange(1900, 2101, 10), rotation='vertical', fontsize=5)
plt.show()

# Create a summary table for other models
other_summary_table = pd.DataFrame(other_summary_data, columns=other_summary_columns)

# Save the summary table to a CSV file for other models
other_summary_file_path = file_path.replace('.csv', '_other_annual_models_summary_table.csv')
other_summary_table.to_csv(other_summary_file_path, index=False)

# Print the other models summary table
print("Other Models Annual Summary Table:")
print(other_summary_table)

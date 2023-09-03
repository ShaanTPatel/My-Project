import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Load the CSV file with climate model data
file_path = "/users/shaanpatel/desktop/Data 2/60km/MeanTempRCP85Global.csv"
data = pd.read_csv(file_path)

# Convert 'Date' column to datetime
data['Date'] = pd.to_datetime(data['Date'])

# Extract the year and month from the 'Date' column
data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month

# Calculate annual mean temperature for each model for all months
annual_data = data.groupby(['Year']).mean()

# Load historical temperature data
data_folder = '/users/shaanpatel/desktop/Data 2'
historical_data_path = os.path.join(data_folder, 'Temp19602020.csv')
historical_data = pd.read_csv(historical_data_path)
historical_data['Date'] = pd.to_datetime(historical_data['Date'], format='%d/%m/%Y')

# Filter historical data for the period between 1981 and 2021
historical_data = historical_data[(historical_data['Date'].dt.year >= 1981) & (historical_data['Date'].dt.year <= 2021)]

# Calculate the yearly average of historical temperature data
historical_yearly_avg = historical_data.groupby(historical_data['Date'].dt.year)['Mean Temp'].mean()

# Separate the columns into models
models = annual_data.columns[0:28]  # Exclude the 'Year' column

# Calculate MAE for each model compared to historical data
mae_data = []

for model in models:
    model_data = annual_data[model]
    
    # Align model data with historical data based on years
    model_data_aligned = model_data.loc[historical_yearly_avg.index]
    
    # Calculate MAE
    mae = np.abs(model_data_aligned - historical_yearly_avg).mean()
    
    # Calculate accuracy percentage (higher is better)
    accuracy = 1 - (mae / historical_yearly_avg.mean())
    
    mae_data.append({'Model': model, 'MAE': mae, 'Accuracy (%)': accuracy * 100})

# Create a DataFrame for MAE and Accuracy data
mae_accuracy_df = pd.DataFrame(mae_data)

# Sort the DataFrame by MAE in ascending order
mae_accuracy_df = mae_accuracy_df.sort_values(by='MAE')

# Export the accuracies to a CSV file
accuracy_csv_path = os.path.join(data_folder, 'model_accuracies.csv')
mae_accuracy_df.to_csv(accuracy_csv_path, index=False)

# Display the MAE and Accuracy DataFrame
print("MAE and Accuracy for Each Model:")
print(mae_accuracy_df)

# Generate different colors for each model
colors = plt.cm.get_cmap('tab20', len(mae_accuracy_df))

# Create a bar chart to compare MAE for each model
plt.figure(figsize=(12, 8))
plt.barh(mae_accuracy_df['Model'], mae_accuracy_df['MAE'], color=colors(np.arange(len(mae_accuracy_df))))
plt.xlabel('Mean Absolute Error (MAE)')
plt.ylabel('Model')
plt.title('Comparison of Models to Historical Temperature Data')
plt.gca().invert_yaxis()  # Invert y-axis to display the lowest MAE at the top
plt.show()

print(f"Accuracies saved to {accuracy_csv_path}")

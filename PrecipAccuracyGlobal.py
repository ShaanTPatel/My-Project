import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the model data (mean precipitation rate)
model_data_file_path = "/users/shaanpatel/desktop/Data 2/60km/MeanPrecipRCP85Global.csv"
model_data = pd.read_csv(model_data_file_path)

# Load the historical data (daily precipitation)
historical_data_file_path = "/users/shaanpatel/desktop/data 2/totalrainfall19602020.csv"
historical_data = pd.read_csv(historical_data_file_path)

# Convert 'Date' columns to datetime
model_data['Date'] = pd.to_datetime(model_data['Date'])
historical_data['Date'] = pd.to_datetime(historical_data['Date'])

# Extract the year from the 'Date' columns
model_data['Year'] = model_data['Date'].dt.year
historical_data['Year'] = historical_data['Date'].dt.year

# Calculate annual mean precipitation for each model
annual_model_data = model_data.groupby(['Year']).mean()

# Calculate annual mean precipitation for historical data
annual_historical_data = historical_data.groupby(['Year'])['Total rainfall (mm)'].mean()

# Define the time range for comparison (1980-2020)
start_year = 1980
end_year = 2020

# Separate the columns into 'HadGEM3' and 'Other Models'
models = annual_model_data.columns[0:30]  # Exclude the 'Year' column
hadg3_models = [model for model in models if 'HadGEM3' in model]
other_models = [model for model in models if model not in hadg3_models]

# Create a dictionary to store model accuracy metrics
model_accuracies = {
    'Model': [],
    'Accuracy (%)': []
}

# Calculate accuracy metrics for each model for the specified time range
for model in models:
    model_data = annual_model_data[model]
    
    # Check if the model's data is available for the specified time range
    if start_year in model_data.index and end_year in model_data.index:
        # Filter model data for the specified time range
        model_data_range = model_data.loc[start_year:end_year]
        
        # Calculate accuracy as a percentage for the specified time range
        accuracy = (1 - (np.abs(model_data_range - annual_historical_data.loc[start_year:end_year]) /
                         annual_historical_data.loc[start_year:end_year])).mean() * 100
        
    else:
        accuracy = np.nan  # Model data not available
    
    # Store the accuracy in the dictionary
    model_accuracies['Model'].append(model)
    model_accuracies['Accuracy (%)'].append(accuracy)

# Create a DataFrame from the model accuracy metrics
accuracy_table = pd.DataFrame(model_accuracies)

# Sort models by accuracy in descending order
sorted_accuracy_table = accuracy_table.sort_values(by='Accuracy (%)', ascending=False)

# Print the table of model accuracies
print("Model Accuracies:")
print(sorted_accuracy_table)

# Define a unique color for each model
model_colors = sns.color_palette("tab20", len(sorted_accuracy_table))

# Plot accuracies as a horizontal bar chart with values and unique colors
plt.figure(figsize=(12, 8))
bars = sns.barplot(x='Accuracy (%)', y='Model', data=sorted_accuracy_table, orient='h', palette=model_colors)

# Add accuracy values at the end of each bar
for bar, accuracy in zip(bars.patches, sorted_accuracy_table['Accuracy (%)']):
    plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2, f'{accuracy:.2f}%', ha='left', va='center')

plt.title('Comparison of global model accuracies projecting precipitation rate across London', fontsize=16)
plt.xlabel('Accuracy (%)')
plt.ylabel('Model')

plt.tight_layout()
plt.show()

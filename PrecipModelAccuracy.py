import os
import pandas as pd
import matplotlib.pyplot as plt

# Load data and convert 'Date' column to datetime
data_folder = '/users/shaanpatel/desktop/Data 2/'
historical_rainfall_path = os.path.join(data_folder, 'TotalRainfall19602020.csv')
regional_projection_rainfall_path = os.path.join(data_folder, '12km/MeanPrecipRCP85Regional.csv')

historical_rainfall_df = pd.read_csv(historical_rainfall_path)
historical_rainfall_df['Date'] = pd.to_datetime(historical_rainfall_df['Date'], format='%d/%m/%Y')

regional_projection_rainfall_df = pd.read_csv(regional_projection_rainfall_path)
regional_projection_rainfall_df['Date'] = pd.to_datetime(regional_projection_rainfall_df['Date'], format='%d/%m/%Y')

# Filter data for the period between 1980 and 2021
historical_rainfall_df = historical_rainfall_df[(historical_rainfall_df['Date'] >= '1980-01-01') & (historical_rainfall_df['Date'] <= '2021-12-31')]
regional_projection_rainfall_df = regional_projection_rainfall_df[(regional_projection_rainfall_df['Date'] >= '1980-01-01') & (regional_projection_rainfall_df['Date'] <= '2021-12-31')]

# Convert daily values to monthly mean values for historical data
historical_rainfall_df['Year'] = historical_rainfall_df['Date'].dt.year
historical_rainfall_df['Month'] = historical_rainfall_df['Date'].dt.month
monthly_mean_historical = historical_rainfall_df.groupby(['Year', 'Month'])['Total rainfall (mm)'].mean().reset_index()

# Create a 'Date' column for historical data to enable plotting
monthly_mean_historical['Date'] = pd.to_datetime(monthly_mean_historical[['Year', 'Month']].assign(day=1))

# Initialize a list to store the names of the model columns
model_columns = []

# Create a 3x4 grid of subplots
num_rows = 3
num_cols = 4
fig, axes = plt.subplots(num_rows, num_cols, figsize=(18, 12))
plt.subplots_adjust(wspace=0.4, hspace=0.4)  # Adjust spacing between subplots

# Define a list of distinct contrasting colors
colors = ['violet', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'magenta', 'yellow']

# Initialize a list to store accuracy results
model_accuracies = []

# Iterate through each column in the regional projection data
for i, model_column in enumerate(regional_projection_rainfall_df.columns[1:]):
    # Convert daily values to monthly mean values for the current model
    regional_projection_rainfall_df['Year'] = regional_projection_rainfall_df['Date'].dt.year
    regional_projection_rainfall_df['Month'] = regional_projection_rainfall_df['Date'].dt.month
    monthly_mean_model = regional_projection_rainfall_df.groupby(['Year', 'Month'])[model_column].mean().reset_index()

    # Create a 'Date' column for the current model to enable plotting
    monthly_mean_model['Date'] = pd.to_datetime(monthly_mean_model[['Year', 'Month']].assign(day=1))

    # Determine subplot position
    row_idx = i // num_cols
    col_idx = i % num_cols

    # Plot the monthly mean from historical data and the current model on the subplot
    ax = axes[row_idx, col_idx]

    ax.plot(monthly_mean_historical['Date'], monthly_mean_historical['Total rainfall (mm)'], label='Historical Rainfall', color='blue')
    ax.plot(monthly_mean_model['Date'], monthly_mean_model[model_column], label=f'Model: {model_column}', color=colors[i], alpha=0.7)

    ax.set_xlabel('Year-Month')
    ax.set_ylabel('Monthly Mean Rainfall (mm)')
    ax.set_title(f'Model: {model_column}')
    ax.legend().set_visible(False)  # Hide legend
    ax.grid(True)

    # Append the model column name to the list
    model_columns.append(model_column)

    # Calculate accuracy for the current model
    mae_model = abs(monthly_mean_historical['Total rainfall (mm)'] - monthly_mean_model[model_column]).mean()
    accuracy_model = 1 - mae_model / monthly_mean_historical['Total rainfall (mm)'].mean()
    model_accuracies.append({'Model': model_column, 'Accuracy (%)': accuracy_model * 100})

# Hide empty subplots (if any)
for i in range(len(model_columns), num_rows * num_cols):
    row_idx = i // num_cols
    col_idx = i % num_cols
    fig.delaxes(axes[row_idx, col_idx])

# Sort accuracy data in ascending order by accuracy percentage
model_accuracies.sort(key=lambda x: x['Accuracy (%)'])

# Show all subplots
plt.tight_layout()

# Create a horizontal bar chart for model accuracies with accuracy labels
plt.figure(figsize=(10, 6))
model_names = [x['Model'] for x in model_accuracies]
accuracies = [x['Accuracy (%)'] for x in model_accuracies]
colors = ['violet', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'magenta', 'yellow']
bars = plt.barh(model_names, accuracies, color=colors)
plt.xlabel('Accuracy (%)')
plt.ylabel('Model')
plt.title('Accuracy for Different Regional Models projecting precipitation rates across London')
plt.tight_layout()

# Add accuracy values as labels on the bars
for bar, accuracy in zip(bars, accuracies):
    plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2, f'{accuracy:.2f}%', ha='center', va='center', fontsize=10, color='black')

plt.show()

# Display accuracy results
accuracy_df = pd.DataFrame(model_accuracies)
print("Accuracy Table for Each Model (Ascending Order):")
print(accuracy_df)

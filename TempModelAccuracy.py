import os
import pandas as pd
import matplotlib.pyplot as plt

# Load data and convert 'Date' column to datetime
data_folder = '/users/shaanpatel/desktop/Data 2'
historical_data_path = os.path.join(data_folder, 'Temp19602020.csv')
projection_data_path = os.path.join(data_folder, '12km', 'meantemprcp85regional.csv')

historical_df = pd.read_csv(historical_data_path)
historical_df['Date'] = pd.to_datetime(historical_df['Date'], format='%d/%m/%Y')

projection_df = pd.read_csv(projection_data_path)
projection_df['Date'] = pd.to_datetime(projection_df['Date'], format='%d/%m/%Y')

# Filter data for the period between 1980 and 2021
historical_df = historical_df[(historical_df['Date'] >= '1980-01-01') & (historical_df['Date'] <= '2021-12-31')]
projection_df = projection_df[(projection_df['Date'] >= '1980-01-01') & (projection_df['Date'] <= '2021-12-31')]

# Merge dataframes on 'Date' column
merged_df = pd.merge(historical_df, projection_df, on='Date', how='inner')

# Calculate MAE for each model and convert to accuracy percentage
model_columns = projection_df.columns[1:]
accuracy_data = []

for model_col in model_columns:
    mae = abs(merged_df['Mean Temp'] - merged_df[model_col]).mean()
    accuracy = 1 - mae / merged_df['Mean Temp'].mean()
    accuracy_data.append({'Model': model_col, 'Accuracy (%)': accuracy * 100})

# Sort accuracy data in ascending order by accuracy percentage
accuracy_data.sort(key=lambda x: x['Accuracy (%)'])

# Create an accuracy DataFrame
accuracy_df = pd.DataFrame(accuracy_data)

# Display the accuracy DataFrame
print("Accuracy Table (Ascending Order):")
print(accuracy_df)

# Save the accuracy data to a CSV file
accuracy_csv_path = os.path.join(data_folder, 'accuracy_data.csv')
accuracy_df.to_csv(accuracy_csv_path, index=False)
print(f"Accuracy data saved to {accuracy_csv_path}")

# Create a horizontal bar chart for accuracies with distinct colors and labels
plt.figure(figsize=(12, 6))
colors = ['violet', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'magenta', 'yellow']
bars = plt.barh(accuracy_df['Model'], accuracy_df['Accuracy (%)'], color=colors)
plt.xlabel('Accuracy (%)')
plt.ylabel('Model')
plt.title('Accuracy for Different Regional Models projecting mean temperature across London ')

# Add accuracy values as labels on the bars
for bar in bars:
    width = bar.get_width()
    plt.annotate(f'{width:.2f}%', xy=(width, bar.get_y() + bar.get_height() / 2), xytext=(5, 0),
                 textcoords='offset points', va='center', fontsize=8)

plt.tight_layout()
plt.show()

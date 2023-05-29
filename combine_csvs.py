import pandas as pd
import glob

# Get a list of all CSV files in the directory
csv_files = glob.glob('*.csv')

# Create an empty DataFrame to store the combined data
combined_data = pd.DataFrame()

# Iterate over each CSV file
for file in csv_files:
    # Read the CSV file into a DataFrame
    data = pd.read_csv(file)

    # Append the data to the combined_data DataFrame
    combined_data = combined_data.append(data, ignore_index=True)

# Save the combined data to a new CSV file
combined_data.to_csv('combined_data.csv', index=False)

import os
import pandas as pd

# Directory containing the individual CSV files
source_dir = "data/raw"
# Directory to save the combined CSV file
destination_dir = "data/US"
# Create the destination directory if it doesn't exist
os.makedirs(destination_dir, exist_ok=True)

# List to hold individual dataframes
dataframes = []

# Iterate over all files in the source directory
for filename in os.listdir(source_dir):
    if filename.endswith(".csv") and "united-states" in filename:
        file_path = os.path.join(source_dir, filename)
        df = pd.read_csv(file_path)
        dataframes.append(df)

# Concatenate all dataframes into a single dataframe
combined_df = pd.concat(dataframes, ignore_index=True)

# Save the combined dataframe to a new CSV file
combined_csv_path = os.path.join(destination_dir, "combined_listings.csv")
combined_df.to_csv(combined_csv_path, index=False)

print(f"Combined CSV file saved to {combined_csv_path}")

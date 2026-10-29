# Industrial Compressor Energy Analytics
# Day 3: Introduction to Pandas

import pandas as pd

# Load the dataset
file_path = "DATA/RAW/synthetic_compressor_data_raw.csv"

df = pd.read_csv(file_path)

# Display the first five rows
print("\n--- First Five Rows ---")
print(df.head())

# Display the last five rows
print("\n--- Last Five Rows ---")
print(df.tail())

# Check the number of rows and columns
print("\n--- Dataset Shape ---")
print(df.shape)

# Display column names
print("\n--- Column Names ---")
print(df.columns)

# Display data types and non-null counts
print("\n--- Dataset Information ---")
df.info()

# Generate descriptive statistics
print("\n--- Descriptive Statistics ---")
print(df.describe())

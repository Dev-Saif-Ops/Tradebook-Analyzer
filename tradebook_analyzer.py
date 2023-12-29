#Import Necessary things...

import pandas as pd
import yfinance as yf
from pytz import timezone
from datetime import datetime

# Replace 'your_file.csv' with the actual filename 
csv_file_path = 'put your actual path here'

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv(csv_file_path)

# List of columns to be removed(You can add what you want to remove)
columns_to_remove = ['Column1', 'Column2', 'Column3']  # Replace with actual column names

# Drop the specified columns
df = df.drop(columns=columns_to_remove, errors='ignore')

# Create a new column "Amount" and calculate cumulative sum based on conditions
df['Amount'] = df.apply(lambda row: row['Quantity'] * row['Price'] if row['Trade Type'] == 'buy' else -row['Quantity'] * row['Price'], axis=1).cumsum()

# Use yfinance to fetch additional data based on 'Symbol' column
for symbol in df['Symbol'].unique():
    try:
        # Determine the exchange suffix based on 'Exchange' column
        exchange_suffix = '.BO' if df.loc[df['Symbol'] == symbol, 'Exchange'].iloc[0] == 'BSE' else '.NS'
        
        # Add the determined suffix to the symbol
        symbol_bo = f"{symbol}{exchange_suffix}"

        stock_data = yf.download(symbol_bo, start="2023-03-08", end="2023-12-11", ignore_tz=True)

        # Check if the DataFrame is not empty
        if not stock_data.empty:
            # Convert the timezone to 'Asia/Kolkata'
            stock_data.index = stock_data.index.tz_localize('UTC').tz_convert(timezone('Asia/Kolkata'))

            # Do something with stock_data, e.g., print it
            print(f"Additional data for {symbol}:\n{stock_data}")
        else:
            print(f"No data available for {symbol}")
    except Exception as e:
        print(f"Failed to fetch data for {symbol}: {e}")

# Replace 'output_file.csv' with the desired name for your CSV file
output_csv_path = 'put the location here'  #give your desired location

# Convert the DataFrame to a CSV file
df.to_csv(output_csv_path, index=False)

import yfinance as yf
import pandas as pd

# Prompt the user to input the file path for input.txt
input_file = input("Enter the path to the input.txt file: ")

# Read stock symbols from the provided input file
with open(input_file, 'r') as file:
    stock_symbols = [line.strip() for line in file]

# Prompt the user to input the date range
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")

# Prompt the user to input the desired Excel file name
excel_file_name = input("Enter the desired Excel file name (without extension): ")

# Create an Excel writer to save data to the specified Excel file
excel_writer = pd.ExcelWriter(f'{excel_file_name}.xlsx', engine='openpyxl')

# Iterate through each stock symbol
for symbol in stock_symbols:
    try:
        # Download stock data using yfinance for the specified date range
        stock_data = yf.download(symbol, start=start_date, end=end_date)

        # Print dates and download status
        print(f"Downloaded data for {symbol} from {start_date} to {end_date}")
        
        # Write stock data to the Excel file in a separate sheet
        stock_data.to_excel(excel_writer, sheet_name=symbol)
        
    except Exception as e:
        print(f"Failed to download data for {symbol}: {str(e)}")

# Save and close the Excel file
excel_writer._save()
excel_writer.close()

print(f"Task completed successfully. Data saved to {excel_file_name}.xlsx")


import os
import json
import pandas as pd
from io import StringIO
from datetime import datetime

# Define local folder paths
to_process_path = "raw_data/to_process/"
processed_path = "raw_data/processed/"
transformed_path = "transformed_data/"

def process_file(file_name):
    file_path = os.path.join(to_process_path, file_name)

    # Read the JSON data from the file
    with open(file_path, 'r') as f:
        json_data = json.load(f)
        print(json_data)

    # Transforming data with pandas
    prices = pd.DataFrame(json_data)

    # Add 'price_gram_1k' column
    prices['price_gram_1k'] = prices['price_gram_10k'] / 10

    # Remove unwanted columns (ignore missing columns)
    prices.drop([
        'price_gram_24k',
        'price_gram_22k',
        'price_gram_21k',
        'price_gram_20k',
        'price_gram_18k',
        'price_gram_16k',
        'price_gram_14k',
        'price_gram_10k',
        'ch',
        'chp',
        'ask',
        'bid',
        'timestamp',
        'open_time'], axis=1, inplace=True, errors="ignore")

    # Convert timestamp to SQL-like date format (handle errors)
    prices['date'] = prices['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S'))

    # Convert pandas DataFrame to CSV
    transformed_file_name = f"data_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.csv"
    transformed_file_path = os.path.join(transformed_path, transformed_file_name)
    prices.to_csv(transformed_file_path, index=False)

    print(f"Transformed data saved to: {transformed_file_path}")

    # Move the original file to 'processed' folder
    processed_file_path = os.path.join(processed_path, file_name)
    os.rename(file_path, processed_file_path)

    print(f"File moved to processed: {processed_file_path}")

if __name__ == "__main__":
    # List all files in the 'to_process' folder
    files = os.listdir(to_process_path)

    for file_name in files:
        if file_name.endswith('.json'):
            process_file(file_name)

    print("Transformation Completed!")
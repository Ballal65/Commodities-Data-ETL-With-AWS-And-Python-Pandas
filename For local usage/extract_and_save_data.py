import requests
import os
import json
from datetime import timedelta, datetime
from dotenv import load_dotenv
load_dotenv()
"""
Makes an API request to fetch the price of a commodity (Gold or Silver) for a specific date.

Parameters:
curr (str): The currency in which the price will be quoted (default is 'USD').
symbol (str): The symbol representing the commodity:
    + 'XAU' for Gold
    + 'XAG' for Silver
    + 'XPT' for Platinum
    + 'XPD' for Palladium
date (str): The date for which the data should be fetched (in 'YYYYMMDD' format).

Returns:
dict: A dictionary containing the JSON response from the API.
None: Returns None if there is an error with the API request.
"""

def make_api_request(curr: str = "USD", symbol: str = "XAU", date: str = ""):
    # Get the API key from environment variables
    api_key = os.getenv('API_KEY')
    print(api_key)
    if not api_key:
        print("API_KEY not found in environment variables.")
        return None
    
    # Construct the URL for the API request
    url = f"https://www.goldapi.io/api/{symbol}/{curr}/{date}"
    
    # Set the request headers
    headers = {
        "x-access-token": api_key,
        "Content-Type": "application/json"
    }
    
    # Make the API request and handle possible exceptions
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an error for bad HTTP responses (4xx and 5xx)

        if response.status_code == 200:
            result = response.json()
            print(f"Currency: {curr} \nSymbol: {symbol}\nResponse: {result}")
            return result
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {symbol} on {date}: {str(e)}")
        return None

if __name__ == "__main__":
    commodities = []
    current_date = datetime.now()
    # Extracting data for today and the previous 6 days
    for i in range(7):
        date =  current_date - timedelta(days=i)
        date = date.strftime("%Y%m%d")  # Corrected date format
        print(f"Fetching data for date: {date}")
        
        # Fetch data for Gold (XAU) and Silver (XAG)
        gold = make_api_request(symbol="XAU", date=date)
        silver = make_api_request(symbol="XAG", date=date)

        # Check if data exists and append it to the commodities list
        if gold and 'error' not in gold:
            commodities.append(gold)
        if silver and 'error' not in silver:
            commodities.append(silver)

    # Save the API responses to a JSON file if we have valid results
    if commodities:
        with open(f'raw_data/to_process/commodities_{current_date.strftime("%Y_%m_%d")}.json', 'w') as file:
            json.dump(commodities, file, indent=4)
        print("Commodities data saved to raw_data/to_process/commodities.json")
    else:
        print("No valid data to save.")
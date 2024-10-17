import time
import json
import requests
import os
import boto3
from datetime import datetime, timedelta

s3 = boto3.client('s3')

#The API responses are better with USD
def make_api_request(curr: str = "USD", symbol: str = "XAU", date: str = ""):
    api_key = os.getenv('API_KEY')
    if not api_key:
        print("API_KEY not found in environment variables.")
        return None

    url = f"https://www.goldapi.io/api/{symbol}/{curr}/{date}"
    headers = {
        "x-access-token": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {symbol}: {str(e)}")
        return None
    
    
def lambda_handler(event, context):
    try:
        global s3
        commodities = []
        current_date = datetime.now()
        
        #Fetching today's and previous 6 days data
        for i in range(7):
            date =  current_date - timedelta(days=i)
            date = date.strftime("%Y%m%d")
 
            # Fetch data for Gold (XAU) and Silver (XAG)
            gold = make_api_request(symbol="XAU", date=date)
            silver = make_api_request(symbol="XAG", date=date)
    
            # Check if data exists and append it to the commodities list
            if gold and 'error' not in gold:
                commodities.append(gold)
            if silver and 'error' not in silver:
                commodities.append(silver)

        if commodities:
            json_data = json.dumps(commodities)
    
            bucket_name = 'commodities-data-simple-etl-pipeline'
            file_name = f"raw_data/to_process/data_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.json"
            
            s3.put_object(Body=json_data, Bucket=bucket_name, Key=file_name)
            return { 
                "statusCode" : 200
                , "Message" : f"File {file_name} added to bucket {bucket_name}"}
        else:
            print("No data found.")

    except Exception as e:
        print(f"Error uploading file to S3: {str(e)}")
import json
import boto3
import pandas as pd
from io import StringIO
from datetime import datetime, timezone

# Initialize the boto3 client
s3 = boto3.client("s3")

def lambda_handler(event, context):
    # S3 bucket and folder paths
    Bucket = "commodities-data-simple-etl-pipeline"
    to_process_key = "raw_data/to_process/"
    processed_key = "raw_data/processed/"
    transformed_key = "transformed_data/"
    
    # Iterate over files in the 'to_process' folder
    for file in s3.list_objects(Bucket=Bucket, Prefix=to_process_key)['Contents']:
        file_key = file['Key']
        
        if file_key.split('.')[-1] == 'json':
            # Extract JSON data from the file
            response = s3.get_object(Bucket=Bucket, Key=file_key)
            content = response['Body']
            json_data = json.loads(content.read())
            print(json_data)

            # Transforming data with pandas
            prices = pd.DataFrame(json_data)
            
            # Add 'price_gram_1k' column
            prices['price_gram_1k'] = prices['price_gram_10k'] / 10
            
            # Remove unwanted columns (ignore missing columns)
            prices.drop(['price_gram_24k',
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
            buffer = StringIO()
            prices.to_csv(buffer, index=False)
            content = buffer.getvalue()
            
            # Save the transformed data to the 'transformed' folder
            transformed_file_key = f"{transformed_key}data_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.csv"
            s3.put_object(Bucket=Bucket, Key=transformed_file_key, Body=content)

            # Copy the original file to the 'processed' folder and delete the original from 'to_process'
            s3_resource = boto3.resource("s3")
            copy_source = {
                'Bucket': Bucket,
                'Key': file_key
            }
            processed_file_key = f"{processed_key}data_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.json"  # Keep original filename in 'processed' folder
            s3_resource.meta.client.copy(copy_source, Bucket, processed_file_key)
            s3_resource.Object(Bucket, file_key).delete()
            
            #print(f"File moved to processed and deleted from to_process: {file_key}")
    
    # Return a success response
    return {
        'statusCode': 200,
        'body': 'Transformation Completed!'
    }
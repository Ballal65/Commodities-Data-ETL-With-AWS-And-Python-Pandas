# Commodity Data ETL Pipeline

## Project Overview
This project is an automated **ETL pipeline** (Extract, Transform, Load) designed to extract commodity data (specifically **Gold** and **Silver**) from a free public API, transform the data, and load it into a structured format for analysis using AWS services. The pipeline runs on a weekly schedule, pulling fresh data using AWS Lambda functions, and storing both raw and transformed data in Amazon S3. AWS Glue is used to infer the schema, and Amazon Athena is used to query the data.

## Architecture

The ETL pipeline has three main phases: **Extract**, **Transform**, and **Load**.
![ETL Architecture](https://github.com/Ballal65/Commodities-Data-ETL-With-AWS-And-Python-Pandas/blob/main/Commodities%20ETL%20Flowchart.jpg)

### 1. **Extract Phase**:
   - A **Lambda function** (`commodities_data_extraction`) pulls raw commodity data (Gold and Silver prices) from a free API and stores it in the S3 bucket under the folder `raw_data/to_process`.
   - **CloudWatch** triggers this function to run on a weekly schedule.

### 2. **Transform Phase**:
   - When new data is added to `raw_data/to_process`, an S3 event trigger fires, invoking the second **Lambda function** (`commodities_data_transform_and_load`).
   - This function processes and transforms the raw data into a clean, structured format.
   - The transformed data is stored in `transformed_data/` in S3.

### 3. **Load Phase**:
   - An AWS Glue **Crawler** is set up to infer the schema of the transformed data in S3.
   - The schema is stored in the **AWS Glue Data Catalog**, which makes the data queryable through **Amazon Athena**.
   - The pipeline is now ready for querying and analysis using SQL.

### Folder Description:
- `raw_data/to_process`: New raw data from the API lands here.
- `raw_data/processed`: Once processed, the raw data is moved to this folder.
- `transformed_data/`: Data that has been transformed and is ready for querying.

## Lambda Functions

### 1. `commodities_data_extraction`
   - This Lambda function is responsible for **extracting** raw data from the API.
   - It writes the raw data to the `raw_data/to_process` folder in S3.
   - **Trigger**: Runs on a schedule (weekly) using **CloudWatch Events**.

### 2. `commodities_data_transform_and_load`
   - This Lambda function **transforms** the raw data and loads the clean data into the `transformed_data` folder in S3.
   - **Trigger**: Automatically invoked when new data is added to the `raw_data/to_process` folder (via S3 trigger).

## How the Pipeline Works

1. **CloudWatch** triggers the `commodities_data_extraction` Lambda function every week.
2. This Lambda function fetches commodity data (Gold and Silver) from the API and stores it in the `raw_data/to_process` folder in the S3 bucket.
3. The S3 event trigger detects new data in the `to_process` folder and invokes the `commodities_data_transform_and_load` Lambda function.
4. The second Lambda function transforms the raw data and stores the cleaned version in the `transformed_data` folder in S3.
5. AWS Glue **Crawler** runs periodically to update the schema in the **Glue Data Catalog**.
6. **Amazon Athena** can then be used to run SQL queries on the transformed data for analytics and reporting.

## Try it Yourself:

1. **Get Your Free API Key**: Visit [GoldAPI](https://www.goldapi.io/) and sign up to obtain your API key.

2. **Clone the Repository**: Clone this project to your local machine.

3. **Set Up Your Environment**: Create a `.env` file inside 'For local usage' and add your API key like this:
   ```bash
   API_KEY=your_api_key
   ```
4. Install Dependencies: You'll need the pandas and requests libraries. Install them by running:
   ```bash
   pip install pandas requests dotenv
   ```
   Alternatively, feel free to use a virtual environment if you prefer.
5. Create following folders inside 'For local usage'
   ```
   |- raw_data
   |--- to_process
   |--- processed
   |- transformed_data
   ```
7. Run the Scripts: Execute the scripts from the "For local usage" section to extract and transform data.

## AWS Lambda Suggestions
- You can copy the provided Lambda functions or modify them to suit your use case.
- For the extraction function, you'll need to include the requests library. A pre-packaged requests layer is included in this repository; simply rename the folder to 'python' before deploying.
- For the transformation function, you can leverage AWS's managed pandas layer to handle the data transformation.

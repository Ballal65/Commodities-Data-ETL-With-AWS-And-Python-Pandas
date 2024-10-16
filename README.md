# Commodity Data ETL Pipeline

## Project Overview
This project is an automated **ETL pipeline** (Extract, Transform, Load) designed to extract commodity data (specifically **Gold** and **Silver**) from a free public API, transform the data, and load it into a structured format for analysis using AWS services. The pipeline runs on a weekly schedule, pulling fresh data using AWS Lambda functions, and storing both raw and transformed data in Amazon S3. AWS Glue is used to infer the schema, and Amazon Athena is used for querying the data.

## Architecture

The ETL pipeline has three main phases: **Extract**, **Transform**, and **Load**.

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

## S3 Bucket Structure

The S3 bucket is organized with the following folder structure:
commodities_data_bucket/ 
├── raw_data/ 
│ ├── to_process/ # Raw API data stored here before processing 
│ └── processed/ # Raw data moved here after processing 
├── transformed_data/ # Transformed data after processing

#!/usr/bin/env python3
import boto3
import pandas as pd
import pymysql
from sqlalchemy import create_engine

# Use default AWS credentials
s3 = boto3.client('s3')

# Download data from S3
bucket_name = 'Your_bucket_name_goes_here'
file_key = 'dataset_you_are_working_with.csv'  # Path within the bucket, not a local path
local_file = f'{file_key}'

try:
    print(f"Attempting to download {file_key} from bucket {bucket_name}")
    s3.download_file(bucket_name, file_key, local_file)
    print("Download successful")
    
    # Load data into pandas DataFrame
    df = pd.read_csv(local_file)
    print(f"CSV loaded with {len(df)} rows and {len(df.columns)} columns")
    
    # Connect to local MySQL container
    db_username = 'your_user'
    db_password = 'your_password'
    db_host = 'localhost'
    db_port = '3307'
    db_name = f'{file_key}'
    
    print(f"Connecting to MySQL at {db_host}:{db_port}")
    # Create SQLAlchemy engine
    engine = create_engine(f'mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}')
    
    # Upload data to MySQL
    # Change table name if needed
    table_name = f'{file_key}'
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"Data successfully loaded into {db_name}.{table_name}")
    
except Exception as e:
    print(f"An error occurred: {str(e)}")
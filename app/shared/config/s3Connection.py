import boto3
from botocore.exceptions import NoCredentialsError
import os
#s3 credentials


aws_access_key = os.getenv("aws_access_key")
aws_secret_key = os.getenv("aws_secret_key")
region_name = "us-east-1"

#IDk

def getS3_connection():
     s3 = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=region_name
    )
     
     return s3


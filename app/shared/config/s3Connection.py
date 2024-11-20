import boto3
from fastapi import HTTPException, status
from botocore.exceptions import NoCredentialsError
import os
#s3 credentials


aws_access_key_id = os.getenv("aws_access_key_id")
aws_secret_access_key = os.getenv("aws_secret_access_key")
aws_session_token = os.getenv("aws_session_token")
region_name = "us-east-1"

#IDk


def get_s3_connection():
    
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            region_name="us-east-1"
        )
        return s3
    except NoCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No se encontraron las credenciales de AWS."
        )


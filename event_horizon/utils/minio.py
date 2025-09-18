import os

import boto3


def get_minio_client():
    """
    Creates and returns a Boto3 client for the MinIO service.
    """

    s3_endpoint_url = os.getenv("MINIO_URL", "http://localhost:9000")
    access_key = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    secret_key = os.getenv("MINIO_SECRET_KEY", "minioadmin")

    try:
        s3_client = boto3.client(
            "s3",
            endpoint_url=s3_endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
        print("Successfully created MinIO client.")
        return s3_client
    except Exception as e:
        print(f"Failed to create MinIO client: {e}")
        return None

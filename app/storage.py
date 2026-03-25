import boto3

s3= boto3.client(
    "s3",
    endpoint_url = "http://minio:9000",
    aws_access_key_id="admin",
    aws_secret_access_key="password",
)

BUCKET="files"

def create_bucket():
    buckets=s3.list_buckets()["Buckets"]
    names = [b["Name"] for b in buckets]

    if BUCKET not in names:
        s3.create_bucket(Bucket=BUCKET)
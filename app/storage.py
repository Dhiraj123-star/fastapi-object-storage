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

def upload_file(file,key):
    s3.upload_fileobj(file,BUCKET,key)

def list_files():
    response = s3.list_objects_v2(Bucket=BUCKET)
    return [obj["Key"]for obj in response.get("Contents",[])]

def delete_file(key):
    s3.delete_object(Bucket=BUCKET,Key=key)

def generate_download_url(key):
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket":BUCKET,"Key":key},
        ExpiresIn=3600
    )
from fastapi import FastAPI, UploadFile,File
import boto3

app =FastAPI()

# S3 client(MinIO)
s3 = boto3.client(
    "s3",
    endpoint_url="http://minio:9000",
    aws_access_key_id="admin",
    aws_secret_access_key="password",
)
BUCKET="videos"

@app.on_event("startup")
def startup():
    buckets=s3.list_buckets()["Buckets"]
    names = [b["Name"]for b in buckets]

    if BUCKET not in names:
        s3.create_bucket(Bucket=BUCKET)

# Upload with optional folder support
@app.post("/upload")
async def upload(file: UploadFile=File(...),folder:str=""):

    # If folder provided -- add prefix
    key= f"{folder}/{file.filename}" if folder else file.filename

    s3.upload_fileobj(file.file,BUCKET,key)

    return {"file":key}

# Presigned Upload URL
@app.get("/upload-url")
def get_upload_url(filename:str,folder:str=""):
    key= f"{folder}/{filename}" if folder else filename

    url = s3.generate_presigned_url(
        ClientMethod="put_object",
        Params={"Bucket":BUCKET,"Key":key},
        ExpiresIn=3000,
    )
    return {"upload_url":url,"key":key}

# List files 
@app.get("/files")
def files():
    objects= s3.list_objects_v2(Bucket=BUCKET)
    if "Contents" not in objects:
        return {"files":[]}
    
    return {"files":[obj["Key"]for obj in objects["Contents"]]}

# Download 
@app.get("/download/{filename:path}")
def download(filename: str):
    url= s3.generate_presigned_url(
        "get_object",
        Params= {"Bucket":BUCKET,"Key":filename},
        ExpiresIn=3600,
    )
    return {"url":url}

# Delete 
@app.delete("/delete/{filename:path}")
def delete_file(filename:str):
    s3.delete_object(Bucket=BUCKET,Key=filename)
    return {"message":f"{filename} deleted"}
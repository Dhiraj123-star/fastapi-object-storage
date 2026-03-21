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

@app.post("/upload")
async def upload(file: UploadFile=File(...)):
    s3.upload_fileobj(file.file,BUCKET,file.filename)
    return {"file":file.filename}

@app.get("/files")
def files():
    objects= s3.list_objects_v2(Bucket=BUCKET)
    if "Contents" not in objects:
        return {"files":[]}
    return {"files":[obj["Key"]for obj in objects["Contents"]]}

@app.get("/download/{filename}")
def download(filename: str):
    url= s3.generate_presigned_url(
        "get_object",
        Params= {"Bucket":BUCKET,"Key":filename},
        ExpiresIn=3600,
    )
    return {"url":url}
from fastapi import FastAPI, UploadFile,File,Depends
import uuid
import os

from db import SessionLocal, engine
from models import Base, FileMetadata
from storage import s3, BUCKET,create_bucket

app =FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# DB dependency
def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def startup():
    buckets=s3.list_buckets()["Buckets"]
    names = [b["Name"]for b in buckets]

    if BUCKET not in names:
        s3.create_bucket(Bucket=BUCKET)

# Upload with optional folder support
@app.post("/upload")
async def upload(file: UploadFile=File(...),user:str="default",db=Depends(get_db)):

    # extract extension
    ext = os.path.splitext(file.filename)[1]
    file_id=str(uuid.uuid4())
    # generate uuid filename
    unique_name = f"{file_id}{ext}"

    key = f"{user}/{unique_name}"

    # upload to s3
    s3.upload_fileobj(
        file.file,
        BUCKET,
        key
    )
    # Save metadata in DB
    file_meta = FileMetadata(
        id= file_id,
        user=user,
        original_name = file.filename,
        s3_key = key,
    )

    db.add(file_meta)
    db.commit()

    return {
        "id": file_id,
        "stored_as":key,
        "original_name": file.filename
    }

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

# List files from DB
@app.get("/files")
def list_files(db=Depends(get_db)):
    files = db.query(FileMetadata).all()
    
    return [
        {
            "id":f.id,
            "user":f.user,
            "original_name":f.s3_key,
            "uploaded_at":f.uploaded_at
        }
        for f in files
    ]
    

# Download 
@app.get("/download/{file_id}")
def download(file_id: str,db=Depends(get_db)):

    file = db.query(FileMetadata).filter(FileMetadata.id==file_id).first()

    if not file:
        return {"error":"File not found"}
    url = s3.generate_presigned_url (
        "get_object",
        Params= {"Bucket":BUCKET,"Key":file.s3_key},
        ExpiresIn=3000,
    )
    return {"url":url}

# Delete 
@app.delete("/delete/{file_id}")
def delete_file(file_id:str,db=Depends(get_db)):
    file = db.query(FileMetadata).filter(FileMetadata.id==file_id).first()

    if not file:
        return {"error":"File not found"}

    s3.delete_object(Bucket=BUCKET,Key=file.s3_key)

    db.delete(file)
    db.commit()
    return {"message":"deleted"}
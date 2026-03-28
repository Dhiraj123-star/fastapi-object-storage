from fastapi import FastAPI, UploadFile,File,Depends,HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import uuid
import os

from db import Base,engine,get_db
from models import Base, FileMetadata,User
from storage import upload_file,list_files,delete_file,generate_download_url,create_bucket
from auth import hash_password,verify_password,create_access_token,verify_token

app =FastAPI(
    title= "FastAPI Object Storage API",
    description= "S3-compatible object storage service using MinIO with JWT auth and PostgreSQL metadata management.",
    version="1.0.0"
)

# Create tables
Base.metadata.create_all(bind=engine)
create_bucket()

security=HTTPBearer()

# ---------------- AUTH Headers ---------- # 
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    return payload["sub"]

# -----------  AUTH APIs -------------------- #
@app.post("/register")
def register(username:str,password:str,db:Session=Depends(get_db)):
    user = User(
        id= str(uuid.uuid4()),
        username = username,
        password = hash_password(password)
    )
    db.add(user)
    db.commit()
    return {"message":"User created"}


@app.post("/login")
def login(username:str,password:str,db:Session=Depends(get_db)):
    user = db.query(User).filter(User.username==username).first()

    if not user or not verify_password(password,user.password):
        raise HTTPException(status_code=401,detail="Invalid credentials")

    token = create_access_token({"sub":user.username})
    return {"access_token":token}




# ---------------- FILE APIs ---------------- #

@app.post("/upload")
def upload(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    file_id = str(uuid.uuid4())
    key = f"{current_user}/{file_id}_{file.filename}"

    upload_file(file.file, key)

    metadata = FileMetadata(
        id=file_id,
        user=current_user,
        original_name=file.filename,
        s3_key=key
    )

    db.add(metadata)
    db.commit()

    return {
        "file_id": file_id,
        "stored_as": key
    }


@app.get("/files")
def get_files(current_user: str = Depends(get_current_user)):
    files = list_files()
    user_files = [f for f in files if f.startswith(current_user)]
    return {"files": user_files}


@app.get("/file/{file_id}")
def get_file(file_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    file = db.query(FileMetadata).filter(FileMetadata.id == file_id).first()

    if not file or file.user != current_user:
        raise HTTPException(status_code=404, detail="File not found")

    return {
        "id": file.id,
        "user": file.user,
        "original_name": file.original_name,
        "s3_key": file.s3_key,
        "uploaded_at": file.uploaded_at,
    }


@app.get("/download/{file_id}")
def download(file_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    file = db.query(FileMetadata).filter(FileMetadata.id == file_id).first()

    if not file or file.user != current_user:
        raise HTTPException(status_code=404, detail="File not found")

    url = generate_download_url(file.s3_key)
    return {"download_url": url}


@app.delete("/delete/{file_id}")
def delete(file_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    file = db.query(FileMetadata).filter(FileMetadata.id == file_id).first()

    if not file or file.user != current_user:
        raise HTTPException(status_code=404, detail="File not found")

    delete_file(file.s3_key)
    db.delete(file)
    db.commit()

    return {"message": "File deleted"}

from sqlalchemy import Column,String, DateTime
from datetime import datetime, timezone
from db import Base

class FileMetadata(Base):
    __tablename__ = "files"

    id = Column(String, primary_key=True)
    user= Column(String)
    original_name= Column(String)
    s3_key = Column(String)
    uploaded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class User(Base):
    __tablename__="users"

    id = Column(String,primary_key=True)
    username = Column(String,unique=True)
    password = Column(String)
    
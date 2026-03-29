# 📦 FastAPI + MinIO Object Storage (JWT Secured)

A minimal project to learn **object storage + metadata management** with **secure authentication** using:

* FastAPI (API layer)
* MinIO (S3-compatible storage)
* PostgreSQL (metadata storage)
* boto3 (AWS SDK)
* SQLAlchemy (ORM)
* JWT Authentication (secure APIs)

---

## 🚀 Features

* 🔐 JWT Authentication (login + protected APIs)
* Upload any file (`.txt`, `.json`, `.jpg`, etc.)
* UUID-based file storage (no name conflicts)
* User-based folder structure (prefix)
* Store original filename as metadata (PostgreSQL)
* List uploaded files (auth required)
* Get file metadata by ID (auth required)
* Download files using presigned URL (auth required)
* Delete files (auth required)
* Automatic bucket creation

---

## 📁 Project Structure

```
fastapi-object-storage/
│
├── docker-compose.yml
├── requirements.txt
│
└── app/
    ├── main.py        # API routes + auth integration
    ├── db.py          # DB connection
    ├── models.py      # ORM models
    ├── storage.py     # MinIO (S3) logic
    └── auth.py        # JWT + password hashing
```

---

## ⚙️ Setup & Run

### 1. Start services

```bash
docker compose up --build
```

---

## 🌐 Access URLs

* FastAPI Docs → [http://localhost:8000/docs](http://localhost:8000/docs)
* MinIO Console → [http://localhost:9001](http://localhost:9001)

---

## 🔐 MinIO Login

```
Username: admin
Password: password
```

---

## 🔑 Authentication Flow

### 1. Login

**POST** `/login`

Example:

```
/login?username=dhiraj&password=pass
```

Response:

```json
{
  "access_token": "your_jwt_token"
}
```

---

### 2. Authorize in Swagger

1. Open `/docs`
2. Click **Authorize 🔐**
3. Paste:

```
your_jwt_token
```

Now all protected APIs will work.

---

## 🧪 API Endpoints

---

### 1. Upload File 🔐

**POST** `/upload`

* Requires JWT
* Optional: `user` parameter

Example:

```
/upload?user=dhiraj
```

Stored as:

```
dhiraj/<uuid>.pdf
```

---

### 2. List Files 🔐

**GET** `/files`

---

### 3. Get File Metadata 🔐

**GET** `/file/{file_id}`

---

### 4. Download File 🔐

**GET** `/download/{filename}`

Returns a **presigned URL**

---

### 5. Delete File 🔐

**DELETE** `/delete/{filename}`

---

## 🏗️ Architecture

```
        FastAPI
           │
           ├── JWT Auth Layer
           │
           ├── PostgreSQL (metadata)
           │
           ├── boto3 (S3 SDK)
           ▼
        MinIO (S3-compatible)
           │
           ▼
        Bucket → Objects (UUID keys)
```

---

## 🧠 What You Learn

* JWT Authentication (login + protected APIs)
* S3-compatible APIs
* Buckets & Objects
* Object key (folder simulation)
* UUID-based storage pattern
* Metadata persistence using PostgreSQL
* Upload / download / delete flow
* Presigned URLs
* SDK interaction (boto3)
* Secure API design (Bearer Token)
* Clean architecture (separation of concerns)

---

## 🛠️ Useful Commands

Start:

```bash
docker compose up
```

Stop:

```bash
docker compose down
```

Rebuild:

```bash
docker compose up --build
```

---

## 🎯 Notes

* All APIs (except `/login`) are protected using JWT
* You can upload **any file type**
* No real folders in S3 — only object keys
* File names are replaced with UUIDs
* Metadata is stored in PostgreSQL
* Works like AWS S3 (locally with MinIO)

---

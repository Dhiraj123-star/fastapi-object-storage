# 📦 FastAPI + MinIO Object Storage (Simple Project)

A minimal project to learn **object storage + metadata management** using:

* FastAPI (API layer)
* MinIO (S3-compatible storage)
* PostgreSQL (metadata storage)
* boto3 (AWS SDK)
* SQLAlchemy (ORM)

This setup simulates how **Amazon S3 + DB-backed metadata systems** work in real-world applications.

---

## 🚀 Features

* Upload any file (`.txt`, `.json`, `.jpg`, etc.)
* UUID-based file storage (no name conflicts)
* User-based folder structure (prefix)
* Store original filename as metadata (PostgreSQL)
* List uploaded files
* Get file metadata by ID
* Download files using presigned URL
* Delete files
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
    ├── main.py
    ├── db.py
    ├── models.py
    └── storage.py
```

---

## ⚙️ Setup & Run

### 1. Start services

```bash
docker compose up
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

## 🧪 API Endpoints

### 1. Upload File

**POST** `/upload`

* Optional: `user` parameter (default: `default`)

Example:

```
/upload?user=dhiraj
```

👉 If you upload `resume.pdf`, it will be stored as:

```
dhiraj/550e8400-e29b-41d4-a716-446655440000.pdf
```

Response:

```json
{
  "file_id": "uuid",
  "stored_as": "dhiraj/uuid.pdf",
  "original_name": "resume.pdf"
}
```

---

### 2. List Files

**GET** `/files`

```json
{
  "files": [
    "dhiraj/uuid.pdf"
  ]
}
```

---

### 3. Get File Metadata

**GET** `/file/{file_id}`

Example:

```
/file/uuid
```

Response:

```json
{
  "id": "uuid",
  "user": "dhiraj",
  "original_name": "resume.pdf",
  "s3_key": "dhiraj/uuid.pdf",
  "uploaded_at": "timestamp"
}
```

---

### 4. Download File

**GET** `/download/{filename}`

Example:

```
/download/dhiraj/uuid.pdf
```

Returns a **presigned URL**.

---

### 5. Delete File

**DELETE** `/delete/{filename}`

Example:

```
/delete/dhiraj/uuid.pdf
```

---

## 🏗️ Architecture

```
FastAPI
   │
   ├── PostgreSQL (metadata)
   │
   ├── boto3 (S3 SDK)
   ▼
MinIO (S3-compatible)
   │
   ▼
Bucket → Objects (UUID-based keys)
```

---

## 🧠 What You Learn

* S3-compatible APIs
* Buckets & Objects
* Object key (folder simulation)
* UUID-based storage pattern
* Metadata persistence using PostgreSQL
* Upload / download / delete flow
* Presigned URLs
* SDK interaction (boto3)
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

* You can upload **any file type**
* No real folders in S3 — only object keys (prefix-based)
* File names are replaced with UUIDs to avoid conflicts
* Metadata is stored in PostgreSQL
* Works exactly like AWS S3 (locally)

---

## 🚀 Next Steps

* Authentication (JWT)
* File access control (RBAC)

---

This is a **beginner-friendly foundation** to understand how real-world storage systems like S3 + metadata DB work.

---


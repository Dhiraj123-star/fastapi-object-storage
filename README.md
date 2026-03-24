# 📦 FastAPI + MinIO Object Storage (Simple Project)

A minimal project to learn **object storage basics** using:

* FastAPI (API layer)
* MinIO (S3-compatible storage)
* boto3 (AWS SDK)

This setup simulates how **Amazon S3** works locally.

---

## 🚀 Features

* Upload any file (`.txt`, `.json`, `.jpg`, etc.)
* UUID-based file storage (no name conflicts)
* User-based folder structure (prefix)
* Store original filename as metadata
* List uploaded files
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
    └── main.py
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

### 🔐 MinIO Login

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

### 3. Download File

**GET** `/download/{filename}`

Example:

```
/download/dhiraj/uuid.pdf
```

Returns a **presigned URL**.

---

### 4. Delete File

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
   │ boto3 (S3 SDK)
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
* Metadata handling
* Upload / download / delete flow
* Presigned URLs
* SDK interaction (boto3)

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
* Original filename is stored as metadata
* Works exactly like AWS S3 (locally)


---

This is a **beginner-friendly foundation** to understand how real-world storage systems like S3 work.

---

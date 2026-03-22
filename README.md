# 📦 FastAPI + MinIO Object Storage (Simple Project)

A minimal project to learn **object storage basics** using:

* FastAPI (API layer)
* MinIO (S3-compatible storage)
* boto3 (AWS SDK)

This setup simulates how **Amazon S3** works locally.

---

## 🚀 Features

* Upload any file (`.txt`, `.json`, `.jpg`, etc.)
* Upload with folder support (object key prefix)
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

* Optional: `folder` parameter

Example:

```
folder=user1
```

Stored as:

```
user1/file.txt
```

---

### 2. List Files

**GET** `/files`

```json
{
  "files": ["test.txt", "user1/file.txt"]
}
```

---

### 3. Download File

**GET** `/download/{filename}`

Example:

```
/download/user1/file.txt
```

Returns a **presigned URL**.

---

### 4. Delete File

**DELETE** `/delete/{filename}`

Example:

```
/delete/user1/file.txt
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
Bucket → Objects
```

---

## 🧠 What You Learn

* S3-compatible APIs
* Buckets & Objects
* Object key (folder simulation)
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
* Works exactly like AWS S3 (locally)

---

## 🚀 Next Steps

* Presigned upload URLs
* Multipart upload (large files)
* Authentication (JWT)
* Metadata handling

---

This is a **beginner-friendly foundation** to understand how real-world storage systems like S3 work.

---

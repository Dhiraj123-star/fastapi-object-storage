# 📦 FastAPI + MinIO Object Storage (JWT Secured + CI/CD)

A minimal yet practical project to learn **object storage + metadata management** with **secure authentication and CI/CD** using:

* FastAPI (API layer)
* MinIO (S3-compatible storage)
* PostgreSQL (metadata storage)
* boto3 (AWS SDK)
* SQLAlchemy (ORM)
* JWT Authentication (secure APIs)
* GitHub Actions (CI/CD pipeline)

---

## 🚀 Features

* 🔐 JWT Authentication (login + protected APIs)
* 📦 Upload any file (`.txt`, `.json`, `.jpg`, etc.)
* 🆔 UUID-based file storage (no name conflicts)
* 📁 User-based folder structure (prefix)
* 🗄️ Store original filename as metadata (PostgreSQL)
* 📄 List uploaded files (auth required)
* 🔍 Get file metadata by ID (auth required)
* ⬇️ Download files using presigned URL (auth required)
* ❌ Delete files (auth required)
* ⚙️ Automatic bucket creation
* 🚀 CI/CD with GitHub Actions (Docker build & push)

---

## 📁 Project Structure

```
fastapi-object-storage/
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
└── app/
    ├── main.py        # API routes + auth
    ├── db.py          # DB connection
    ├── models.py      # ORM models
    ├── storage.py     # MinIO logic
    └── auth.py        # JWT + hashing
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
3. Paste token:

```
your_jwt_token
```

---

## 🧪 API Endpoints

### 1. Upload File 🔐

**POST** `/upload`

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

👉 Returns a **presigned URL**

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

* JWT Authentication (secure APIs)
* S3-compatible object storage
* UUID-based file handling
* Metadata persistence (PostgreSQL)
* Presigned URL workflow
* SDK interaction (boto3)
* Clean architecture design
* Docker & containerization
* CI/CD with GitHub Actions

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

## 🔄 CI/CD Pipeline

* Triggered on push to `main`
* Builds Docker image
* Pushes to DockerHub:

```
dhiraj918106/fastapi-object-storage:latest
```

---

## 🎯 Notes

* All APIs (except `/login`) require JWT
* Supports **any file type**
* S3 uses **object keys (no real folders)**
* UUID prevents filename conflicts
* Metadata stored in PostgreSQL
* Works like AWS S3 (via MinIO locally)

---

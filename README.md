# 🔑 API Key Manager

A complete, production-ready API key management system built with **FastAPI + SQLite**.

---

## 📁 Project Structure

```
my-api/
├── .env                        # Your secrets (never commit!)
├── .env.example                # Template to share
├── .gitignore
├── requirements.txt
├── main.py                     # App entry point
│
├── app/
│   ├── core/
│   │   ├── config.py           # Load env variables
│   │   └── security.py         # Key generation & hashing
│   ├── db/
│   │   ├── database.py         # SQLite connection
│   │   └── models.py           # Table creation
│   ├── routes/
│   │   ├── keys.py             # Key CRUD endpoints
│   │   └── protected.py        # Example protected routes
│   └── middleware/
│       └── auth.py             # API key validation
│
├── static/
│   └── index.html              # Admin dashboard UI
└── storage/
    └── api_keys.db             # SQLite DB (auto-created)
```

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy and edit your .env
cp .env.example .env

# 3. Run the server
uvicorn main:app --reload

# 4. Open dashboard
# http://localhost:8000
```

---

## 📡 API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/keys/create` | Admin | Generate a new API key |
| GET | `/keys/list` | Admin | List all keys |
| PATCH | `/keys/revoke/{id}` | Admin | Revoke a key |
| DELETE | `/keys/delete/{id}` | Admin | Delete a key |
| GET | `/api/data` | API Key | Protected example |
| GET | `/api/profile` | API Key | Protected example |
| GET | `/health` | None | Health check |

---

## 🔐 How Auth Works

- Admin routes require `X-Admin-Token` header
- Protected routes require `X-Api-Key` header
- Keys are hashed with SHA-256 before storage
- Raw key is shown **only once** at creation

---

## 🧪 Test with curl

```bash
# Create a key
curl -X POST http://localhost:8000/keys/create \
  -H "x-admin-token: admin-secret-token" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-app"}'

# Use the key
curl http://localhost:8000/api/data \
  -H "x-api-key: sk-YOUR_KEY_HERE"
```

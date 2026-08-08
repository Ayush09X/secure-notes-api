# Secure Notes API

A secure RESTful API for managing personal notes, built with **FastAPI**, **PostgreSQL**, and **Redis**. Features JWT authentication, Redis caching, and Docker deployment.

## Live Demo

**API Base URL:** https://secure-notes-api-lolr.onrender.com  
**Interactive Docs (Swagger UI):** https://secure-notes-api-lolr.onrender.com/docs

## Features

- User registration & login with bcrypt-hashed passwords
- JWT token authentication (24-hour expiry)
- CRUD operations for personal notes
- Redis caching for note lists and individual notes
- Automatic cache invalidation on create/update/delete
- Pydantic input validation
- PostgreSQL for persistent storage
- Docker containerization
- Deployed on Render

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI |
| Database | PostgreSQL |
| Cache | Redis |
| Auth | JWT + bcrypt |
| Validation | Pydantic |
| Container | Docker |
| Deployment | Render |

## API Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/auth/register` | No | Create new account |
| POST | `/auth/login` | No | Login, get JWT token |
| POST | `/notes/` | Yes | Create a note |
| GET | `/notes/` | Yes | List all your notes |
| GET | `/notes/{id}` | Yes | Get a single note |
| PUT | `/notes/{id}` | Yes | Update a note |
| DELETE | `/notes/{id}` | Yes | Delete a note |

## Local Setup

### Prerequisites
- Python 3.11+
- PostgreSQL
- Redis

### 1. Clone & Setup

```bash
git clone https://github.com/Ayush09X/secure-notes-api.git
cd secure-notes-api
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/securenotes
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
```

### 3. Run

```bash
uvicorn main:app --reload
```

API will be at: `http://localhost:8000`  
Docs at: `http://localhost:8000/docs`

## Testing with Swagger UI

1. Go to `/docs`
2. **Register** a user via `POST /auth/register`
3. **Login** via `POST /auth/login` → copy the `access_token`
4. Click **Authorize** (green button) → paste `Bearer YOUR_TOKEN`
5. Test note CRUD operations

## Docker

Build and run locally:

```bash
docker build -t secure-notes-api .
docker run -p 10000:10000 --env-file .env secure-notes-api
```

## Deployment

Deployed on Render using Docker with:
- Render PostgreSQL (managed database)
- Render Key Value (Redis)
- Render Web Service (Docker runtime)

## Project Structure

```
secure-notes-api/
├── main.py              # FastAPI app entry point
├── database.py          # PostgreSQL connection
├── cache.py             # Redis helper functions
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic validation
├── auth_utils.py        # Password hashing & JWT
├── routers/
│   ├── auth.py          # Auth endpoints
│   └── notes.py         # Notes endpoints
├── tests/
│   └── test_api.py      # Basic tests
├── Dockerfile           # Docker config
├── requirements.txt     # Dependencies
└── README.md            # This file
```

## Author

**Ayush Singh**  
[LinkedIn](https://linkedin.com/in/ayush-singh-215526204) | [GitHub](https://github.com/Ayush09X)

# Secure Notes API

A simple RESTful API built with **FastAPI**, **PostgreSQL**, and **Redis**. Features user authentication (JWT), CRUD operations for notes, caching, and rate-limiting-ready structure.

## Features

- User registration & login with bcrypt-hashed passwords
- JWT token authentication
- CRUD operations for personal notes
- Redis caching for note lists and individual notes
- Cache invalidation on create/update/delete
- Input validation with Pydantic
- PostgreSQL for persistent storage

## Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy + PostgreSQL
- Redis
- Pydantic
- Passlib (bcrypt)
- python-jose (JWT)

## Local Setup

### 1. Clone & Enter Directory

```bash
cd secure-notes-api
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
# OR
venv\Scripts\activate    # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start PostgreSQL & Redis

Make sure PostgreSQL and Redis are running locally.

Create a database:
```bash
psql -U postgres -c "CREATE DATABASE securenotes;"
```

### 5. Set Environment Variables

```bash
cp .env.example .env
# Edit .env with your actual DB and Redis URLs
```

### 6. Run the App

```bash
uvicorn main:app --reload
```

API will be at: `http://localhost:8000`

Docs at: `http://localhost:8000/docs`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login, get JWT token |
| POST | `/notes/` | Create a note (auth required) |
| GET | `/notes/` | List all your notes (auth required) |
| GET | `/notes/{id}` | Get a single note (auth required) |
| PUT | `/notes/{id}` | Update a note (auth required) |
| DELETE | `/notes/{id}` | Delete a note (auth required) |

## Testing

```bash
pytest
```

## Deployment on Render (Free)

See `DEPLOY.md` for step-by-step Render deployment instructions.

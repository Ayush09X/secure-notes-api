# Deploy on Render (Free Tier)

## Step 1: Push Code to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/secure-notes-api.git
git push -u origin main
```

## Step 2: Create PostgreSQL on Render

1. Go to [render.com](https://render.com) and sign up/login.
2. Click **"New +"** → **"PostgreSQL"**
3. Name it: `secure-notes-db`
4. Region: Choose closest to you (Singapore for India)
5. Plan: **Free**
6. Click **"Create Database"**
7. Copy the **"Internal Database URL"** — you will need it.

## Step 3: Create Redis on Render

1. Click **"New +"** → **"Redis"**
2. Name it: `secure-notes-redis`
3. Region: Same as PostgreSQL
4. Plan: **Free**
5. Click **"Create Redis"**
6. Copy the **"Internal Redis URL"**.

## Step 4: Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repo: `secure-notes-api`
3. Fill in:
   - **Name:** `secure-notes-api`
   - **Region:** Same as above
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Click **"Advanced"** → **"Add Environment Variable"**
   - `DATABASE_URL` = your PostgreSQL internal URL
   - `REDIS_URL` = your Redis internal URL
   - `SECRET_KEY` = generate a random string (e.g., from randomkeygen.com)
5. Click **"Create Web Service"**

Render will build and deploy. Your API will be live at:
`https://secure-notes-api-XXXX.onrender.com`

## Step 5: Test Your Live API

```bash
curl https://YOUR_RENDER_URL/
```

You should see:
```json
{"message":"Secure Notes API is running"}
```

## Step 6: Test with Swagger UI

Visit:
```
https://YOUR_RENDER_URL/docs
```

Try the `/auth/register` endpoint first, then `/auth/login`, then use the token to test `/notes/` endpoints.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Database connection error | Check DATABASE_URL has correct password |
| Redis connection error | Check REDIS_URL is the internal URL |
| 500 errors | Check Render logs (Dashboard → Logs) |
| Tables not created | Run locally once or add a startup script to create tables |

## Bonus: Auto-Create Tables on Startup

Add this to `main.py` before `app.include_router(...)`:

```python
from database import engine, Base
Base.metadata.create_all(bind=engine)
```

This creates tables automatically when the app starts.

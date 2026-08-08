from fastapi import FastAPI
from routers import auth, notes

app = FastAPI(
    title="Secure Notes API",
    description="A simple secure notes API with auth, caching, and rate limiting.",
    version="1.0.0"
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(notes.router, prefix="/notes", tags=["Notes"])

@app.get("/")
def root():
    return {"message": "Secure Notes API is running"}

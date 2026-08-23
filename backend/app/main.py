from fastapi import FastAPI, HTTPException
from app.core.config import settings
from app.core.supabase import supabase_client

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/health/db")
def db_health_check():
    try:
        # A simple check to verify connection without exposing data or schema details
        response = supabase_client.table("profiles").select("id").limit(1).execute()
        return {"status": "healthy", "db_connection": "successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database connection failed")

from supabase import create_client, Client
from app.core.config import settings

def get_supabase_client() -> Client:
    url: str = settings.SUPABASE_URL
    key: str = settings.SUPABASE_SECRET_KEY
    if not url or not key:
        raise ValueError("Supabase credentials are not set")
    return create_client(url, key)

supabase_client: Client = get_supabase_client()

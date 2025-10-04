from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from mysql.connector import Error as MySQLError
from sqlalchemy.exc import OperationalError
from src.config import SOURCE_SETTINGS
from supabase import create_client, Client
import os

# Global cached engines
_source_engine: Engine | None = None
_supabase_client: Client | None = None


# ----------------------
# SOURCE (MySQL)
# ----------------------
def get_source_engine() -> Engine:
    global _source_engine
    if _source_engine is None:
        _source_engine = create_engine(
            SOURCE_SETTINGS.sqlalchemy_url(),
            pool_size=SOURCE_SETTINGS.pool_size,
            pool_pre_ping=True,
            pool_timeout=SOURCE_SETTINGS.pool_timeout,
            future=True,
            echo=True,
        )
    return _source_engine


@retry(
    reraise=True,
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=0.5, min=0.5, max=8),
    retry=retry_if_exception_type((OperationalError, MySQLError)),
)
def ping_source() -> None:
    """Ping the source MySQL DB to verify connectivity"""
    engine = get_source_engine()
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))


# ----------------------
# WAREHOUSE (Supabase/Postgres)
# ----------------------
def get_supabase_client():
    """
    Create or return a cached Supabase client for the warehouse.
    Requires SUPABASE_URL and SUPABASE_SERVICE_KEY in .env
    """
    global _supabase_client
    if _supabase_client is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_KEY")

        if not url or not key:
            raise ValueError(
                "Missing Supabase credentials. Ensure SUPABASE_URL and SUPABASE_SERVICE_KEY are set in .env"
            )

        _supabase_client = create_client(url, key)
    return _supabase_client


def ping_warehouse() -> None:
    """Ping Supabase by performing a lightweight query."""
    supabase = get_supabase_client()
    try:
        response = supabase.table("ETLControl").select("tableName").limit(1).execute()
        print(response)
        print("✅ Supabase connection successful!")
    except Exception as e:
        raise ConnectionError(f"❌ Supabase connection failed: {e}")

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
from src.config import SOURCE_SETTINGS, WAREHOUSE_SETTINGS

# Global cached engines
_source_engine: Engine | None = None
_warehouse_engine: Engine | None = None


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
def get_warehouse_engine() -> Engine:
    global _warehouse_engine
    if _warehouse_engine is None:
        _warehouse_engine = create_engine(
            WAREHOUSE_SETTINGS.sqlalchemy_url(),
            pool_size=WAREHOUSE_SETTINGS.pool_size,
            pool_pre_ping=True,
            pool_timeout=WAREHOUSE_SETTINGS.pool_timeout,
            future=True,
        )
    return _warehouse_engine


@retry(
    reraise=True,
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=0.5, min=0.5, max=8),
    retry=retry_if_exception_type(OperationalError),
)
def ping_warehouse() -> None:
    """Ping the warehouse (Supabase/Postgres) DB to verify connectivity"""
    engine = get_warehouse_engine()
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

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
from src.config import MYSQL_SETTINGS

_engine: Engine | None = None


def get_source_engine() -> Engine:
    global _engine
    if _engine is None:
        _engine = create_engine(
            MYSQL_SETTINGS.sqlalchemy_url(),
            pool_size=MYSQL_SETTINGS.pool_size,
            pool_pre_ping=True,
            pool_timeout=MYSQL_SETTINGS.pool_timeout,
            future=True,
        )
    return _engine


@retry(
    reraise=True,
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=0.5, min=0.5, max=8),
    retry=retry_if_exception_type((OperationalError, MySQLError)),
)
def ping() -> None:
    engine = get_source_engine()
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

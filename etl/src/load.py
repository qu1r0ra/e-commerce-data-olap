import pandas as pd
from sqlalchemy.engine import Engine
from sqlalchemy import text
from typing import Dict
from .warehouse_models import Base


def create_warehouse_schema(engine: Engine) -> None:
    """Create all warehouse tables if not exist"""
    Base.metadata.create_all(engine)


def get_last_load_time(engine: Engine, table_name: str):
    with engine.connect() as conn:
        result = conn.execute(
            text('SELECT lastLoadTime FROM "ETLControl" WHERE tableName = :t'),
            {"t": table_name},
        ).fetchone()
        return result[0] if result else None


def get_last_load_times(engine: Engine) -> dict:
    return {
        t: get_last_load_time(engine, t)
        for t in ["Users", "Products", "Orders", "OrderItems", "Riders", "Couriers"]
    }


def upsert(
    engine: Engine, table_name: str, df: pd.DataFrame | pd.Series, pk: str = "id"
) -> int:
    """
    Append new rows and update existing ones on conflict.
    NOTE: SQLAlchemy ORM `merge()` can also be used, but here we keep it SQL-level.
    """
    # Stage data in temp table
    temp_name = f"{table_name}_staging"
    df.to_sql(temp_name, engine, if_exists="replace", index=False)

    # Use ON CONFLICT upsert
    cols = ", ".join(df.columns)
    updates = ", ".join([f"{col}=EXCLUDED.{col}" for col in df.columns if col != pk])

    merge_sql = f"""
        INSERT INTO "{table_name}" ({cols})
        SELECT {cols} FROM "{temp_name}"
        ON CONFLICT ({pk}) DO UPDATE SET {updates};
    """

    with engine.begin() as conn:
        conn.execute(text(merge_sql))
        conn.execute(text(f'DROP TABLE "{temp_name}"'))

    return len(df)


def update_last_load_time(engine: Engine, table_name: str, load_time) -> None:
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                INSERT INTO "ETLControl" (tableName, lastLoadTime)
                VALUES (:t, :lt)
                ON CONFLICT (tableName) DO UPDATE
                SET lastLoadTime = EXCLUDED.lastLoadTime
                """
            ),
            {"t": table_name, "lt": load_time},
        )

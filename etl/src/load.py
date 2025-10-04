import numpy as np
import pandas as pd
from datetime import datetime
from src.db import get_supabase_client


def get_last_load_time(table_name: str):
    """Fetch the last load time for a given table from ETLControl."""
    supabase = get_supabase_client()
    try:
        response = (
            supabase.table("ETLControl")
            .select("lastLoadTime")
            .eq("tableName", table_name)
            .execute()
        )
        print(response)
        # data = response.get("lastLoadTime", [])
        # return data[0]["lastLoadTime"] if data else None
    except Exception as e:
        raise RuntimeError(f"Failed to get last load time for {table_name}: {e}")


def get_last_load_times() -> dict:
    """Fetch last load times for all key tables."""
    tables = ["DimUsers", "DimDate", "DimRiders", "DimProducts", "FactSales"]
    return {t: get_last_load_time(t) for t in tables}


def upsert(table_name: str, df: pd.DataFrame, pk: str = "id") -> None:
    """
    Bulk upsert (insert/update) records in Supabase table.
    Handles pandas/numpy datatypes so data is JSON serializable.
    """
    supabase = get_supabase_client()

    # Clean and convert to JSON-safe types
    df = df.copy()
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].astype(str)  # converts to ISO-like string
        elif pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].apply(
                lambda x: (
                    None if pd.isna(x) else x.item() if isinstance(x, np.generic) else x
                )
            )
    df = df.where(pd.notnull(df), None)

    # Convert to list of dicts
    records = df.to_dict(orient="records")

    try:
        response = supabase.table(table_name).upsert(records).execute()

        # if not hasattr(response, "data"):
        #     raise RuntimeError(f"Unexpected response type: {type(response)}")

        print(f"✓ Upserted {len(records)} rows into {table_name}")
        # return len(response) if response else len(records)

    except Exception as e:
        raise RuntimeError(f"Upsert to {table_name} failed: {e}")


def update_last_load_time(table_name: str, load_time: datetime) -> None:
    """Insert or update the last load time for a given table."""
    supabase = get_supabase_client()
    try:
        payload = [{"tableName": table_name, "lastLoadTime": load_time.isoformat()}]
        supabase.table("ETLControl").upsert(payload).execute()
    except Exception as e:
        raise RuntimeError(f"Failed to update ETLControl for {table_name}: {e}")

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


def upsert(table_name: str, df: pd.DataFrame, pk: str = "id") -> int:
    """
    Upsert (insert/update) records in Supabase table.
    NOTE: Supabase’s .upsert() automatically handles conflicts on primary keys.
    """
    supabase = get_supabase_client()
    try:
        data = df.to_dict(orient="records")
        response = supabase.table(table_name).upsert(data).execute()
        return len(response.get("data", [])) if response.get("data") else len(data)
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

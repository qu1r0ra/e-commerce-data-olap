from src.db import get_supabase_client


def fetch_all_rows(table_name: str, batch_size: int = 1000):
    supabase = get_supabase_client()
    offset = 0
    all_data = []

    while True:
        response = (
            supabase.table(table_name)
            .select("*")
            .range(offset, offset + batch_size - 1)
            .execute()
        )
        data = response.data or []
        all_data.extend(data)
        if len(data) < batch_size:
            break
        offset += batch_size

    return all_data

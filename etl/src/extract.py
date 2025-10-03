import pandas as pd
from sqlalchemy import select, text
from typing import Dict
from datetime import datetime
from .db import get_source_engine
from .source_models import User, Product, Order, OrderItem, Rider, Courier


def extract_all_tables(
    last_load_times: Dict[str, str] | None = None,
) -> Dict[str, pd.DataFrame]:
    """Extract source tables into DataFrames, optionally filtered by last load times"""
    engine = get_source_engine()
    last_load_times = last_load_times or {}

    # Consistent table mapping to avoid name mismatches
    table_mapping = {
        "users": (User, "Users"),
        "products": (Product, "Products"),
        "orders": (Order, "Orders"),
        "order_items": (OrderItem, "OrderItems"),
        "riders": (Rider, "Riders"),
        "couriers": (Courier, "Couriers"),
    }

    results = {}
    for key, (model, table_name) in table_mapping.items():
        last_time = last_load_times.get(table_name)
        if last_time:
            print(f"📥 Incremental load for {key} since {last_time}")
        else:
            print(f"📥 Full load for {key}")

        results[key] = extract_table(engine, model, last_time)
        print(f"✓ Extracted {len(results[key])} rows from {key}")

    return results


def extract_table(engine, model_class, last_load_time=None) -> pd.DataFrame:
    """Extract a single table with optional incremental filter"""
    try:
        query = select(model_class)
        if last_load_time:
            # Convert string to datetime if needed
            if isinstance(last_load_time, str):
                try:
                    last_load_time = datetime.fromisoformat(last_load_time)
                except ValueError as e:
                    print(
                        f"⚠️ Invalid timestamp format for {model_class.__tablename__}: {last_load_time}"
                    )
                    print(f"⚠️ Error: {e}. Falling back to full extract.")
                    return pd.read_sql(query, engine)

            query = query.where(model_class.updatedAt > last_load_time)

        df = pd.read_sql(query, engine)
        if df.empty:
            print(f"⚠️ No data found for {model_class.__tablename__}")
        return df

    except Exception as e:
        print(f"❌ Error extracting {model_class.__tablename__}: {e}")
        raise


def extract_joined_data(last_load_time=None) -> pd.DataFrame:
    """Extract order data with related info, optionally incremental"""
    engine = get_source_engine()

    query = """
    SELECT
        o.id AS order_id,
        o.orderNumber,
        o.userId,
        o.deliveryDate,
        o.deliveryRiderId,
        o.createdAt AS order_created,
        o.updatedAt AS order_updated,

        oi.OrderId AS order_item_id,
        oi.ProductId AS product_id,
        oi.quantity,
        oi.notes,
        oi.createdAt AS order_item_created,
        oi.updatedAt AS order_item_updated,

        u.id AS user_id,
        u.username,
        u.firstName,
        u.lastName,
        u.city,
        u.country,
        u.zipCode,
        u.phoneNumber,
        u.dateOfBirth,
        u.gender,
        u.createdAt AS user_created,
        u.updatedAt AS user_updated,

        p.productCode,
        p.category,
        p.description,
        p.name AS product_name,
        p.price,
        p.createdAt AS product_created,
        p.updatedAt AS product_updated,

        r.id AS rider_id,
        r.firstName AS rider_first_name,
        r.lastName AS rider_last_name,
        r.vehicleType,
        r.age,
        r.gender AS rider_gender,
        r.createdAt AS rider_created,
        r.updatedAt AS rider_updated,

        c.name AS courier_name,
        c.createdAt AS courier_created,
        c.updatedAt AS courier_updated

    FROM Orders o
    JOIN OrderItems oi ON o.id = oi.OrderId
    JOIN Users u ON o.userId = u.id
    JOIN Products p ON oi.ProductId = p.id
    LEFT JOIN Riders r ON o.deliveryRiderId = r.id
    LEFT JOIN Couriers c ON r.courierId = c.id
    WHERE 1=1
    """

    params = {}
    if last_load_time:
        # Convert string to datetime if needed
        if isinstance(last_load_time, str):
            try:
                last_load_time = datetime.fromisoformat(last_load_time)
            except ValueError as e:
                print(f"⚠️ Invalid timestamp format for joined data: {last_load_time}")
                print(f"⚠️ Error: {e}. Proceeding with full extract.")
                last_load_time = None

        if last_load_time:
            query += " AND (o.updatedAt > :ts OR oi.updatedAt > :ts)"
            params["ts"] = last_load_time

    query += " ORDER BY o.id, oi.ProductId"

    try:
        df = pd.read_sql(query, engine, params=params)
        if df.empty:
            print("⚠️ No joined order data found")
        else:
            print(f"✓ Extracted {len(df)} joined order records")
        return df
    except Exception as e:
        print(f"❌ Error extracting joined data: {e}")
        raise


def get_table_counts() -> Dict[str, int]:
    """Get row counts for all source tables"""
    engine = get_source_engine()
    tables = ["Users", "Products", "Orders", "OrderItems", "Riders", "Couriers"]
    counts = {}

    try:
        with engine.connect() as conn:
            for table in tables:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar_one()
                counts[table] = count
                print(f"📊 {table}: {count:,} rows")
    except Exception as e:
        print(f"❌ Error getting table counts: {e}")
        raise

    return counts

import pandas as pd
from sqlalchemy import select, text
from typing import Dict
from .db import get_source_engine
from .source_models import User, Product, Order, OrderItem, Rider, Courier


def extract_all_tables(
    last_load_times: Dict[str, str] | None = None,
) -> Dict[str, pd.DataFrame]:
    """Extract source tables into DataFrames, optionally filtered by last load times"""
    engine = get_source_engine()
    last_load_times = last_load_times or {}

    return {
        "users": extract_table(engine, User, last_load_times.get("Users")),
        "products": extract_table(engine, Product, last_load_times.get("Products")),
        "orders": extract_table(engine, Order, last_load_times.get("Orders")),
        "order_items": extract_table(
            engine, OrderItem, last_load_times.get("OrderItems")
        ),
        "riders": extract_table(engine, Rider, last_load_times.get("Riders")),
        "couriers": extract_table(engine, Courier, last_load_times.get("Couriers")),
    }


def extract_table(engine, model_class, last_load_time=None) -> pd.DataFrame:
    """Extract a single table with optional incremental filter"""
    query = select(model_class)
    if last_load_time:
        query = query.where(model_class.updatedAt > last_load_time)
    return pd.read_sql(query, engine)


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

    if last_load_time:
        query += " AND (o.updatedAt > %(ts)s OR oi.updatedAt > %(ts)s)"
        params = {"ts": last_load_time}
    else:
        params = {}

    query += " ORDER BY o.id, oi.ProductId"

    return pd.read_sql(query, engine, params=params)


def get_table_counts() -> Dict[str, int]:
    """Get row counts for all source tables"""
    engine = get_source_engine()
    tables = ["Users", "Products", "Orders", "OrderItems", "Riders", "Couriers"]
    counts = {}

    with engine.connect() as conn:
        for table in tables:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
            counts[table] = result.scalar_one()

    return counts

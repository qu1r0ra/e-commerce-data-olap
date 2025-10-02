import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from typing import Dict
from .db import get_source_engine
from .source_models import User, Product, Order, OrderItem, Rider, Courier


def extract_all_tables() -> Dict[str, pd.DataFrame]:
    """Extract all source tables into DataFrames"""
    engine = get_source_engine()

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        users_df = extract_table(session, User)
        products_df = extract_table(session, Product)
        orders_df = extract_table(session, Order)
        order_items_df = extract_table(session, OrderItem)
        riders_df = extract_table(session, Rider)
        couriers_df = extract_table(session, Courier)

        return {
            "users": users_df,
            "products": products_df,
            "orders": orders_df,
            "order_items": order_items_df,
            "riders": riders_df,
            "couriers": couriers_df,
        }

    finally:
        session.close()


def extract_table(session, model_class) -> pd.DataFrame:
    """Extract a single table into a DataFrame"""
    query = session.query(model_class)
    df = pd.read_sql(query.statement, session.bind)
    return df


def extract_joined_data() -> pd.DataFrame:
    """Extract order data with all related information in one query"""
    engine = get_source_engine()

    query = """
    SELECT
        o.id as order_id,
        o.orderNumber,
        o.userId,
        o.deliveryDate,
        o.deliveryRiderId,
        o.createdAt as order_created,
        o.updatedAt as order_updated,

        oi.OrderId,
        oi.ProductId,
        oi.quantity,
        oi.notes,
        oi.createdAt as order_item_created,
        oi.updatedAt as order_item_updated,

        u.username,
        u.firstName as user_first_name,
        u.lastName as user_last_name,
        u.address1,
        u.address2,
        u.city,
        u.country,
        u.zipCode,
        u.phoneNumber,
        u.dateOfBirth,
        u.gender as user_gender,
        u.createdAt as user_created,
        u.updatedAt as user_updated,

        p.productCode,
        p.category,
        p.description,
        p.name as product_name,
        p.price,
        p.createdAt as product_created,
        p.updatedAt as product_updated,

        r.firstName as rider_first_name,
        r.lastName as rider_last_name,
        r.vehicleType,
        r.age as rider_age,
        r.gender as rider_gender,
        r.createdAt as rider_created,
        r.updatedAt as rider_updated,

        c.name as courier_name,
        c.createdAt as courier_created,
        c.updatedAt as courier_updated,

    FROM Orders o
    JOIN OrderItems oi ON o.id = oi.OrderId
    JOIN Users u ON o.userId = u.id
    JOIN Products p ON oi.ProductId = p.id
    LEFT JOIN Riders r ON o.deliveryRiderId = r.id
    LEFT JOIN Couriers c ON r.courierId = c.id
    ORDER BY o.id, oi.ProductId
    """

    df = pd.read_sql(query, engine)
    return df


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

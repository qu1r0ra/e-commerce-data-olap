import logging
from .db import get_warehouse_engine
from .extract import extract_all_tables, extract_joined_data
from .transform import (
    transform_dim_users,
    transform_dim_products,
    transform_dim_riders,
    transform_fact_sales,
    generate_dim_date,
)
from .load import get_last_load_times, upsert, update_last_load_time
from sqlalchemy import inspect
import pandas as pd


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_etl():
    logger.info("Starting ETL pipeline...")

    warehouse_engine = get_warehouse_engine()

    try:
        # 1. Get last load times for incremental extraction
        last_load_times = get_last_load_times(warehouse_engine)
        logger.info(f"Last load times: {last_load_times}")

        # 2. Extract only new/updated rows from source
        extracted = extract_all_tables(last_load_times)
        facts_df = extract_joined_data(last_load_times.get("Orders"))

        # 3. Transform dimensions
        dim_users_df = transform_dim_users(extracted["users"])
        dim_products_df = transform_dim_products(extracted["products"])
        dim_riders_df = transform_dim_riders(extracted["riders"], extracted["couriers"])

        # 3a. Ensure DimDate exists (only create if it does not)
        inspector = inspect(warehouse_engine)
        if not inspector.has_table("DimDate"):
            dim_date_df = generate_dim_date()
            dim_date_df.to_sql(
                "DimDate",
                warehouse_engine,
                if_exists="replace",
                index=False,
                method="multi",
                chunksize=1000,
            )
        else:
            with warehouse_engine.connect() as conn:
                dim_date_df = pd.read_sql("SELECT * FROM DimDate", conn)

        # 4. Load dimensions
        if not dim_users_df.empty:
            upsert(warehouse_engine, "DimUsers", dim_users_df, pk="sourceId")
        if not dim_products_df.empty:
            upsert(warehouse_engine, "DimProducts", dim_products_df, pk="sourceId")
        if not dim_riders_df.empty:
            upsert(warehouse_engine, "DimRiders", dim_riders_df, pk="sourceId")

        # 5. Transform and load facts
        if not facts_df.empty:
            fact_sales_df = transform_fact_sales(facts_df, dim_date_df=dim_date_df)
            fact_sales_df.to_sql(
                "FactSales",
                warehouse_engine,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=1000,
            )

        # 6. Update ETLControl with new max times
        for table_name, df in extracted.items():
            if not df.empty:
                new_time = df["updatedAt"].max()
                update_last_load_time(warehouse_engine, table_name, new_time)

        logger.info("ETL pipeline completed successfully.")

    finally:
        warehouse_engine.dispose()


if __name__ == "__main__":
    run_etl()

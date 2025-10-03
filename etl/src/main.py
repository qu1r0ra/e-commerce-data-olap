import logging
from datetime import datetime
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
import pandas as pd
from sqlalchemy import inspect


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_etl():
    logger.info("🚀 Starting ETL pipeline...")
    start_time = datetime.now()

    warehouse_engine = get_warehouse_engine()

    try:
        # 1. Get last load times for incremental extraction
        last_load_times = get_last_load_times(warehouse_engine)
        logger.info(f"📅 Last load times: {last_load_times}")

        # 2. Extract only new/updated rows from source
        logger.info("📥 Extracting data from source...")
        extracted = extract_all_tables(last_load_times)
        facts_df = extract_joined_data(last_load_times.get("Orders"))

        # 3. Transform dimensions
        logger.info("🔄 Transforming dimension data...")
        dim_users_df = transform_dim_users(extracted["users"])
        dim_products_df = transform_dim_products(extracted["products"])
        dim_riders_df = transform_dim_riders(extracted["riders"], extracted["couriers"])

        logger.info(
            f"✓ Transformed {len(dim_users_df)} users, {len(dim_products_df)} products, {len(dim_riders_df)} riders"
        )

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
        logger.info("📤 Loading dimension data to warehouse...")
        if not dim_users_df.empty:
            logger.info(f"📤 Upserting {len(dim_users_df)} users to DimUsers")
            upsert(warehouse_engine, "DimUsers", dim_users_df, pk="sourceId")
        if not dim_products_df.empty:
            logger.info(f"📤 Upserting {len(dim_products_df)} products to DimProducts")
            upsert(warehouse_engine, "DimProducts", dim_products_df, pk="sourceId")
        if not dim_riders_df.empty:
            logger.info(f"📤 Upserting {len(dim_riders_df)} riders to DimRiders")
            upsert(warehouse_engine, "DimRiders", dim_riders_df, pk="sourceId")

        # 5. Transform and load facts
        logger.info("📤 Loading fact data to warehouse...")
        if not facts_df.empty:
            fact_sales_df = transform_fact_sales(facts_df, dim_date_df=dim_date_df)
            logger.info(f"📤 Loading {len(fact_sales_df)} sales records to FactSales")
            fact_sales_df.to_sql(
                "FactSales",
                warehouse_engine,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=1000,
            )

        # 6. Update ETLControl with new max times
        logger.info("📝 Updating ETL metadata...")
        for table_name, df in extracted.items():
            if not df.empty:
                new_time = df["updatedAt"].max()
                update_last_load_time(warehouse_engine, table_name, new_time)
                logger.info(f"📝 Updated {table_name} last load time to {new_time}")

        end_time = datetime.now()
        duration = end_time - start_time
        logger.info(
            f"✅ ETL pipeline completed successfully in {duration.total_seconds():.2f} seconds"
        )

    except Exception as e:
        logger.error(f"❌ ETL pipeline failed: {e}")
        raise
    finally:
        warehouse_engine.dispose()


if __name__ == "__main__":
    run_etl()

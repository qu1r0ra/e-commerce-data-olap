import logging
from datetime import datetime
import pandas as pd
from .db import get_source_engine, ping_source, get_supabase_client, ping_warehouse
from .extract import extract_all_tables, extract_joined_data
from .transform import (
    transform_dim_users,
    transform_dim_products,
    transform_dim_riders,
    transform_fact_sales,
    generate_dim_date,
)
from .load import get_last_load_times, upsert, update_last_load_time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EXTRACT_LIMIT = None
UPSERT_BATCH_SIZE = 20000
UPSERT_WAIT_SEC = 1.0


def run_etl():
    logger.info("Starting ETL pipeline...")
    start_time = datetime.now()

    # Test source connection
    get_source_engine()
    ping_source()
    logger.info("Source engine connected!")

    # Test warehouse connection
    supabase_client = get_supabase_client()
    ping_warehouse()
    logger.info("Supabase client connected!")

    # ETL pipeline
    try:
        # 1. Get last load times (for incremental loading)
        last_load_times = get_last_load_times()
        logger.info(f"Last load times: {last_load_times}")

        # 2. Extract data
        extracted = extract_all_tables(last_load_times, limit=EXTRACT_LIMIT)
        facts_df = extract_joined_data(
            last_load_times.get("FactSales"), limit=EXTRACT_LIMIT
        )

        # 3. Transform dimensions
        logger.info("Transforming dimension data...")
        dim_users_df = transform_dim_users(extracted["users"])
        dim_products_df = transform_dim_products(extracted["products"])
        dim_riders_df = transform_dim_riders(extracted["riders"], extracted["couriers"])

        logger.info(
            f"Transformed {len(dim_users_df)} users, {len(dim_products_df)} products, {len(dim_riders_df)} riders"
        )

        # 4. Load to Supabase
        logger.info("Loading dimension data to Supabase...")
        if not dim_users_df.empty:
            print(dim_users_df.head(20))
            print(dim_users_df.dtypes)
            logger.info(f"Upserting {len(dim_users_df)} → DimUsers")
            assert isinstance(dim_users_df, pd.DataFrame)
            upsert(
                "DimUsers",
                dim_users_df,
                conflict="sourceId",
                batch_size=UPSERT_BATCH_SIZE,
                wait_seconds=UPSERT_WAIT_SEC,
            )

        if not dim_products_df.empty:
            print(dim_products_df.head(20))
            print(dim_products_df.dtypes)
            logger.info(f"Upserting {len(dim_products_df)} → DimProducts")
            assert isinstance(dim_products_df, pd.DataFrame)
            upsert(
                "DimProducts",
                dim_products_df,
                conflict="sourceId",
                batch_size=UPSERT_BATCH_SIZE,
                wait_seconds=UPSERT_WAIT_SEC,
            )

        if not dim_riders_df.empty:
            print(dim_riders_df.head(20))
            print(dim_riders_df.dtypes)
            logger.info(f"Upserting {len(dim_riders_df)} → DimRiders")
            assert isinstance(dim_riders_df, pd.DataFrame)
            upsert(
                "DimRiders",
                dim_riders_df,
                conflict="sourceId",
                batch_size=UPSERT_BATCH_SIZE,
                wait_seconds=UPSERT_WAIT_SEC,
            )

        # Create DimDate as needed
        dim_date_df = None
        try:
            existing_dim_date = (
                supabase_client.table("DimDate")
                .select("fullDate", count="exact")
                .limit(1)
                .execute()
            )
            print(
                f"Existing DimDate table: data={existing_dim_date.data}, count={existing_dim_date.count}"
            )

            if not existing_dim_date.data:
                logger.info("No DimDate records found — generating date dimension...")
                dim_date_df = generate_dim_date()
                upsert("DimDate", dim_date_df, conflict="fullDate")
                logger.info(f"Created DimDate with {len(dim_date_df)} records")
            else:
                dim_date_df = existing_dim_date
                logger.info("DimDate already exists — skipping generation.")

        except Exception as e:
            logger.error(f"Failed to check or generate DimDate: {e}")
            raise

        # 5. Transform + load facts
        if not facts_df.empty:
            fact_sales_df = transform_fact_sales(facts_df)
            logger.info(f"Upserting {len(fact_sales_df)} → FactSales")
            upsert("FactSales", fact_sales_df, conflict="id")

        # 6. Update ETLControl
        logger.info("Updating ETL metadata...")
        for table_name in [
            "DimUsers",
            "DimDate",
            "DimRiders",
            "DimProducts",
            "FactSales",
        ]:
            update_last_load_time(table_name, start_time)
            logger.info(f"Updated {table_name} lastLoadTime → {start_time}")

        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"ETL pipeline completed in {duration:.2f} seconds")

    except Exception as e:
        logger.error(f"ETL pipeline failed: {e}")
        raise


if __name__ == "__main__":
    run_etl()

import logging
from datetime import datetime
from .db import get_source_engine, get_supabase_client
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


def run_etl():
    logger.info("🚀 Starting ETL pipeline...")
    start_time = datetime.now()

    source_engine = get_source_engine()
    print("✅ Source engine connected!")

    supabase_client = get_supabase_client()
    print("✅ Supabase client connected!")

    try:
        # 1️⃣ Get last load times
        last_load_times = get_last_load_times()
        logger.info(f"📅 Last load times: {last_load_times}")

        # 2️⃣ Extract
        extracted = extract_all_tables(last_load_times, limit=1000)
        facts_df = extract_joined_data(last_load_times.get("FactSales"), limit=1000)

        # 3️⃣ Transform dimensions
        logger.info("🔄 Transforming dimension data...")
        dim_users_df = transform_dim_users(extracted["users"])
        dim_products_df = transform_dim_products(extracted["products"])
        dim_riders_df = transform_dim_riders(extracted["riders"], extracted["couriers"])

        logger.info(
            f"✓ Transformed {len(dim_users_df)} users, {len(dim_products_df)} products, {len(dim_riders_df)} riders"
        )

        # 4️⃣ Load to Supabase
        logger.info("📤 Loading dimension data to Supabase...")
        if not dim_users_df.empty:
            logger.info(f"📤 Upserting {len(dim_users_df)} → DimUsers")
            upsert("DimUsers", dim_users_df, pk="sourceId")

        if not dim_products_df.empty:
            logger.info(f"📤 Upserting {len(dim_products_df)} → DimProducts")
            upsert("DimProducts", dim_products_df, pk="sourceId")

        if not dim_riders_df.empty:
            logger.info(f"📤 Upserting {len(dim_riders_df)} → DimRiders")
            upsert("DimRiders", dim_riders_df, pk="sourceId")

        # 5️⃣ Transform + load facts
        if not facts_df.empty:
            fact_sales_df = transform_fact_sales(facts_df)
            logger.info(f"📤 Upserting {len(fact_sales_df)} → FactSales")
            upsert("FactSales", fact_sales_df, pk="id")

        # 6️⃣ Update ETLControl
        logger.info("📝 Updating ETL metadata...")
        for table_name, df in extracted.items():
            if not df.empty:
                new_time = df["updatedAt"].max()
                update_last_load_time(table_name, new_time)
                logger.info(f"🕒 Updated {table_name} lastLoadTime → {new_time}")

        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"✅ ETL pipeline completed in {duration:.2f} seconds")

    except Exception as e:
        logger.error(f"❌ ETL pipeline failed: {e}")
        raise


if __name__ == "__main__":
    run_etl()

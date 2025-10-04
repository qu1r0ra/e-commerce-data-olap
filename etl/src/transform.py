import pandas as pd
from datetime import date
from .warehouse_models import SourceSystem


def transform_dim_users(users_df: pd.DataFrame) -> pd.DataFrame | pd.Series:
    """Transform Users table into DimUsers"""
    new_df = users_df.copy()

    new_df["firstName"] = new_df["firstName"].fillna("")
    new_df["lastName"] = new_df["lastName"].fillna("")
    new_df["city"] = new_df["city"].fillna("")
    new_df["country"] = new_df["country"].fillna("")
    new_df["dateOfBirth"] = pd.to_datetime(new_df["dateOfBirth"], errors="coerce")
    new_df["gender"] = (
        new_df["gender"]
        .str.strip()
        .str.lower()
        .map({"m": "male", "f": "female"})
        .str.title()
        .fillna("")
    )
    new_df["createdAt"] = pd.to_datetime(new_df["createdAt"], errors="coerce")
    new_df["updatedAt"] = pd.to_datetime(new_df["updatedAt"], errors="coerce")
    new_df["sourceId"] = new_df["id"]
    new_df["sourceSystem"] = SourceSystem.MYSQL.value

    return new_df[
        [
            "firstName",
            "lastName",
            "city",
            "country",
            "dateOfBirth",
            "gender",
            "createdAt",
            "updatedAt",
            "sourceId",
            "sourceSystem",
        ]
    ]


def transform_dim_products(products_df: pd.DataFrame) -> pd.DataFrame | pd.Series:
    """Transform Products table into DimProducts"""
    new_df = products_df.copy()

    new_df["productCode"] = new_df["productCode"].fillna("")
    new_df["category"] = (
        new_df["category"]
        .str.strip()
        .str.lower()
        .map({"toy": "toys", "bag": "bags", "make up": "makeup"})
        .str.title()
        .fillna("")
    )
    new_df["description"] = new_df["description"].fillna("")
    new_df["name"] = new_df["name"].fillna("")
    new_df["price"] = new_df["price"].fillna(0.0)
    new_df["createdAt"] = pd.to_datetime(new_df["createdAt"], errors="coerce")
    new_df["updatedAt"] = pd.to_datetime(new_df["updatedAt"], errors="coerce")
    new_df["sourceId"] = new_df["id"]
    new_df["sourceSystem"] = SourceSystem.MYSQL.value

    return new_df[
        [
            "productCode",
            "category",
            "description",
            "name",
            "price",
            "createdAt",
            "updatedAt",
            "sourceId",
            "sourceSystem",
        ]
    ]


def transform_dim_riders(
    riders_df: pd.DataFrame, couriers_df: pd.DataFrame
) -> pd.DataFrame | pd.Series:
    """Transform joined riders and couriers data into DimRiders"""
    new_df = riders_df.copy()

    # Rename columns to avoid id collisions
    new_df = new_df.rename(columns={"id": "riderId"})
    couriers_df = couriers_df.rename(
        columns={"id": "courierIdRef", "name": "courierName"}
    )

    new_df = new_df.merge(
        couriers_df[["courierIdRef", "courierName"]],
        how="left",
        left_on="courierId",
        right_on="courierIdRef",
    )

    new_df["firstName"] = new_df["firstName"].fillna("")
    new_df["lastName"] = new_df["lastName"].fillna("")
    new_df["vehicleType"] = (
        new_df["vehicleType"]
        .str.strip()
        .str.lower()
        .map({"motorbike": "motorcycle"})
        .str.title()
        .fillna("")
    )
    new_df["courierName"] = new_df["courierName"].fillna("")
    new_df["age"] = new_df["age"].fillna(0)
    new_df["gender"] = new_df["gender"].fillna("")
    new_df["createdAt"] = pd.to_datetime(new_df["createdAt"], errors="coerce")
    new_df["updatedAt"] = pd.to_datetime(new_df["updatedAt"], errors="coerce")
    new_df["sourceId"] = new_df["riderId"]
    new_df["sourceSystem"] = SourceSystem.MYSQL.value

    return new_df[
        [
            "firstName",
            "lastName",
            "vehicleType",
            "courierName",
            "age",
            "gender",
            "createdAt",
            "updatedAt",
            "sourceId",
            "sourceSystem",
        ]
    ]


def generate_dim_date(
    start_date: date = date(2020, 1, 1), end_date: date = date(2029, 12, 31)
) -> pd.DataFrame | pd.Series:
    """Create a date dimension table for DimDate"""
    dates = pd.date_range(start=start_date, end=end_date)

    df = pd.DataFrame({"fullDate": dates})
    df["year"] = df["fullDate"].dt.year
    df["month"] = df["fullDate"].dt.month
    df["day"] = df["fullDate"].dt.day
    df["monthName"] = df["fullDate"].dt.month_name()
    df["dayOfTheWeek"] = df["fullDate"].dt.day_name()
    df["quarter"] = df["fullDate"].dt.quarter

    return df


def transform_fact_sales(
    joined_df: pd.DataFrame, dim_date_df: pd.DataFrame
) -> pd.DataFrame | pd.Series:
    """
    Transform raw order/order_item data into FactSales table.

    Assumes dimension data have already been loaded.
    Maps deliveryDate to DimDate and assigns keys.
    """

    new_df = joined_df.copy()

    new_df["userId"] = new_df["userId"].fillna(0).astype(int)

    # Map deliveryDate to DimDate
    dim_date_df["fullDate"] = pd.to_datetime(dim_date_df["fullDate"], errors="coerce")
    new_df["deliveryDate"] = pd.to_datetime(new_df["deliveryDate"], errors="coerce")
    new_df = new_df.merge(
        dim_date_df[["fullDate", "dateId"]],
        how="left",
        left_on="deliveryDate",
        right_on="fullDate",
    )
    new_df.rename(columns={"dateId": "deliveryDateId"}, inplace=True)

    new_df["deliveryDateId"] = new_df["deliveryDateId"].fillna(0).astype(int)
    new_df["deliveryRiderId"] = new_df["deliveryRiderId"].fillna(0).astype(int)
    new_df["productId"] = new_df["productId"].fillna(0).astype(int)
    new_df["quantitySold"] = new_df["quantity"].fillna(0).astype(int)
    new_df["createdAt"] = pd.to_datetime(new_df["order_created"], errors="coerce")
    new_df["sourceId"] = new_df["orderId"]
    new_df["sourceSystem"] = SourceSystem.MYSQL.value

    return new_df[
        [
            "userId",
            "deliveryDateId",
            "deliveryRiderId",
            "productId",
            "quantitySold",
            "createdAt",
            "sourceId",
            "sourceSystem",
        ]
    ]

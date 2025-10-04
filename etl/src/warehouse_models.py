# from sqlalchemy import Column, Integer, String, Float, DateTime, Date, BigInteger, Enum
# from sqlalchemy.ext.declarative import declarative_base
import enum

# Base = declarative_base()


class SourceSystem(enum.Enum):
    MYSQL = "MySQL"


class RiderVehicleType(enum.Enum):
    MOTORCYCLE = "Motorcycle"
    BIKE = "Bike"
    TRIKE = "Trike"
    CAR = "Car"


# class DimUsers(Base):
#     __tablename__ = "DimUsers"

#     id = Column(BigInteger, primary_key=True, autoincrement=True)
#     firstName = Column(String(255), nullable=False)
#     lastName = Column(String(255), nullable=False)
#     city = Column(String(255), nullable=False)
#     country = Column(String(255), nullable=False)
#     dateOfBirth = Column(Date, nullable=False)
#     gender = Column(String(255), nullable=False)
#     createdAt = Column(DateTime, nullable=False)
#     updatedAt = Column(DateTime, nullable=False)
#     sourceId = Column(BigInteger, nullable=False)
#     sourceSystem = Column(Enum(SourceSystem), nullable=False)


# class DimDate(Base):
#     __tablename__ = "DimDate"

#     id = Column(BigInteger, primary_key=True, autoincrement=True)
#     fullDate = Column(Date, nullable=False, unique=True)
#     year = Column(Integer, nullable=False)
#     month = Column(Integer, nullable=False)
#     day = Column(Integer, nullable=False)
#     monthName = Column(String(255), nullable=False)
#     dayOfTheWeek = Column(String(255), nullable=False)
#     quarter = Column(String(255), nullable=False)


# class DimRiders(Base):
#     __tablename__ = "DimRiders"

#     id = Column(BigInteger, primary_key=True, autoincrement=True)
#     firstName = Column(String(255), nullable=False)
#     lastName = Column(String(255), nullable=False)
#     vehicleType = Column(String(255), nullable=False)
#     courierName = Column(String(255), nullable=False)
#     age = Column(Integer, nullable=False)
#     gender = Column(String(255), nullable=False)
#     createdAt = Column(DateTime, nullable=False)
#     updatedAt = Column(DateTime, nullable=False)
#     sourceId = Column(BigInteger, nullable=False)
#     sourceSystem = Column(Enum(SourceSystem), nullable=False)


# class DimProducts(Base):
#     __tablename__ = "DimProducts"

#     id = Column(BigInteger, primary_key=True, autoincrement=True)
#     productCode = Column(String(255), nullable=False)
#     category = Column(String(255), nullable=False)
#     description = Column(String(255))
#     name = Column(String(255), nullable=False)
#     price = Column(Float, nullable=False)
#     createdAt = Column(DateTime, nullable=False)
#     updatedAt = Column(DateTime, nullable=False)
#     sourceId = Column(BigInteger, nullable=False)
#     sourceSystem = Column(Enum(SourceSystem), nullable=False)


# class FactSales(Base):
#     __tablename__ = "FactSales"

#     id = Column(BigInteger, primary_key=True, autoincrement=True)
#     userId = Column(BigInteger, nullable=False)
#     deliveryDateId = Column(BigInteger, nullable=False)
#     deliveryRiderId = Column(BigInteger, nullable=False)
#     productId = Column(BigInteger, nullable=False)
#     quantitySold = Column(BigInteger, nullable=False)
#     createdAt = Column(DateTime, nullable=False)
#     sourceId = Column(BigInteger, nullable=False)
#     sourceSystem = Column(Enum(SourceSystem), nullable=False)


# class ETLControl(Base):
#     __tablename__ = "ETLControl"

#     tableName = Column(String(255), primary_key=True)
#     lastLoadTime = Column(DateTime, nullable=False)

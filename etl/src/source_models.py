from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255))
    firstName = Column(String(255))
    lastName = Column(String(255))
    address1 = Column(String(255))
    address2 = Column(String(255))
    city = Column(String(255))
    country = Column(String(255))
    zipCode = Column(String(255))
    phoneNumber = Column(String(255))
    dateOfBirth = Column(String(255))
    gender = Column(String(255))
    createdAt = Column(DateTime, nullable=False)
    updatedAt = Column(DateTime, nullable=False)


class Product(Base):
    __tablename__ = "Products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    productCode = Column(String(255))
    category = Column(String(255))
    description = Column(String(255))
    name = Column(String(255))
    price = Column(Float)
    createdAt = Column(DateTime, nullable=False)
    updatedAt = Column(DateTime, nullable=False)


class Courier(Base):
    __tablename__ = "Couriers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    createdAt = Column(DateTime, nullable=False)
    updatedAt = Column(DateTime, nullable=False)


class Rider(Base):
    __tablename__ = "Riders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstName = Column(String(255))
    lastName = Column(String(255))
    vehicleType = Column(String(255))
    courierId = Column(Integer, ForeignKey("Couriers.id"))
    age = Column(Integer)
    gender = Column(String(255))
    createdAt = Column(DateTime, nullable=False)
    updatedAt = Column(DateTime, nullable=False)


class Order(Base):
    __tablename__ = "Orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    orderNumber = Column(String(255))
    userId = Column(Integer, ForeignKey("Users.id"))
    deliveryDate = Column(String(255))
    deliveryRiderId = Column(Integer, ForeignKey("Riders.id"))
    createdAt = Column(DateTime, nullable=False)
    updatedAt = Column(DateTime, nullable=False)


class OrderItem(Base):
    __tablename__ = "OrderItems"

    OrderId = Column(Integer, ForeignKey("Orders.id"), primary_key=True)
    ProductId = Column(Integer, ForeignKey("Products.id"), primary_key=True)
    quantity = Column(Integer)
    notes = Column(String(255))
    createdAt = Column(DateTime, nullable=False)
    updatedAt = Column(DateTime, nullable=False)

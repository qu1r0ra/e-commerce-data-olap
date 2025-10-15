# e-commerce-data-olap <!-- omit from toc -->

<!-- ![title](./readme/title.jpg) -->

<!-- Refer to https://shields.io/badges for usage -->

![Year, Term, Course](https://img.shields.io/badge/AY2526--T1-STADVDB-blue)

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff) ![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=fff) ![MySQL](https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=fff) ![Supabase](https://img.shields.io/badge/Supabase-3FCF8E?logo=supabase&logoColor=fff)

An OLAP application that queries from generated e-commerce data stored in a Data Warehouse through ETL. Created for STADVDB (Advanced Database Systems).

## Table of Contents <!-- omit from toc -->

- [1. Overview](#1-overview)
- [2. Getting Started](#2-getting-started)
  - [2.1. Prerequisites](#21-prerequisites)
  - [2.2. Building](#22-building)
  - [2.3. Running](#23-running)
- [3. Data Warehouse Schema Dimensions](#3-data-warehouse-schema-dimensions)
  - [3.1. DimDate](#31-dimdate)
  - [3.2. DimProducts](#32-dimproducts)
  - [3.3. DimRiders](#33-dimriders)
  - [3.4. DimUsers](#34-dimusers)
  - [3.5. FactSales](#35-factsales)
  - [3.6. ETLControl](#36-etlcontrol)

## 1. Overview

> [fill up]

## 2. Getting Started

### 2.1. Prerequisites

> [fill up]

### 2.2. Building

> [fill up]

### 2.3. Running

> [fill up]

## 3. Data Warehouse Schema Dimensions

These are the dimensions and fact tables for our OLAP application.

### 3.1. DimDate

This dimension table contains attributes related to specific dates.

- `id`: `int8`
- `fullDate`: `date`
- `year`: `int2`
- `month`: `int2`
- `day`: `int2`
- `monthName`: `varchar`
- `dayOfTheWeek`: `varchar`
- `quarter`: `varchar`

### 3.2. DimProducts

This dimension stores information about each product.

- `id`: `int8`
- `productCode`: `varchar`
- `category`: `varchar`
- `description`: `varchar`
- `name`: `varchar`
- `price`: `float8`
- `createdAt`: `timestamp`
- `updatedAt`: `timestamp`
- `sourceId`: `int8`
- `sourceSystem`: `source_system`

### 3.3. DimRiders

This dimension holds details about the delivery riders.

- `id`: `int8`
- `firstName`: `varchar`
- `lastName`: `varchar`
- `vehicleType`: `rider_vehicle_type`
- `courierName`: `varchar`
- `age`: `int2`
- `gender`: `varchar`
- `createdAt`: `timestamp`
- `updatedAt`: `timestamp`
- `sourceId`: `int8`
- `sourceSystem`: `source_system`

### 3.4. DimUsers

This dimension contains information about registered users.

- `id`: `int8`
- `firstName`: `varchar`
- `lastName`: `varchar`
- `city`: `varchar`
- `country`: `varchar`
- `dateOfBirth`: `date`
- `gender`: `varchar`
- `createdAt`: `timestamp`
- `updatedAt`: `timestamp`
- `sourceId`: `int8`
- `sourceSystem`: `source_system`

### 3.5. FactSales

This is the central fact table that records sales transactions.

- `id`: `int8`
- `userId`: `int8`
- `deliveryDateId`: `int8`
- `deliverRiderId`: `int8`
- `productId`: `int8`
- `quantitySold`: `int8`
- `createdAt`: `timestamp`
- `sourceId`: `int8`
- `source_system`: `source_system`

### 3.6. ETLControl

This table is used for metadata to track the ETL (Extract, Transform, Load) process.

- `tableName`: `text`
- `lastLoadTime`: `timestamp`

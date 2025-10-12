# e-commerce-data-olap <!-- omit from toc -->

![title](./readme/title.jpg)

<!-- Refer to https://shields.io/badges for usage -->

![Year, Term, Course](https://img.shields.io/badge/AY2526--T1-STADVDB-blue) ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)

A reusable GitHub repository template for programming projects.

Includes a standardized folder structure, README layout, and common configurations to speed up project setup and maintain consistency.

## Table of Contents <!-- omit from toc -->

- [1. Overview](#1-overview)
  - [1.1. Topic 1](#11-topic-1)
  - [1.2. Topic 2](#12-topic-2)
- [2. Getting Started](#2-getting-started)
  - [2.1. Prerequisites](#21-prerequisites)
  - [2.2. Installation](#22-installation)
  - [2.3. Running the Project](#23-running-the-project)
- [3. Usage](#3-usage)
  - [3.1. Use Case 1](#31-use-case-1)
  - [3.2. Use Case 2](#32-use-case-2)
- [4. References](#4-references)
  - [4.1. API](#41-api)
  - [4.2. Q\&A](#42-qa)

## 1. Overview

### 1.1. Topic 1

> [fill up]

### 1.2. Topic 2

> [fill up]

## 2. Getting Started

### 2.1. Prerequisites

> [fill up]

### 2.2. Installation

> [fill up]

### 2.3. Running the Project

> [fill up]

## 3. Usage

### 3.1. Use Case 1

> [fill up]

### 3.2. Use Case 2

> [fill up]

## 4. References

### 4.1. API

> [fill up]

### 4.2. Q&A

> [fill up]


# Data Warehouse Schema Dimensions

These are the dimensions and fact tables for our OLAP application.

### `DimDate`
This dimension table contains attributes related to specific dates.
- `id`: `int8`
- `fullDate`: `date`
- `year`: `int2`
- `month`: `int2`
- `day`: `int2`
- `monthName`: `varchar`
- `dayOfTheWeek`: `varchar`
- `quarter`: `varchar`

***

### `DimProducts`
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

***

### `DimRiders`
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

***

### `DimUsers`
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

***

### `FactSales`
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

***

### `ETLControl`
This table is used for metadata to track the ETL (Extract, Transform, Load) process.
- `tableName`: `text`
- `lastLoadTime`: `timestamp`


<!-- ### 4.3. Disclaimer

> [!WARNING]
>
> ![ChatGPT](https://img.shields.io/badge/ChatGPT-74aa9c?logo=openai&logoColor=white) ![Claude](https://img.shields.io/badge/Claude-D97757?logo=claude&logoColor=white)
>
> Parts of this project were generated or assisted by AI tools, including OpenAI's [ChatGPT](https://chatgpt.com/) and Anthropic's [Claude](https://www.anthropic.com/claude). While care has been taken to review and verify the generated outputs, it may still contain errors. Please review the code critically and contribute improvements where necessary. -->

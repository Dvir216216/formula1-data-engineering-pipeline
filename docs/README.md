# 📚 Project Documentation & Architecture

This folder contains the architectural blueprints and documentation for the Formula 1 Data Engineering pipeline.

## 🗺️ Entity Relationship Diagram (ERD)

The database schema follows a **normalized relational model** designed to optimize data integrity and analytical query performance.

![Formula 1 Schema ERD](f1_schema_erd.png)
*(Note: Please ensure the image file is named `f1_schema_erd.png` and located in this folder)*

### 🏗️ Schema Architecture Breakdown

The schema is organized into three logical layers:

#### 1. Core Dimensions (Reference Data)
Tables that describe the "Who", "Where", and "When".
* **`circuits`**: Static data about race tracks (Location, Country).
* **`drivers`**: Driver profiles (Name, Nationality, DOB).
* **`constructors`**: Team information.
* **`seasons`**: Historical timeline metadata.

#### 2. Event Log (Fact Tables)
Tables that record the actual race events.
* **`races`**: The central event table connecting a circuit to a specific season/round.
* **`status`**: Lookup table for race outcomes (Finished, Accident, Engine Failure).

#### 3. Performance Metrics (Detailed Facts)
High-granularity tables containing the telemetry and results.
* **`results`**: The primary fact table linking Drivers, Constructors, and Races.
* **`lap_times`** & **`pit_stops`**: Detailed event logs with **Composite Primary Keys** for granular analysis.
* **`qualifying`**: Pre-race performance data.

## 🔑 Key Design Decisions

* **Data Integrity**: Strict `FOREIGN KEY` constraints are enforced to prevent orphan records (e.g., a result cannot exist without a valid driver).
* **Composite Keys**: Used in `lap_times` (RaceID + DriverID + Lap) to ensure uniqueness at the lap level.
* **Data Types**: 
    * `NUMERIC` used for points to handle half-points (e.g., 1984 Monaco GP).
    * `VARCHAR` used for time intervals where formats vary (e.g., "+1 Lap" vs "1:24.00").
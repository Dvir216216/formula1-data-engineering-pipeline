# 🗄️ Database Architecture & Schema

This directory contains the SQL scripts required to define the Formula 1 PostgreSQL database structure.

## 📂 File Structure

* **`00_init_database_schema.sql`**: The master DDL (Data Definition Language) script.
    * **Clean Slate**: Begins with `DROP TABLE IF EXISTS ... CASCADE` to ensure a completely fresh environment on every run[cite: 19].
    * [cite_start]**Strict Typing**: Defines precise data types (e.g., `NUMERIC` for points, `VARCHAR` for text)[cite: 21].
    * [cite_start]**Integrity**: Establishes Primary Keys and Foreign Keys to enforce relationships between drivers, races, and results[cite: 20, 21].

* **`f1_complete_install.sql`**: A "Northwind-style" distribution file [cite: 44-47].
    * Contains both the **Structure** and the **Data** (INSERT statements).
    * Use this for a quick "One-Click Install" without needing to run the Python ETL pipeline.

## 🛠️ How to Execute (The Engineer's Way)

To build the schema from scratch before running the ETL pipeline:

1. Open your SQL Client (pgAdmin / DBeaver / psql).
2. Connect to your database.
3. Run the initialization script:
   ```sql
   \i 00_init_database_schema.sql
import pandas as pd
from sqlalchemy import create_engine, text
import os

# ==========================================
# 1. CONFIGURATION
# ==========================================

# ⚠️ IMPORTANT: Change the password below to your actual PostgreSQL password!
# Format: postgresql://username:password@localhost:5432/database_name
DB_CONNECTION_STR = 'postgresql://postgres:password@localhost:5432/formula1'

# Path to the data folder (Updated to point to 'raw' inside 'data')
DATA_FOLDER = './data'

# List of files to load in specific order (Hierarchy Matters for Foreign Keys!)
FILES_TO_LOAD = [
    # Level 1: Lookup Tables (Independent tables)
    {'file': 'circuits.csv', 'table': 'circuits'},
    {'file': 'seasons.csv', 'table': 'seasons'},
    {'file': 'status.csv', 'table': 'status'},
    {'file': 'drivers.csv', 'table': 'drivers'},
    {'file': 'constructors.csv', 'table': 'constructors'},

    # Level 2: Core Tables (Depend on Level 1)
    {'file': 'races.csv', 'table': 'races'},

    # Level 3: Results & Linking Tables (Depend on Level 2)
    {'file': 'constructor_results.csv', 'table': 'constructor_results'},
    {'file': 'constructor_standings.csv', 'table': 'constructor_standings'},
    {'file': 'driver_standings.csv', 'table': 'driver_standings'},
    {'file': 'qualifying.csv', 'table': 'qualifying'},
    {'file': 'results.csv', 'table': 'results'},
    {'file': 'sprint_results.csv', 'table': 'sprint_results'},
    {'file': 'pit_stops.csv', 'table': 'pit_stops'},
    {'file': 'lap_times.csv', 'table': 'lap_times'}
]

def load_data():
    print("🚀 Starting ETL Pipeline...")

    # Create database engine
    try:
        engine = create_engine(DB_CONNECTION_STR)
        conn = engine.connect()
        print("Connected to Database successfully.")
        conn.close()
    except Exception as e:
        print(f"Connection Failed! Check your password/database name.\nError: {e}")
        return

    # Loop through files and load them
    for item in FILES_TO_LOAD:
        # Construct file path compatible with any OS
        file_path = os.path.join(DATA_FOLDER, item['file'])
        table_name = item['table']

        if not os.path.exists(file_path):
            print(f"⚠️ Warning: File {item['file']} not found in '{DATA_FOLDER}'. Skipping.")
            continue

        print(f"🔄 Processing '{item['file']}' -> Table: '{table_name}'...")

        try:
            # 1. EXTRACT & TRANSFORM
            # Read CSV and treat '\N' as actual NULL (NaN in pandas)
            df = pd.read_csv(file_path, na_values=['\\N'])

            # Convert column names to lowercase (to match PostgreSQL schema)
            df.columns = [c.lower() for c in df.columns]

            # 2. LOAD
            # Load data into SQL.
            # 'if_exists=append': Adds data to the empty tables we created.
            # 'index=False': Do not write the pandas index as a column.
            df.to_sql(table_name, engine, if_exists='append', index=False, method='multi', chunksize=1000)

            print(f"   ✅ Loaded {len(df)} rows.")

        except Exception as e:
            print(f"   ❌ Error loading {table_name}: {e}")

    # ==========================================
    # FINAL STEP: Create Materialized Views Automatically
    # ==========================================
    print("🛠️ Creating Materialized Views...")
    try:
        # Read the SQL view definition file
        with open('./sql/01_views.sql', 'r') as f:
            sql_script = f.read()
        
        # Connect and execute the SQL script
        engine = create_engine(DB_CONNECTION_STR)
        with engine.connect() as conn:
            conn.execute(text(sql_script))
            conn.commit() # Required to save changes
            print("   ✅ Views created successfully!")
            
    except Exception as e:
        print(f"   ❌ Error creating views: {e}")

    print("\n🎉 DONE! Pipeline finished.")


if __name__ == "__main__":
    load_data()
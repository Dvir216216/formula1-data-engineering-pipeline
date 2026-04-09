import os
import time
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# ==========================================
# 1. CONFIGURATION & ENVIRONMENT
# ==========================================
# Load environment variables from .env file
load_dotenv()

# ⚠️ SECURE: Fetching connection string from environment variables
DB_CONNECTION_STR = os.getenv("DATABASE_URL")

if not DB_CONNECTION_STR:
    raise ValueError("❌ DATABASE_URL is missing! Please check your .env file.")

# ⚠️ SECURE & DYNAMIC: Path to the data folder
DATA_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'data')

# List of files to load in specific order (Hierarchy Matters for Foreign Keys!)
FILES_TO_LOAD = [
    # Level 1: Lookup Tables
    {'file': 'circuits.csv', 'table': 'circuits'},
    {'file': 'seasons.csv', 'table': 'seasons'},
    {'file': 'status.csv', 'table': 'status'},
    {'file': 'drivers.csv', 'table': 'drivers'},
    {'file': 'constructors.csv', 'table': 'constructors'},

    # Level 2: Core Tables
    {'file': 'races.csv', 'table': 'races'},

    # Level 3: Results & Linking Tables
    {'file': 'constructor_results.csv', 'table': 'constructor_results'},
    {'file': 'constructor_standings.csv', 'table': 'constructor_standings'},
    {'file': 'driver_standings.csv', 'table': 'driver_standings'},
    {'file': 'qualifying.csv', 'table': 'qualifying'},
    {'file': 'results.csv', 'table': 'results'},
    {'file': 'sprint_results.csv', 'table': 'sprint_results'},
    
    # Level 4: Heavy Tables (Prone to network issues)
    {'file': 'pit_stops.csv', 'table': 'pit_stops'},
    {'file': 'lap_times.csv', 'table': 'lap_times'}
]

def run_pipeline():
    print("🚀 Starting Fault-Tolerant ETL Pipeline...")
    
    try:
        engine = create_engine(DB_CONNECTION_STR)
        print("✅ Connected to Database successfully.")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return

    # ==========================================
    # 2. EXTRACT, TRANSFORM, LOAD (Robust)
    # ==========================================
    for file_info in FILES_TO_LOAD:
        file_name = file_info['file']
        table_name = file_info['table']
        file_path = os.path.join(DATA_FOLDER, file_name)

        if not os.path.exists(file_path):
            print(f"   ⚠️ Skipping {file_name}: File not found at {file_path}")
            continue

        try:
            # 1. EXTRACT & TRANSFORM
            df = pd.read_csv(file_path, na_values=['\\N'])
            df.columns = [c.lower() for c in df.columns]

            # 2. LOAD
            print(f"🔄 Processing '{file_name}' -> Table: '{table_name}'...")
            
            # A. Idempotency Check: Clear table before loading
            with engine.begin() as conn:
                conn.execute(text(f"TRUNCATE TABLE {table_name} CASCADE;"))
            print(f"   🧹 Cleared existing data in '{table_name}' (Idempotency maintained)")

            # B. Chunking & Exponential Backoff Retry Mechanism
            chunk_size = 5000
            max_retries = 3
            total_rows = len(df)

            for i in range(0, total_rows, chunk_size):
                chunk = df.iloc[i:i+chunk_size]
                retries = 0
                
                while retries <= max_retries:
                    try:
                        # Wrap EACH chunk in its own transaction
                        with engine.begin() as conn:
                            chunk.to_sql(table_name, conn, if_exists='append', index=False, method='multi')
                        break  # Success! Break the retry loop and move to the next chunk
                        
                    except Exception as e:
                        retries += 1
                        if retries > max_retries:
                            raise Exception(f"Chunk failed after {max_retries} attempts. Last error: {e}")
                        
                        wait_time = 3 * retries  # Waits 3s, then 6s, then 9s...
                        print(f"   ⚠️ Network glitch. Retrying rows {i} to {i+len(chunk)} in {wait_time}s... (Attempt {retries}/{max_retries})")
                        time.sleep(wait_time)

            print(f"   ✅ Successfully loaded all {total_rows} rows.")

        except Exception as e:
            print(f"   ❌ CRITICAL ERROR loading {table_name}: {e}")
            print("   🛑 Halting ETL pipeline to prevent data corruption.")
            return  # Stop the entire pipeline because downstream tables depend on this one

    # ==========================================
    # 3. APPLY ADVANCED SQL ARCHITECTURE
    # ==========================================
    print("\n🛠️ Applying Advanced SQL Architecture (Views & Triggers)...")
    sql_dir = os.path.join(os.path.dirname(__file__), '..', 'sql')
    
    # Files must be executed in this exact order due to dependencies
    sql_files = [
        'analysis/00_create_master_view.sql',
        'optimization/materialization/01_create_materialized_view.sql',
        'automation/01_create_refresh_function.sql',
        'automation/02_create_trigger.sql'
    ]
    
    try:
        with engine.begin() as conn:
            for filename in sql_files:
                filepath = os.path.join(sql_dir, filename)
                print(f"   📂 Executing {filename}...")
                
                if not os.path.exists(filepath):
                    raise FileNotFoundError(f"Missing SQL file: {filepath}")
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    sql_script = f.read()
                
                # Execute the script
                conn.execute(text(sql_script))
                
        print("   ✅ All SQL architecture files executed successfully!")
        print("🎉 ETL Pipeline Completed Successfully!")
            
    except Exception as e:
        print(f"   ❌ Error applying SQL architecture: {e}")

if __name__ == "__main__":
    run_pipeline()
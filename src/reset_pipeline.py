import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# 1. Load environment variables
load_dotenv()

# 2. Configuration
DB_URI = os.getenv("DATABASE_URL")
# Adjust the path to go up one level from 'src' to the root, then into 'sql'
SQL_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'sql', '00_init_database_schema.sql')

def reset_database():
    if not DB_URI:
        print("❌ Error: DATABASE_URL is missing. Check your .env file.")
        return

    if not os.path.exists(SQL_FILE_PATH):
        print(f"❌ Error: SQL file not found at {SQL_FILE_PATH}")
        return

    print(f"🔄 Starting Database Reset Protocol...")
    print(f"📂 Reading schema from: {SQL_FILE_PATH}")

    try:
        # Read the SQL file
        with open(SQL_FILE_PATH, 'r', encoding='utf-8') as file:
            sql_script = file.read()

        # Connect to DB and execute
        engine = create_engine(DB_URI)
        
        # Using engine.begin() ensures the transaction is automatically committed
        with engine.begin() as conn:
            conn.execute(text(sql_script))
            
        print("✅ Database reset successfully! All tables dropped and recreated (Clean Slate).")

    except Exception as e:
        print(f"❌ Database Reset Failed: {e}")

if __name__ == "__main__":
    # Safety mechanism to prevent accidental runs in production
    confirmation = input("⚠️ WARNING: This will DROP all data in the database! Are you sure? (yes/no): ")
    if confirmation.lower() == 'yes':
        reset_database()
    else:
        print("🛑 Reset cancelled.")
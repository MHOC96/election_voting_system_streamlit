from sqlalchemy import create_engine, text
import pandas as pd

DATABASE_URL = "postgresql://postgres.sahpsmlifypeafjvsrwq:xOs9iTdM33rtrMeH@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres"

def database_connection():
    try:
        engine = create_engine(DATABASE_URL)
        print("Successfully connected to Supabase PostgreSQL!")
        return engine
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

engine = database_connection()

if engine:
    with engine.connect() as connection:
        query = text("SELECT * FROM nominee;")
        df = pd.read_sql(query, connection)
        
    print("\n--- Current Nominees ---")
    print(df)
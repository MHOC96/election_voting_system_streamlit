import os

from sqlalchemy import create_engine, text


def get_database_url():
    try:
        import streamlit as st

        return st.secrets["DATABASE_URL"]
    except Exception:
        pass

    url = os.environ.get("DATABASE_URL")
    if url:
        return url

    raise RuntimeError(
        "DATABASE_URL not found. Set it in .streamlit/secrets.toml or as an environment variable."
    )


def database_connection():
    try:
        engine = create_engine(get_database_url())
        print("Successfully connected to Supabase PostgreSQL!")
        return engine
    except Exception as e:
        print(f"Connection failed: {e}")
        return None


if __name__ == "__main__":
    import pandas as pd

    engine = database_connection()

    if engine:
        with engine.connect() as connection:
            query = text("SELECT * FROM nominee;")
            df = pd.read_sql(query, connection)

        print("\n--- Current Nominees ---")
        print(df)

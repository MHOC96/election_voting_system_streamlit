import os

from sqlalchemy import create_engine, text

try:
    import streamlit as st

    _STREAMLIT_AVAILABLE = True
except ImportError:
    _STREAMLIT_AVAILABLE = False


def get_database_url():
    if _STREAMLIT_AVAILABLE:
        try:
            return st.secrets["DATABASE_URL"]
        except Exception:
            pass

    url = os.environ.get("DATABASE_URL")
    if url:
        return url

    raise RuntimeError(
        "DATABASE_URL not found. Set it in .streamlit/secrets.toml or as an environment variable."
    )


def _create_engine():
    return create_engine(get_database_url(), pool_pre_ping=True)


if _STREAMLIT_AVAILABLE:

    @st.cache_resource
    def get_engine():
        return _create_engine()


def database_connection():
    try:
        if _STREAMLIT_AVAILABLE:
            return get_engine()
        return _create_engine()
    except Exception as e:
        print(f"Connection failed: {e}")
        return None


if __name__ == "__main__":
    import pandas as pd

    engine = database_connection()

    if engine:
        with engine.connect() as connection:
            df = pd.read_sql(text("SELECT * FROM nominee"), connection)

        print("\n--- Current Nominees ---")
        print(df)

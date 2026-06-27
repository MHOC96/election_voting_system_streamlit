from sqlalchemy import text

from connection import database_connection


def admin_login(admin_email, admin_password):
    try:
        engine = database_connection()
        if engine is None:
            return None

        with engine.connect() as conn:
            row = conn.execute(
                text("SELECT password FROM admin WHERE email = :email"),
                {"email": admin_email},
            ).fetchone()

        if row and row[0] == admin_password:
            return True
        return False

    except Exception as e:
        print(f"Error: {e}")
        return None


def add_nominee(nominee_name, nominee_party):
    try:
        engine = database_connection()
        if engine is None:
            return False

        with engine.begin() as conn:
            existing = conn.execute(
                text("SELECT 1 FROM nominee WHERE name = :name"),
                {"name": nominee_name},
            ).fetchone()

            if existing:
                return False

            conn.execute(
                text(
                    "INSERT INTO nominee (name, nominee_party) VALUES (:name, :party)"
                ),
                {"name": nominee_name, "party": nominee_party},
            )
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False


def get_nominee_list():
    try:
        engine = database_connection()
        if engine is None:
            return None

        with engine.connect() as conn:
            return conn.execute(
                text("SELECT nominee_id, name, nominee_party FROM nominee")
            ).fetchall()

    except Exception as e:
        print(f"Error: {e}")
        return None

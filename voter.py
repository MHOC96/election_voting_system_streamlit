from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from connection import database_connection


def get_voter_details(nic):
    try:
        engine = database_connection()
        if engine is None:
            return None, "Database connection failed."

        with engine.connect() as conn:
            voter_details = conn.execute(
                text(
                    "SELECT name, electoral_district, electorates "
                    "FROM voter_details WHERE nic_number = :nic"
                ),
                {"nic": nic},
            ).fetchone()

        if voter_details:
            return voter_details, None
        return None, "User not available in the system, please contact Gramasewaka."

    except Exception as e:
        return None, f"Error found: {e}"


def voter_vote(nic_number, voter_name, electoral_district, electorate, vote_nominee):
    try:
        engine = database_connection()
        if engine is None:
            return "Database connection failed."

        with engine.begin() as conn:
            conn.execute(
                text(
                    "INSERT INTO voter "
                    "(nic_no, voter_name, electoral_district, electorates, nominee_id) "
                    "VALUES (:nic, :name, :district, :electorate, :nominee_id)"
                ),
                {
                    "nic": nic_number,
                    "name": voter_name,
                    "district": electoral_district,
                    "electorate": electorate,
                    "nominee_id": vote_nominee,
                },
            )
        return f"Voter: {voter_name} successfully voted."

    except IntegrityError:
        return f"Voter: {voter_name} has already voted."

    except Exception as e:
        return f"Error encountered: {e}"

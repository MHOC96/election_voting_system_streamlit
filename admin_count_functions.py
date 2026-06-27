from sqlalchemy import text

from connection import database_connection


def get_top3_nominees():
    try:
        engine = database_connection()
        if engine is None:
            return False

        with engine.connect() as conn:
            return conn.execute(
                text(
                    """
                    SELECT n.nominee_id, n.name, n.nominee_party,
                           COUNT(v.nominee_id) AS vote_count
                    FROM nominee n
                    LEFT JOIN voter v ON n.nominee_id = v.nominee_id
                    GROUP BY n.nominee_id, n.name, n.nominee_party
                    ORDER BY vote_count DESC
                    LIMIT 3
                    """
                )
            ).fetchall()

    except Exception as e:
        print(f"Error found: {e}")
        return False


def individual_nominee_vote(nominee_id):
    try:
        engine = database_connection()
        if engine is None:
            return False

        with engine.connect() as conn:
            result = conn.execute(
                text(
                    """
                    SELECT n.nominee_id, n.name, n.nominee_party,
                           COUNT(v.nic_no) AS total_votes
                    FROM nominee n
                    LEFT JOIN voter v ON n.nominee_id = v.nominee_id
                    WHERE n.nominee_id = :nominee_id
                    GROUP BY n.nominee_id, n.name, n.nominee_party
                    """
                ),
                {"nominee_id": nominee_id},
            ).fetchone()

        return result if result else False

    except Exception as e:
        print(f"Error found: {e}")
        return False

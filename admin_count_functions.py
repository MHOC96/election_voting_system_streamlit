from connection import database_connection

def get_top3_nominees():
    try:
        connection = database_connection()

        cursor = connection.cursor()
        query = """
        SELECT n.nominee_id, n.name, n.nominee_party, COUNT(v.nominee_id) AS vote_count
        FROM nominee n
        LEFT JOIN voter v ON n.nominee_id = v.nominee_id
        GROUP BY n.nominee_id
        ORDER BY vote_count DESC
        LIMIT 3
        """
        cursor.execute(query)
        return cursor.fetchall()

    except Exception as e:
        print(f"Error found: {e}")
        return False

    finally:
        cursor.close()
        connection.close()

def individual_nominee_vote(nominee_id):
    try:
        connection = database_connection()

        cursor = connection.cursor()
        query = """
        SELECT n.nominee_id, n.name, n.nominee_party, COUNT(v.nic_no) AS total_votes
        FROM nominee n
        LEFT JOIN voter v ON n.nominee_id = v.nominee_id
        WHERE n.nominee_id = %s
        GROUP BY n.nominee_id
        """
        cursor.execute(query, (nominee_id,))
        result = cursor.fetchone()

        if result:
            return result
        else:
            return False

    except Exception as e:
        print(f"Error found: {e}")

    finally:
        cursor.close()
        connection.close()

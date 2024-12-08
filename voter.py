from admin import get_nominee_list
from connection import database_connection
from mysql.connector import IntegrityError


def get_voter_details(nic):

    try:
        voter_connection = database_connection()
            
        voter_details_get_cursor = voter_connection.cursor()
        query = "SELECT name, electoral_district, electorates FROM voter_details WHERE nic_number=%s"
        voter_details_get_cursor.execute(query, (nic,))
        voter_details = voter_details_get_cursor.fetchone()

        if voter_details:
            print(voter_details)
            return voter_details, None
        else:
            return None, "User not available in the system, please contact Gramasewaka."

    except Exception as e:
        return None, f"Error found: {e}"

    finally:
            voter_details_get_cursor.close()
            voter_connection.close()


def voter_vote(nic_number, voter_name, electoral_district, electorate, vote_nominee):

    voter_vote_connection = database_connection()

    try:
        voter_vote_connection = database_connection()
        voter_vote_cursor = voter_vote_connection.cursor()
        query_vote = """
            INSERT INTO voter(nic_no, voter_name, electoral_district, electorates, nominee_id) 
            VALUES (%s, %s, %s, %s, %s)
        """
        voter_vote_cursor.execute(query_vote, (nic_number, voter_name, electoral_district, electorate, vote_nominee))
        voter_vote_connection.commit()
        return f"Voter: {voter_name} successfully voted."

    except IntegrityError:
        return f"Voter: {voter_name} has already voted."

    except Exception as e:
        return f"Error encountered: {e}"

    finally:
            voter_vote_cursor.close()
            voter_vote_connection.close()

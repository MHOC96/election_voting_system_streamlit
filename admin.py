from connection import database_connection

def admin_login(admin_email, admin_password):
    try:
        connection = database_connection()

        cursor = connection.cursor()
        cursor.execute("SELECT password FROM admin WHERE email = %s", (admin_email,))
        result = cursor.fetchone()
        if result[0] == admin_password:
            return True
        return False

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        cursor.close()
        connection.close()

def add_nominee(nominee_name, nominee_party):
    try:
        connection = database_connection()
        
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM nominee WHERE name = %s", (nominee_name,))
        existing_nominee = cursor.fetchone()

        if existing_nominee:
            return False 

        cursor.execute("INSERT INTO nominee (name, nominee_party) VALUES (%s, %s)", (nominee_name, nominee_party))
        connection.commit()
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

    finally:
        cursor.close()
        connection.close()

def get_nominee_list():
    try:
        connection = database_connection()

        cursor = connection.cursor()
        cursor.execute("SELECT nominee_id, name, nominee_party FROM nominee")
        return cursor.fetchall()

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        cursor.close()
        connection.close()

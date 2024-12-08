import mysql.connector
from mysql.connector import Error


def database_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost", user="root", database="voting", password=""
        )
        if connection.is_connected():
            return connection

    except Error as e:
        print(f"The error:{e}")

import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="yaswanth@630",
        database="logaudit_db"
    )
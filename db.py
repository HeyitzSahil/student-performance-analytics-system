import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="Sahil",
        password="Sahil@1234",
        database="std_performance"
    )
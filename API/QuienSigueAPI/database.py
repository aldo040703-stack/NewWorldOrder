import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='usuarioEmp',
            password='123456',
            database='sistema_clientes'
        )
        return connection
    except Error as e:
        print(f"Error conectando a MySQL: {e}")
        return None
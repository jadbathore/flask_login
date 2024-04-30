from mysql import connector

def connect_func():
    try: 
        connection = connector.connect(
        host="localhost",
        database="flask_login",
        user="root",
        password="root",
        unix_socket = '/Applications/MAMP/tmp/mysql/mysql.sock',
    )
    except connector.errors as err:
        print(f"une erreur est survenu : {err}")
    return connection

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
        return connection
    except Exception :
        raise Exception('connection à la base de donné a echoué')
    

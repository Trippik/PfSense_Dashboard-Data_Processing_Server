import mysql.connector
import os

def pull_db_details():
    return (os.environ["DB_IP"],os.environ["DB_USER"],os.environ["DB_PASS"],os.environ["DB_SCHEMA"],os.environ["DB_PORT"])

def create_db_connection():
    db_details = pull_db_details()
    return mysql.connector.connect(
        host=db_details[0],
        user=db_details[1],
        password=db_details[2],
        database=db_details[3],
        port=db_details[4]
    )

#READ FROM DB
def query_db(query):
    with create_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return(result)

def list_clients():
    query = "SELECT id, pfsense_name, hostname FROM pfsense_instances"
    results = query_db(query)
    clients = []
    for client in results:
        clients = clients + [[client[0], client[1], client[2]]]
    return(clients)

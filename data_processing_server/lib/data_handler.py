from data_processing_server.lib import db_handler

def list_clients():
    query = "SELECT id, pfsense_name, hostname FROM pfsense_instances"
    results = db_handler.query_db(query)
    clients = []
    for client in results:
        clients = clients + [[client[0], client[1], client[2]]]
    return(clients)

def row_sanitize(value, new_row):
    if(value == None):
        value = 0
    elif(value == "NaN"):
        value = 0
    value = int(value)
    new_row = new_row + [value]
    return(new_row)
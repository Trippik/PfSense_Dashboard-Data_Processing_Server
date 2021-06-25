#----------------------------------------------------
#INITIALISATION
#----------------------------------------------------
#IMPORT LIBRARIES
import logging
import mysql.connector
import os
import datetime
from sklearn.ensemble import IsolationForest
import numpy as np
import calendar
import pickle
from datetime import date

#ADD TO LOG
logging.warning("Program Started")

#SET DB PARAMETERS
db_host = "192.168.40.47"
db_user = "root"
db_password = "Cl0udyDay!"
db_schema = "Dashboard_DB"
db_port = "3306"

#SET STORAGE DIRECTORY
dir = "/"

loop = True

#----------------------------------------------------
#UNDERLYING FUNCTIONS
#----------------------------------------------------
#READ FROM DB
def query_db(query):
    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_schema,
        port=db_port
    )
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return(result)

#WRITE TO DB
def update_db(query):
    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_schema,
        port=db_port
    )
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()

def list_clients():
    query = "SELECT id, pfsense_name, hostname FROM pfsense_instances"
    results = query_db(query)
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

#----------------------------------------------------
#PRIMARY FUNCTIONS
#----------------------------------------------------

def daily_model(client):
    now = datetime.datetime.now()
    timestamp_now = now.strftime("%Y-%m-%d %H:%M:%S")
    query = """SELECT 
	`pfsense_logs`.`type_code`,
    `pfsense_logs`.`pfsense_instance`,
    `pfsense_logs`.`log_type`,
    `pfsense_logs`.`rule_number`,
    `pfsense_logs`.`sub_rule_number`,
    `pfsense_logs`.`anchor`,
    `pfsense_logs`.`tracker`,
    `pfsense_logs`.`real_interface`,
    `pfsense_logs`.`reason`,
    `pfsense_logs`.`act`,
    `pfsense_logs`.`direction`,
    `pfsense_logs`.`ip_version`,
    `pfsense_logs`.`flags`,
    `pfsense_logs`.`protocol`,
    `pfsense_logs`.`source_ip`,
    `pfsense_logs`.`destination_ip`,
    `pfsense_logs`.`source_port`,
    `pfsense_logs`.`destination_port`
FROM `Dashboard_DB`.`pfsense_logs` WHERE record_time <= '{}' AND record_time >='{}' AND pfsense_instance = '{}'"""
    day_ago = now - datetime.timedelta(days=1)
    timestamp_week_ago = day_ago.strftime("%Y-%m-%d %H:%M:%S")
    input(query.format(timestamp_now, timestamp_week_ago, client[0]))
    results = query_db(query.format(timestamp_now, timestamp_week_ago, client[0]))
    model = IsolationForest(max_features = 18, n_estimators = 100)
    # fit model
    max = len(results)
    count = 0
    data = []
    while(count < max):
        row = results[count]
        max_row = len(row)
        count_row = 0
        new_row = []
        while(count_row < max_row):
            value = row[count_row]
            new_row = row_sanitize(value, new_row)
            count_row = count_row + 1
        data = data + [new_row]
        count = count + 1
    final_results = np.array(data)
    input(final_results)
    model.fit(final_results)
    return(model)

def process():
    clients = list_clients()
    models = []
    for client in clients:
        input(client)
        model = daily_model(client)
        models = models + [client, model]
    return(models)

models = process()
for item in models:
    client = item[0]
    model = item[1]
    hostname = client[2]
    sub_path = os.path.join(dir + "/" + hostname)
    try:
        sub_path = os.mkdir(sub_path)
    except:
        pass
    pickle.dump(model, open(sub_path + "/yesterday.pickle"), 'wb')

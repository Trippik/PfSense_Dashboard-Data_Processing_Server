#----------------------------------------------------
#INITIALISATION
#----------------------------------------------------
#IMPORT LIBRARIES
import logging
import mysql.connector
import os
import re
import datetime
from sklearn.ensemble import IsolationForest
import numpy as np
import pandas as pd
import time

logging.basicConfig(filename="Test.log", level=logging.DEBUG)

#ADD TO LOG
logging.warning("Program Started")

#SET DB PARAMETERS
db_host = "192.168.40.47"
db_user = "root"
db_password = "Cl0udyDay!"
db_schema = "Dashboard_DB"
db_port = "3306"


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

def weekly_model(client):
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
    week_ago = now - datetime.timedelta(days=7)
    timestamp_week_ago = week_ago.strftime("%Y-%m-%d %H:%M:%S")
    results = query_db(query.format(timestamp_now, timestamp_week_ago, client[0]))
    model = IsolationForest(max_features = 18, n_estimators = 10)
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
    model.fit(final_results)
    return(model)

def process():
    clients = list_clients()
    models = []
    for client in clients:
        model = weekly_model(client)
        models = models + [client, model]
    return(models)

def check(client, model):
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
    `pfsense_logs`.`destination_port` FROM pfsense_logs WHERE pfsense_instance = {} ORDER BY record_time DESC LIMIT 1"""
    result = query_db(query.format(client))[0]
    new_result = []
    for item in result:
        new_result = row_sanitize(item, new_result)
    new_result = np.array([new_result])
    final = model.predict(new_result)
    return(final)
    if(final == 1):
        print("Normal")
    elif(final == -1):
        print("DANGER WILL ROBINSON!!!!!!!!!")
    print("----------------------------------------------------------")
    print("----------------------------------------------------------")


master_count = 0
master_max = 5
while(master_count < master_max):
    models = process()
    max_value = 50
    count = 0
    result_set = []
    while (count < max_value):
        result = check(models[0][0], models[1])
        if(result == 1):
            print("Normal")
        elif(result == -1):
            print("DANGER WILL ROBINSON!!!!!!!!!")
        print("----------------------------------------------------------")
        print("----------------------------------------------------------")
        result_set = result_set + [result]
        time.sleep(5)
        count = count + 1
    logging.debug(str(master_count) + " iteration normal count: " + str(result_set.count(1)))
    logging.debug(str(master_count) + " iteration abnormal count: " + str(result_set.count(-1)))
    logging.debug("Number of entries in DB: " + str((query_db("SELECT COUNT(*) FROM pfsense_logs"))[0][0]))
    logging.debug("----------------------------------------------------------------------------------------")
    master_count = master_count + 1

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
import time
import calendar
import joblib
from datetime import date

logging.basicConfig(filename="Test.log", level=logging.DEBUG)

#ADD TO LOG
logging.warning("Program Started")

#SET DB PARAMETERS
db_host = "192.168.40.47"
db_user = "root"
db_password = "Cl0udyDay!"
db_schema = "Dashboard_DB"
db_port = "3306"

#SET STORAGE DIRECTORY
dir = "/var/models/"

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

def weekly_process(query):
    clients = list_clients()
    now = datetime.datetime.now()
    week_ago = now - datetime.timedelta(days=7)
    timestamp_week_ago = week_ago.strftime("%Y-%m-%d %H:%M:%S")
    timestamp_now = now.strftime("%Y-%m-%d %H:%M:%S")
    final_results = []
    for client in clients:
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
        client_results = np.array(data)
        model.fit(client_results)
        final_results = [[client, model]]
    return(final_results)

def daily_process(query):
    clients = list_clients()
    print(clients)
    now = datetime.datetime.now()
    yesterday = now - datetime.timedelta(days=1)
    timestamp_yesterday = yesterday.strftime("%Y-%m-%d %H:%M:%S")
    timestamp_now = now.strftime("%Y-%m-%d %H:%M:%S")
    final_results = []
    for client in clients:
        print("Single Client Start: " + timestamp_now)
        results = query_db(query.format(timestamp_now, timestamp_yesterday, client[0]))
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
        client_results = np.array(data)
        model.fit(client_results)
        final_results = [[client, model]]
    now = datetime.datetime.now()
    timestamp_now = now.strftime("%Y-%m-%d %H:%M:%S")
    print("Finish: " + timestamp_now)
    return(final_results)

while(loop == True):
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
    now = datetime.datetime.now()
    my_date = date.today()
    todays_day = calendar.day_name[my_date.weekday()]
    current_time = now.strftime("%H:%M")
    if(current_time == "19:46"):
        print("Started")
        print(daily_process(query))
    if(todays_day == "Tuesday"):
        results = weekly_process(query)
    input()

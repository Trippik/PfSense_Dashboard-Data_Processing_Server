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
db_host = os.environ["DB_IP"]
db_user = os.environ["DB_USER"]
db_password = os.environ["DB_PASS"]
db_schema = os.environ["DB_SCHEMA"]
db_port = os.environ["DB_PORT"]

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
        model = IsolationForest(max_features = 18, n_estimators = 100, n_jobs=-1)
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
    logging.warning(clients)
    now = datetime.datetime.now()
    yesterday = now - datetime.timedelta(days=1)
    timestamp_yesterday = yesterday.strftime("%Y-%m-%d %H:%M:%S")
    timestamp_now = now.strftime("%Y-%m-%d %H:%M:%S")
    final_results = []
    for client in clients:
        logging.warning("Single Client Start: " + timestamp_now)
        results = query_db(query.format(timestamp_now, timestamp_yesterday, client[0]))
        model = IsolationForest(max_features = 18, n_estimators = 100, n_jobs=-1)
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
    logging.warning("Finish: " + timestamp_now)
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
    current_date = now.strftime("%Y-%m-%d")
    if(current_time == os.environ["TIME"]):
        results = daily_process(query)
        for result in results:
            sub_path = os.path.join(dir + "/" + result[0][2])
            try:
                sub_path = os.mkdir(sub_path)
            except:
                pass
	    pickle.dump(result[1], open(sub_path + "/yesterday.pickle"), 'wb')
	    pickle.dump(result[1], open(sub_path + "/" + todays_day + ".pickle"), 'wb')
            logging.warning("Done")
            #except:
             #   pass
        if(todays_day == os.environ["day"]):
            logging.warning("start")
            results = weekly_process(query)
            for result in results:
                sub_path = os.path.join(dir + "/" + result[0][2])
                try:
                    sub_path = os.mkdir(sub_path)
                except:
                    pass
                logging.warning(result[1])
                logging.warning(sub_path)
		pickle.dump(result[1], open(sub_path + "/last_week.pickle"), 'wb')
                logging.warning("Done")

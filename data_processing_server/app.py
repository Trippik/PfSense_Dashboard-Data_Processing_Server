#----------------------------------------------------
#INITIALISATION
#----------------------------------------------------
#IMPORT LIBRARIES
import logging
from re import sub
import mysql.connector
import os
import datetime
from sklearn.ensemble import IsolationForest
import numpy as np
import calendar
import pickle
from datetime import date

#ADD TO LOG
logging.warning("----------------------------------------------------")
logging.warning("Program Started")
logging.warning("----------------------------------------------------")
logging.warning(" ")
logging.warning(" ")

#SET DB PARAMETERS
db_host = os.environ["DB_IP"]
db_user = os.environ["DB_USER"]
db_password = os.environ["DB_PASS"]
db_schema = os.environ["DB_SCHEMA"]
db_port = os.environ["DB_PORT"]

#SET STORAGE DIRECTORY
dir = "/var/models"

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

def create_sub_path(sub_path):
    result = os.path.exists(sub_path)
    if(result == False):
        os.mkdir(sub_path)
    
def model_save(model, directory_name):
    pickle.dump(model, open(directory_name, "wb"))

def weekly_process(query, client):
    now = datetime.datetime.now()
    week_ago = now - datetime.timedelta(days=7)
    timestamp_week_ago = week_ago.strftime("%Y-%m-%d %H:%M:%S")
    timestamp_now = now.strftime("%Y-%m-%d %H:%M:%S")
    logging.warning("Single Client Weekly Model Start: " + timestamp_now)
    results = query_db(query.format(timestamp_now, timestamp_week_ago, client))
    model = IsolationForest(max_features = 17, n_estimators = 100, n_jobs=-1)
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
    now = datetime.datetime.now()
    timestamp_now = now.strftime("%Y-%m-%d %H:%M:%S")
    logging.warning("Finish: " + timestamp_now)
    return(model)

def daily_process(query, client):
    now = datetime.datetime.now()
    yesterday = now - datetime.timedelta(days=1)
    timestamp_yesterday = yesterday.strftime("%Y-%m-%d %H:%M:%S")
    timestamp_now = now.strftime("%Y-%m-%d %H:%M:%S")
    logging.warning("Single Client Daily Model Start: " + timestamp_now)
    results = query_db(query.format(timestamp_now, timestamp_yesterday, client))
    model = IsolationForest(max_features = 17, n_estimators = 100, n_jobs=-1)
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
    now = datetime.datetime.now()
    timestamp_now = now.strftime("%Y-%m-%d %H:%M:%S")
    logging.warning("Finish: " + timestamp_now)
    return(model)

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
    `pfsense_logs`.`destination_port`
FROM `Dashboard_DB`.`pfsense_logs` WHERE record_time <= '{}' AND record_time >='{}' AND pfsense_instance = '{}'"""
    now = datetime.datetime.now()
    my_date = date.today()
    todays_day = calendar.day_name[my_date.weekday()]
    current_time = now.strftime("%H:%M")
    current_date = now.strftime("%Y-%m-%d")
    if(current_time == os.environ["TIME"]):
        logging.warning("Overall Modelling Start: " + current_time)
        clients = list_clients()
        for client in clients:
            try:
                logging.warning("Modelling for " + client[2])
                model = daily_process(query, str(client[0]))
                sub_path = os.path.join(dir + "/" + client[2])
                create_sub_path(sub_path)
                model_save(model, sub_path + "/yesterday.pickle")
                model_save(model, sub_path + "/" + todays_day + ".pickle")
                if(todays_day == os.environ["day"]):
                    model = weekly_process(query, str(client[0]))
                    sub_path = os.path.join(dir + "/" + client[2])
                    create_sub_path(sub_path)
                    model_save(model, sub_path + "/last_week.pickle")
            except:
                logging.warning("Error for client: " + str(client[0]))
            logging.warning(" ")
            logging.warning(" ")
        logging.warning("Overall Modelling Complete")

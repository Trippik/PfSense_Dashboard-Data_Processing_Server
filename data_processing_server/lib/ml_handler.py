import os
import pickle
import logging
import datetime
from sklearn.ensemble import IsolationForest
import numpy as np


from data_processing_server.lib import db_handler, data_handler

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
    results = db_handler.query_db(query.format(timestamp_now, timestamp_week_ago, client))
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
            new_row = data_handler.row_sanitize(value, new_row)
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
    results = db_handler.query_db(query.format(timestamp_now, timestamp_yesterday, client))
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
            new_row = data_handler.row_sanitize(value, new_row)
            count_row = count_row + 1
        data = data + [new_row]
        count = count + 1
    client_results = np.array(data)
    model.fit(client_results)
    now = datetime.datetime.now()
    timestamp_now = now.strftime("%Y-%m-%d %H:%M:%S")
    logging.warning("Finish: " + timestamp_now)
    return(model)
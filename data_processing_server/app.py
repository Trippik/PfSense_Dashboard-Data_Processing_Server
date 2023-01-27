#----------------------------------------------------
#INITIALISATION
#----------------------------------------------------
#IMPORT LIBRARIES
import logging
from re import sub
import os
import datetime
import calendar
from datetime import date

from data_processing_server.lib import data_handler, ml_handler

#SET STORAGE DIRECTORY
dir = "/var/models"

loop = True

#----------------------------------------------------
#UNDERLYING FUNCTIONS
#----------------------------------------------------
def main():
    #ADD TO LOG
    logging.warning("----------------------------------------------------")
    logging.warning("Program Started")
    logging.warning("----------------------------------------------------")
    logging.warning(" ")
    logging.warning(" ")
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
    while(loop == True):
        now = datetime.datetime.now()
        my_date = date.today()
        todays_day = calendar.day_name[my_date.weekday()]
        current_time = now.strftime("%H:%M")
        if(current_time == os.environ["TIME"]):
            logging.warning("Overall Modelling Start: " + current_time)
            clients = data_handler.list_clients()
            for client in clients:
                try:
                    logging.warning("Modelling for " + client[2])
                    model = ml_handler.daily_process(query, str(client[0]))
                    sub_path = os.path.join(dir + "/" + client[2])
                    ml_handler.create_sub_path(sub_path)
                    ml_handler.model_save(model, sub_path + "/yesterday.pickle")
                    ml_handler.model_save(model, sub_path + "/" + todays_day + ".pickle")
                    if(todays_day == os.environ["day"]):
                        model = ml_handler.weekly_process(query, str(client[0]))
                        sub_path = os.path.join(dir + "/" + client[2])
                        ml_handler.create_sub_path(sub_path)
                        ml_handler.model_save(model, sub_path + "/last_week.pickle")
                except:
                    logging.warning("Error for client: " + str(client[0]))
                logging.warning(" ")
                logging.warning(" ")
            logging.warning("Overall Modelling Complete")

if __name__ == '__main__':
    main()

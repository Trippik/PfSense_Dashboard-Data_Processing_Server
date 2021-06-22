# PfSense_Dashboard-Data_Processing_Server
Data processing / Machine Learning modelling server component of the PfSense Monitoring dashboard, formatted as a docker container it iterates through data for each PfSense instance within the PfSense dashboard, retreiving data over the last day and week, building Isolation Forest derived models to be able to identify unusual network behavior
  
## ENV Variables  
DB_IP = IP that MySQL is accessible on  
DB_USER = User credential for DB access  
DB_PASS = Password for DB access  
DB_SCHEMA = Name of target Schema in DB  
DB_PORT = Port that DB is accessible on  
TIME = Time of day to compute daily pfsense models (HH:MM)  
day = Day of the week (full name with capitalised first letter) to compute weekly models  

## Volumes
/var/models needs to be mapped to a docker volume, this volume will also be shared with other docker containers to make up the PfSense Dashboard system

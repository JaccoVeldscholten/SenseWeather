import sys, getopt
#import argparse
from sense_hat import SenseHat
import time
import mysql.connector as mariadb
from mysql.connector import errorcode

sensor_name = 'Temperatuur';
# database connection configuration
dbconfig = {
 'user': 'sensem',
 'password': 'h@',
 'host': 'localhost',
 'database': 'weerstation',
 'raise_on_warnings': True,
}

#### Default settings ####
verbose = True  # Debug enabled
interval = 10   # Interval of sending of logging
tempOffset = 20 # Temp Offset
try:
    opts, args = getopt.getopt(sys.argv[1:], "vt:")
except getopt.GetoptError as err:
	print(str(err))
	print('measure.py -v -t <interval>')
	print('-v: be verbose')
	print('-t <interval>: measure each <interval> seconds(default: 10s)')
	sys.exit(2) 
for opt, arg in opts:
    if opt == '-v':
        verbose = True
    elif opt == '-t':
        interval = int(arg)

#### Setup SenseHat ####
sh = SenseHat()

#### Connect to DB ####
try:
    mariadb_connection = mariadb.connect(**dbconfig)
    if verbose:
        print("Database connected")
except mariadb.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print("Error: {}".format(err))
    sys.exit(2)
    
# create the database cursor for executing SQL queries
cursor = mariadb_connection.cursor()
# turn on autocommit
#cursor.autocommit = True

#### Getting Sensor ID ####   
try:
    cursor.execute("SELECT id FROM sensor WHERE naam=%s",[sensor_name])
except mariadb.Error as err:
    print("Error: {}".format(err))
    sys.exit(2)
sensor_id = cursor.fetchone()
if sensor_id == None:
    print("Error: no sensor found with naam = %s" % sensor_name)
    sys.exit(2)
if verbose:
    print("Reading data from sensor %s with id %s" % (sensor_name, sensor_id[0]))
    
    
    
# infinite loop
try:
    while True:
        #### Get Sensor information ####
        tempSensor = round(sh.get_temperature(),1)
        temp = tempSensor - tempOffset
        temp = round(temp,1) ## Double Roundup so we can bypass the overflow
        #### Debug Output ####
        if verbose:
            print("Raw Temperature: %s C" % tempSensor)
            print("Calculated Temperature: %s C" % temp + " | With offset: %s C" % tempOffset)
        try:
            cursor.execute('INSERT INTO meting (waarde, sensor_id) VALUES (%s, %s);', (temp, sensor_id[0]))
        except mariadb.connector.Error as err:
            print("Error: {}".format(err))
        else:
            #### Execute query and send data to database ####
            mariadb_connection.commit();
            if verbose:
                print("Temperature saved in Database");
                print("") ## Empty line to clean
                 #### Wait for a while ####
                time.sleep(interval)
except KeyboardInterrupt: pass
#### Close database ####
mariadb_connection.close()
#### End of script ####



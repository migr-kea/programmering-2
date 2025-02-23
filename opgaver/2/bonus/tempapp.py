import sqlite3
import RPi.GPIO as GPIO
import dht11
import datetime
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

instance = dht11.DHT11(pin=14)

# Database connection setup
conn = sqlite3.connect(database='/home/mikkelgrevy/Desktop/temp/testDB.db')
cur = conn.cursor()

while True:
    result = instance.read()
    timed = str(datetime.datetime.now())
    if result.is_valid():
        print("Temperature: %-3.1f C" % result.temperature)
        print("Humidity: %-3.1f %%" % result.humidity)
        print(timed)

        try:
            sql = f"""INSERT INTO TEMPCHART (DATETIME, TEMPERATURE, HUMIDITY)
            VALUES('{timed}', '{result.temperature}', '{result.humidity}')"""
            cur.execute(sql)
            conn.commit()
        except sqlite3.OperationalError as oe:
            print(f'Transaction could not be processed: {oe}')
        except Exception as e:
            print(f'Some other mishap occurred: {e}')
    else:
        print("Error: %d" % result.error_code)
    
    sleep(2)  # Adjust sleep time if needed

# conn.close() (Unreachable here, consider handling cleanup properly)

from RPi import GPIO
from model.Alarms import Alarms
from model.Feeder import Feeder
from time import sleep
from model.dbsecurity.dbconn import DbConnection
import datetime

try:
    instance_dbconn = DbConnection('petfeeder_db')
    # instance_feeder = Feeder()
    # instance_alarm =  Alarms()

    while True:
        #get the food settings (time, amount, ...) to check if he needs to be feeded
        sql = 'SELECT * FROM petfeeder_db.tblfoodsettings;'
        records  = instance_dbconn.query(sql, dictionary=True)

        for number in range(0, len(records)):
            record = records[number]
            print(record['time'].second)
            print(datetime.datetime.now().second)

            if record['time'].hour == datetime.datetime.now().hour and record['time'].minute == datetime.datetime.now().minute and record['time'].second == datetime.datetime.now().second:
                print("Yes, feed him !!!")
                sleep(1)
            else:
                print("No")

        ## check the drink level
        # drink_in_bowl = instance_feeder.checkDrink(1)

        ## check the food level
        # food_in_bowl = instance_feeder.checkFood(1)

        ## check the provision
        # provision_left = instance_feeder.checkProvision()

        ## check if you need to make an alarm
        # instance_alarm.checkAlarms(drink_in_bowl, food_in_bowl, provision_left)

        sleep(0.1)


except Exception as e:
    print("exection happend:")
    print(str(e))


finally:
    GPIO.cleanup()
    print("Program stopped")
from time import sleep
from model.hx711.hx711 import HX711
from model.dbsecurity.dbconn import DbConnection

from model.Mcp import Mcp
from model.Pir import Pir
from model.ServoMotor import ServoMotor
from model.Ultrasonic import Ultrasonic
import datetime

class Feeder():

    def __init__(self, tolerance_food = 3, reference_unit_hx711 = 96, load_cell_cal = 1.576):
        self.__instance_hx711 = HX711(24, 23)
        self.__instance_dbconn = DbConnection("petfeeder_db")
        self.__instance_mcp = Mcp()
        self.__instance_pir = Pir(21)
        self.__instance_servo_motor = ServoMotor(25, True)
        self.__instance_ultrasonic = Ultrasonic(20, 16)

        self.__instance_hx711.set_reading_format("LSB", "MSB")
        self.__instance_hx711.set_reference_unit(reference_unit_hx711)  # the number is a calibration number, see example
        self.__instance_hx711.reset()
        self.__instance_hx711.tare()
        self.__load_cell_cal =load_cell_cal

        self.__previous_content_food = -1

        while self.__previous_content_food < 0:
            self.__previous_content_food = self.__instance_hx711.get_weight(5)

        print(self.__previous_content_food)

        self.__tolerance_food = tolerance_food  # the amount of tolerance you want to be on the reading

        self.__provision = 0  # a percentage


    def checkFoodNeeded(self):
        #get the food settings (time, amount, ...) to check if he needs to be feeded
        sql = 'SELECT * FROM petfeeder_db.tblfoodsettings;'
        records  = self.__instance_dbconn.query(sql, dictionary=True)

        for number in range(0, len(records)):
            record = records[number]
            print(record['time'].second)
            print(datetime.datetime.now().second)

            if record['time'].hour == datetime.datetime.now().hour and record['time'].minute == datetime.datetime.now().minute and record['time'].second == datetime.datetime.now().second:
                self.__giveFood(amount= record['amount_to_be_dispensed'], cummulative= record['cumulative'])
            else:
                print("No")

    def checkFood(self, dog_id = 1):
        if self.__instance_pir.read_pir() == True:
            # check bowl content with some tolerance
            current_food = -1


            current_food = abs(((self.__instance_hx711.get_weight(5) / 14)) / self.__load_cell_cal)


            if self.__previous_content_food < (current_food - self.__tolerance_food) or self.__previous_content_food > (current_food + self.__tolerance_food ):
                # sent querry to update foodlog

                sql = (
                    'INSERT INTO petfeeder_db.tblfoodlog (grams_left, timestamp, dog_id) '
                    'VALUES ( %(grams_left)s, %(timestamp)s,  %(dog_id)s );'
                )
                params = {
                    'grams_left': current_food,
                    'timestamp': datetime.datetime.now(),
                    'dog_id': dog_id,
                }

                self.__instance_dbconn.execute(sql, params)

                # update current food

                print("food updated")

                self.__previous_content_food = current_food

            return current_food

        else:
            return self.__previous_content_food


    def checkDrink(self, dog_id = 1):
        #check water level
        if self.__instance_pir.read_pir() == True:
            while self.__instance_pir.read_pir() == True:
                #print("Waiting for the dog to leave the water bowl.")
                sleep(0.1)

            #sent querry to update the database
            sql = (
                'INSERT INTO petfeeder_db.tbldrinklog (millilitres_left, timestamp, dog_id) '
                'VALUES ( %(millilitres_left)s, %(timestamp)s,  %(dog_id)s );'
            )
            params = {
                'millilitres_left': self.__instance_ultrasonic.get_content_in_ml(),
                'timestamp': datetime.datetime.now(),
                'dog_id': dog_id,
            }

            self.__instance_dbconn.execute(sql, params)

        return self.__instance_ultrasonic.get_content_in_ml()


    def checkProvision(self):
        # we have 4 ldr's, in a ideal situation (calibration needed)
        # top one < 50% --> 100%
        # top one > 50% --> 75%
        # second one > 50% --> 50%
        # third one > 50% --> 25%
        # bottom one > 50% --> 10%

        current_provision = 0

        if self.__instance_mcp.define_light_percentage(0, 1000) > 0.5:
            if self.__instance_mcp.define_light_percentage(1, 1000) > 0.5:
                if self.__instance_mcp.define_light_percentage(2, 1000) > 0.5:
                    if self.__instance_mcp.define_light_percentage(3, 1000) > 0.5:
                        current_provision = 100
                    else:
                        current_provision = 75
                else:
                    current_provision = 50
            else:
                current_provision = 25
        else:
            current_provision = 10

        # sent querry to update the database
        sql = (
            'INSERT INTO petfeeder_db.tblprovision (percentage_left, timestamp, dog_id) '
            'VALUES ( %(millilitres_left)s, %(timestamp)s);'
        )
        params = {
            'percentage_left': current_provision,
            'timestamp': datetime.datetime.now(),
        }

        self.__instance_dbconn.execute(sql, params)

        return current_provision


    def __giveFood(self, amount, cummulative):
        amount_left = self.__instance_hx711.get_weight(5)

        if cummulative == True:
            self.__instance_servo_motor.open()

            while self.__instance_hx711.get_weight(5) <= amount:
                #print("Food is being dispensed")
                sleep(0.1)

            self.__instance_servo_motor.close()

        else:
            self.__instance_servo_motor.open()

            while self.__instance_hx711.get_weight(5) - amount_left <= amount:
                print("Food is being dispensed")

            self.__instance_servo_motor.close()

        self.checkProvision()

        return self.__instance_hx711.get_weight(5)
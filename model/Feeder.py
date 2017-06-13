

class Feeder():
    from model.hx711.hx711 import HX711
    from model.dbsecurity.dbconn import DbConnection
    from model.Lcd import Lcd
    from model.Mcp import Mcp
    from model.Pir import Pir
    from model.ServoMotor import ServoMotor
    from model.Ultrasonic import Ultrasonic
    from RPi import GPIO
    import time
    import datetime


    def __init__(self, tolerance_food = 2, reference_unit_hx711 = 92):
        self.__instance_hx711 = self.HX711(24, 23)
        self.__instance_dbconn = self.DbConnection("petfeeder_db")
        self.__instance_lcd = self.Lcd(5, 22, 26, 19, 13, 6)
        self.__instance_mcp = self.Mcp()
        self.__instance_pir = self.Pir(21)
        self.__instance_servo_motor = self.ServoMotor(25, True)
        self.__instance_ultrasonic = self.Ultrasonic(20, 16)

        self.__instance_hx711.set_reading_format("LSB", "MSB")
        self.__instance_hx711.set_reference_unit(reference_unit_hx711)  # the numer is a calibration number, see example
        self.__instance_hx711.reset()
        self.__instance_hx711.tare()

        self.__instance_lcd.init_display()

        self.__previous_content_food = self.__instance_hx711.get_weight(5)
        self.__tolerance_food = tolerance_food  # the amount of tolerance you want to be on the reading

        self.__provision = 0  # a percentage


    def checkFood(self, dog_id):
        #check bowl content with some tolerance
        if  self.__previous_content_food <= (self.__instance_hx711.get_weight(5) - self.__tolerance_food):
            #sent querry to update foodlog

            sql = (
                'INSERT INTO petfeeder_db.tblfoodlog (grams_left, timestamp, dog_id) '
                'VALUES ( %(grams_left)s, %(timestamp)s,  %(dog_id)s );'
            )
            params = {
                'grams_left': self.__instance_hx711.get_weight(5),
                'timestamp': self.datetime.datetime.now(),
                'dog_id': dog_id,
            }

            self.__instance_dbconn.execute(sql, params)

    def checkDrink(self, dog_id):
        #check water level
        if self.__instance_pir.read_pir() == True:
            while self.__instance_pir.read_pir() == True:
                print("Waiting for the dog to leave the water bowl.")

            sql = (
                'INSERT INTO petfeeder_db.tbldrinklog (millilitres_left, timestamp, dog_id) '
                'VALUES ( %(millilitres_left)s, %(timestamp)s,  %(dog_id)s );'
            )
            params = {
                'millilitres_left': self.__instance_ultrasonic.get_content_in_ml(),
                'timestamp': self.datetime.datetime.now(),
                'dog_id': 1,
            }

            self.__instance_dbconn.execute(sql, params)


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

        sql = (
            'INSERT INTO petfeeder_db.tblprovision (percentage_left, timestamp, dog_id) '
            'VALUES ( %(millilitres_left)s, %(timestamp)s);'
        )
        params = {
            'percentage_left': current_provision,
            'timestamp': self.datetime.datetime.now(),
        }



    def giveFood(self, amount, cummulative):
        amount_left = self.__instance_hx711.get_weight(5)

        if cummulative == True:
            self.__instance_servo_motor.open()

            while self.__instance_hx711.get_weight(5) <= amount:
                print("Food is being dispensed")

            self.__instance_servo_motor.close()

        else:
            self.__instance_servo_motor.open()

            while self.__instance_hx711.get_weight(5) - amount_left <= amount:
                print("Food is being dispensed")

            self.__instance_servo_motor.close()

        self.checkProvision()
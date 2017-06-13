from RPi import GPIO
from time import sleep
from model.dbsecurity.dbconn import DbConnection


class Alarms():
    def __init__(self, buzzer_pin = 12, led_pin = 27):
        self.__instance_dbconn = DbConnection(database="petfeeder_db")
        self.__buzzerpin = buzzer_pin
        self.__led_pin = led_pin
        GPIO.setup(self.__buzzerpin, GPIO.OUT)
        GPIO.setup(self.__led_pin, GPIO.OUT)

    def getSettings(self):
        sql = 'SELECT led_alarm_enabeld, sound_alarm_enabled, email_alarm_enabled, sms_alarm_enabled, food_alarm_enabled, drink_alarm_enabled, provision_alarm_enabled, food_alarm_threshold, drink_alarm_threshold, provision_alarm_threshold FROM tblsettings;'
        result = self.__instance_dbconn.query(sql, dictionary = True)
        result = result[0]
        self.__led_alarm_enabeld = result['led_alarm_enabeld']
        self.__sound_alarm_enabled = result['sound_alarm_enabled']
        self.__email_alarm_enabled = result['email_alarm_enabled']
        self.__sms_alarm_enabled = result['sms_alarm_enabled']

        self.__food_alarm_enabled = result['food_alarm_enabled']
        self.__drink_alarm_enabled = result['provision_alarm_enabled']
        self.__provision_alarm_enabled = result['provision_alarm_enabled']

        self.__food_alarm_threshold = result['food_alarm_threshold']
        self.__drink_alarm_threshold = result['drink_alarm_threshold']
        self.__provision_alarm_threshold = result['provision_alarm_threshold']
        self.__alarm_interval = result['alarm_interval']

    def checkAlarms(self, food_in_bowl, drink_in_bowl, provison_left):
        if self.__food_alarm_enabled == True:
            if food_in_bowl < self.__food_alarm_threshold:
                self.makeAlarms(message=("The food in the bowl is low " + str(food_in_bowl) + "g"))

        if self.__drink_alarm_enabled == True:
            if drink_in_bowl < self.__drink_alarm_threshold:
                self.makeAlarms(message=("The drink in the bowl is low " + str(drink_in_bowl) + "ml"))

        if self.__provision_alarm_enabled == True:
            if provison_left < self.__provision_alarm_threshold:
                self.makeAlarms(message=("The provision is low "+ str(provison_left) + "%"))

    def makeAlarms(self, message = "Warning, threshold passed"):
        if self.__led_alarm_enabeld == True:
            self.makeLedAlarm()

        if self.__sound_alarm_enabled == True:
            self.makeSoundAlarm()

        if self.__email_alarm_enabled == True:
            self.makeEmailAlarm()

        if self.__sms_alarm_enabled == True:
            self.makeSmsAlarm()


    def makeLedAlarm(self, period = 1):
        GPIO.output(self.__led_pin, GPIO.OUT)
        sleep(period)
        GPIO.output(self.__led_pin, GPIO.LOW)


    def makeSoundAlarm(self, period = 0.1):
        GPIO.output(self.__buzzerpin, GPIO.HIGH)
        sleep(period)
        GPIO.output(self.__buzzerpin, GPIO.LOW)

    def makeEmailAlarm(self):
        pass

    def makeSmsAlarm(self):
        pass
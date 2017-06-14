from RPi import GPIO
from time import sleep
from model.dbsecurity.dbconn import DbConnection
import datetime


class Alarms():
    def __init__(self, buzzer_pin=12, led_pin=27):
        self.__instance_dbconn = DbConnection(database="petfeeder_db")
        self.__buzzerpin = buzzer_pin
        self.__led_pin = led_pin
        GPIO.setup(self.__buzzerpin, GPIO.OUT)
        GPIO.setup(self.__led_pin, GPIO.OUT)

    def getSettings(self):
        # gets all the setting from the db

        sql = 'SELECT led_alarm_enabeld, sound_alarm_enabled, email_alarm_enabled, sms_alarm_enabled, food_alarm_enabled, drink_alarm_enabled, provision_alarm_enabled, food_alarm_threshold, drink_alarm_threshold, provision_alarm_threshold, alarm_interval_hours, email, phone_number FROM tblsettings;'
        result = self.__instance_dbconn.query(sql, dictionary=True)
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
        self.__email = result['email']
        self.__phone_number = result['phone_number']

        self.__last_alarm = datetime.datetime(year=2017, month=1, day=1)  # creats an datetimeobject to be able to check the interval time


    def checkAlarms(self, food_in_bowl, drink_in_bowl, provison_left):
        # check for all the enabled alarms, will create an alarmm when the the time interval is passesed (exept fot the led)
        alarm_detected = False

        if self.__food_alarm_enabled == True:
            if food_in_bowl < self.__food_alarm_threshold:
                self.makeAlarms(message=("The food in the bowl is low " + str(food_in_bowl) + "g"))
                alarm_detected = True

        if self.__drink_alarm_enabled == True:
            if drink_in_bowl < self.__drink_alarm_threshold:
                self.makeAlarms(message=("The drink in the bowl is low " + str(drink_in_bowl) + "ml"))
                alarm_detected = True

        if self.__provision_alarm_enabled == True:
            if provison_left < self.__provision_alarm_threshold:
                self.makeAlarms(message=("The provision is low " + str(provison_left) + "%"))
                alarm_detected = True

        #will turn the led off if it is no longer needed to be
        if alarm_detected == False:
            GPIO.output(self.__led_pin, GPIO.LOW)


    def makeAlarms(self, message="Warning, threshold passed"):
        # makes an alarm after the if they are enabeled
        time_passed = datetime.datetime.now() - self.__last_alarm

        if self.__led_alarm_enabeld == True:
            self.makeLedAlarm()

        if time_passed >= self.__alarm_interval:
            if self.__sound_alarm_enabled == True:
                self.makeSoundAlarm()

            if self.__email_alarm_enabled == True:
                self.makeEmailAlarm()

            if self.__sms_alarm_enabled == True:
                self.makeSmsAlarm()


    def makeLedAlarm(self, period=1):
        GPIO.output(self.__led_pin, GPIO.OUT)


    def makeSoundAlarm(self, period=0.1):
        GPIO.output(self.__buzzerpin, GPIO.HIGH)
        sleep(period)
        GPIO.output(self.__buzzerpin, GPIO.LOW)
        sleep(period)

    def makeEmailAlarm(self):
        pass

    def makeSmsAlarm(self):
        pass

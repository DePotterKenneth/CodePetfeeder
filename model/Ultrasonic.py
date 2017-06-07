import RPi.GPIO as GPIO
import time


class Ultrasonic():
    def __init__(self, trigger_pin, echo_pin):
        GPIO.setmode(GPIO.BCM)

        self.__trigger_pin = trigger_pin
        self.__echo_pin = echo_pin

        GPIO.setup(self.__trigger_pin, GPIO.OUT)
        GPIO.setup(self.__echo_pin, GPIO.IN)


    def distance(self):
        GPIO.output(self.__trigger_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.__trigger_pin, False)

        StartTime = time.time()
        StopTime = time.time()

        while GPIO.input(self.__echo_pin) == 0:
            StartTime = time.time()


        while GPIO.input(self.__echo_pin) == 1:
            StopTime = time.time()

        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2

        return distance

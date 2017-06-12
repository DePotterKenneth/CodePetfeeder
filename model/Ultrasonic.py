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
        #print("Pulse sent")
        GPIO.output(self.__trigger_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.__trigger_pin, False)

        StartTime = time.time()
        StopTime = time.time()

        #print("Waiting for an echo")
        while GPIO.input(self.__echo_pin) == 0:
            StartTime = time.time()


        while GPIO.input(self.__echo_pin) == 1:
            StopTime = time.time()

        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2

        return distance


    def get_content_in_percent(self):
        content = 500 #ml
        distance_empty = 45    #distance when the bowl is empty = 0 ml
        distance_at_defined_content = 40    #distance when the bowl is at max

        distance = self.distance()

        return distance/ (distance_at_defined_content - distance_empty) * 100


    def get_content_in_ml(self):
        content = 500 #ml
        distance_empty = 45    #distance when the bowl is empty = 0 ml
        distance_at_defined_content = 40    #distance when the bowl is at max

        distance = self.distance()

        return distance/ (distance_at_defined_content - distance_empty) * content
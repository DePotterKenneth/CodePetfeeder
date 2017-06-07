from RPi import GPIO

class Pir():

    def __init__(self, pin_nummer):
        self.__pin_nummer =  pin_nummer

    def read_pir(self):
        return GPIO.input(self.__pin_nummer)


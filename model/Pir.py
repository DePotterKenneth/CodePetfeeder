from RPi import GPIO


class Pir():

    def __init__(self, pin_nummer):
        self.__pin_pir =  pin_nummer
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__pin_pir, GPIO.IN)

    def read_pir(self):
        if GPIO.input(self.__pin_pir) == 1:
            return True
        else:
            return False




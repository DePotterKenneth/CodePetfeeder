from RPi import GPIO
from time import sleep

class ServoMotor():

    def __init__(self, pinnummer_servo, omgekeerd =False):
        self.__pinnummer_servo = pinnummer_servo
        self.__omgekeerd = omgekeerd

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pinnummer_servo, GPIO.OUT)

        if omgekeerd == False:
            self.__pwm_servo = GPIO.PWM(self.__pinnummer_servo, 7.5)
            self.__pwm_servo.start(7.5)
        else:
            self.__pwm_servo = GPIO.PWM(self.__pinnummer_servo, 92.5)
            self.__pwm_servo.start(92.5)


    def set_angle(self, angle_in_degrees):
        # 20ms = 50Hz (50 pulsen in een seconde)
        #
        # 0° = singaal van 0.5ms [500µs] --> 0.5 / 20 = 2.5
        # 90° = singaal van 1.5ms [500µs] --> 1.5 / 20 = 7.5
        # 180° = singaal van 2.4ms [2400µs] --> 2.5 / 20 = 12.5
        # Indien omgekeer nog 100 - doen omdat we door de tranistor de alles omdraaien

        duur_singaal = (angle_in_degrees / 180.0 * 10.0) + 2.5

        if self.__omgekeerd == True:
            duur_singaal= 100 - duur_singaal
        print(str(duur_singaal))

        self.__pwm_servo.ChangeDutyCycle(duur_singaal)


    def open(self):
        pass


    def close(self):
        pass
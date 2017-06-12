from model.hx711.hx711 import HX711
from model.DbConn import DbConnection
from model.Lcd import Lcd
from model.Mcp import Mcp
from model.Pir import Pir
from model.ServoMotor import ServoMotor
from model.Ultrasonic import Ultrasonic
from RPi import GPIO
import time

try:
    instance_hx711 = HX711(24, 23)
    instance_lcd = Lcd(5, 22, 26, 19, 13, 6)
    instance_mcp = Mcp()
    instance_pir = Pir(21)
    instance_servo_motor = ServoMotor(25, True)
    instance_ultrasonic = Ultrasonic(20, 16)

    previous_content_food = instance_hx711.get_weight(5)
    tolerance_food = 2

    while True:
        #check water level
        if instance_pir.read_pir() == True:
            while instance_pir.read_pir() == True:
                print("Waiting for the do to leave the water bowl.")



        #check bowl content
        if  previous_content_food <= (instance_hx711.get_weight(5) - tolerance_food):
            #sent querry to update foodlog
            pass



except Exception as e:
    print("exection happend:")
    print(str(e))


finally:
    GPIO.cleanup()
    print("Program stopped")
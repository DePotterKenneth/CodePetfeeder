from model.hx711.hx711 import HX711
from  model.DbConn import DbConnection
from model.Lcd import Lcd
from model.Mcp import Mcp
from model.Ultrasonic import Ultrasonic
from RPi import GPIO
import time

try:
    while True:
        dist = Ultrasonic(20, 16)
        print(str(dist.distance()))

        time.sleep(2)

except Exception as e:
    print("exection happend:")
    print(str(e))


finally:
    GPIO.cleanup()
    print("Program stopped")
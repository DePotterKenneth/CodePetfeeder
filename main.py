from model.Ultrasonic import Ultrasonic
from RPi import GPIO
import time

try:
    dist = Ultrasonic(20,16)
    print(str(dist.distance()))
    time.sleep(2)

except Exception as e:
    print("exection happend:")
    print(str(e))


finally:
    GPIO.cleanup()
    print("Program stopped")
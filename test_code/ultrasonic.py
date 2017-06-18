from model.Ultrasonic import Ultrasonic
from RPi import GPIO
import time

try:
    while True:
        dist = Ultrasonic(20, 16)
        print(str(dist.distance()))
        print("conten: =" + str(dist.get_content_in_ml()))
        time.sleep(3)

except Exception as e:
    print("exection happend:")
    print(str(e))


finally:
    GPIO.cleanup()
    print("Program stopped")
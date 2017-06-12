from ..model.ServoMotor import servo_motor
from RPi import GPIO
from time import sleep

try:
    instantie_servo = servo_motor(21, 1)

    while True:
        instantie_servo.zet_hoek(50)
        sleep(2)
        instantie_servo.zet_hoek(90)
        sleep(2)
        instantie_servo.zet_hoek(130)
        sleep(2)

except Exception as e:
    print(str(e))

finally:
    GPIO.cleanup()

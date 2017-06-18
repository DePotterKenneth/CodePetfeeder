from model.ServoMotor import ServoMotor
from RPi import GPIO
from time import sleep

try:
    instantie_servo = ServoMotor(25, 1)

    while True:
        instantie_servo.set_angle(40)
        print("hoek op 4 0 graden")
        sleep(4)
        instantie_servo.set_angle(90)
        print("hoek op 90 graden")
        sleep(4)
        instantie_servo.set_angle(150)
        print("hoek op 150 graden")
        sleep(4)

except Exception as e:
    print(str(e))

finally:
    GPIO.cleanup()
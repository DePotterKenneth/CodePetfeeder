from model.Pir import Pir
from RPi import GPIO
import time

try:
    while True:
        pir_instance = Pir(21)

        if pir_instance.read_pir() == True:
            print("Motion")
        else:
            print("Nothing")

except Exception as e:
    print("exection happend:")
    print(str(e))

finally:
    GPIO.cleanup()
    print("Program stopped")
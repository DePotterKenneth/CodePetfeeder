from RPi import GPIO
from model.Alarms import Alarms
from model.Feeder import Feeder

try:

    instance_feeder = Feeder()
    instance_alarm =  Alarms()

    while True:
        drink_in_bowl = instance_feeder.checkDrink(1)
        food_in_bowl = instance_feeder.checkFood(1)
        provision_left = instance_feeder.checkProvision()

        instance_alarm.checkAlarms(drink_in_bowl, food_in_bowl, provision_left)


except Exception as e:
    print("exection happend:")
    print(str(e))


finally:
    GPIO.cleanup()
    print("Program stopped")
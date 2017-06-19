from RPi import GPIO
from time import sleep
from model.Feeder import Feeder
from model.Alarms import Alarms
from model.Lcd import Lcd

try:
    instance_feeder = Feeder()
    instance_alarm = Alarms()

    instance_lcd = Lcd(5, 22, 26, 19, 13, 6)
    instance_lcd.init_display()

    while True:
    # check the drink level
    #     drink_in_bowl = instance_feeder.checkDrink(1)

    # check the food level
        food_in_bowl = instance_feeder.checkFood(1)
    #
    # check the provision
        print("here")
        provision_left = instance_feeder.checkProvision()
        print(str(provision_left))

    #
    # # check if you need to make an alarm
    #     instance_alarm.checkAlarms(drink_in_bowl, food_in_bowl, provision_left)
    #
    # # a sleep to make the program not to heavy



except Exception as e:
    print("exection happend:")
    print(str(e))


finally:
    GPIO.cleanup()
    print("Program stopped")

    print("please")

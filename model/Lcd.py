from RPi import GPIO
from time import sleep

class lcd:
    def __init__(self, e, rs, d7, d6, d5, d4, d3=0, d2=0, d1=0, d0=0, achtbit=False, four_bit_instruction_hard_wired=True):
        self.__e = e
        self.__rs = rs
        self.__pinnen_array = [d7, d6, d5, d4, d3, d2, d1, d0]
        self.__delay = 0.015
        self.__achtbit = achtbit
        self.__four_bit_instruction_hard_wired =four_bit_instruction_hard_wired


    def set_GPIO_bits(self, byte):
        shift_bit = 128

        if self.__achtbit == True or self.__four_bit_instruction_hard_wired == False:
            for getal in range(0, 8):
                te_sturen = byte & shift_bit
                GPIO.output(self.__pinnen_array[getal], te_sturen)
                # print("Er is vertuurd: " + str(te_sturen) + " naar pin: " + str(self.__pinnen_array[getal]))
                shift_bit = shift_bit >> 1
        else:
            for getal in range(0, 4):
                te_sturen = byte & shift_bit
                GPIO.output(self.__pinnen_array[getal], te_sturen)
                # print("Er is vertuurd: " + str(te_sturen) + " naar pin: " + str(self.__pinnen_array[getal]))
                shift_bit = shift_bit >> 1


    def stuur_teken(self, char):
        byte = ord(char) #getal omzetten naar een acii waarde

        GPIO.output(self.__e, GPIO.HIGH)
        GPIO.output(self.__rs, GPIO.HIGH)
        self.set_GPIO_bits(byte)
        GPIO.output(self.__e, GPIO.LOW)
        GPIO.output(self.__e, GPIO.HIGH)
        sleep(self.__delay)

        if self.__achtbit == False:
            geshifte_byte = byte << 4

            GPIO.output(self.__e, GPIO.HIGH)
            GPIO.output(self.__rs, GPIO.HIGH)
            self.set_GPIO_bits(geshifte_byte)
            GPIO.output(self.__e, GPIO.LOW)
            GPIO.output(self.__e, GPIO.HIGH)
            sleep(self.__delay)


    def stuur_instructie(self, byte):
        GPIO.output(self.__e, GPIO.HIGH)
        GPIO.output(self.__rs, GPIO.LOW)
        self.set_GPIO_bits(byte)
        GPIO.output(self.__e, GPIO.LOW)
        sleep(self.__delay)

        if self.__achtbit == False and byte != 0x28:
            geshifte_byte = byte << 4

            GPIO.output(self.__e, GPIO.HIGH)
            GPIO.output(self.__rs, GPIO.LOW)
            self.set_GPIO_bits(geshifte_byte)
            GPIO.output(self.__e, GPIO.LOW)
            sleep(self.__delay)


    def init_display(self):
        # print("1ste:")
        if self.__achtbit == True:
            self.stuur_instructie(0x38)  # fuction set 8bit
        else:
            self.stuur_instructie(0x28)  # fuction set 4bit

        # print("2de:")
        self.stuur_instructie(0x0d)  # display on

        # print("3de:")
        self.stuur_instructie(0x01)  # clear display and cursor home

    def schrijf_woord(self, woord):
        for getal in range(0, int(len(woord))):
            self.stuur_teken(woord[getal:getal + 1])

    def verzet_naar_lijn_twee(self):
        self.stuur_instructie(0xC0)

    def reset_display(self):
        pass
from RPi import GPIO
import spidev
import time

class mcp:

    def __init__(self, spi_busnumber =0, spi_apparaat_number=0):#RBP heeft maar 1 bus, en maar 1 naar buitengebrachte apparaat
        self.__spi = spidev.SpiDev()                            #creeert een spi instantie
        self.__spi.open(spi_busnumber, spi_apparaat_number)     #openent de instanite

    def read_channel(self, channel):
        # instructie om waarde van het kanaal in te kunnen lezen
        # 1: de start code (0b00000001)
        # 8 + kanaal <<4: 8 om de byte te doen beginnen met 1, + kanaal voor het juiste kanaal, en 4 shiften om ze in het bigin van de byte te krijgen
        # 0: de don't care bit's, mag elke random byte zijn
        adc_data = self.__spi.xfer2([1, (8 + channel) << 4, 0])


        # de mcp antwoord in 3 bytes (omdat hij namelijk 10 bits precisie heeft)
        # 1ste byte = niks; 2de bevat de 1ste en 2de bit van het getal; 3de de 3 tem de 10 de bit
        # daarom gaan we de 2de bit filteren met 3 (0b00000011) om de overbodige data er uit te halen
        # dan shiften we ze op hun juiste plaats en voegen we het andere deel toe
        data = ((adc_data[1] & 3) << 8) + adc_data[2]

        return data

    def calculate_volts(self, data, digits = 2):
        #   maxwaarde voltage       maximaal mogelijke waarde binare waarde, 2^10 - 1 = 1023
        volts = (data * 3.3) / float(1023)
        # print("Voltage voor afronding: " + str(volts))
        volts = round(volts, digits)
        return volts

    def define_temp(self, temp_channel):
        temp_level = self.read_channel(temp_channel)
        temp_volts = self.calculate_volts(temp_level, 2)
        temp =temp_volts*100 - temp_volts*10
        return int(temp)


    def define_light_percentage(self, light_channel, resistor_value = 1000):
        light_level = self.read_channel(light_channel)
        light_volts = self.calculate_volts(light_level, 2)
        licht_percentage = 100 - (light_volts/3.3)*100
        return int(licht_percentage)
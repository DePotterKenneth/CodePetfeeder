from RPi import GPIO
import spidev
import time

class mpc:

    def __init__(self, spi_busnummer =0, spi_apparaat_nummer=0):#RBP heeft maar 1 bus, en maar 1 naar buitengebrachte apparaat
        self.__spi = spidev.SpiDev()                            #creeert een spi instantie
        self.__spi.open(spi_busnummer, spi_apparaat_nummer)     #openent de instanite

    def lees_kanaal_uit(self, kanaal):
        # instructie om waarde van het kanaal in te kunnen lezen
        # 1: de start code (0b00000001)
        # 8 + kanaal <<4: 8 om de byte te doen beginnen met 1, + kanaal voor het juiste kanaal, en 4 shiften om ze in het bigin van de byte te krijgen
        # 0: de don't care bit's, mag elke random byte zijn
        adc_data = self.__spi.xfer2([1, (8 + kanaal) << 4, 0])


        # de mcp antwoord in 3 bytes (omdat hij namelijk 10 bits precisie heeft)
        # 1ste byte = niks; 2de bevat de 1ste en 2de bit van het getal; 3de de 3 tem de 10 de bit
        # daarom gaan we de 2de bit filteren met 3 (0b00000011) om de overbodige data er uit te halen
        # dan shiften we ze op hun juiste plaats en voegen we het andere deel toe
        data = ((adc_data[1] & 3) << 8) + adc_data[2]

        return data

    def zet_om_naar_voltage(self, data, getallen_na_komma = 2):
        #   maxwaarde voltage       maximaal mogelijke waarde binare waarde, 2^10 - 1 = 1023
        volts = (data * 3.3) / float(1023)
        # print("Voltage voor afronding: " + str(volts))
        volts = round(volts, getallen_na_komma)
        return volts

    def bepaal_temperatuur(self, temp_kanaal):
        temp_level = self.lees_kanaal_uit(temp_kanaal)
        temp_volts = self.zet_om_naar_voltage(temp_level, 2)
        temp =temp_volts*100 - temp_volts*10
        return int(temp)


    def bepaal_percentage_licht(self, licht_kanaal):
        licht_level = self.lees_kanaal_uit(licht_kanaal)
        licht_volts = self.zet_om_naar_voltage(licht_level, 2)
        licht_percentage = 100 - (licht_volts/3.3)*100
        return int(licht_percentage)
from RPi import GPIO
from model.Mcp import Mcp

instance_mcp = Mcp()

try:
    for number in range(0,4):
        print(instance_mcp.define_light_percentage(light_channel=number))

except Exception as e:
    print("Somehting went wrong")
    print(e)
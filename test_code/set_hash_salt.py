from model.dbsecurity.pwdhashpetfeeder import setpasword, verify_credentials
import datetime
from time import sleep

setpasword("Xd7mpAn39")
sleep(1)
print(verify_credentials("Xd7mpAn39"))
from model.dbsecurity.pwdhashpetfeeder import setpasword, verify_credentials
import datetime
from time import sleep

setpasword("koekjestrommel")
sleep(1)
print(verify_credentials("koekjestrommel"))
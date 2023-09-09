import time
import util
from WifiManager import WifiManager
import ServerManager
import network

import medicoes
import json
#import ntptime
#ntptime.settime()

print(util.df())
print(util.free(True))
util.connectSDCard()


wm = WifiManager(ssid="Horta",password="Fatec123")
wm.connect()

ServerManager.init()

n = 0
while True:
  time.sleep(100)
  medidas = json.dumps(medicoes.getLeituras())
  f = open("/sd/readings.json",'+a')
  f.write(",")
  f.write(medidas)
  f.flush()
  f.close()



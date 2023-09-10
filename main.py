import time
import util
from WifiManager import WifiManager
import ServerManager
import network

print(util.df())
print(util.free(True))
util.connectSDCard()

network.hostname("horta")

wm = WifiManager(ssid="Horta",password="Fatec123")
wm.connect()

lock = ServerManager.init()

import ntptime
ntptime.settime()


def leitura():
  print("Leitura Programada")  
  import medicoes
  import json
  jsonMedidas = json.dumps(medicoes.getLeituras())
  with lock:
    with open('/sd/leituras.json','a+') as f:
        f.write("\n")
        f.write(jsonMedidas)
        f.write(",")
  pass
     
while True:
  leitura()
  time.sleep(300)

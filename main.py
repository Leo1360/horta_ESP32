import time
import util
from WifiManager import WifiManager
import ServerManager
import network
import medicoes

print(util.df())
print(util.free(True))
util.connectSDCard()

network.hostname("horta")

wm = WifiManager(ssid="Horta",password="Fatec123")
wm.connect()

lock = ServerManager.init()

util.atualizarTempo()

import utelegram

with lock:
    utelegram.sendMsg("6742344655:AAGnLnHFrSJhmCdIDx9RBIe96PSejxXOlwI",-4099373084,"Teste notificação esp")

def leitura():
  print("Leitura Programada")  
  import json
  jsonMedidas = json.dumps(medicoes.getLeituras())
  with lock:
    with open('/sd/leituras.json','a+') as f:
        f.write("\n")
        f.write(jsonMedidas)
        f.write(",")
  pass

medicoes.init()

while True:
  with lock:
      wm.connect()
      leitura()
  time.sleep(300)

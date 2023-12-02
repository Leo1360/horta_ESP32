from time import sleep
import util
from WifiManager import WifiManager
import medicoes

def setup():
  from network import hostname
  import ServerManager
  print("Disk usage: " + util.df())
  print("Ram usage: " + util.free(True))
  util.connectSDCard()
  hostname("horta")
  global wm
  wm = WifiManager(ssid="Horta",password="Fatec123")
  wm.connect()
  ServerManager.init()
  util.atualizarTempo()
  medicoes.init()

def loop():
  print("Ram usage: " + util.free())
  medicoes.persistReadings(medicoes.getReadings())
  wm.connect()
  sleep(300)

#----------
setup()
while True:
  loop()

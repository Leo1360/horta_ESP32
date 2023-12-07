import json
import medicoes
from micropyserver import MicroPyServer
import _thread
from time import localtime
serverLock = ""

def readNow(request):
    print("/readNow")
    server.send("HTTP/1.0 200\r\n")
    server.send("Content-Type: aplication/json\r\n\r\n")
    server.send(json.dumps(medicoes.getReadings()))

def addSensor(request):
  from SensorManager import addSensor
  print("/addSensor")
  infos = json.loads(request.split("\r\n\r\n")[1])
  ret, msg = addSensor(infos)
  server.send("HTTP/1.0 200\r\n")
  server.send("Content-Type: aplication/json\r\n\r\n")
  if(ret == True):
    server.send("""{"status":"OK"}""")
  else:
    server.send("""{"status":"Fail","msg":" """ + msg + """ "}""")

def listSensores(request):
  from SensorManager import getSensorListJson
  print("/listSensores")
  server.send("HTTP/1.0 200\r\n")
  server.send("Content-Type: aplication/json\r\n\r\n")
  server.send(getSensorListJson())

def readsHistory(request):
  print("/readsHistory")  
  server.send("HTTP/1.0 200\r\n")
  server.send("Content-Type: aplication/json\r\n\r\n")
  medicoes.streamHistoryToServer(server)
  server.send("\n]")
  pass
  
def limparLeituras(request):
  medicoes.clearHistoryFile()
  server.send("HTTP/1.0 200\r\n")
  server.send("Content-Type: aplication/json\r\n\r\n")
  server.send("""{"status":"OK"}""")

def updateTime(request):
  data = MicroPyServer.get_request_query_params(request)
  resp = "OK"
  msg = ""
  if(len(data) == 0):
    from util import atualizarTempo
    if(atualizarTempo()):
      resp = "OK"
    else:
      resp = "FAIL"
  else:
    from machine import RTC
    RTC().datetime([data["Y"],data["M"],data["D"],data["h"],data["m"],data["s"]])
  try:
    msg = localtime()
  except:
    pass
  server.send_response("""{"status":" """ + resp + """ ","msg":" """ + msg + """ "}""",content_type="aplication/json")
  pass

def getDashBoard(request):
  server.send("HTTP/1.0 200\r\n")
  server.send("Content-Type: text/html\r\n\r\n")
  with open("/sd/index.html","r") as f:
    for line in f:
      server.send(line)

def listSensorMods():
  from SensorModManager import getJson
  server.send("HTTP/1.0 200\r\n")
  server.send("Content-Type: aplication/json\r\n\r\n")
  server.send(getJson())

def listPlugins():
  from PluginManager import getJson
  server.send("HTTP/1.0 200\r\n")
  server.send("Content-Type: aplication/json\r\n\r\n")
  server.send(getJson())

def activatePlugin():
  from PluginManager import activatePlugin
  server.send("HTTP/1.0 200\r\n")
  server.send("Content-Type: aplication/json\r\n\r\n")
  server.send("""{"ok":""" + activatePlugin() +"""}""")

def deactivatePlugin():
  from PluginManager import deactivatePlugin
  server.send("HTTP/1.0 200\r\n")
  server.send("Content-Type: aplication/json\r\n\r\n")
  server.send("""{"ok":""" + deactivatePlugin() +"""}""")

def getConfigs():
  server.send("HTTP/1.0 200\r\n")
  server.send("Content-Type: aplication/json\r\n\r\n")
  with open("/sd/config.json","r") as f:
    server.send(f.read())

def saveConfigs(request):
  with open("/sd/config.json","w") as f:
    f.write(request.split("\r\n\r\n")[1])


def getTrigrams():
  from medicoes import getTrigramsJson
  server.send("HTTP/1.0 200\r\n")
  server.send("Content-Type: aplication/json\r\n\r\n")
  server.send(getTrigramsJson())

def init():
  server.on_not_found(getDashBoard)
  server.add_route("/readNow", readNow)
  server.add_route("/addSensor", addSensor,method="POST")
  server.add_route("/listSensores",listSensores)
  server.add_route("/history.json",readsHistory)
  server.add_route("/limparHistorico",limparLeituras)
  server.add_route("/updateTime",updateTime)
  
  #/config -              GET: show all configs - POST: save configuration

  #/plugin/list -         GET: List existing plugins and if they are active or not
  server.add_route("/plugin/list",listPlugins)

  #/sensorMod/list -      GET: list all avaible sensor modules
  server.add_route("/sensorMod/list",listSensorMods)

  #/plugin/activate -     POST: activates the discribed plugin
  server.add_route("/plugin/activate",activatePlugin)
  #/plugin/deactivate -   POST: deactivate the discribed plugin
  server.add_route("/plugin/deactivate",deactivatePlugin)

  server.add_route("/getTrigrams",getTrigrams)

    #* /plugin?plugin=abcd -  ANY: binds request to the plugin described
    #* /plugin/add -          POST: recives the plugin file and saves it in the "plugins" folder
    #* /plugin/delete -       POST: delete the informed plugin file
    #* /sensorMod/add -       POST: recives the sensor module file, saves it and register it
    #* /sensorMod/delete -    POST: delete the sensor module file and its register
  
  _thread.start_new_thread(server.start,[])

server = MicroPyServer()


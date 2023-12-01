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
  ret = addSensor(infos)
  server.send("HTTP/1.0 200\r\n")
  server.send("Content-Type: aplication/json\r\n\r\n")
  if(ret == True):
    server.send("""{"status":"OK"}""")
  else:
    server.send("""{"status":"Fail","msg":" """ + ret + """ "}""")

def listSensores(request):
  from SensorManager import loadSensorRegistry
  print("/listSensores")
  temp = json.dumps(loadSensorRegistry())
  server.send("HTTP/1.0 200\r\n")
  server.send("Content-Type: aplication/json\r\n\r\n")
  server.send(temp)

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
    RTC().datetime([data["Y"],data["M"],data["D"],data["h"],data["m"]])
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

def init():
  server.add_route("/readNow", readNow)
  server.add_route("/addSensor", addSensor,method="POST")
  server.add_route("/listSensores",listSensores)
  server.add_route("/history.json",readsHistory)
  server.add_route("/limparHistorico",limparLeituras)
  server.add_route("/updateTime",updateTime)
  server.on_not_found(getDashBoard)
  _thread.start_new_thread(server.start,[])

server = MicroPyServer()


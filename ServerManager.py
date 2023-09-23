import json
import medicoes
from micropyserver import MicroPyServer
import _thread

serverLock = ""

def readNow(request):
    print("/readNow")
    server.send("HTTP/1.0 200\r\n")
    server.send("Content-Type: aplication/json\r\n\r\n")
    server.send(json.dumps(medicoes.getLeituras()))

def addSensor(request):
  print("/addSensor")
  infos = json.loads(request.split("\r\n\r\n")[1])
  ret = medicoes.addSensor(infos["nome"],infos["pinos"],infos["tipo"])
  server.send("HTTP/1.0 200\r\n")
  server.send("Content-Type: aplication/json\r\n\r\n")
  if(ret == True):
    server.send("""{"status":"OK"}""")
  else:
    server.send("""{"status":"Fail","msg":" """ + ret + """ "}""")

def listSensores(request):
  print("/listSensores")
  temp = medicoes.listarSensores()
  server.send("HTTP/1.0 200\r\n")
  server.send("Content-Type: aplication/json\r\n\r\n")
  server.send(temp)

def readsHistory(request):
  print("/readsHistory")  
  server.send("HTTP/1.0 200\r\n")
  server.send("Content-Type: aplication/json\r\n\r\n")
  with serverLock:
    with open("/sd/leituras.json","r") as f:
      for line in f:
        server.send(line)
  server.send("\n]")
  pass
  
def limparLeituras(request):
  with serverLock:
    with open("/sd/leituras.json","w") as f:
      f.write("[")
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
  server.send_response("""{"status":" """ + resp + """ ","msg":" """ + msg + """ "}""",content_type="aplication/json")
  pass

def setHandlers():
  server.add_route("/readNow", readNow)
  server.add_route("/addSensor", addSensor,method="POST")
  server.add_route("/listSensores",listSensores)
  server.add_route("/readsHistory",readsHistory)
  server.add_route("/limparHistorico",limparLeituras)
  server.add_route("/updateTime",updateTime)


def init():
    global serverLock 
    serverLock = _thread.allocate_lock()
    _thread.start_new_thread(server.start,[])
    return serverLock

server = MicroPyServer()
setHandlers()



  
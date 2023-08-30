import json
import medicoes
from micropyserver import MicroPyServer
import _thread

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
  if(ret):
    server.send("""{"status":"OK"}""")
  else:
    server.send("""{"status":"Fail"}""")

def listSensores(request):
  print("/listSensores")
  temp = medicoes.listarSensores()
  server.send("HTTP/1.0 200\r\n")
  server.send("Content-Type: aplication/json\r\n\r\n")
  server.send(temp)

def readsHistory(request):
  print("/readsHistory")  
  f = open("medicoes.json","r")
  server.send("HTTP/1.0 200\r\n")
  server.send("Content-Type: aplication/json\r\n\r\n")
  server.send(f.read())


def setHandlers():
  server.add_route("/readNow", readNow)
  server.add_route("/addSensor", addSensor,method="POST")
  server.add_route("/listSensores",listSensores)
  server.add_route("/readsHistory",readsHistory)

def init():
    _thread.start_new_thread(server.start,[])

print("Jabuticaba")
server = MicroPyServer()
setHandlers()



  
import _thread

def init():
    global lock
    lock = _thread.allocate_lock() # lock para leitura do arquivo de histórico de leituras

def getReadings():
    from SensorManager import readAllSensor
    import time
    from util import formatTime
    medicoes = readAllSensor()
    hora = formatTime(time.localtime())
    return {"dataHora":hora,"medicoes":medicoes}

def streamHistoryToServer(server):
    with lock:
        with open("/sd/leituras.json","r") as f:
            for line in f:
                server.send(line)
    pass

def clearHistoryFile():
    with lock:
        with open("/sd/leituras.json","w") as f:
            f.write("[")
    pass

def persistReadings(readings):
    import json
    jsonMedidas = json.dumps(readings)
    with lock:
        with open('/sd/leituras.json','a+') as f:
            f.write("\n")
            f.write(jsonMedidas)
            f.write(",")


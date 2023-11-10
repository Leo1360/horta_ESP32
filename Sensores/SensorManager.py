# hum - humidade
# tmp - temperatura
# ecs - eletrocondutividade de solo
# lux - luminosidade
import gc

def loadSensorRegistry():
    import json
    sensores = []
    with open("/sd/sensores.json","r") as f:
        temp = f.readline()
        print(temp)
        try:
            sensores = json.loads(temp)
        except:
            sensores = None
    return sensores

def updateSensorRegistry(sensores):
    import json
    with open("/sd/sensores.json","w") as f:
        f.write(json.dumps(sensores))
    pass

ports = {
    "1" : [15,2],
    "2" : [4,16],
    "3" : [17,5],
    "4" : [18,19],
    "5" : [21,3],
    "6" : [1,22],
    "7" : [26,25],
    "8" : [33],
    "9" : [32],
    "10" : [35],
    "11" : [34],
    "12" : [39],
    "13" : [36]
}

def getpin(port):
    from machine import Pin
    temp = ports[port]
    out = []
    for pino in temp:
        out.append(Pin(pino))
    return out

def readAllSensor():
    readings = []
    sensores = loadSensorRegistry()
    for key in sensores:
        mod = None
        try:
            __import__(sensores[key]["tipo"])
        except:
            continue
        read, notify = {key : mod.read(getpin(sensores[key]["port"]),sensores[key]["faixas"])}
        if(notify):
            import Notification
            Notification.sendNotification(sensores[key],read)
        readings.append(read)
        del mod
        gc.collect()
    return readings

def getSensorInfo(sensorName):
    senosores = loadSensorRegistry()
    return senosores[sensorName]

def addSensor(sensor):
    try: #try para pegar caso o campo n exista
        sensor["faixas"]
        if(sensor["nome"] == "" or sensor["tipo"] == "" or sensor["port"] == ""):
            return False
        sensores = loadSensorRegistry()
        sensores[sensor["nome"]] = {
            "port":sensor["port"],
            "tipo":sensor["tipo"],
            "faixas":sensor["faixas"]}
        updateSensorRegistry(sensores)
        return True
    except:
            return False
    pass

def removeSensor(sensorName):
    sensores = loadSensorRegistry()
    try:
        sensores.pop(sensorName)
        updateSensorRegistry(sensores)
    except:
        pass


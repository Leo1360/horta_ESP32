# umd - humidade
# tmp - temperatura
# ecs - eletrocondutividade de solo
# lux - luminosidade
import gc

def loadSensorModRegistry():
    import json
    with open("sd/sensorModules/registry.json") as f:
        return json.loads(f.read())

def getSensorModRegistry():
    with open("sd/sensorModules/registry.json") as f:
        return f.read()

def loadSensorRegistry():
    import json
    sensores = {}
    with open("sd/sensores.json","r") as f:
        temp = f.read()
        try:
            sensores = json.loads(temp)
            print("Registry loaded")
            print(sensores)
        except:
            print("Json to dict conversion failed")
            sensores = {}
        print(sensores)
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
    temp = ports[str(port)]
    out = []
    for pino in temp:
        out.append(Pin(pino))
    return out

def readAllSensor():
    from PluginManager import callHandler
    callHandler("befor_readingSession")
    readings = []
    sensores = loadSensorRegistry()
    if(sensores == {}):
        print("No Sensor registerd")
        return {}
    for key in sensores:
        callHandler("befor_sensorReading")
        mod = None
        print("Reading sensor: ")
        print(sensores[key]["tipo"])
        modName = sensores[key]["tipo"]
        print(modName)
        try:
            mod = __import__(modName)
            print("Sensor driver loaded")
        except:
            print("Sensor driver nor found")
            callHandler("on_sensorFailedReading",sensores[key])
            continue
        print(mod)
        read, notify = mod.read(getpin(sensores[key]["port"]),sensores[key]["faixas"])
        callHandler("after_sensorReading",{"read":read,"name":key})
        read = {key:read}
        if(notify):
            from Notification import sendNotification
            sendNotification(sensores[key],read,key)
        readings.append(read)
        del mod
        gc.collect()
    callHandler("after_readingSession",readings)
    return readings

def getSensorInfo(sensorName):
    senosores = loadSensorRegistry()
    return senosores[sensorName]

def addSensor(sensor):
    try: #try para pegar caso o campo n exista
        sensor["faixas"]
        if(sensor["nome"] == "" or sensor["tipo"] == "" or sensor["port"] == ""):
            return False
        tipos = loadSensorModRegistry()
        sensor["tipo"] = tipos[sensor["tipo"]]["moduleName"]
        del tipos
        sensores = loadSensorRegistry()
        sensores[sensor["nome"]] = {
            "port":sensor["port"],
            "tipo":sensor["tipo"],
            "faixas":sensor["faixas"]}
        updateSensorRegistry(sensores)
        gc.collect()
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

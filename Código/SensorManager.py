# umd - humidade
# tmp - temperatura
# ecs - eletrocondutividade de solo
# lux - luminosidade
regPath = "sd/sensores.json"

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
    import gc
    from PluginManager import callHandler
    from Registry import load
    callHandler("befor_readingSession",{})
    readings = {}
    sensores = load(regPath)
    if(sensores == {}):
        print("No Sensor registerd")
        return {}
    for key in sensores.keys():
        callHandler("befor_sensorReading",{})
        mod = None
        modName = sensores[key]["tipo"]
        try:
            mod = __import__("sd/sensorModules/" + modName)
            print("Sensor driver loaded")
        except:
            print("Sensor driver nor found")
            callHandler("on_sensorFailedReading",sensores[key])
            continue
        print(mod)
        read, notify = mod.read(getpin(sensores[key]["port"]),sensores[key]["faixas"])
        callHandler("after_sensorReading",{"read":read,"name":key,"outOfRange":notify})
        readings[key] = read
        del mod
        gc.collect()
    callHandler("after_readingSession",readings)
    return readings

def getSensorInfo(sensorName):
    import Registry
    return Registry.getElement(regPath,sensorName)

def addSensor(sensor):
    import gc
    import Registry
    try: #try para pegar caso o campo n exista
        sensor["faixas"]
        if(sensor["nome"] == "" or sensor["tipo"] == "" or sensor["port"] == ""):
            return False,"Campos de Nome,Tipo ou Port vazios"
    except:
        return False, "Todos os campos devem ser preenchidos"
    tipo = Registry.getElement("sd/sensorModules/registry.json",sensor["tipo"])
    if(tipo == {}):    
        return False,"Tipo de sensor não suportado"
    nome = sensor["nome"]
    sensor.pop("nome")
    Registry.addElement(regPath,nome,sensor)
    gc.collect()
    return True,"ok"
    
def removerSensor(sensorName):
    from Registry import removeElement
    removeElement(regPath,sensorName)

def getSensorList():
    from Registry import load
    return load(regPath)

def getSensorListJson():
    from Registry import getString
    return getString(regPath)


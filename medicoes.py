import json
import machine

sensores = []

def listarSensores():
    return json.dumps(sensores)

def addSensor(nome,pinos,tipo):
    if(sensorFunctions.get(tipo)==None):
        return False
    for sensor in sensores:
        if(sensor["nome"] == None):
            return False
    sensores.append({"nome":nome,"pinos":pinos,"tipo":tipo})
    return True

def removeSensor(nome):
    for sensor in sensores:
        if(sensor["nome"] == nome):
            sensores.remove(sensor)
            return
    pass

def getLeituras():
    medicoes = []
    for sensor in sensores:
        try:
            medicoes.append(sensorFunctions[sensor["tipo"]](sensor))
        except:
            medicoes.append({"nome":sensor["nome"]})
        
    return {"hora":0,"medicoes":medicoes}

def rdht11(cfg):
    from dht import DHT11
    d = DHT11(machine.Pin(cfg["pinos"][0])) 
    d.measure()
    return {
        "tmp":d.temperature(),
        "hum":d.humidity(),
        "nome":cfg["nome"]
    }

def rdht22(cfg):
    from dht import DHT22
    d = DHT22(machine.Pin(cfg["pinos"][0]))
    d.measure()
    return {
        "tmp":d.temperature(),
        "hum":d.humidity(),
        "nome":cfg["nome"]
    }

sensorFunctions = {
    "DHT11":rdht11,
    "DHT22":rdht22
}
import json
from machine import Pin, ADC
from time import sleep
from easydate import DateTime

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
    hora = str(DateTime.now())
    for sensor in sensores:
        try:
            medicoes.append(sensorFunctions[sensor["tipo"]](sensor))
        except:
            medicoes.append({"nome":sensor["nome"]})
    return {"dataHora":hora,"medicoes":medicoes}

def filtroDesvPad(arr, num_std_dev=1):
    if len(arr) == 0:
        return 0

    # Calculate the mean of the input array
    arr_mean = sum(arr) / len(arr)

    # Calculate the standard deviation of the input array
    arr_std = (sum((x - arr_mean) ** 2 for x in arr) / len(arr)) ** 0.5

    # Calculate the threshold for filtering
    threshold = arr_std * num_std_dev

    # Filter out values more than 'num_std_dev' standard deviations away from the mean
    filtered_arr = [x for x in arr if abs(x - arr_mean) <= threshold]

    return filtered_arr

def mediaArray(arr):
    if len(arr) == 0:
        return 0  # Avoid division by zero if all values are filtered out
    media = sum(arr) / len(arr)
    return media

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
    d = DHT22(Pin(cfg["pinos"][0]))
    d.measure()
    return {
        "temperatura":d.temperature(),
        "umidade":d.humidity(),
        "nome":cfg["nome"]
    }

def capacitivoUmidadeSolo(cfg):
    p = cfg["pinos"][0]
    cap = ADC(Pin(p))
    cap.atten(ADC.ATTN_11DB)

    amostras = []
    for c in range(0,20):
        amostras.append(cap.read())
        sleep(0.01)
    amostras = filtroDesvPad(amostras,1)
    umidade = 100 - ((mediaArray(amostras)-1024) * 0.05537)

    return {
        "umidade":umidade,
        "nome":cfg["nome"]
    }


sensorFunctions = {
    "DHT11":rdht11,
    "DHT22":rdht22,
    "HumidadeSolo":capacitivoUmidadeSolo
}
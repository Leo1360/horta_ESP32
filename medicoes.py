import json
from machine import Pin, ADC
from easydate import DateTime

def listarSensores():
    from Sensores.SensorManager import loadSensorRegistry
    return json.dumps(loadSensorRegistry())

def getLeituras():
    from Sensores.SensorManager import readAllSensor
    medicoes = readAllSensor()
    hora = str(DateTime.now())
    return {"dataHora":hora,"medicoes":medicoes}

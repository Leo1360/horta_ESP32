def read(pinos,faixas):
    from ds18x20 import DS18X20
    from onewire import OneWire
    from ReadingCorrection import mediaArray
    sensor = DS18X20(OneWire(pinos[0]))
    rom = sensor.scan()
    temp = 0
    if(len(rom) > 0):
        sensor.convert_temp()
        medidas = []
        for c in range(0,20):
            medidas.append(sensor.read_temp(rom[0]))
        temp = mediaArray(medidas)
    read = {"tmp":temp}
    del OneWire
    del DS18X20
    del mediaArray
    
    from Notification import validarLeitura
    notify = validarLeitura(faixas,read)
        
    return read, notify

def getMedicoes():
    return ["tmp"]
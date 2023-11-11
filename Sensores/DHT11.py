def read(pinos,faixas):
    print("Reading DHT11 on pins " + pinos)
    from dht import DHT11
    import Sensores.Notification as Notification
    d = DHT11(pinos[0])
    d.measure()
    medicao = {
        "tmp":d.temperature(),
        "hum":d.humidity(),
    }
    notify = Notification.validarLeitura(faixas,medicao)
    return medicao,notify
def read(pinos,faixas):
    from dht import DHT22
    import Sensores.Notification as Notification
    d = DHT22(pinos[0])
    d.measure()
    medicao = {
        "tmp":d.temperature(),
        "hum":d.humidity(),
    }
    notify = Notification.validarLeitura(faixas,medicao)
    return medicao,notify
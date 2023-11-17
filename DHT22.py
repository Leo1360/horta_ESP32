def read(pinos,faixas):
    from dht import DHT22
    from Notification import validarLeitura
    d = DHT22(pinos[0])
    d.measure()
    medicao = {
        "tmp":d.temperature(),
        "hum":d.humidity(),
    }
    notify = validarLeitura(faixas,medicao)
    return medicao,notify
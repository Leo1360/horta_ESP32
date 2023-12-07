def read(pinos,faixas):
    print("Reading DHT11 on pins ")
    print(pinos)
    from dht import DHT11
    from Notification import validarLeitura
    d = DHT11(pinos[0])
    d.measure()
    medicao = {
        "tmp":d.temperature(),
        "umd":d.humidity(),
    }
    notify = validarLeitura(faixas,medicao)
    return medicao,notify

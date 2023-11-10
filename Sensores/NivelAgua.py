def read(pinos,faixas):
    from ReadingCorrection import filtroDesvPad,mediaArray
    from time import sleep
    from machine import ADC
    from Notification import validarLeitura
    cap = ADC(pinos[0])
    cap.atten(ADC.ATTN_11DB)

    amostras = []
    for c in range(0,20):
        amostras.append(cap.read())
        sleep(0.01)
    amostras = filtroDesvPad(amostras,1)
    umidade = 100 - ((mediaArray(amostras)-1024) * 0.05537)

    read = {"umd":umidade}
    notify = validarLeitura(faixas,read)
    return read, notify
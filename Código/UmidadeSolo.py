def read(pinos,faixas):
    from machine import ADC
    from ReadingCorrection import filtroDesvPad,mediaArray
    from time import sleep
    cap = ADC(pinos[0])
    cap.atten(ADC.ATTN_11DB)

    amostras = []
    for c in range(0,20):
        amostras.append(cap.read())
        sleep(0.01)
    amostras = filtroDesvPad(amostras,1)
    umidade = 100 - ((mediaArray(amostras)-1024) * 0.05537)
    read = {"umd":umidade}
    from Notification import validarLeitura
    notify = validarLeitura(faixas,read)

    return read, notify

def getMedicoes():
    return ["umd"]
def read(pinos,faixas):
    from machine import I2C
    from bh1750 import BH1750

    i2c0_scl = pinos[0]
    i2c0_sda = pinos[1]
    i2c0 = I2C(0, sda=i2c0_sda, scl=i2c0_scl)

    bh1750 = BH1750(0x23, i2c0)
    temp = bh1750.measurement

    read = {"lux":temp}
    from Notification import validarLeitura
    notify = validarLeitura(faixas,read)

    return read, notify
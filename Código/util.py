def connectSDCard():
  import os
  import machine
  from sdcard import SDCard
  spisd = machine.SoftSPI(-1,miso=machine.Pin(13),mosi=machine.Pin(12),sck=machine.Pin(14))
  sd = SDCard(spisd,machine.Pin(27))
  vfs = os.VfsFat(sd)
  os.mount(vfs,"/sd")
  print(os.listdir())

def df():
  import os
  s = os.statvfs('//')
  return ('{0} MB'.format((s[0]*s[3])/1048576))

def free(full=False):
  import gc
  F = gc.mem_free()
  A = gc.mem_alloc()
  T = F+A
  P = '{0:.2f}%'.format(F/T*100)
  if not full: return P
  else : return ('Total:{0} \n Free:{1} ({2})'.format(T,F,P))

def atualizarTempo():
  import ntptime
  try:
    ntptime.settime()
  except:
    print("NTP time sincronization fail")
    pass

def getConfiguration(configName):
  import json
  print("getConfiguration() configName: " + configName)
  with open("sd/config.json","r") as f:
    configs = f.read()
    print(configs)  
    configuracoes = json.loads(configs)
    print("Pegando configuração " + configName + ":= " + str(configuracoes[configName]))
    return configuracoes[configName]


def formatTime(data):
  #(year, month, mday, hour, minute, second, weekday, yearday)
  return str(data[2]) + "/" + str(data[1]) + "/" + str(data[0]) + " " + str(data[3]) + ":" + str(data[4]) + ":" + str(data[5])

def streamFile(server,filePath):
  with open(filePath,"r") as f:
    for line in f:
        server.send(line)
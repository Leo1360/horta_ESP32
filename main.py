from time import sleep
import util
import WifiManager
import ServerManager

print(util.df())
print(util.free(True))
util.connectSDCard()

WifiManager.init()

ServerManager.init()

n = 0
while True:
    #Looop de medições, automações e agendamentos
    print(n)
    n = n + 1
    sleep(3)
    

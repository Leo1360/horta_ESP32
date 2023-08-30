import network
from time import sleep

def init():
    wlan_id = "ROSE"
    wlan_pass = "Lhs140798"

    network.hostname("horta")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    while not wlan.isconnected():
        wlan.connect(wlan_id, wlan_pass)
        sleep(2)
    print("Connected... IP: " + wlan.ifconfig()[0]) 